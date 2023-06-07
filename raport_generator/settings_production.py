"""
Django settings for raport_generator project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/Raport-Generator')  # adjust the path to your project folder
load_dotenv(os.path.join(project_folder, '.env'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['www.raport-generator.pl']
# ALLOWED_HOSTS = ['luksonini.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    "users",
    "django_cron",
    "aboutme",
    "raport_from_list",
    "raport_from_excel",
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

ROOT_URLCONF = "raport_generator.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "raport_generator.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# import os
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATIC_ROOT = '/home/Luksonini/Raport-Generator/static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "raport_from_list/static",
    BASE_DIR / "users/static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_ROOT = '/home/Luksonini/Raport-Generator/media/'
MEDIA_URL = '/media/'

# DEFAULT_FILE_STORAGE = 'myapp.storage_backend.MyCustomStorage'
#AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

# EMAIL BACKEND
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'lukasz.jozef.gasior@gmail.com'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "lukasz.jozef.gasior@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True


CRON_CLASSES = [
    "users.tasks.DeleteOldFilesCronJob",
    # ...
]

REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.AllowAny',
  ],
}

