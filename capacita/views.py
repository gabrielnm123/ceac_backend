from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ficha
from .serializers import FichaSerializer
from rest_framework_simplejwt import authentication

class FichaViewSet(viewsets.ModelViewSet):
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nome_completo']  # Campos nos quais a busca será feita
