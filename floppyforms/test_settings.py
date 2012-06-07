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

TEST_RUNNER = 'discover_runner.DiscoverRunner'

SECRET_KEY = '0'
