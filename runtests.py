#!/usr/bin/env python
import os, sys
import subprocess


os.environ['PYTHONPATH'] = '.'
os.environ['DJANGO_SETTINGS_MODULE'] = 'floppyforms.test_settings'


def runtests(*args):
    _process = subprocess.Popen(['which', 'django-admin.py'], stdout=subprocess.PIPE)
    _process.wait()
    django_admin_file = _process.stdout.read().decode('utf-8')
    command = 'coverage run --branch --source=floppyforms {0} test'.format(django_admin_file).split()
    args = list(args) or [
        'floppyforms',
    ]
    exit_code = subprocess.call(command + args)
    if exit_code != 0:
        sys.exit(exit_code)
    subprocess.call('coverage report --omit=floppyforms/test*', shell=True)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
