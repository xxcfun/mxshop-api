from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from goods import views

router = DefaultRouter()

# 商品列表
router.register(r'goods/list', views.GoodsListViewSet, basename='goods_list')
# 商品分类
router.register(r'categorys', views.CategoryViewSet, basename='categorys')
# 首页轮播图
router.register(r'banners', views.BannerViewset, basename='banners')
# 首页系列商品展示
router.register(r'indexgoods', views.IndexCategoryViewset, basename='indexgoods')

urlpatterns = [
    re_path('^', include(router.urls))
]
