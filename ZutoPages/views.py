from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .models import Work
from .serializers import WorkSerializer

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


@api_view(["POST"])
def write(request):
    return Response({"message": "Write"}, status=status.HTTP_200_OK)


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
