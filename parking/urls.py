from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'usuarios',  views.UsuarioViewSet)
router.register(r'vehiculos', views.VehiculoViewSet)
router.register(r'tarifas',   views.TarifaParqueoViewSet)
router.register(r'registros', views.RegistroParqueoViewSet)

urlpatterns = [
    # API REST
    path('api/', include(router.urls)),
    # Frontend
    path('',                          views.vista_inicio,     name='inicio'),
    path('usuarios/',                 views.vista_usuarios,   name='usuarios'),
    path('usuarios/crear/',           views.crear_usuario,    name='crear_usuario'),
    path('vehiculos/',                views.vista_vehiculos,  name='vehiculos'),
    path('vehiculos/crear/',          views.crear_vehiculo,   name='crear_vehiculo'),
    path('registros/',                views.vista_registros,  name='registros'),
    path('registros/entrada/',        views.registrar_entrada,name='registrar_entrada'),
    path('registros/salida/<int:pk>/',views.registrar_salida, name='registrar_salida'),
]