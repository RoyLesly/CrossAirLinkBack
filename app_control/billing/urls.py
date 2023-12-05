from django.urls import path, include
from rest_framework import routers
from .views import *

app_name = "app_control.billing"

router = routers.DefaultRouter(trailing_slash=False)
router.register('crud-customer',  CustomerCRUDView, "crud-customer" ),
router.register('bundle',  BundleView, "bundle" ),
router.register('crud-transactions',  CRUDTransactions, "crud-transactions" ),

urlpatterns = [
    path('', include(router.urls)),
]
