"""
Django settings for share_stuff project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_DIRS = (TEMPLATE_PATH,)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'not shown'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = ('Pat Martinez', 'patmartinezmtn@gmail.com')

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [
'sharestuffnow.net',
'www.sharestuffnow.net',
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sharing',
    'django_messages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'myproject.urls' # *** was share_stuff.urls

WSGI_APPLICATION = 'myproject.wsgi.application' # *** was share_stuff


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'share_stuff',
        'USER': 'martinej123',
        'PASSWORD': 'not shown', 
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# This worked with DEBUG= True
# STATIC_URL = 'http://www.sharestuffnow.net/static/'

STATIC_URL = '/static/'
STATIC_ROOT = '/home/martinej123/webapps/share_stuff_static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

#Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/martinej123/webapps/share_stuff_static/media/'
# MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

LOGIN_URL = '/sharing/sign_in/'
