from amazon.api import AmazonAPI
from flask import render_template

amazon = AmazonAPI('***REMOVED***', '***REMOVED***', '***REMOVED***', region='UK')


def search_for(text, top=3):
    products = amazon.search(Keywords=text, SearchIndex='All')

    top_products = []

    for product in products:
        if product.title is not None and product.price_and_currency is not None:

            top_products.append(product)
            top -= 1
            if top == 0:
                break

    return top_products


def get_amazon_items(text, preview):
    products = search_for(text)
    return render_template('amazon.html', products=products, preview=preview)
