from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .filter import FichaFilter
from .models import Ficha
from .serializers import FichaSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class FichaViewSet(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FichaFilter
    ordering_fields = '__all__'
