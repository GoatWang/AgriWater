"""
Django settings for ArgriWater project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&h*zeb443n0ujbb2u2sym=qpxnhr!i52h)%&&9hwx52u39x(#9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.0.181", "argri-water.herokuapp.com", "rd.thinktronltd.com"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainapp.apps.MainappConfig'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'ArgriWater.urls'

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

WSGI_APPLICATION = 'ArgriWater.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'ArgriWater',
#         'USER': 'postgres',
#         'PASSWORD': os.environ['POSTGRESQL_PASSWORD'],
#         'HOST': os.environ['POSTGRESQL_HOST'],
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, "static/")
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'


# LINE_CHANNEL_ACCESS_TOKEN=os.environ['LINE_CHANNEL_ACCESS_TOKEN_AIR']
# LINE_CHANNEL_SECRET=os.environ['LINE_CHANNEL_SECRET_AIR']


GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')


# heroku stack:set cedar-14 --app argri-water
# heroku git:remote -a argri-water
# heroku config:set POSTGRESQL_PASSWORD=?? POSTGRESQL_HOST=??
# heroku config:set BUILD_WITH_GEO_LIBRARIES=1

# make sure to have requirements.txt >> or will not detect language
# make sure to have static dir in the git root.
# make sure to install gunicorn: pip install gunicorn


# PROJ4_LIBRARY_PATH = os.environ.get('PROJ4_LIBRARY_PATH')
# heroku buildpacks:remove heroku-community/apt
# heroku buildpacks:set heroku/python
# heroku buildpacks:add --index 1 heroku-community/apt
# heroku buildpacks:add https://github.com/diogojc/heroku-buildpack-python-opencv-scipy
# heroku config:set DISABLE_COLLECTSTATIC=1
# heroku buildpacks:add http://github.com/dulaccc/heroku-buildpack-geodjango/	
# heroku buildpacks:add https://github.com/KevinBrolly/heroku-geodjango-buildpack.git


