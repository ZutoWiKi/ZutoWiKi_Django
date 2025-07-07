from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .models import Work
from .serializers import WorkSerializer


@api_view(["GET"])
def work(request):
    typeindex = request.query_params.get("type", None)

    qs = Work.objects.all()
    if typeindex is not None:
        try:
            idx = int(typeindex)
        except ValueError:
            return Response(
                {"error": "typeindex는 정수여야 합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        qs = qs.filter(type_index=idx)

    serializer = WorkSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
