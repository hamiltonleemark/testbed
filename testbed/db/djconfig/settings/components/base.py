"""
Django settings for djconfig project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from split_settings.tools import optional, include
import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__, "..", "..")))
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2)_mx$*994pc!^dyc*0b3*n^=h3#b32g6j0v6$evq49^l4m^^3'

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.core.management',
    'pure_pagination',
    'testdb',
    'product',
    'branch',
)

#TEMPLATE_LOADERS = (
    #"django.template.loaders.filesystem.Loader",
    #"django.template.loaders.app_directories.Loader",
    #"django.template.loaders.eggs.Loader",
#)

#TEMPLATE_DIRS = (
    #os.path.join(BASE_DIR, "..", "templates"),
#)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'djconfig.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
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



# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

sqllite_path = os.path.abspath(os.path.join(BASE_DIR, 'db.sqlite3'))

##
# Values are provided by the settings/__init__.py content.
DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'USER': '{{USER}}',
#        'PASSWORD': '{{PASSWORD}}',
#        'HOST': '{{HOST}}',
#        'NAME': 'testbed',
#        'init_command': 'Set storage_engine=INNODB',
#    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

##
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
