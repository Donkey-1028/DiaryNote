from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializer import UserRegistrationSerializer

# Create your views here.


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        # Returns a serializer instance.
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Called by CreateModelMixin when saving a new object instance.
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    """user 생성시 token 자동 생성"""
    if created:
        Token.objects.create(user=instance)
