import os
import sys
import warnings
warnings.simplefilter('always')


demo_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.dirname(os.path.dirname(demo_path))
sys.path.insert(0, base_path)


DEBUG = True

USE_I18N = True
USE_L10N = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'floppyforms',
]

MIDDLEWARE_CLASSES = ()

ROOT_URLCONF = 'tests.demo.urls'

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(demo_path, 'templates'),
)

SECRET_KEY = '0'
