from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Diary
from .serializer import DiarySerializer
# Create your views here.


@api_view()
def diary_list(request):
    diaries = Diary.objects.filter(author_id=request.user.id)
    # 데이터가 여러개 일경우 many=True 파라미터를 줘야한다는것 같다.
    serializers = DiarySerializer(diaries, many=True)
    return Response({'diaries': serializers.data})


