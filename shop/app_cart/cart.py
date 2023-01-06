from decimal import Decimal

from django.conf import settings

from app_shop.models import Product
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, F
from django.shortcuts import render

from .models import Cart_db


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """

        self.use_db = False
        self.cart = None
        self.user = request.user
        self.session = request.session
        self.qs = None
        cart = self.session.get(settings.CART_SESSION_ID)
        if self.user.is_authenticated:
            self.use_db = True
            if cart:
                self.save_in_db(cart, request.user)
                self.clear(True)
            self.qs = Cart_db.objects.filter(user=self.user)
            cart = self.get_cart_from_db(self.qs)
        else:
            # save an empty cart in the session
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def get_cart_from_db(self, qs):
        cart = {}
        for item in qs:
            cart[str(item.good.id)] = {'product': item.good, 'quantity': item.quantity, 'price': item.price}
        return cart

    def save_in_db(self, cart, user):
        for key, value in cart.items():
            if Cart_db.objects.filter(user=user, good=key).exists():
                good = Cart_db.objects.select_for_update().get(user=user, good=key)
                good.quantity += cart[key]['quantity']
                good.price = cart[key]['price']
                good.save()
            else:
                product = Product.objects.get(id=key)
                Cart_db.objects.create(
                    user=user,
                    good=product,
                    quantity=value['quantity'],
                    price=value['price'],
                )

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        if self.use_db:
            if self.qs.filter(good=product).exists():
                cart = self.qs.select_for_update().get(good=product)
            else:
                cart = Cart_db(
                    user=self.user,
                    good=product,
                    quantity=0,
                    price=product.price
                )
            if update_quantity:
                cart.quantity = quantity
            else:
                cart.quantity += quantity
            cart.save()
        else:
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()

    def save(self):
        if not self.use_db:
            # update the session cart
            self.session[settings.CART_SESSION_ID] = self.cart
            # mark the session as "modified" to make sure it is saved
            self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        :param product:
        :return:
        """
        if self.use_db:
            if self.qs.filter(good=product).exists():
                self.qs.filter(good=product).delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        if self.use_db:
            for item in self.cart.values():
                item['total_price'] = item['price'] * item['quantity']
                yield item
        else:
            product_ids = self.cart.keys()
            # get the product objects and add them to the cart
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                self.cart[str(product.id)]['product'] = product

            for item in self.cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        if self.use_db:
            total = self.qs. \
                only('quantity', 'price'). \
                aggregate(total=Sum(F('quantity') * F('price')))['total']
            if not total:
                total = 0
            return total
        else:
            return sum(Decimal(item['price']) * item['quantity'] for item in
                       self.cart.values())

    def clear(self, only_session=False):
        """
        remove cart from session or from db if user authorized
        :return:
        """
        if only_session:
            del self.session[settings.CART_SESSION_ID]
            self.session.modified = True
        else:
            if self.qs:
                self.qs.delete()
