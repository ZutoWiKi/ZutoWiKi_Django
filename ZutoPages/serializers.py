from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Work, Write, WriteLike

User = get_user_model()


class WorkSerializer(serializers.ModelSerializer):
    typeindex = serializers.IntegerField(source="type_index", write_only=True)
    coverImage = serializers.URLField(
        source="cover_image", required=False, allow_blank=True
    )

    class Meta:
        model = Work
        fields = ("id", "typeindex", "title", "author", "coverImage", "description")

    def to_representation(self, instance):
        # GET 요청시 응답 데이터 구조
        data = super().to_representation(instance)
        # write_only 필드 제거하고 읽기용 필드 추가
        data.pop("typeindex", None)
        return data


class WriteSerializer(serializers.ModelSerializer):
    # Django 기본 User 모델은 username 필드를 사용
    user_name = serializers.CharField(source="user.username", read_only=True)
    work_title = serializers.CharField(source="work.title", read_only=True)
    work_author = serializers.CharField(source="work.author", read_only=True)
    is_liked = serializers.SerializerMethodField()  # 현재 사용자의 좋아요 상태

    class Meta:
        model = Write
        fields = (
            "id",
            "title",
            "user",
            "user_name",
            "content",
            "work",
            "work_title",
            "work_author",
            "created_at",
            "views",
            "likes",
            "parentID",
            "is_liked",
        )
        read_only_fields = (
            "id",
            "created_at",
            "views",
            "likes",
            "user_name",
            "work_title",
            "work_author",
            "is_liked",
        )

    def get_is_liked(self, obj):
        """현재 사용자가 이 게시글을 좋아요 했는지 확인"""
        request = self.context.get("request")
        if request and hasattr(request, "user_id") and request.user_id:
            try:
                return WriteLike.objects.filter(
                    user_id=request.user_id, write=obj
                ).exists()
            except Exception as e:
                print(f"좋아요 상태 확인 중 오류: {e}")
                return False
        return False

    def validate_user(self, value):
        """사용자 존재 여부 검증"""
        try:
            User.objects.get(id=value.id)
        except User.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 사용자입니다.")
        return value

    def validate_work(self, value):
        """작품 존재 여부 검증"""
        try:
            Work.objects.get(id=value.id)
        except Work.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 작품입니다.")
        return value
