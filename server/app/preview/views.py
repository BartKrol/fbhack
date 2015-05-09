from app.amazon_search import get_amazon_items
from . import preview
from app.rome_rio import get_rome_rio
from app.people import People
from app.film import Film


@preview.route("/amazon/<item>")
def amazon(item):
    return get_amazon_items(item, True)


@preview.route("/route/<from_address>/<to_address>")
def rome_rio(from_address, to_address):
    return get_rome_rio(from_address, to_address, True)


@preview.route("/people/<person>/<description>")
def people(person, description):
    p = People(person, description)
    return p.get_html(True)


@preview.route("/film/<film>")
def films(film):
    f = Film(film, "Description here.")
    f.get_info()
    return f.get_html()
