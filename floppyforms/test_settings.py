DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'floppyforms.sqlite',
    },
}

INSTALLED_APPS = [
    'django.contrib.gis',
    'floppyforms',
    'floppyforms.tests',
]

STATIC_URL = '/static/'

SECRET_KEY = '0'

import django
if django.VERSION < (1, 6):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
