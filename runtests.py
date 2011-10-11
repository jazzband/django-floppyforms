#!/usr/bin/env python
import os
import sys

from django.conf import settings
try:
    from django.utils.functional import empty
except ImportError:
    empty = None


def setup_test_environment():
    # reset settings
    settings._wrapped = empty

    apps = [
        'django.contrib.gis',
        'floppyforms',
    ]

    settings_dict = {
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'floppyforms.sqlite',
            },
        },
        'INSTALLED_APPS': apps,
        'STATIC_URL': '/static/',
    }

    # set up settings for running tests for all apps
    settings.configure(**settings_dict)


def runtests(*test_args):
    setup_test_environment()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)
    try:
        from django.test.simple import DjangoTestSuiteRunner

        def run_tests(test_args, verbosity, interactive):
            runner = DjangoTestSuiteRunner(
                verbosity=verbosity, interactive=interactive, failfast=False)
            return runner.run_tests(test_args)
    except ImportError:
        # for Django versions that don't have DjangoTestSuiteRunner
        from django.test.simple import run_tests
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
