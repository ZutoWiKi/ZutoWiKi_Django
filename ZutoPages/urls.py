from django.urls import path
from . import views

urlpatterns = [
    path("novel/", views.novel, name="novel"),
    path("poem/", views.poem, name="poem"),
    path("music/", views.music, name="music"),
    path("game/", views.game, name="game"),
    path("movie/", views.movie, name="movie"),
    path("performance/", views.performance, name="performance"),
    path("animation/", views.animation, name="animation"),
]
