from django.urls import path
from . import views

urlpatterns = [
    path("work/", views.work, name="work"),
    path("write/", views.write, name="write"),
    path(
        "write/<int:write_id>/views/",
        views.update_write_views,
        name="update_write_views",
    ),
    path(
        "write/<int:write_id>/likes/",
        views.update_write_likes,
        name="update_write_likes",
    ),
    path("user/", views.create_user, name="create_user"),
    path("upload/", views.ImageUploadView.as_view(), name="image-upload"),
]
