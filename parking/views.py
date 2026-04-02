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
        
        # ─────────────────────────────────────────
# VISTAS FRONTEND
# ─────────────────────────────────────────
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

def vista_inicio(request):
    context = {
        'total_usuarios':   Usuario.objects.count(),
        'total_vehiculos':  Vehiculo.objects.count(),
        'total_registros':  RegistroParqueo.objects.count(),
        'vehiculos_activos': RegistroParqueo.objects.filter(fecha_salida__isnull=True).count(),
        'registros_activos': RegistroParqueo.objects.filter(fecha_salida__isnull=True),
    }
    return render(request, 'parking/inicio.html', context)

def vista_usuarios(request):
    return render(request, 'parking/usuarios.html', {
        'usuarios': Usuario.objects.all()
    })

def crear_usuario(request):
    if request.method == 'POST':
        Usuario.objects.create(
            nombre    = request.POST['nombre'],
            documento = request.POST['documento'],
            telefono  = request.POST.get('telefono', ''),
            email     = request.POST.get('email', ''),
        )
        messages.success(request, 'Usuario registrado correctamente.')
    return redirect('/usuarios/')

def vista_vehiculos(request):
    return render(request, 'parking/vehiculos.html', {
        'vehiculos': Vehiculo.objects.all(),
        'usuarios':  Usuario.objects.all(),
    })

def crear_vehiculo(request):
    if request.method == 'POST':
        Vehiculo.objects.create(
            placa        = request.POST['placa'].upper(),
            tipo         = request.POST['tipo'],
            marca        = request.POST.get('marca', ''),
            color        = request.POST.get('color', ''),
            propietario  = Usuario.objects.get(id=request.POST['propietario']),
        )
        messages.success(request, 'Vehículo registrado correctamente.')
    return redirect('/vehiculos/')

def vista_registros(request):
    return render(request, 'parking/registros.html', {
        'registros': RegistroParqueo.objects.all(),
        'vehiculos': Vehiculo.objects.all(),
    })

def registrar_entrada(request):
    if request.method == 'POST':
        RegistroParqueo.objects.create(
            vehiculo      = Vehiculo.objects.get(id=request.POST['vehiculo']),
            observaciones = request.POST.get('observaciones', ''),
        )
        messages.success(request, 'Entrada registrada correctamente.')
    return redirect('/registros/')

def registrar_salida(request, pk):
    registro = get_object_or_404(RegistroParqueo, pk=pk)
    if not registro.fecha_salida:
        registro.fecha_salida = timezone.now()
        registro.total_cobrado = registro.calcular_total()
        registro.save()
        messages.success(request, f'Salida registrada. Total: ${registro.total_cobrado}')
    return redirect('/registros/')