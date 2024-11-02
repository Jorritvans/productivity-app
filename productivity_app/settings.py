from pathlib import Path
import os
import dj_database_url
from datetime import timedelta

if os.path.isfile('env.py'):
    import env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '8000-jorritvans-productivity-9zhpc5cokwg.ws.codeinstitute-ide.net',
    '8080-jorritvans-productivity-zqeljsth1ag.ws.codeinstitute-ide.net',
    os.environ.get('ALLOWED_HOST'),
]

# CORS Settings
if "CLIENT_ORIGIN" in os.environ:
    CORS_ALLOWED_ORIGINS = [os.environ.get("CLIENT_ORIGIN")]
else:
    CORS_ALLOWED_ORIGINS = [
        'https://8080-jorritvans-productivity-zqeljsth1ag.ws.codeinstitute-ide.net',
        'http://localhost:3000',
        'https://productivity-app-frontend-ea5313cc46b8.herokuapp.com',
    ]

if 'FRONTEND_BASE_URL' in os.environ:
    CORS_ALLOWED_ORIGINS.append(os.environ.get('FRONTEND_BASE_URL'))

CORS_ALLOW_ORIGIN_REGEXES = [
    r"^https://.*\.codeinstitute-ide\.net$"
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'authorization',
    'content-type',
    'x-csrftoken',
]

CORS_ALLOW_CREDENTIALS = True  # Allow credentials like cookies or tokens

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://8080-jorritvans-productivity-zqeljsth1ag.ws.codeinstitute-ide.net',
    'https://8000-jorritvans-productivity-9zhpc5cokwg.ws.codeinstitute-ide.net',
    'http://localhost:3000',
    'https://productivity-app-frontend-ea5313cc46b8.herokuapp.com',
]

CSRF_COOKIE_NAME = 'csrftoken'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'

INSTALLED_APPS = [
    'corsheaders',  # Make sure this is included
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'cloudinary',
    'cloudinary_storage',
    'accounts',
    'tasks',
    'django_filters',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be first
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'productivity_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'productivity_app.wsgi.application'
ASGI_APPLICATION = 'productivity_app.asgi.application'

database_url = os.environ.get("DATABASE_URL")

if 'DEV' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    if database_url:
        DATABASES = {
            'default': dj_database_url.parse(database_url)
        }
    else:
        raise ValueError("DATABASE_URL is not set or is empty.")

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'JWT_AUTH_COOKIE': 'my-app-auth',
    'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token',
    'JWT_AUTH_SAMESITE': 'None'
}
