from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth import authenticate
from rest_framework import permissions, viewsets, status, decorators, response
from .serializers import GroupSerializer, UserSerializer, PermissionSerializer, ContentTypeSerializer
from rest_framework_simplejwt import authentication

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
