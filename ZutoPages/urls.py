from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello_world, name="hello"),
    path("users/", views.create_user, name="create_user"),
]
