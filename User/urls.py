from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.hello_world, name="login"),
    path("register/", views.create_user, name="create_user"),
    path("mypage/", views.hello_world, name="mypage"),
]
