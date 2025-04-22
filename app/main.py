from pyngrok import ngrok
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db import get_session
from typing import List
from . import (
    config,
    db,
    models,
    schema,
    crud
)
from cassandra.cqlengine.management import sync_table

settings = config.get_settings()
Product = models.Product
ProductScrapeEvent = models.ProductScrapeEvent
ngrok_authtoken = settings.ngrok_authtoken
ngrok.set_auth_token(ngrok_authtoken)
@asynccontextmanager
async def lifespan(app: FastAPI):
    global session
    session = db.get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)
    # Optionally, open a tunnel automatically on startup:
    public_url = ngrok.connect(8000)
    print("ngrok tunnel available at:", public_url)
    yield
    session.close()
    # Optionally, kill the ngrok tunnel when closing:
    ngrok.disconnect(public_url)

app = FastAPI(lifespan=lifespan)
session = None

@app.get("/")
def read_index():
    return {"Hello": "World", "name": settings.proj_name}

@app.get("/products", response_model=List[schema.ProductListSchema])
def products_list_view():
    return list(Product.objects.all())

@app.post("/events/scrape")
def events_scrape_create_view(data: schema.ProductListSchema):
    product, _ = crud.add_scrape_event(data.dict())
    return product

@app.get("/products/{asin}")
def products_detail_view(asin):
    data = dict(Product.objects.get(asin=asin))
    events = list(ProductScrapeEvent.objects().filter(asin=asin).allow_filtering().limit(5))
    events = [schema.ProductScrapeEventDetailSchema(**x) for x in events]
    data['events'] = events
    data['events_url'] = f"/products/{asin}/events"
    return data

@app.get("/products/{asin}/events", response_model=List[schema.ProductScrapeEventDetailSchema])
def products_scrapes_list_view(asin):
    events = list(ProductScrapeEvent.objects().filter(asin=asin).allow_filtering())
    # Convert to dictionaries before sending to the schema
    return [dict(event) for event in events]