# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from shop.modifiers.pool import cart_modifiers_pool
from shop.serializers.cart import ExtraCartRow
from shop.modifiers.base import ShippingModifier
from shop.money import Money
from shop.shipping.defaults import DefaultShippingProvider
from shop.payment.defaults import ForwardFundPayment
from myshop.payment import CodPayment

from shop.modifiers.base import PaymentModifier


class PostalShippingModifier(ShippingModifier):
    identifier = 'postal-shipping'
    shipping_provider = DefaultShippingProvider()

    def get_choice(self):
        return (self.identifier, _("Postal shipping"))

    def add_extra_cart_row(self, cart, request):
        if not self.is_active(cart) and len(cart_modifiers_pool.get_shipping_modifiers()) > 1:
            return
        # postal tarifs by Siarhei
        if cart.total_weight == 0:
            amount = 0
        elif cart.total_weight<1:
            amount = Money('4')
        elif cart.total_weight >=1 and cart.total_weight < 3:
            amount = Money('7.5')
        elif cart.total_weight >=3 and cart.total_weight < 15:
            amount = Money('10')
        elif cart.total_weight >=15 and cart.total_weight < 30:
            amount = Money('20')
        elif cart.total_weight > 30:
            amount = Money('500')
        else:
            amount = Money('999')
        # add a shipping flat fee
        instance = {'label': _("Shipping costs"), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount


class PostalPremiumShippingModifier(ShippingModifier):
    "class implement premium shipping modifier (from post to door)"
    identifier = 'postal-shipping-premium'
    shipping_provider = DefaultShippingProvider()

    def get_choice(self):
        return (self.identifier, _("Postal shipping premium"))

    def add_extra_cart_row(self, cart, request):
        if not self.is_active(cart) and len(cart_modifiers_pool.get_shipping_modifiers()) > 1:
            return
        # postal tarifs by Siarhei
        if cart.total_weight<1:
            amount = Money('6')
        elif cart.total_weight >=1 and cart.total_weight < 3:
            amount = Money('9')
        elif cart.total_weight >=3 and cart.total_weight < 15:
            amount = Money('12')
        elif cart.total_weight >=15 and cart.total_weight < 30:
            amount = Money('23')
        elif cart.total_weight > 30:
            amount = Money('500')
        else:
            amount = Money('999')
        # add a shipping flat fee
        instance = {'label': _("Shipping costs to home"), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount


class CustomerPickupModifier(ShippingModifier):
    identifier = 'customer-pickup'

    def get_choice(self):
        return (self.identifier, _("Customer pickups the goods"))

class CourierModifier(ShippingModifier):
    identifier = 'courier-delivery'
    shipping_provider = DefaultShippingProvider()

    def get_choice(self):
        return (self.identifier, _("Courier delivery. Onliy within Minsk"))

    def add_extra_cart_row(self, cart, request):
        if not self.is_active(cart) and len(cart_modifiers_pool.get_shipping_modifiers()) > 1:
            return
        # add a shipping flat fee
        amount = Money('3')
        instance = {'label': _("Courier shipping costs"), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount


class CashOnDeliveryPostModifier(PaymentModifier):
    """
    This modifiers has 5% influence on the cart final. It used,
    to enable the customer to pay the products on postal-delivery.
    """
    identifier = 'cash-on-post'
    payment_provider = CodPayment()
    commision_percentage = 5

    def get_choice(self):
        return (self.identifier, _("Cash on Post"))

    def add_extra_cart_row(self, cart, request):
        from decimal import Decimal
        if not self.is_active(cart) or not self.commision_percentage:
            return
        amount = cart.total * Decimal(self.commision_percentage / 100.0)
        instance = {'label': _("+ {}% handling fee").format(self.commision_percentage), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount


class CashOnDeliveryModifier(PaymentModifier):
    """
    This modifiers no influence on the cart final. It used,
    to enable the customer to pay the products on postal-delivery.
    """
    identifier = 'cash-on-delivery'
    payment_provider = CodPayment()
    commision_percentage = 0

    def get_choice(self):
        return (self.identifier, _("Cash on Delivery"))

    def add_extra_cart_row(self, cart, request):
        from decimal import Decimal
        if not self.is_active(cart) or not self.commision_percentage:
            return
        amount = cart.total * Decimal(self.commision_percentage / 100.0)
        instance = {'label': _("+ {}% handling fee").format(self.commision_percentage), 'amount': amount}
        cart.extra_rows[self.identifier] = ExtraCartRow(instance)
        cart.total += amount

# class StripePaymentModifier(modifiers.StripePaymentModifier):
#     commision_percentage = 3
