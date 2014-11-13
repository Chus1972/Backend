"""
Django settings for LosBarkitosProyecto project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import urlparse

#Registra database schemes en la URL's
urlparse.uses_netloc.append('mysql')
DATABASES = {}
'''try:
    # Chequea para asegurarse de que DATABASES esta en settings.py
    if 'DATABASES' not in locals():
        DATABASES = {}
    if 'DATABASE_URL' in os.environ:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])

        # Se asegura que  la BDD por default existe
        DATABASES['default'] = DATABASES.get('default', {})

        # update con la configuracion de environment
        DATABASES['default'].update({
            'NAME' : url.path[1:],
            'USER' : url.username,
            'PASSWORD' : url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        })

        if url.scheme == 'mysql':
            DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
except Exception:
    print 'Error en la BDD:', sys.exc_info()'''

#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(80r!achazq71v7+3hav8lv4q3le8v#p#mxng4acjfa85l=bwy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'south',
    'LosBarkitosApp',
    'rest_framework',
    'mockups',)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'zonahoraria.TimezoneMiddleware',
)

ROOT_URLCONF = 'LosBarkitosProyecto.urls'

WSGI_APPLICATION = 'LosBarkitosProyecto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LosBarkitosNAS',
        'USER': 'chus',
        'PASSWORD': 'Otisuhc0',
        'HOST': 'marinaferry.no-ip.org',
        'PORT': '3306',
    }
}'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_c71c74c67cde020',
        'USER': 'b17e70697e2374',
        'PASSWORD': '3eaf2e91',
        'HOST': 'eu-cdbr-west-01.cleardb.com',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
