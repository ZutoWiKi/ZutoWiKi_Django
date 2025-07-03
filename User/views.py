from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()


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

    user = User.objects.create(name=name, email=email)

    return Response(
        {"id": user.id, "name": user.name, "email": user.email},
        status=status.HTTP_201_CREATED,
    )

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail':'이메일 또는 비밀번호가 올바르지 않습니다.'},
                             status=401)

        if not user.check_password(password):
            return Response({'detail':'이메일 또는 비밀번호가 올바르지 않습니다.'},
                             status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})
    
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        passwordcheck = request.data.get('passwordcheck')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail':'이메일 또는 비밀번호가 올바르지 않습니다.'},
                             status=401)

        if not user.check_password(password):
            return Response({'detail':'이메일 또는 비밀번호가 올바르지 않습니다.'},
                             status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})
    
class MypageView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail':'이메일 또는 비밀번호가 올바르지 않습니다.'},
                             status=401)

        if not user.check_password(password):
            return Response({'detail':'이메일 또는 비밀번호가 올바르지 않습니다.'},
                             status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})
    