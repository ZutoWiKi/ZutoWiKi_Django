from django.urls import path
from . import views

urlpatterns = [
    path("novel/", views.hello_world, name="novel"),
    path("poem/", views.hello_world, name="poem"),
    path("music/", views.hello_world, name="music"),
    path("game/", views.hello_world, name="game"),
    path("movie/", views.hello_world, name="movie"),
    path("perfomance/", views.hello_world, name="perfomance"),
]
