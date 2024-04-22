from parser.celery import app
from . import ozon_parser


@app.task()
def parse_product(products_count):
    ozon_parser.parse_product(products_count)
