from django.shortcuts import render
from .models import Diary
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


@api_view()
def diary_list(request):
    return Response({'message': 'hi'})