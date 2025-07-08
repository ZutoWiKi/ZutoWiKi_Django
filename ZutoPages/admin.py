from django.contrib import admin
from .models import Work, Write, WriteLike


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "get_type_index_display"]
    list_filter = ["type_index"]
    search_fields = ["title", "author"]
    ordering = ["-id"]


@admin.register(Write)
class WriteAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "work", "created_at", "views", "likes"]
    list_filter = ["work", "created_at"]
    search_fields = ["title", "user__username", "work__title"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "views", "likes"]


@admin.register(WriteLike)
class WriteLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "write", "created_at"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]
