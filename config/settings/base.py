"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from utils.KMSHelper import get_kms_value

import os

# 파일에서 서버 정보 로드(SECRET_KEY, ALLOWED_HOSTS, DATABASES)
SETTING_PRD_DIC = get_kms_value()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SETTING_PRD_DIC['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = SETTING_PRD_DIC['ALLOWED_HOSTS']

AES_KEY = SETTING_PRD_DIC['AES_KEY']
AES_KEY_IV = SETTING_PRD_DIC['AES_KEY_IV']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'note',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',        ## 순서 중요!!
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.custom_exception_handler.ExceptionMiddleware',
]

# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:3000',
    'https://127.0.0.1:3000',
    'http://localhost:3000',
    'https://localhost:3000',
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': SETTING_PRD_DIC['DATABASES']['default'],
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    # 버저닝 클래스를 URLPathVersioning으로 설정
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    # DRF 기본 렌더링을 json으로 설정 (json으로 설정하지 않으면 HTML로 렌더링되며, 파라미터 추가를 통해 json으로 응답을 받아야하므로 설정함)
    'DEFAULT_RENERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # DRF 기본 파서를 json으로 설정
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    # 필터 설정
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    # Custom 페이징 클래스 설정
    'DEFAULT_PAGINATION_CLASS': 'config.paginations.CustomPagination',
    # Custom 예외처리 핸들러 설정
    'EXCEPTION_HANDLER': 'config.custom_exception_handler.handle_exception',
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.TokenAuthentication',
    # ],
}

SWAGGER_SETTINGS = {
    # 인증 정보 관련 버튼 삭제 처리 (실제 배포 시에는 필요함)
    'SECURITY_DEFINITIONS': None,
}

LOGDIR = Path(os.getenv('LOGDIR')) if os.getenv('LOGDIR') else BASE_DIR / 'logs'
LOGGING = {
    'version': 1,
    'diable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)8s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,   # 로그 파일 당 10M 까지
            'backupCount': 10,              # 로그 파일을 최대 10개까지 유지
            # 'class': 'logging.FileHandler',
            'filename': LOGDIR / 'django.log',
            'formatter': 'default'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': False
        },
        'note': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': False
        },
        'django_crontab': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': False
        },
    },
}

CRONTAB_DJANGO_MANAGE_PATH = BASE_DIR / 'manage.py'
CRONTAB_COMMENT = 'note'

CRONJOBS = [
    ('0 0 * * *', 'django.core.management.call_command', ['clearsessions']),     # 매 일 0시 만료 세션 정리 수행
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# 웹페이지에 사용할 정적파일의 최상위 URL 경로
STATIC_URL = 'static/'

# 개발 단계에서 사용하는 정적 파일이 위치한 경로들을 지정하는 설정 항목 (현재 사용하는 static 파일이 없어서 주석 처리 함)
# STATICFILES_DIRS = [BASE_DIR / 'static']

# Django 프로젝트에서 사용하는 모든 정적 파일을 한 곳에 모아넣는 경로
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
