from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PublicacionViewSet,
    CategoriaViewSet,
    EvidenciaViewSet,
    RegistroUsuarioViewSet
)

# Crear un enrutador
router = DefaultRouter()

# Registrar los ViewSets
router.register(r'publicaciones', PublicacionViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'evidencias', EvidenciaViewSet)
router.register(r'registro',RegistroUsuarioViewSet, basename='registro_usuario')
router.register(r'login',LoginViewSet,basename='log')

# Incluir las rutas generadas por el enrutador
urlpatterns = router.urls
