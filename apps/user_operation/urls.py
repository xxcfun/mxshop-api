from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from user_operation import views

router = DefaultRouter()

# 用户收藏
router.register(r'userfav', views.UserFavViewset, basename='userfav')
# 用户留言
router.register(r'message', views.LeavingMessageViewset, basename='message')
# 用户收货地址
router.register(r'address', views.AddressViewset, basename='address')

urlpatterns = [
    re_path('^', include(router.urls))
]
