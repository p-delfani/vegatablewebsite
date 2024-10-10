from product.models import Product

WISHLIST_SESSION_ID = 'wishlist'


class WishList:
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get(WISHLIST_SESSION_ID)

        if not wishlist:
            wishlist = self.session[WISHLIST_SESSION_ID] = {}

        self.wishlist = wishlist

    def __iter__(self):
        product_ids = [int(item['id']) for item in self.wishlist.values()]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {product.id: product for product in products}

        for item in self.wishlist.values():
            product = product_map.get(int(item['id']))
            if product:
                yield {
                    'product': product,
                    'quantity': item['quantity'],
                    'size': item['size'],
                }

    def add(self, product, quantity=1, size=None):
        unique = f'{product.id}-{size}'
        if unique not in self.wishlist:
            self.wishlist[unique] = {
                'id': product.id,
                'quantity': quantity,
                'size': size,
            }
        self.save()

    def empty_cart(self):
        return not bool(self.wishlist)

    def delete_item(self, product_id, size=None):
        if size:
            unique = f'{product_id}-{size}'
        else:
            unique = f'{product_id}-None'

        if unique in self.wishlist:
            del self.wishlist[unique]
            self.save()

    def save(self):
        self.session[WISHLIST_SESSION_ID] = self.wishlist
        self.session.modified = True
