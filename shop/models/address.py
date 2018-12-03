# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Holds all the information relevant to the client (addresses for instance)
"""
from six import with_metaclass

from django.db import models
from django.template.loader import select_template
from django.utils.translation import ugettext_lazy as _

from shop import deferred
from shop.conf import app_settings


class AddressManager(models.Manager):
    def get_max_priority(self, customer):
        aggr = self.get_queryset().filter(customer=customer).aggregate(models.Max('priority'))
        priority = aggr['priority__max'] or 0
        return priority

    def get_fallback(self, customer):
        """
        Return a fallback address, whenever the customer has not declared one.
        """
        return self.get_queryset().filter(customer=customer).order_by('priority').last()


class BaseAddress(models.Model):
    customer = deferred.ForeignKey('BaseCustomer')

    priority = models.SmallIntegerField(
        default=0,
        db_index=True,
        help_text=_("Priority for using this address"),
    )

    class Meta:
        abstract = True

    objects = AddressManager()

    def as_text(self):
        """
        Return the address as plain text to be used for printing, etc.
        """
        template_names = [
            '{}/{}-address.txt'.format(app_settings.APP_LABEL, self.address_type),
            '{}/address.txt'.format(app_settings.APP_LABEL),
            'shop/address.txt',
        ]
        template = select_template(template_names)
        context = {'address': self}
        return template.render(context)
    as_text.short_description = _("Address")


class BaseShippingAddress(with_metaclass(deferred.ForeignKeyBuilder, BaseAddress)):
    address_type = 'shipping'

    class Meta:
        abstract = True

ShippingAddressModel = deferred.MaterializedModel(BaseShippingAddress)


class BaseBillingAddress(with_metaclass(deferred.ForeignKeyBuilder, BaseAddress)):
    address_type = 'billing'

    class Meta:
        abstract = True

BillingAddressModel = deferred.MaterializedModel(BaseBillingAddress)

ISO_3166_CODES = (
    ('BB', _("Barbados")),
    ('BY', _("Belarus")),
)

class CountryField(models.CharField):
    """
    This creates a simple input field to choose a country.
    """
    def __init__(self, *args, **kwargs):
        defaults = {
            'max_length': 3,
            'choices': ISO_3166_CODES,
        }
        defaults.update(kwargs)
        super(CountryField, self).__init__(*args, **defaults)

    def deconstruct(self):
        name, path, args, kwargs = super(CountryField, self).deconstruct()
        if kwargs['max_length'] == 3:
            kwargs.pop('max_length')
        if kwargs['choices'] == ISO_3166_CODES:
            kwargs.pop('choices')
        return name, path, args, kwargs
