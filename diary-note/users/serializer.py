from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    # 해당 데이터를 직렬화하지 않으려면 write_only=True
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password")

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('Passwords do no match')
        del attrs['confirm_password']
        attrs['password'] = make_password(attrs['password'])
        return attrs
