from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import FichaFilter
from .models import Ficha, ModulosCapacita
from .serializers import FichaSerializer, ModulosCapacitaSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt import authentication

class FichaViewSet(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FichaFilter
    ordering_fields = '__all__'

class ModulosCapacitaViewSet(viewsets.ModelViewSet):
    queryset = ModulosCapacita.objects.all()
    serializer_class = ModulosCapacitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
