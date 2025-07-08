from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User, Work, Write, WriteLike
from .serializers import WorkSerializer, WriteSerializer
from django.db.models import F, Count
from django.db import transaction
from django.conf import settings
import uuid, os


class ImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response(
                {"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 확장자 보존, UUID로 파일명 중복 방지
        ext = os.path.splitext(file_obj.name)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        save_path = os.path.join(settings.MEDIA_ROOT, filename)

        # 실제 저장
        with open(save_path, "wb+") as dest:
            for chunk in file_obj.chunks():
                dest.write(chunk)

        # 완전한 URL 만들어서 반환
        url = request.build_absolute_uri(settings.MEDIA_URL + filename)
        return Response({"url": url}, status=status.HTTP_201_CREATED)


TYPE_CHOICES = {
    "novel": 0,
    "poem": 1,
    "music": 2,
    "game": 3,
    "movie": 4,
    "performance": 5,
    "animation": 6,
}


@api_view(["GET", "POST"])
def work(request):
    if request.method == "GET":
        type_param = request.query_params.get("type", None)

        qs = Work.objects.all()
        if type_param is not None:
            typeindex = TYPE_CHOICES.get(type_param)
            if typeindex is not None:
                qs = qs.filter(type_index=typeindex)
            else:
                return Response(
                    {"error": "유효하지 않은 타입입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = WorkSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = WorkSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            out = WorkSerializer(instance)
            return Response(out.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def write(request):
    if request.method == "GET":
        # 쿼리 파라미터로 필터링
        work_id = request.query_params.get("work_id", None)
        user_id = request.query_params.get("user_id", None)
        parent_id = request.query_params.get("parent_id", None)

        # 기본 쿼리셋
        qs = Write.objects.select_related("user", "work").all()

        # 작품별 필터링
        if work_id is not None:
            try:
                work_id = int(work_id)
                qs = qs.filter(work_id=work_id)
            except ValueError:
                return Response(
                    {"error": "work_id는 숫자여야 합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # 사용자별 필터링
        if user_id is not None:
            try:
                user_id = int(user_id)
                qs = qs.filter(user_id=user_id)
            except ValueError:
                return Response(
                    {"error": "user_id는 숫자여야 합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # 부모 댓글별 필터링 (대댓글 조회)
        if parent_id is not None:
            try:
                parent_id = int(parent_id)
                qs = qs.filter(parentID=parent_id)
            except ValueError:
                return Response(
                    {"error": "parent_id는 숫자여야 합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # 최신순 정렬
        qs = qs.order_by("-created_at")

        serializer = WriteSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = WriteSerializer(data=request.data)
        if serializer.is_valid():
            # 해석글 생성
            instance = serializer.save()

            # 생성된 해석글 데이터 반환
            out = WriteSerializer(instance)
            return Response(out.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_user(request):
    name = request.data.get("name")
    email = request.data.get("email")

    if not name or not email:
        return Response(
            {"error": "Name and email are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(name=name, email=email)

    return Response(
        {"id": user.id, "name": user.name, "email": user.email},
        status=status.HTTP_201_CREATED,
    )


@api_view(["PUT"])
def update_write_views(request, write_id):
    """해석글 조회수 증가"""
    try:
        write = Write.objects.get(id=write_id)
        write.views = F("views") + 1
        write.save()
        write.refresh_from_db()

        serializer = WriteSerializer(write, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Write.DoesNotExist:
        return Response(
            {"error": "해석글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_write_likes(request, write_id):
    """해석글 좋아요 토글"""
    try:
        write = Write.objects.get(id=write_id)
        user = request.user

        with transaction.atomic():
            # 좋아요 상태 확인
            like_obj, created = WriteLike.objects.get_or_create(user=user, write=write)

            if created:
                # 새로 좋아요를 누른 경우
                write.likes = F("likes") + 1
                is_liked = True
                action = "liked"
            else:
                # 이미 좋아요를 누른 경우 - 좋아요 취소
                like_obj.delete()
                write.likes = F("likes") - 1
                is_liked = False
                action = "unliked"

            write.save()
            write.refresh_from_db()

        # 업데이트된 데이터 반환
        serializer = WriteSerializer(write, context={"request": request})
        response_data = serializer.data
        response_data["action"] = action  # 프론트엔드에서 애니메이션에 사용

        return Response(response_data, status=status.HTTP_200_OK)

    except Write.DoesNotExist:
        return Response(
            {"error": "해석글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
def popular(request):
    # write__writelike 로 Join → WriteLike 테이블의 수를 Count
    qs = (
        Work.objects
            .annotate(num_likes=Count('write__writelike'))
            .order_by('-num_likes')[:4]
    )
    serializer = WorkSerializer(qs, many=True)
    return Response({'works': serializer.data}, status=status.HTTP_200_OK)