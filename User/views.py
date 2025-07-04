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
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.views import APIView
User = get_user_model()

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
    
class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "회원가입이 성공적으로 완료되었습니다.",
            "user": {
                "username": user.username,
                "email": user.email,
                "password": user.password,
            }
        }, status=status.HTTP_201_CREATED)
    
class MypageView(APIView):
    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "date_joined": user.date_joined,
        })