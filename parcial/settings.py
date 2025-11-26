import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-clave-temporal-12345')

# SECURITY WARNING: don't run with debug turned on in production!
# Se define como True por defecto, pero se cambia a False en el bloque RENDER de abajo
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Mis apps
    'usuarios',
    'alumnos',
    'scraper',
    # Librerías de terceros
    'crispy_forms',
    'crispy_bootstrap5',
]

# CONFIGURACIÓN CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Vital para archivos estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'parcial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'parcial.wsgi.application'

# Database
# NOTA: En Render esto usa SQLite efímero (se borra al reiniciar).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Configuración de Whitenoise para servir archivos en producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'


# --- CONFIGURACIÓN DE EMAIL (DINÁMICA) ---
# Lee los datos de las variables de entorno de Render.
# Si no existen las variables, usa valores por defecto (útil para local).
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True

# Estos valores se llenarán con lo que pongas en "Environment" en Render
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'tu_email_local@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'tu_pass_local')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# --- CONFIGURACIÓN ESPECÍFICA DE RENDER ---
if 'RENDER' in os.environ:
    # Hosts permitidos en producción
    ALLOWED_HOSTS = ['sistema-alumnos-mxzq.onrender.com', 'localhost', '127.0.0.1']
    
    # Desactivar modo debug por seguridad
    DEBUG = False
    
    # Seguridad adicional para formularios y HTTPS
    CSRF_TRUSTED_ORIGINS = ['https://sistema-alumnos-mxzq.onrender.com']
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS settings (Opcional, fuerza HTTPS)
    SECURE_SSL_REDIRECT = True
else:
    # Configuración Local
    ALLOWED_HOSTS = ['*']
    DEBUG = True