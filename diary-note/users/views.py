from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializer import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer

# Create your views here.


class UserRegistrationAPIView(CreateAPIView):
    """회원 가입"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        # Returns a serializer instance.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Called by CreateModelMixin when saving a new object instance.
        self.perform_create(serializer)

        data = serializer.data
        """user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data["token"] = token.key"""

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    """user 생성시 token 자동 생성"""
    if created:
        Token.objects.create(user=instance)


class UserLoginAPIView(GenericAPIView):
    """로그인"""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class UserTokenAPIView(RetrieveAPIView):
    """로그인 된 유저의 토큰 확인"""
    lookup_field = "key"
    serializer_class = TokenSerializer
    authentication_classes = (SessionAuthentication,)
    # 인증이 되어야만 확인가능, api-doc에도 인증이 되어야만 추가됨.
    permission_classes = (IsAuthenticated,)
    queryset = Token.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = Token.objects.get(user=self.request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
