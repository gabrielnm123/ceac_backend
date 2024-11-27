"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the environment variables
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

def get_env(var_name: str, var_sub: str):
    if DEBUG:
        return os.getenv(var_name, var_sub)
    else:
        if var_name in os.environ:
            return os.getenv(var_name)
        else:
            raise ValueError(f'A variável de ambiente {var_name} não foi definida')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env('SECRET_KEY', 'o==5e^esun8)xwh1*8dog(o!0!v+dfsme8d+1#sj=qeakrq62m')

# If database is installed on the machine
DATABASES_IN_MACHINE = False

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env('POSTGRES_DB', 'ceac'),
        'HOST': get_env('POSTGRES_HOST', '0.0.0.0'),
        'PORT': 5432,
        'USER': get_env('POSTGRES_USER', 'admin'),
        'PASSWORD': get_env('POSTGRES_PASSWORD', 'z_xs-!@*wyq6&ewf38rtjl#!5-obs*8mtdrpov%zq_91w6')
    }
}

ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = get_env('CSRF_TRUSTED_ORIGINS', 'http://localhost:8002,http://127.0.0.1:8002').split(',')

CORS_ALLOWED_ORIGINS = get_env('CORS_ALLOWED_ORIGINS', 'http://localhost:9000,http://127.0.0.1:9000').split(',')

CORS_ALLOW_CREDENTIALS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication.CookieJWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'capacita',
    'administrator',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Deve estar antes do CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # O middleware CSRF deve estar ativado
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necessário para o CSRF
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Configurar o local onde os arquivos estáticos serão coletados para produção
STATIC_ROOT = os.path.join(BASE_DIR, './static')
if DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Define o tempo de vida do access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),   # Tempo de vida do refresh token
    'ROTATE_REFRESH_TOKENS': True,                # Renova o refresh token quando o access token é renovado
    'BLACKLIST_AFTER_ROTATION': True,             # Coloca o refresh token antigo na lista negra após a renovação
}

# Configurações de cookies
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG        # True em produção, False em desenvolvimento
CSRF_COOKIE_SECURE = not DEBUG           # True em produção, False em desenvolvimento

# Cabeçalhos de segurança
SECURE_CONTENT_TYPE_NOSNIFF = True       # Protege contra ataques MIME sniffing
SECURE_BROWSER_XSS_FILTER = True         # Protege contra ataques XSS
X_FRAME_OPTIONS = 'DENY'                 # Protege contra ataques de Clickjacking

if not DEBUG:
    SECURE_HSTS_SECONDS = 3600               # Força o navegador a usar HTTPS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True    # Aplica HSTS a todos os subdomínios
    SECURE_HSTS_PRELOAD = True               # Pré-carrega HSTS para os navegadores
