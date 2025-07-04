from django.urls import path
from . import views
from .views import LoginView
from .views import RegisterView
from .views import MypageView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("mypage/", MypageView.as_view(), name="mypage"),
]
