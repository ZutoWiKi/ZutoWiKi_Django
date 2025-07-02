from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User


@api_view(["GET"])
def novel(request):
    return Response({"message": "Hello novel!"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def poem(request):
    return Response({"message": "Hello poem!"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def music(request):
    return Response({"message": "Hello music!"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def game(request):
    return Response({"message": "Hello game!"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def movie(request):
    return Response({"message": "Hello movie!"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def perfomance(request):
    return Response({"message": "Hello from Django!"}, status=status.HTTP_200_OK)


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
