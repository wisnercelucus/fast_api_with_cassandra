from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


data = {
    "asin": "AMZIDNUMBER",
    "title": "My Cool Product"
}


# List View -> Detail View
class Product(Model): # -> table
    __keyspace__ = "scrapper_app" #
    asin = columns.Text(primary_key=True, required=True)
    title = columns.Text()
    brand = columns.Text()
    price_str = columns.Text(default="-100")
    country_of_origin = columns.Text()

# Detail View for asin
class ProductScrapeEvent(Model): # -> table
    __keyspace__ = "scrapper_app" #
    uuid = columns.UUID(primary_key=True) # uuid.uuid1() -> #time
    asin = columns.Text(index=True)
    title = columns.Text()
    brand = columns.Text()
    country_of_origin = columns.Text() 
    price_str = columns.Text(default="-100")

# def this -> ProductScrapeEvent.objects().filter(asin="AMZNIDNUMBER")

