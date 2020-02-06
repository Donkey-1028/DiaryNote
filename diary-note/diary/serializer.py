from .models import Diary
from rest_framework import serializers


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'
