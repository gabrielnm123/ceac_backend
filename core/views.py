from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth import authenticate
from rest_framework import permissions, viewsets, status, decorators, response
from .serializers import GroupSerializer, UserSerializer, PermissionSerializer, ContentTypeSerializer
from rest_framework_simplejwt import authentication, views
from django.conf import settings

class CustomTokenObtainPairView(views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Adiciona o refresh token como um cookie seguro
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                httponly=True,
                secure=not settings.DEBUG,  # Usa HTTPS apenas em produção
                samesite='Lax',  # Protege contra CSRF
                max_age=7 * 24 * 60 * 60  # Tempo de vida do cookie (7 dias)
            )
            # Remove o refresh token da resposta JSON
            del response.data['refresh']
        return response

class CustomTokenRefreshView(views.TokenRefreshView):
    def post(self, request, *args, **kwargs):
        request.data['refresh'] = request.COOKIES.get('refresh_token')
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Verifique se 'refresh' está em response.data
            if 'refresh' in response.data:
                # Atualiza o token de atualização no cookie
                response.set_cookie(
                    key='refresh_token',
                    value=response.data['refresh'],
                    httponly=True,
                    secure=not settings.DEBUG,  # Usa HTTPS apenas em produção
                    samesite='Lax',
                    max_age=7 * 24 * 60 * 60
                )
                del response.data['refresh']
            else:
                # Se 'refresh' não estiver na resposta, isso é um problema
                return views.Response({'detail': 'Token de atualização não retornado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]

@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.JWTAuthentication])
def get_current_user(request):
    user = request.user
    return response.Response({'id': user.id})

@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
@decorators.authentication_classes([authentication.JWTAuthentication])
def check_password(request, user_id):
    """
    Verifica se a senha fornecida é correta para o usuário atual.
    """
    password = request.data.get('password')
    if not password:
        return response.Response({'error': 'Senha necessária.'}, status=status.HTTP_400_BAD_REQUEST)
    user = request.user  # Já autenticado
    if user.check_password(password):  # Método nativo do modelo User
        return response.Response({'valid': True})
    else:
        return response.Response({'valid': False})
