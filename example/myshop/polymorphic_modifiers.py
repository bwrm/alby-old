# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from shop.modifiers.defaults import DefaultCartModifier


class MyShopCartModifier(DefaultCartModifier):
    """
    Extended default cart modifier which handles the price for product variations
    """
    def process_cart_item(self, cart_item, request):
        # variant = cart_item.product.get_product_variant(product_code=cart_item.product_code)
        # cart_item.product.get_price(request)
        # variant = cart_item.product.get(product_code=cart_item.product_code)
        # cart_item.unit_price = cart_item.product.get(request)
        cart_item.unit_price = cart_item.product.get_price(request)
        try:
            discount = cart_item.product.get_rebate(cart_item.quantity)
        except:
            discount = 0
        if discount:
            cart_item.unit_price = cart_item.unit_price - (cart_item.unit_price*discount)/100
        cart_item.line_total = discount
        cart_item.line_total = cart_item.unit_price * cart_item.quantity
        # get price with rebate depending on order's quantity
        # cart_item.line_total = cart_item.line_total - (cart_item.line_total*discount)/100
        # grandparent super
        return super(DefaultCartModifier, self).process_cart_item(cart_item, request)
