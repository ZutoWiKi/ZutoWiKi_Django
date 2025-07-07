from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import User
from django.contrib.auth import get_user_model, login
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.db import IntegrityError

User = get_user_model()


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 입력값 검증
        if not email:
            return Response(
                {"detail": "이메일을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {"detail": "비밀번호를 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "등록되지 않은 이메일입니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"detail": "비밀번호가 올바르지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"detail": "비활성화된 계정입니다. 관리자에게 문의하세요."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        login(request, user)

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "message": "로그인에 성공했습니다."},
            status=status.HTTP_200_OK,
        )


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # 기본 입력값 검증
            username = request.data.get("username", "").strip()
            email = request.data.get("email", "").strip()
            password = request.data.get("password", "")
            confirm_password = request.data.get("confirmPassword", "")

            # 필수 필드 검증
            if not username:
                return Response(
                    {"detail": "이름을 입력해주세요."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not email:
                return Response(
                    {"detail": "이메일을 입력해주세요."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not password:
                return Response(
                    {"detail": "비밀번호를 입력해주세요."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not confirm_password:
                return Response(
                    {"detail": "비밀번호 확인을 입력해주세요."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 비밀번호 일치 검증
            if password != confirm_password:
                return Response(
                    {"detail": "비밀번호가 일치하지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 비밀번호 강도 검증
            if len(password) < 8:
                return Response(
                    {"detail": "비밀번호는 최소 8자 이상이어야 합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 이메일 중복 검증
            if User.objects.filter(email=email).exists():
                return Response(
                    {"detail": "이미 사용중인 이메일입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 사용자명 중복 검증 (선택사항)
            if User.objects.filter(username=username).exists():
                return Response(
                    {"detail": "이미 사용중인 이름입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 시리얼라이저를 통한 생성
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    {
                        "message": "회원가입이 성공적으로 완료되었습니다.",
                        "user": {
                            "username": user.username,
                            "email": user.email,
                        },
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                # 시리얼라이저 에러 메시지 반환
                error_messages = []
                for field, errors in serializer.errors.items():
                    for error in errors:
                        error_messages.append(f"{field}: {error}")

                return Response(
                    {"detail": ", ".join(error_messages)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except IntegrityError as e:
            return Response(
                {
                    "detail": "데이터베이스 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"detail": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MypageView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user or not user.is_authenticated:
            return Response(
                {"detail": "인증이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "date_joined": user.date_joined.isoformat(),
            },
            status=status.HTTP_200_OK,
        )
