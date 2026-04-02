from rest_framework import serializers
from .models import Usuario, Vehiculo, TarifaParqueo, RegistroParqueo


# ─────────────────────────────────────────
# SERIALIZER: Usuario
# ─────────────────────────────────────────
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Usuario
        fields = '__all__'


# ─────────────────────────────────────────
# SERIALIZER: Vehículo
# ─────────────────────────────────────────
class VehiculoSerializer(serializers.ModelSerializer):
    # Muestra el nombre del propietario además del ID
    propietario_nombre = serializers.CharField(
        source='propietario.nombre',
        read_only=True
    )

    class Meta:
        model  = Vehiculo
        fields = '__all__'


# ─────────────────────────────────────────
# SERIALIZER: Tarifa
# ─────────────────────────────────────────
class TarifaParqueoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = TarifaParqueo
        fields = '__all__'


# ─────────────────────────────────────────
# SERIALIZER: Registro de Parqueo
# ─────────────────────────────────────────
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