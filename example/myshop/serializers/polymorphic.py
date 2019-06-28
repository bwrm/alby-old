# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.fields import empty

from shop.serializers.bases import ProductSerializer
from shop.serializers.defaults import AddToCartSerializer

from myshop.models import SmartCard, SmartPhoneModel, LamellaFix, Fabric
from django.utils import six
from django.utils.html import strip_spaces_between_tags
from django.template.loader import select_template
from django.utils.safestring import mark_safe, SafeText
from django.core.cache import cache


class FabricSerializer(ProductSerializer):
    class Meta:
        model = Fabric
        fields = ['id', 'product_name', 'slug', 'unit_price', 'fabric_type', 'composition', 'care',
                  'product_code']


# class FabricToCartSerializer(AddToCartSerializer):
#
#     def get_instance(self, context, data, extra_args):
#         """
#         Method calculate product's subtotal price depending on order number
#         """
#         product = context['product']
#         return {
#             'product': product.id,
#             'product_code': product.product_code,
#         }
#

class SmartCardSerializer(ProductSerializer):
    class Meta:
        model = SmartCard
        fields = ['product_name', 'slug', 'unit_price', 'manufacturer', 'card_type', 'speed',
                  'product_code', 'storage']


class SmartPhoneSerializer(ProductSerializer):
    class Meta:
        model = SmartPhoneModel
        fields = ['product_name', 'slug', 'battery_type', 'battery_capacity']


class LamellaFixToCartSerializer(AddToCartSerializer):

    def get_instance(self, context, data, extra_args):
        """
        Method calculate product's subtotal price depending on order number
        """
        product = context['product']
        extra = data.get('extra', {}) if data is not empty else {}
        unit_price = product.get_price(context['request'])
        try:
            rebate = product.get_rebate(data.get('quantity'))
        except:
            rebate = 0
        price = unit_price * data.get('quantity')
        rebate_price = price - (price*rebate)/100
        if rebate:
            unit_price = unit_price - (unit_price*rebate)/100

        return {
            'product': product.id,
            'product_code': product.product_code,
            'unit_price': unit_price,
            'subtotal': rebate_price,
            'extra': extra,
        }


class AddSmartPhoneToCartSerializer(AddToCartSerializer):
    """
    Modified AddToCartSerializer which handles SmartPhones
    """
    def get_instance(self, context, data, extra_args):
        product = context['product']
        if data is empty:
            product_code = None
            extra = {}
        else:
            product_code = data.get('product_code')
            extra = data.get('extra', {})
        try:
            variant = product.get_product_variant(product_code=product_code)
        except product.DoesNotExist:
            variant = product.variants.first()
        extra.update(storage=variant.storage)
        instance = {
            'product': product.id,
            'product_code': variant.product_code,
            'unit_price': variant.unit_price,
            'extra': extra,
        }
        return instance
