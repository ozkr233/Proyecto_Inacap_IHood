import cloudinary.uploader
from rest_framework import serializers
from .models import (
    Usuario,
    DepartamentoMunicipal,
    Categoria,
    SituacionPublicacion,
    JuntaVecinal,
    Publicacion,
    Evidencia,
    AnuncioMunicipal,
    RespuestaMunicipal
)
import cloudinary

# Serializer para Usuario
class UsuarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['rut', 'email', 'nombre', 'password', 'numero_telefonico_movil']

    def create(self, validated_data):
        user = Usuario(
            username=validated_data['rut'],  # Asigna rut al campo username
            rut=validated_data['rut'],
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            numero_telefonico_movil=validated_data.get('numero_telefonico_movil', None),
        )
        user.set_password(validated_data['password'])  # Encripta la contraseña
        user.save()
        return user
    
# Serializer para Departamento Municipal
class DepartamentoMunicipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartamentoMunicipal
        fields = ['id', 'nombre', 'descripcion']

# Serializer para Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'departamento']

# Serializer para SituacionPublicacion
class SituacionPublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SituacionPublicacion
        fields = ['id', 'nombre', 'descripcion']

# Serializer para Junta Vecinal
class JuntaVecinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JuntaVecinal
        fields = ['id', 'nombre_calle', 'numero_calle', 'departamento', 'villa', 'comuna', 'latitud', 'longitud']



# Serializer para Evidencia
class EvidenciaSerializer(serializers.ModelSerializer):
    publicacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Publicacion.objects.all()
    )

    class Meta:
        model = Evidencia
        fields = [
            "id",
            "publicacion",
            "archivo",
            "fecha",
            "extension",
            "publicacion_id",
        ]

    def create(self, validated_data):
        archivo = validated_data.pop("archivo")
        upload_data = cloudinary.uploader.upload(archivo)
        validated_data["archivo"] = upload_data["url"]
        return Evidencia.objects.create(**validated_data)
    
# Serializer para Publicacion
class PublicacionCreateSerializer(serializers.ModelSerializer):
    evidencias = EvidenciaSerializer(many=True, required=False)

    class Meta:
        model = Publicacion
        fields = [
            "id",
            "usuario",
            "junta_vecinal",
            "categoria",
            "departamento",
            "descripcion",
            "situacion",
            "fecha_publicacion",
            "titulo",
            "latitud",
            "longitud",
            "evidencias",
        ]

    def create(self, validated_data):
        evidencias_data = validated_data.pop('evidencias', [])
        publicacion = Publicacion.objects.create(**validated_data)
        
        for evidencia_data in evidencias_data:
            Evidencia.objects.create(publicacion=publicacion, **evidencia_data)
        
        return publicacion

# Serializer para Anuncio Municipal
class AnuncioMunicipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnuncioMunicipal
        fields = ['id', 'usuario', 'titulo', 'descripcion', 'fecha']

# Serializer para Respuesta Municipal
class RespuestaMunicipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaMunicipal
        fields = ['id', 'usuario', 'publicacion', 'fecha', 'descripcion', 'acciones',
                  'situacion_inicial', 'situacion_posterior']