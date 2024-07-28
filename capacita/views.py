from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ClienteFilter
from .models import Cliente
from .serializers import ClienteSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ClienteFilter
    ordering_fields = '__all__'
