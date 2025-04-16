from .models import Product 
from .db import get_session
from cassandra.cqlengine.management import sync_table
from .models import Product, ProductScrapeEvent
import uuid
import copy #safe duplication

#  Initialize Tabless
session = get_session()
sync_table(Product) # ensures the schema exists.
sync_table(ProductScrapeEvent)# Sync the Product table with the database



def create_entry(data:dict):
    return Product.create(**data)


def create_scrape_entry(data:dict ):
    data['uuid'] = uuid.uuid1() 
    return ProductScrapeEvent.create(**data)


     
def add_scrape_event(data:dict , fresh=False):
    if  fresh:
        data = copy.deepcopy(data)
    product = create_entry(data)
    scrape_obj = create_scrape_entry(data)
    return product, scrape_obj