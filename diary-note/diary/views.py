from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import Diary
from .serializer import DiarySerializer
from .permissons import UserIsOwnedDiary


"""def diary_list(request):
    diaries = Diary.objects.filter(author_id=request.user.id)
    # 데이터가 여러개 일경우 many=True 파라미터를 줘야한다는것 같다.
    serializers = DiarySerializer(diaries, many=True)
    return Response({'diaries': serializers.data})"""


class DiaryList(ListAPIView):
    # 마찬가지로 session 추가 안했더니 안된다.
    # default로 정해놓은다고 전부다 적용이 아니라 이런 방식으로 따로
    # ()로 해놓을경우 디폴트르 따라가지 않는다. 즉 아무것도 없는 권한, 인증처리이다
    authentication_classes = (SessionAuthentication, )
    permission_classes = ()
    serializer_class = DiarySerializer
    queryset = Diary.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(author_id=self.request.user.id)

