from contextlib import asynccontextmanager
from fastapi import FastAPI
from .db import get_session
from typing import List
from . import (
    config,
    db,
    models,
    schema
)
from cassandra.cqlengine.management import sync_table
settings = config.get_settings()
Product = models.Product
ProductScrapeEvent = models.ProductScrapeEvent

@asynccontextmanager
async def lifespan(app: FastAPI):
    global session
    session = db.get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)
    yield
    session.close()

app = FastAPI(lifespan=lifespan)
session = None
@app.get("/")
def read_index():
    return {"Hello": "World", "name":settings.proj_name}


@app.get("/products", response_model=List[schema.ProductListSchema])
def products_list_view():
    return list(Product.objects.all())



@app.get("/products/{asin}")
def products_detail_view(asin):
    data = dict(Product.objects.get(asin=asin))
    events = list(ProductScrapeEvent.objects().filter(asin=asin).allow_filtering().limit(5))
    events = [schema.ProductScrapeEventDetailSchema(**x) for x in events]
    data['events'] = events
    data['events_url'] = f"/products/{asin}/events"
    return data