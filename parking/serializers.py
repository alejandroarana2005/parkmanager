from rest_framework import serializers
from .models import Usuario, Vehiculo, TarifaParqueo, RegistroParqueo


#USUARIO
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Usuario
        fields = '__all__'


#VEHICULO
class VehiculoSerializer(serializers.ModelSerializer):
    # Muestra el nombre del propietario además del ID
    propietario_nombre = serializers.CharField(
        source='propietario.nombre',
        read_only=True
    )

    class Meta:
        model  = Vehiculo
        fields = '__all__'


#TARIFA
class TarifaParqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TarifaParqueo
        fields = '__all__'


#REGISTRO DE PARQUEO
class RegistroParqueoSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para mostrar info del vehículo
    vehiculo_placa = serializers.CharField(
        source='vehiculo.placa',
        read_only=True
    )
    vehiculo_tipo = serializers.CharField(
        source='vehiculo.tipo',
        read_only=True
    )

    class Meta:
        model  = RegistroParqueo
        fields = '__all__'