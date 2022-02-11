from typing import List
from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table

from . import (
    db,
    config,
    models,
    schema,
    crud
)

Product = models.Product
ProductScrapeEvent = models.ProductScrapeEvent

settings = config.get_settings()

session = None
app = FastAPI()

@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()

    sync_table(Product)
    sync_table(ProductScrapeEvent)


@app.get("/")
def read_index():
    return {"Hello": "World", "name": settings.name}

@app.get("/products", response_model=List[schema.ProductSchema])
def product_list_view():
    return list(Product.objects.all())

@app.post("/events/scrape")
def events_scrape_create_view(data: schema.ProductListSchema):
    product, _ = crud.add_scrape_event(data.dict())
    return product


@app.get("/products/{asin}")
def product_detail_view(asin):
    data = dict(Product.objects.get(asin=asin))
    events = list(ProductScrapeEvent.objects().filter(asin=asin).limit(5))
    events = [schema.ProductScrapeEventDetailSchema(**x) for x in events]
    data['envents'] = events
    data['events_url'] = f"/products/{asin}/events"
    return data


@app.get("/products/{asin}/events", response_model=List[schema.ProductScrapeEventDetailSchema])
def products_scrapes_list_view(asin):
    return list(ProductScrapeEvent.objects().filter(asin=asin))