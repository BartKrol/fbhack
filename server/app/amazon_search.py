from amazon.api import AmazonAPI
from flask import render_template

amazon = AmazonAPI('***REMOVED***', '***REMOVED***', '***REMOVED***', region='UK')


def search_for(text, top=3):
    products = amazon.search(Keywords=text, SearchIndex='All')

    top_products = []

    product_titles = {}

    for product in products:
        if product.title is not None and product.price_and_currency is not None:
            title = product.title
            if len(title) > 50:
                title = title[:50] + "..."

            product_titles[product.offer_url] = title
            top_products.append(product)
            top -= 1
            if top == 0:
                break

    return top_products, product_titles


def get_amazon_items(text, preview):
    (products, product_titles) = search_for(text)
    return render_template('amazon.html', products=products, titles=product_titles, preview=preview)
