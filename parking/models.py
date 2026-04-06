from django.db import models

#USUARIO
class Usuario(models.Model):
    nombre        = models.CharField(max_length=100)
    documento     = models.CharField(max_length=20, unique=True)
    telefono      = models.CharField(max_length=15, blank=True)
    email         = models.EmailField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.documento})"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['nombre']


#VEHICULO
class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('carro',  'Carro'),
        ('moto',   'Moto'),
        ('camion', 'Camión'),
        ('bicicleta', 'Bicicleta'),
    ]

    placa    = models.CharField(max_length=10, unique=True)
    tipo     = models.CharField(max_length=20, choices=TIPO_CHOICES)
    marca    = models.CharField(max_length=50, blank=True)
    color    = models.CharField(max_length=30, blank=True)
    propietario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='vehiculos'
    )

    def __str__(self):
        return f"{self.placa} - {self.tipo}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"


#TARIFAS
class TarifaParqueo(models.Model):
    TIPO_CHOICES = [
        ('carro',  'Carro'),
        ('moto',   'Moto'),
        ('camion', 'Camión'),
        ('bicicleta', 'Bicicleta'),
    ]

    tipo_vehiculo   = models.CharField(max_length=20, choices=TIPO_CHOICES, unique=True)
    precio_por_hora = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.tipo_vehiculo} - ${self.precio_por_hora}/hora"

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"


#REGISTRO DE ENTRADA Y SALIDA
class RegistroParqueo(models.Model):
    vehiculo        = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name='registros'
    )
    fecha_entrada   = models.DateTimeField(auto_now_add=True)
    fecha_salida    = models.DateTimeField(null=True, blank=True)
    total_cobrado   = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    observaciones   = models.TextField(blank=True)

    def calcular_total(self):
        """Calcula el costo según el tiempo y la tarifa del vehículo."""
        if not self.fecha_salida:
            return None
        duracion = self.fecha_salida - self.fecha_entrada
        horas = duracion.total_seconds() / 3600
        try:
            tarifa = TarifaParqueo.objects.get(
                tipo_vehiculo=self.vehiculo.tipo
            )
            return round(horas * float(tarifa.precio_por_hora), 2)
        except TarifaParqueo.DoesNotExist:
            return None

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.fecha_entrada.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Registro de Parqueo"
        verbose_name_plural = "Registros de Parqueo"
        ordering = ['-fecha_entrada']