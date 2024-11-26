from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Publicacion ,Categoria, Evidencia
from rest_framework.views import APIView
from .serializers import (
    PublicacionSerializer,
    CategoriaSerializer,
    EvidenciaSerializer,
    UsuarioRegistroSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from api.models import Usuario


# ViewSet para Publicacion
class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer

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

class LoginViewSet(ViewSet):
    """
    ViewSet para manejar el inicio de sesión sin usar authenticate.
    """
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Acción personalizada para manejar el inicio de sesión.
        """
        rut = request.data.get('rut')
        password = request.data.get('password')

        if not rut or not password:
            return Response(
                {'error': 'Debe proporcionar rut y contraseña'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Buscar usuario en la base de datos
            user = Usuario.objects.get(rut=rut)

            # Verificar contraseña
            if check_password(password, user.password):
                return Response(
                    {
                        'message': 'Login exitoso',
                        'user': {
                            'rut': user.rut,
                            'nombre': user.nombre,
                            'email': user.email
                        }
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Contraseña incorrecta'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
# Create your views here.
