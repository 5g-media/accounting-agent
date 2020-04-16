""" 5G-MEDIA project """
import os

# =================================
# PROJECT ROOT
# =================================
from datetime import timedelta

PROJECT_ROOT = os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir)))

# =================================
# DEBUG SETTINGS
# =================================
DEBUG = os.getenv('ACC_DEBUG')

# =================================
# Accounting ADMIN/MANAGER
# =================================
DEVELOPER_EMAIL = 'pathanasoulis@ep.singularlogic.eu'
ADMINS = (
    ('admin', DEVELOPER_EMAIL),
)
MANAGERS = ADMINS

# =================================
# Allowed Hosts
# =================================
ALLOWED_HOSTS = ['*']

# =================================
# RDBMS CONFIGURATION
# =================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('ACC_DB_NAME'),
        'USER': os.getenv('ACC_DB_USER'),
        'PASSWORD': os.getenv('ACC_DB_PASSWORD'),
        'HOST': os.getenv('ACC_DB_HOST'),
        'PORT': os.getenv('ACC_DB_PORT')
    }
}
MIN_STR_LEN, MID_STR_LEN, MAX_STR_LEN = 16, 64, 256

# ==================================
# APPLICATIONS DEFINITION
# ==================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'openmanoapi',
    'nbiapi',
    'api',
    'metric_collector',
    'accounting_client',
    'drf_yasg'
]

# ==================================
# MIDDLEWARES MANAGEMENT
# ==================================
MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================================
# TEMPLATES CONFIGURATION
# ==================================
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

# ==================================
# PASSWORD VALIDATION
# ==================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==================================
# BASIC SETTINGS
# ==================================
SITE_ID = 1
ROOT_URLCONF = 'accounting.urls'
WSGI_APPLICATION = 'accounting.wsgi.application'
SECRET_KEY = 'jh^^w_z@q@+o(28)67js(ljz+vpf@gtp8wl%*j@_r$#2xj+zid'

# =================================
# TIMEZONE SETTINGS
# =================================
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'
USE_TZ = True

# =================================
# MULTILINGUAL SETTINGS
# =================================
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True

# ==================================
# REST FRAMEWORK
# ==================================
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_xml.renderers.XMLRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

# =================================
# STATIC FILES SETTINGS
# =================================
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
STATIC_URL = '/static/'

# ==================================
# LOGGING SETTINGS
# ==================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] - [%(name)s:%(lineno)s] - [%(levelname)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'api': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(PROJECT_ROOT) + "/logs/api.log",
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'openmanoapi': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(PROJECT_ROOT) + "/logs/openmanoapi.log",
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'nbiapi': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(PROJECT_ROOT) + "/logs/nbiapi.log",
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'accounting_client': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(PROJECT_ROOT) + "/logs/accounting_client.log",
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'metric_collector': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(PROJECT_ROOT) + "/logs/metric_collector.log",
            'maxBytes': 2024 * 2024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'api': {
            'handlers': ['api'],
            'level': 'INFO',
        },
        'openmanoapi': {
            'handlers': ['openmanoapi'],
            'level': 'DEBUG',
        },
        'nbiapi': {
            'handlers': ['nbiapi'],
            'level': 'DEBUG',
        },
        'accounting_client': {
            'handlers': ['accounting_client'],
            'level': 'DEBUG',
        },
        'metric_collector': {
            'handlers': ['metric_collector'],
            'level': 'DEBUG',
        },
    }
}

# ==================================
#   CACHE SETTINGS
# ==================================
# Cache time to live is 30 minutes.
CACHE_TTL = 60 * 30

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# =================================
# Accounting HOST INFO
# =================================
ACC_HOST = {
    'PROTOCOL': os.getenv('ACC_HOST_PROTOCOL'),
    'IP': os.getenv('ACC_HOST_IP'),
    'PORT': os.getenv('ACC_HOST_PORT'),
    'PATH': ''
}

# ==================================
# OSM SETTINGS
# ==================================
OSM_IP = os.getenv('ACC_OSM_HOST_IP')
OSM_ADMIN_CREDENTIALS = {"username": "admin", "password": "password"}
OSM_COMPONENTS = {"UI": 'http://{}:80'.format(OSM_IP),
                  "RO-API": 'http://{}:9090'.format(OSM_IP),
                  "NBI-API": 'https://{}:9999'.format(OSM_IP)}
OSM_KAFKA_BOOTSTRAP = "{}:9094".format(OSM_IP)

# =================================
# KAFKA SETTINGS
# =================================
BOOTSTRAP_SERVER = os.getenv('ACC_KAFKA_SERVER')

# ==================================
#   REDIS SETTINGS
# ==================================
REDIS_HOST = os.getenv('ACC_REDIS_HOST')
REDIS_PORT = os.getenv('ACC_REDIS_PORT')
BROKER_URL = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
RESULT_BACKEND = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)

# ==================================
#   CELERY SETTINGS
# ==================================
CELERY_BROKER_URL = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULE = {
    'send_metrics': {
        'task': 'metric_collector.tasks.send_metrics',
        'schedule': timedelta(seconds=300)
    }
}

# =================================
#    DB INSTANCE DEFAULT VALUES
# =================================
MANO_ID = os.getenv('ACC_MANO_ID')
NFVIPOP_ID = os.getenv('ACC_NFVIPOP_ID')
