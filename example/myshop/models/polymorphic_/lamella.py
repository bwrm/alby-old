# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from djangocms_text_ckeditor.fields import HTMLField
from ..discount import Discount
from shop.money.fields import MoneyField
from random import randint

from .product import Product, BaseProductManager


class LamellaFix(Product):
    # common product fields
    unit_price = MoneyField(
        _("Unit price"),
        decimal_places=3,
        help_text=_(" per unit"),
    )
    LAM_WIDTH = (('38', '38 mm'), ('53', '53 mm'), ('63', '63 mm'), ('68', '68 mm'))

    lamella_width = models.CharField(
        _('width'),
        default=53,
        max_length=6,
        choices=LAM_WIDTH,
        help_text=_("Lammelas width")
    )

    length = models.CharField(
        _("Lamella's length"),
        max_length=25,
        blank=True,
    )

    depth = models.CharField(
        _("Lamella's depth"),
        max_length=25,
        blank=True,
    )

    weight = models.CharField(
        _('weight'),
        default=0,
        max_length=6,
        help_text=_("Weight of item, kg")
    )
    is_lamella = models.BooleanField(
        _("Lamella"),
        default=True,
        help_text=_("Is this lamella (for calculating weight)."),
    )

    weight_by_hand = models.BooleanField(
        _("Enter weight by hand"),
        default=False,
        help_text=_("For enter lamella weight by hand"),
    )

    discont_scheme = models.ForeignKey(Discount, blank=True, on_delete=models.CASCADE)

    product_code = models.CharField(
        _("Product code"),
        max_length=255,
        blank=True,
    )

    description = HTMLField(
        verbose_name=_("Description"),
        configuration='CKEDITOR_SETTINGS_DESCRIPTION',
        help_text=_("Full description used in the catalog's detail view of Smart Cards."),
    )

    default_manager = BaseProductManager()

    class Meta:
        verbose_name = _("Lamella")
        verbose_name_plural = _("Lamellas")

    def is_unique_scu(self, scu):
        scu = str(scu)
        try:
            LamellaFix.objects.get(product_code=scu)
            return False
        except:
            return True

    def set_num_scu(self, scu, n):
        scu = str(scu)
        while len(scu) <= int(n):
            scu = '0'+ scu
        return scu

    def get_max_scu(self):
        codes = LamellaFix.objects.all()
        max_scu = 0
        for code in codes:
            code = int(code.product_code)
            if code > max_scu:
                max_scu = code
        return max_scu

    def save(self, *args, **kwargs):
        if not self.product_code or not self.is_unique_scu(self.product_code):
            max_scu = int(self.get_max_scu())
            while True:
                new_scu = max_scu + 1
                if self.is_unique_scu(new_scu):
                    self.product_code = self.set_num_scu(new_scu, 4)
                    break

        # TODO: unique product_code

        if(self.is_lamella and not self.weight_by_hand):
            m = 0.00075  # calculated empiric method
            vol = float(self.length) * float(self.lamella_width) * float(self.depth)
            self.weight = round((vol * m / 1000), 3)
        super(LamellaFix, self).save(*args, **kwargs)


    def get_price(self, request):
        return self.unit_price

    def get_rebate(self, x):
        some_str = self.discont_scheme.discont_scheme.split("\r\n")
        x = int(x)
        temp_discont = 0
        for i in some_str:
            discont = i.split(":")
            num = int(discont[0]) #get first element of tuple for get quantity in db
            if x>=num:
                temp_discont = int(discont[1])
            elif x<=num:
                return temp_discont
        return temp_discont
