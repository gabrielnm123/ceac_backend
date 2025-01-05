from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, viewsets, status, decorators
from .serializers import (
    GroupSerializer,
    UserSerializer,
    PermissionSerializer,
    ContentTypeSerializer,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,  # confirmar se realmente ta indo altomaticamente para o black list
)
from rest_framework.response import Response
from django.conf import settings
from .authentication import CookieJWTAuthentication
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([CookieJWTAuthentication])
def get_current_user(request):
    user = request.user
    return Response({'id': user.id})


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([CookieJWTAuthentication])
def check_password(request, user_id):
    """
    Verifica se a senha fornecida é correta para o usuário atual.
    """
    password = request.data.get('password')
    if not password:
        return Response(
            {'error': 'Senha necessária.'}, status=status.HTTP_400_BAD_REQUEST
        )
    user = request.user  # Já autenticado
    if user.check_password(password):  # Método nativo do modelo User
        return Response({'valid': True})
    else:
        return Response({'valid': False})


@decorators.api_view(['POST'])
def logout_view(request):
    response = Response(
        {'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK
    )
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


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


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            tokens = response.data
            res = Response(
                {'message': 'Login realizado com sucesso'}, status=status.HTTP_200_OK
            )
            res.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            )
            res.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            )
            return res
        else:
            return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            request.data['refresh'] = refresh_token
        else:
            return Response(
                {'error': 'Refresh token não encontrado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            tokens = response.data
            res = Response(
                {'message': 'Token atualizado com sucesso'}, status=status.HTTP_200_OK
            )
            res.set_cookie(
                key='access_token',
                value=tokens['access'],
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            )
            res.set_cookie(
                key='refresh_token',
                value=tokens['refresh'],
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            )
            return res
        else:
            return response


class CustomRefreshTokenVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtém o Refresh Token diretamente dos cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'error': 'Refresh token não encontrado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Tenta verificar o Refresh Token
        try:
            # Cria uma instância do RefreshToken para verificar a validade
            token = RefreshToken(refresh_token)
            return Response(
                {'message': 'Refresh Token é válido'}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': f'Refresh Token inválido: {str(e)}'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
