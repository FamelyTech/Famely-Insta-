"""
Django settings for jalodei project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the .env variables
env = environ.Env()
if(os.path.isfile(os.path.join(BASE_DIR.parent, '.env')) or os.
   path.isfile(env.str('ENV_PATH', ''))):
    env.read_env(env.str('ENV_PATH', os.path.join(BASE_DIR.parent, '.env')))

PROD = env.bool('PRODUCTION', False)
DEBUG_POSTGRES = env.bool('DEBUG_POSTGRES', False)
UPDATE = env.bool('UPDATE', False)
TEST = env.bool('TEST', False)
ACCOUNT_USERNAME = env.str('ACCOUNT_USERNAME', '')
ACCOUNT_PASSWORD = env.str('ACCOUNT_PASSWORD', '')
PROXY_1 = env.str('PROXY_1', '')
WEBSHARE_API_KEY = env.str('WEBSHARE_API_KEY', default='')
OPENAI_API_KEY = env.str('OPENAI_API_KEY', default='')
AZUREAI_KEY_1 = env.str('AZUREAI_KEY_1', default='')
AZUREAI_ENDPOINT = env.str('AZUREAI_ENDPOINT', default='')
OPENAI_ENGINE = env.str('OPENAI_ENGINE', default='gpt-3.5-turbo-instruct')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]


# Application definition

INSTALLED_APPS = [
    "page.apps.PageConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "jalodei.urls"

LOGIN_REDIRECT_URL = '/'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jalodei.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR / 'theme/static')]
STATIC_ROOT = f'{BASE_DIR}/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"