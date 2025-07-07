from django.urls import path
from . import views

urlpatterns = [
    path("work/", views.work, name="work"),
    path("write/", views.write, name="write"),
]
