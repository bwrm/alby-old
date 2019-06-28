# -*- coding: utf-8 -*-
"""
These URL routings are used by the example `polymorphic` as found in the django-SHOP's tutorials.
The difference here is that we added a special serializer class to add smart phones with their
variations to the cart.
"""
from __future__ import unicode_literals

from django.conf.urls import url

from shop.search.views import CMSPageCatalogWrapper
from shop.views.catalog import AddToCartView, ProductRetrieveView, ProductListView

# from myshop.filters import CustomFilterSet
# from myshop.filters import ManufacturerFilterSet
from myshop.serializers import FabricSerializer, CatalogSearchSerializer
from myshop.models import Fabric


urlpatterns = [
    # url(r'^$', CMSPageCatalogWrapper.as_view()),
    url(r'^$', ProductListView.as_view(product_model=Fabric, serializer_class=FabricSerializer)),
]
