from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email"]  # 목록에서 보여줄 필드
    list_filter = ["email"]  # 필터 옵션
    search_fields = ["name", "email"]  # 검색 가능한 필드
    ordering = ["-id"]  # 정렬 순서 (최신순)
