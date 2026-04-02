from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Usuario, Vehiculo, TarifaParqueo, RegistroParqueo
from .serializers import (
    UsuarioSerializer,
    VehiculoSerializer,
    TarifaParqueoSerializer,
    RegistroParqueoSerializer,
)


# ─────────────────────────────────────────
# VISTA: Usuario
# ─────────────────────────────────────────
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset         = Usuario.objects.all()
    serializer_class = UsuarioSerializer


# ─────────────────────────────────────────
# VISTA: Vehículo
# ─────────────────────────────────────────
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset         = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer


# ─────────────────────────────────────────
# VISTA: Tarifa
# ─────────────────────────────────────────
class TarifaParqueoViewSet(viewsets.ModelViewSet):
    queryset         = TarifaParqueo.objects.all()
    serializer_class = TarifaParqueoSerializer


# ─────────────────────────────────────────
# VISTA: Registro de Parqueo
# ─────────────────────────────────────────
class RegistroParqueoViewSet(viewsets.ModelViewSet):
    queryset         = RegistroParqueo.objects.all()
    serializer_class = RegistroParqueoSerializer

    @action(detail=True, methods=['post'])
    def salida(self, request, pk=None):
        """
        Endpoint especial: POST /api/registros/{id}/salida/
        Registra la salida del vehículo y calcula el total.
        """
        registro = self.get_object()

        # Validar que no tenga ya una salida registrada
        if registro.fecha_salida:
            return Response(
                {'error': 'Este vehículo ya registró su salida.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Registrar la salida con la hora actual
        registro.fecha_salida = timezone.now()
        total = registro.calcular_total()
        registro.total_cobrado = total
        registro.save()

        serializer = self.get_serializer(registro)
        return Response({
            'mensaje': 'Salida registrada correctamente.',
            'total_cobrado': total,
            'registro': serializer.data
        })