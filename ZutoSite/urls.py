from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("user/", include("User.urls")),
    path("pages/", include("ZutoPages.urls")),
]
