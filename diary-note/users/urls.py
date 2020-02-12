from django.urls import path

from .views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserLogoutAPIView

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('token/<key>', UserTokenAPIView.as_view(), name='token'),
]
