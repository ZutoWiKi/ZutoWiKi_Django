from rest_framework import serializers
from .models import Work


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
