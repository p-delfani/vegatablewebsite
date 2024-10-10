from product.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(item['price'])
            item['unique_id'] = self.unique_id_generator(product.id, item['size'])
            yield item

    def unique_id_generator(self, id, size):
        result = f'{id}-{size}'
        return result

    def get_total_quantity(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity, size):
        unique = self.unique_id_generator(product.id, size)
        if unique not in self.cart:
            self.cart[unique] = {'quantity': 0, 'price': str(product.price), 'size': size, 'id': product.id}

        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def total(self):
        cart = self.cart.values()
        total_price = sum(int(item['price']) * int(item['quantity']) for item in cart)
        return total_price

    def remove_cart(self):
        del self.session[CART_SESSION_ID]

    def empty_cart(self):
        if not self.cart:
            return True

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True
