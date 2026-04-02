# ParkManager — Sistema de Gestión de Parqueadero

Aplicación web desarrollada con Django y Django REST Framework para gestionar
usuarios, vehículos, entradas y salidas de un parqueadero.

---

## Tecnologías usadas

- Python 3.11
- Django 5.x
- Django REST Framework
- SQLite 
- Bootstrap 

---

## Requisitos 

- [Python 3.11 o superior](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Visual Studio Code](https://code.visualstudio.com/) (recomendado)

---

## Pasos para correr el proyecto

### 1. Clonar el repositorio

Abre una terminal y ejecuta:
```bash
git clone https://github.com/TU_USUARIO/parkmanager.git
```

Entra a la carpeta del proyecto:
```bash
cd parkmanager
```

### 2. Crear el entorno virtual
```bash
python -m venv venv
```

### 3. Activar el entorno virtual

**Windows (PowerShell):**
```bash
venv\Scripts\activate
```

**Windows (Command Prompt / cmd):**
```bash
venv\Scripts\activate.bat
```

**Mac / Linux:**
```bash
source venv/bin/activate
```


### 4. Instalar las dependencias
```bash
python -m pip install -r requirements.txt
```

### 5. Aplicar las migraciones (crear la base de datos)
```bash
python manage.py migrate
```

### 6. Crear un superusuario para el panel Admin
```bash
python manage.py createsuperuser
```

Te pedirá un nombre de usuario y contraseña. Elige los que prefieras.

### 7. Iniciar el servidor
```bash
python manage.py runserver
```

### 8. Abrir en el navegador

| Aplicación principal | http://127.0.0.1:8000 |
| Panel de administración | http://127.0.0.1:8000/admin |
| API REST | http://127.0.0.1:8000/api/ |

---

##  Estructura del proyecto
```
Parking/
├── parkmanager/        ← configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── parking/            ← aplicación principal
│   ├── models.py       ← modelos de base de datos
│   ├── views.py        ← lógica de vistas
│   ├── serializers.py  ← serializers de la API
│   ├── urls.py         ← rutas de la app
│   └── tests.py        ← pruebas unitarias
├── templates/          ← archivos HTML
├── manage.py
├── requirements.txt    ← dependencias del proyecto
└── .gitignore
```

---

##  Comandos útiles del día a día

| Acción | Comando |
|--------|---------|
| Activar entorno virtual (Windows) | `venv\Scripts\activate` |
| Activar entorno virtual (Mac/Linux) | `source venv/bin/activate` |
| Iniciar servidor | `python manage.py runserver` |
| Crear migraciones | `python manage.py makemigrations` |
| Aplicar migraciones | `python manage.py migrate` |
| Correr pruebas | `python manage.py test` |
| Desactivar entorno virtual | `deactivate` |

---

##  Equipo de desarrollo

- Alejandro Arana
- Anthony Vanegas
- Julio Luna