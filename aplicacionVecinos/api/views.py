from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Publicacion ,Categoria, Evidencia
from rest_framework.views import APIView
from .serializers import (
    PublicacionCreateSerializer,
    CategoriaSerializer,
    EvidenciaSerializer,
    UsuarioRegistroSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from api.models import Usuario
from django.utils import timezone


# ViewSet para Publicacion
class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionCreateSerializer

class RegistroUsuarioViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UsuarioRegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Crea el nuevo usuario
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            respose_data = {
                'user': UsuarioRegistroSerializer(user).data,  # Incluye datos del usuario
                'refresh': str(refresh),
                'access': str(access),
            }

            return Response(respose_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet para Categoria
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# ViewSet para Evidencia
class EvidenciaViewSet(viewsets.ModelViewSet):
    queryset = Evidencia.objects.all()
    serializer_class = EvidenciaSerializer
    def perform_create(self, serializer):
        publicacion_id = self.request.data.get('publicacion')  # Asegura que es un ID
        serializer.save(fecha=timezone.now(), publicacion_id=publicacion_id)

