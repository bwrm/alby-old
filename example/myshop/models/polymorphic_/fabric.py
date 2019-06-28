# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField

from shop.money.fields import MoneyField

from .product import Product, BaseProductManager


class Fabric(Product):
    # common product fields
    unit_price = MoneyField(
        _("Price per meter"),
        decimal_places=3,
        help_text=_("Net price for this product by meter"),
    )

    # product properties
    FABRIC_TYPE = [
        ('leath','leather'),
        ('velv', 'velvet'),
        ('wool','wool'),
    ]
    fabric_type = models.CharField(
        _("Fabric type"),
        choices=FABRIC_TYPE,
        max_length=15,
    )

    product_code = models.CharField(
        _("Product code"),
        max_length=255,
        unique=True,
    )
    composition = models.CharField(
        _("Comosition of fabric"),
        max_length=255,
        unique=False,
    )
    care = models.CharField(
        _("Recommended wash care"),
        max_length=255,
        unique=False,
    )

    description = HTMLField(
        verbose_name=_("Description"),
        configuration='CKEDITOR_SETTINGS_DESCRIPTION',
        help_text=_("Full description used in the catalog's detail view of Fabrics"),
    )

    default_manager = BaseProductManager()

    class Meta:
        verbose_name = _("Fabric")
        verbose_name_plural = _("Fabrics")

    def get_price(self, request):
        return self.unit_price
