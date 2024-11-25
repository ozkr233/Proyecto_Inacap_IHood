from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Publicacion ,Categoria, Evidencia
from rest_framework.views import APIView
from .serializers import (
    PublicacionSerializer,
    CategoriaSerializer,
    EvidenciaSerializer,
    UsuarioRegistroSerializer
)


# ViewSet para Publicacion
class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

class RegistroUsuarioViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UsuarioRegistroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Crea el nuevo usuario
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# ViewSet para Categoria
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# ViewSet para Evidencia
class EvidenciaViewSet(viewsets.ModelViewSet):
    queryset = Evidencia.objects.all()
    serializer_class = EvidenciaSerializer
# Create your views here.
