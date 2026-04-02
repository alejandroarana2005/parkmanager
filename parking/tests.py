from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from .models import Usuario, Vehiculo, TarifaParqueo, RegistroParqueo


# ═══════════════════════════════════════════════════
# PRUEBAS DEL MODELO: Usuario
# ═══════════════════════════════════════════════════
class UsuarioModelTest(TestCase):

    def setUp(self):
        """
        setUp se ejecuta antes de cada prueba.
        Aquí creamos los datos que necesitamos.
        """
        self.usuario = Usuario.objects.create(
            nombre    = 'Carlos Pérez',
            documento = '123456789',
            telefono  = '3001234567',
            email     = 'carlos@email.com',
        )

    def test_usuario_creado_correctamente(self):
        """Verifica que el usuario se guardó en la base de datos."""
        self.assertEqual(self.usuario.nombre, 'Carlos Pérez')
        self.assertEqual(self.usuario.documento, '123456789')

    def test_usuario_str(self):
        """Verifica que el método __str__ funciona bien."""
        self.assertEqual(
            str(self.usuario),
            'Carlos Pérez (123456789)'
        )

    def test_documento_unico(self):
        """Verifica que no se pueden crear dos usuarios con el mismo documento."""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Usuario.objects.create(
                nombre    = 'Otro Usuario',
                documento = '123456789',  # documento repetido
            )


# ═══════════════════════════════════════════════════
# PRUEBAS DEL MODELO: Vehículo
# ═══════════════════════════════════════════════════
class VehiculoModelTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre    = 'Ana Gómez',
            documento = '987654321',
        )
        self.vehiculo = Vehiculo.objects.create(
            placa       = 'ABC123',
            tipo        = 'carro',
            marca       = 'Toyota',
            color       = 'Rojo',
            propietario = self.usuario,
        )

    def test_vehiculo_creado_correctamente(self):
        """Verifica que el vehículo se guardó correctamente."""
        self.assertEqual(self.vehiculo.placa, 'ABC123')
        self.assertEqual(self.vehiculo.tipo, 'carro')

    def test_vehiculo_str(self):
        """Verifica el método __str__ del vehículo."""
        self.assertEqual(str(self.vehiculo), 'ABC123 - carro')

    def test_vehiculo_tiene_propietario(self):
        """Verifica que el vehículo está asociado a un usuario."""
        self.assertEqual(self.vehiculo.propietario.nombre, 'Ana Gómez')

    def test_placa_unica(self):
        """Verifica que no existan dos vehículos con la misma placa."""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Vehiculo.objects.create(
                placa       = 'ABC123',  # placa repetida
                tipo        = 'moto',
                propietario = self.usuario,
            )


# ═══════════════════════════════════════════════════
# PRUEBAS DEL MODELO: Tarifa y cálculo de cobro
# ═══════════════════════════════════════════════════
class TarifaYCalculoTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre    = 'Luis Torres',
            documento = '111222333',
        )
        self.vehiculo = Vehiculo.objects.create(
            placa       = 'XYZ999',
            tipo        = 'carro',
            propietario = self.usuario,
        )
        self.tarifa = TarifaParqueo.objects.create(
            tipo_vehiculo   = 'carro',
            precio_por_hora = Decimal('5000.00'),
        )

    def test_tarifa_creada_correctamente(self):
        """Verifica que la tarifa se guardó bien."""
        self.assertEqual(self.tarifa.tipo_vehiculo, 'carro')
        self.assertEqual(self.tarifa.precio_por_hora, Decimal('5000.00'))

    def test_calculo_sin_salida(self):
        """Si no hay salida, el cálculo debe retornar None."""
        registro = RegistroParqueo.objects.create(
            vehiculo = self.vehiculo
        )
        self.assertIsNone(registro.calcular_total())

    def test_calculo_con_dos_horas(self):
        """Verifica que 2 horas de parqueo a $5000/hora = $10000."""
        ahora = timezone.now()
        registro = RegistroParqueo.objects.create(
            vehiculo     = self.vehiculo,
            fecha_salida = ahora + timedelta(hours=2),
        )
        # Ajustamos manualmente la fecha de entrada
        registro.fecha_entrada = ahora
        total = registro.calcular_total()
        self.assertEqual(total, 10000.0)

    def test_calculo_con_media_hora(self):
        """Verifica que 30 minutos a $5000/hora = $2500."""
        ahora = timezone.now()
        registro = RegistroParqueo.objects.create(
            vehiculo     = self.vehiculo,
            fecha_salida = ahora + timedelta(minutes=30),
        )
        registro.fecha_entrada = ahora
        total = registro.calcular_total()
        self.assertEqual(total, 2500.0)


# ═══════════════════════════════════════════════════
# PRUEBAS DE LA API REST
# ═══════════════════════════════════════════════════
class APIUsuarioTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre    = 'María López',
            documento = '555666777',
            telefono  = '3109876543',
        )

    def test_listar_usuarios(self):
        """GET /api/usuarios/ debe retornar status 200."""
        response = self.client.get('/api/usuarios/')
        self.assertEqual(response.status_code, 200)

    def test_crear_usuario_via_api(self):
        """POST /api/usuarios/ debe crear un usuario nuevo."""
        datos = {
            'nombre':    'Pedro Ramírez',
            'documento': '999888777',
            'telefono':  '3201234567',
            'email':     'pedro@email.com',
        }
        response = self.client.post(
            '/api/usuarios/',
            data        = datos,
            content_type = 'application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Usuario.objects.filter(documento='999888777').exists()
        )

    def test_obtener_usuario_por_id(self):
        """GET /api/usuarios/{id}/ debe retornar el usuario correcto."""
        response = self.client.get(f'/api/usuarios/{self.usuario.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'María López')

    def test_usuario_no_existente(self):
        """GET con un ID que no existe debe retornar 404."""
        response = self.client.get('/api/usuarios/9999/')
        self.assertEqual(response.status_code, 404)


class APIRegistroTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre    = 'Sofía Herrera',
            documento = '444555666',
        )
        self.vehiculo = Vehiculo.objects.create(
            placa       = 'DEF456',
            tipo        = 'moto',
            propietario = self.usuario,
        )
        TarifaParqueo.objects.create(
            tipo_vehiculo   = 'moto',
            precio_por_hora = Decimal('3000.00'),
        )

    def test_registrar_entrada(self):
        """POST /api/registros/ debe crear un registro de entrada."""
        datos = {'vehiculo': self.vehiculo.id}
        response = self.client.post(
            '/api/registros/',
            data         = datos,
            content_type = 'application/json',
        )
        self.assertEqual(response.status_code, 201)

    def test_registrar_salida(self):
        """POST /api/registros/{id}/salida/ debe registrar la salida."""
        registro = RegistroParqueo.objects.create(
            vehiculo = self.vehiculo
        )
        response = self.client.post(
            f'/api/registros/{registro.id}/salida/',
            content_type = 'application/json',
        )
        self.assertEqual(response.status_code, 200)
        # Verificar que se guardó la salida en la base de datos
        registro.refresh_from_db()
        self.assertIsNotNone(registro.fecha_salida)

    def test_salida_doble_debe_fallar(self):
        """Registrar salida dos veces debe retornar error 400."""
        registro = RegistroParqueo.objects.create(
            vehiculo     = self.vehiculo,
            fecha_salida = timezone.now(),
        )
        response = self.client.post(
            f'/api/registros/{registro.id}/salida/',
            content_type = 'application/json',
        )
        self.assertEqual(response.status_code, 400)