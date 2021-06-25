from random import choice

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import viewsets, status, mixins, authentication, permissions
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from MxShop.settings import APIKEY
from users.models import VerifyCode
from users.serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian

User = get_user_model()


class CustomBackend(ModelBackend):
    """ 自定义用户验证 """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用户名和手机都能登录
            user = User.objects.get(
                Q(username=username) | Q(mobile=username)
            )
            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ 手机验证码 """
    serializer_class = SmsSerializer

    def generate_code(self):
        """ 生成思维数字的验证码 """
        seeds = '1234567890'
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证合法化
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        yun_pian= YunPian(APIKEY)
        # 生成验证码
        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    # TODO 接入云片网，完成注册的功能
    """ 用户 """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)

        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 这里需要动态权限配置
    # 1.用户注册的时候不应该有权限限制
    # 2.当想获取用户详细信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    # 这里需要动态选择用哪个序列化方式
    # 1.UserRegSerializer（用户注册），只返回username和mobile，会员中心页面需要显示更多的字段，所以要创建一个UserDetailSerializer
    # 2.如果注册的时候使用UserDetailSerializer，又会导致验证失败，所以需要动态的使用serializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    # 虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所以要重写get_object方法
    # 重写get_object方法，就知道是哪个用户了
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
