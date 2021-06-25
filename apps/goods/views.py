from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from goods.filters import GoodsFilter
from goods.models import Goods, GoodsCategory, Banner
from goods.serializers import GoodsSerializer, CategorySerializer1, BannerSerializer, IndexCategorySerializer


class GoodsPagination(PageNumberPagination):
    """ 商品列表自定义分页 """
    # 默认每页显示的个数
    page_size = 12
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list：
        商品列表页，分页，搜索，过滤，排序
    retrieve：
        获取商品详情
    """
    # 分页
    pagination_class = GoodsPagination
    # 定义一个默认的排序，防止报错
    queryset = Goods.objects.all().order_by('id')
    # 序列化
    serializer_class = GoodsSerializer
    # 过滤器
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # 搜索，=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 排序
    ordering_fields = ('sold_num', 'shop_price')

    # 商品点击数 +1
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance).data
        return Response(serializer)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ list:商品分类列表数据  RetrieveModelMixin查询参数替换 """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer1


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 首页轮播图 """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """ 商品首页分类数据 """
    # 获取is_tab=True（导航栏）里面的分类下的商品数据
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '酒水饮料'])
    serializer_class = IndexCategorySerializer
