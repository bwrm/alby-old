# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import default models from shop to materialize them
from shop.models.defaults.address import ShippingAddress, BillingAddress
from shop.models.defaults.cart import Cart
from shop.models.defaults.cart_item import CartItem
from shop.models.defaults.customer import Customer

__all__ = ['ShippingAddress', 'BillingAddress', 'Cart', 'CartItem', 'Customer', 'OrderItem',
           'Commodity', 'SmartCard', 'SmartPhoneModel', 'SmartPhoneVariant', 'Delivery', 'DeliveryItem']

# models defined by the myshop instance itself
from .polymorphic_.order import OrderItem
from .polymorphic_.product import Product
from .polymorphic_.commodity import Commodity
from .polymorphic_.smartcard import SmartCard
from .polymorphic_.fabric import Fabric
from .polymorphic_.lamella import LamellaFix
from .polymorphic_.smartphone import SmartPhoneModel, SmartPhoneVariant

from shop.models.defaults.delivery import Delivery, DeliveryItem
__all__.extend(['SmartCard', 'SmartPhoneModel', 'SmartPhoneVariant', 'Delivery', 'DeliveryItem'])
