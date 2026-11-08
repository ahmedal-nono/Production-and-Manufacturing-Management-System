
from pathlib import Path
import os
from datetime import timedelta
# settings.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# BACKUP_ROOT = os.path.join(BASE_DIR, 'backups')

# Create the backups directory if it doesn't exist
# if not os.path.exists(BACKUP_ROOT):
#     os.makedirs(BACKUP_ROOT)
# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5q$w7@k3fr8oex8qa=r0uwdzjw7vndyi61$252p50-4x18ito$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    # this line here help with authentication when using the rest_framework auth token .
    'rest_framework.authtoken',
    'administration',
    'workcentre',
    'django_filters',
    'workflow',
    'work_instructions',
    'quality_control',
    'psutil',
    'rest_framework_simplejwt',
    'reports',
    'corsheaders',  # Add this line

]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    # Must sit below GZipMiddleware so the ETag is hashed from the plain
    # body (Django pads gzip output with random bytes to prevent BREACH,
    # which would otherwise change the hash on every response).
    'django.middleware.http.ConditionalGetMiddleware',
    'FPMS.middleware.ApiRevalidateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'administration.middleware.JWTAutoRefreshMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'administration.middleware.ActivityLogMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Should be at the top
    'django.middleware.common.CommonMiddleware',  # After CorsMiddleware
]

# 3. Configure allowed origins (choose one option below)
# Option A: Allow all origins (for development only)
CORS_ALLOW_ALL_ORIGINS = True

# Option B: Allow only specific origins (recommended)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Your Vue.js/React frontend
    "http://127.0.0.1:5173",  # Alternative localhost
    "http://127.0.0.1:*",  # Alternative localhost
    # Add production domains later (e.g., "https://yourdomain.com")
]

# 4. (Optional) Allow cookies/auth headers
CORS_ALLOW_CREDENTIALS = True  # Only needed if frontend sends credentials

ROOT_URLCONF = 'FPMS.urls'

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

WSGI_APPLICATION = 'FPMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if os.environ.get('DB_ENGINE') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.environ.get(
                'DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'FPMSdb'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'root'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            # Reuse database connections instead of opening one per request.
            'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '60')),
            'CONN_HEALTH_CHECKS': True,
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'administration.User'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',  # Useful for admin interface
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    # Pagination is opt-in: clients that send "page" or "page_size" get the
    # paginated {"count", "next", "previous", "results"} shape, while every
    # existing call keeps receiving a plain list.
    'DEFAULT_PAGINATION_CLASS': 'FPMS.pagination.OptInPagination',
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'ROTATE_REFRESH_TOKENS': True,
    # token_blacklist app is not installed; blacklisting after rotation
    # makes /api/token/refresh/ fail with a missing table error.
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
