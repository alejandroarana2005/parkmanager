from django.contrib import admin
from .models import Usuario, Vehiculo, TarifaParqueo, RegistroParqueo

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'documento', 'telefono', 'email']
    search_fields = ['nombre', 'documento']

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ['placa', 'tipo', 'marca', 'color', 'propietario']
    search_fields = ['placa']
    list_filter   = ['tipo']

@admin.register(TarifaParqueo)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ['tipo_vehiculo', 'precio_por_hora']

@admin.register(RegistroParqueo)
class RegistroAdmin(admin.ModelAdmin):
    list_display  = ['vehiculo', 'fecha_entrada', 'fecha_salida', 'total_cobrado']
    list_filter   = ['fecha_entrada']
    search_fields = ['vehiculo__placa']