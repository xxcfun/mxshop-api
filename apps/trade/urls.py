from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from trade import views

router = DefaultRouter()

# 购物车
router.register(r'shopcarts', views.ShoppingCartViewset, basename='shopcarts')
router.register(r'orders', views.OrderViewset, basename='orders')

urlpatterns = [
    re_path('^', include(router.urls))
]
