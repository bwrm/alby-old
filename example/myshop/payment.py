# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from shop.models.order import OrderModel
from shop.payment.base import PaymentProvider
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from django_fsm import transition, RETURN_VALUE

from shop.models.order import BaseOrder, OrderModel
from shop.payment.base import PaymentProvider
from shop.payment.defaults import CancelOrderWorkflowMixin


class CodPayment(PaymentProvider):
    """
    Provides a simple payment provider without payment (C.O.D).
    """
    namespace = 'cash-on-delivery'

    def get_payment_request(self, cart, request):
        order = OrderModel.objects.create_from_cart(cart, request)
        order.populate_from_cart(cart, request)
        order.is_fully_paid()
        order.save()
        thank_you_url = OrderModel.objects.get_latest_url()
        return 'window.location.href="{}";'.format(thank_you_url)


