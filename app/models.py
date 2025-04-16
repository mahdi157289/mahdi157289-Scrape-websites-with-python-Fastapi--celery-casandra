from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
data = {
    "asin": "B00123499t56ty7",
    "title": "Sample Product Title",
}

# Detail view  ->  detail View
class Product(Model):  # --> table
    __keyspace__ = "scrapper_app"  
    asin = columns.Text(primary_key=True, required=True)  # --> partition key
    title = columns.Text()
    Price_str = columns.Text(default="-100") 
    
    
# Detail view for asin
class ProductScrapeEvent(Model):  # --> table
    __keyspace__ = "scrapper_app"  
    uuid = columns.UUID(primary_key=True)  # --> partition key
    asin = columns.Text(primary_key=True, required=True)  # --> partition key
    title = columns.Text()
    Price_str = columns.Text(default="-100")    
    
# def this -> Product.object().filter(asin="B001234567")
# not this -> Product.object().filter(title="Sample Product Title")    