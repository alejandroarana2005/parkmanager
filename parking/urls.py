from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# El router genera automáticamente todas las URLs
router = DefaultRouter()
router.register(r'usuarios',  views.UsuarioViewSet)
router.register(r'vehiculos', views.VehiculoViewSet)
router.register(r'tarifas',   views.TarifaParqueoViewSet)
router.register(r'registros', views.RegistroParqueoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]