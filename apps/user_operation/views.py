from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user_operation.models import UserFav, UserLeavingMessage, UserAddress
from user_operation.serializers import UserFavSerializer, UserFavDetailSerializer, LeavingMessageSerializer, \
    AddressSerializer
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """ 用户收藏 """
    # permission是用来做权限判断的
    # IsAuthenticated：必须登录用户；IsOwnerOrReadOnly：必须是当前登录的用户
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # auth使用来做用户认证的
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 搜索的字段
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 只能查看当前登录用户的收藏，不会获取所有用户的收藏
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer
        return UserFavSerializer

    # 用户收藏的商品数量
    def perform_create(self, serializer):
        instance = serializer.save()
        # 这里instance相当于UserFav model，通过它找到goods
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


class LeavingMessageViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list：
        获取用户留言
    create：
        添加留言
    delete：
        删除留言功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = LeavingMessageSerializer

    # 只能看到自己的留言
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(viewsets.ModelViewSet):
    """
    收货地址管理
    list:
        获取收货地址
    create:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
