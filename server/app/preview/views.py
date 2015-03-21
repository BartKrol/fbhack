from app.amazon_search import get_amazon_items
from . import preview
from app.rome_rio import get_rome_rio
from app.people import People


@preview.route("/amazon/<item>")
def amazon(item):
    return get_amazon_items(item, True)


@preview.route("/route/<from_address>/<to_address>")
def rome_rio(from_address, to_address):
    return get_rome_rio(from_address, to_address, True)

@preview.route("/people/<person>")
def people(person):
    p = People(person)
    return p.get_html(True)
