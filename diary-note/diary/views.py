from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Diary
from .serializer import DiarySerializer


class DiaryList(ListAPIView):
    # 마찬가지로 session 추가 안했더니 안된다.
    # default로 정해놓은다고 전부다 적용이 아니라 이런 방식으로 따로
    # ()로 해놓을경우 디폴트르 따라가지 않는다. 즉 아무것도 없는 권한, 인증처리이다
    # authentication 은 해당하는 기능의 데이터에 접근할때 인증 방법인것 같다.
    # 세션인증 방식이라면 로그인이 되어있으면 되는것이고
    # 토큰 인증방식이라면 토큰을 인증했어야 된다.
    authentication_classes = (TokenAuthentication,)
    # permission 은 해당하는 기능에 접근할 수 있는 권한 인것 같다.
    permission_classes = (IsAuthenticated,)
    serializer_class = DiarySerializer

    def get_queryset(self):
        queryset = Diary.objects.filter(author_id=self.request.user)
        return queryset

