from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Work, Write
from .serializers import WorkSerializer, WriteSerializer
from django.db.models import F

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

        serializer = WriteSerializer(qs, many=True)
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

        serializer = WriteSerializer(write)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Write.DoesNotExist:
        return Response(
            {"error": "해석글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
def update_write_likes(request, write_id):
    """해석글 좋아요 수 증가/감소"""
    try:
        write = Write.objects.get(id=write_id)
        action = request.data.get("action", "increase")  # increase 또는 decrease

        if action == "increase":
            write.likes = F("likes") + 1
        elif action == "decrease":
            write.likes = F("likes") - 1
        else:
            return Response(
                {"error": "action은 'increase' 또는 'decrease'여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        write.save()
        write.refresh_from_db()

        serializer = WriteSerializer(write)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Write.DoesNotExist:
        return Response(
            {"error": "해석글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )
