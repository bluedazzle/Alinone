# -*- coding: utf-8 -*-
"""
Django settings for AlinSite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l_d6a!j5-*&wvt77$l(!oc(xloap@68_a6+nu^2%7av_24jm60'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['121.41.169.114', 'www.alinone.cn', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pagination',
    'merchant_page',
    'CronOrder',
    'AlinApi',
    'AlinLog',
    'ProxyWork',
    'top',
    'Alin_admin',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

#自定义验证后台
# AUTHENTICATION_BACKENDS = (
#
#     'CronOrder.auth.MyCustomBackend',
#
# )

ROOT_URLCONF = 'AlinSite.urls'

WSGI_APPLICATION = 'AlinSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alinone',
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '123456',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',
    }
}

SESSION_ENGINE="django.contrib.sessions.backends.file"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# TEMPLATE_CONTEXT_PROCESSORS = (
#         "django.core.context_processors.auth",
#         "django.core.context_processors.debug",
#         "django.core.context_processors.i18n",
#         "django.core.context_processors.media",
#         "django.core.context_processors.request"
#     )

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

CSS_DIR = './static/css/'
IMG_DIR = './static/img/'
JS_DIR = './static/js/'
FONTS_DIR = './static/fonts/'
DAYIN_DIR = './static/dayin'
STATIC_ROOT = '/home/rapospectre/PycharmProjects/AlinSite/static'
QR_DIR = './qrimg'
MUSIC_DIR = './static/music/'
APK_DIR = './static/apk/'

