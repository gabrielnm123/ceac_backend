from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer, PermissionSerializer, ContentTypeSerializer
from rest_framework_simplejwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate

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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.JWTAuthentication])
def get_current_user(request):
    user = request.user
    return Response({'id': user.id})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([authentication.JWTAuthentication])
def check_password(request, user_id):
    """
    Verifica se a senha fornecida é correta para o usuário atual.
    """
    password = request.data.get('password')
    user = authenticate(username=request.user.username, password=password)
    
    if user is not None:
        return Response({'valid': True})
    else:
        return Response({'valid': False})
