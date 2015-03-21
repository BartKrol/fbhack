from amazon.api import AmazonAPI
amazon = AmazonAPI('***REMOVED***', '***REMOVED***', '***REMOVED***')


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
