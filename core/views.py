from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, viewsets, status, decorators, response
from .serializers import (
    GroupSerializer,
    UserSerializer,
    PermissionSerializer,
    ContentTypeSerializer,
)
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from django.conf import settings
from .authentication import CookieJWTAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]


@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([CookieJWTAuthentication])
def get_current_user(request):
    user = request.user
    return response.Response({"id": user.id})


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([CookieJWTAuthentication])
def check_password(request, user_id):
    """
    Verifica se a senha fornecida é correta para o usuário atual.
    """
    password = request.data.get("password")
    if not password:
        return response.Response(
            {"error": "Senha necessária."}, status=status.HTTP_400_BAD_REQUEST
        )
    user = request.user  # Já autenticado
    if user.check_password(password):  # Método nativo do modelo User
        return response.Response({"valid": True})
    else:
        return response.Response({"valid": False})


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            tokens = response.data
            res = Response(
                {"message": "Login realizado com sucesso"}, status=status.HTTP_200_OK
            )
            res.set_cookie(
                key="access_token",
                value=tokens["access"],
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=5 * 60,  # Deve corresponder ao tempo de vida do access token
            )
            res.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=24
                * 60
                * 60,  # Deve corresponder ao tempo de vida do refresh token
            )
            return res
        else:
            return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            request.data["refresh"] = refresh_token
        else:
            return Response(
                {"error": "Refresh token não encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            tokens = response.data
            res = Response(
                {"message": "Token atualizado com sucesso"}, status=status.HTTP_200_OK
            )
            res.set_cookie(
                key="access_token",
                value=tokens["access"],
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=5 * 60,  # Deve corresponder ao tempo de vida do access token
            )
            return res
        else:
            return response


@decorators.api_view(["POST"])
def logout_view(request):
    response = Response(
        {"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
