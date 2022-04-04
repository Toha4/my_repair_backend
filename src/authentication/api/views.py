from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.utils import get_current_user

from .serializers import CustomUserSerializer


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_current_user(request)
        return Response(CustomUserSerializer(instance=user).data, status=status.HTTP_200_OK)


class CustomUserCreateView(APIView):
    permission_classes = (AllowAny,)

    # TODO R-3: При регистрации сделать is_active = False и активировать с помощью письма на email

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(jwt_views.TokenViewBase):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        response = Response({"access": access_token}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"],
            value=refresh_token,
            httponly=True,
            path="/api/authorization",
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        )
        return response


class RefreshView(jwt_views.TokenViewBase):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data["refresh"] = self.request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"])
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        response = Response({"access": access_token}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"],
            value=refresh_token,
            httponly=True,
            path="/api/authorization",
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        )
        return response


class LogOutView(APIView):
    """Class for logging out a user by clearing tokens."""

    """
        Решение выхода не идеальное, т.к. access токен будет все еще действующем при выходе, но удален из клиента.
        Возможные решения:
        1. Помещать access токен в blacklist, но тогда будет обращение в БД при каждом запросе,
        что лишает преимущество JWT.
        2. Использовать короткий срок жизни access токена (например, 5 мин) что снизит риск.
        3. Использовать Redis и хранить blacklist там.
    """

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = self.request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"])
            token = RefreshToken(refresh_token, verify=False)
            token.blacklist()

            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie(settings.SIMPLE_JWT["REFRESH_COOKIE_NAME"])

            return response
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
