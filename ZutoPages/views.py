from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello from Django!"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_user(request):
    name = request.data.get("name")
    email = request.data.get("email")

    if not name or not email:
        return Response(
            {"error": "Name and email are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {
            "message": f"User {name} created successfully!",
            "user": {"name": name, "email": email},
        },
        status=status.HTTP_201_CREATED,
    )
