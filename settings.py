#--------------------------
# dumpon.us main settings.
#--------------------------

import sys, os
from os.path import join as pjoin

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

sys.path.append(pjoin(PROJECT_PATH,'apps'))

DEBUG = True 

TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_pass',
    }
}

TIME_ZONE = 'America/Toronto'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = pjoin(PROJECT_PATH, 'media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

SECRET_KEY = 'RANDOM_KEY_HERE'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    pjoin(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.comments',
    #'django.contrib.staticfiles', django 1.3
    'upload',
    'tagging',
    'south',
    'sorl.thumbnail',
    'pagination', 
    'django_extensions',
)

#Load instatalltion specific settings/passwords.
execfile(pjoin(PROJECT_PATH, '.private-settings'))

