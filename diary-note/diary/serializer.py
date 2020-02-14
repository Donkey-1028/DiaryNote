from rest_framework import serializers

from .models import Diary


class DiaryListAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = '__all__'


class DiaryCreateAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        exclude = ['created', 'updated', 'author']


class DiaryRetrieveUpdateDestroyAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        exclude = ['created', 'updated', 'author']
