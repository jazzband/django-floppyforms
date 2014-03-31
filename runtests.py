#!/usr/bin/env python
import os, sys
from coverage import coverage


os.environ['DJANGO_SETTINGS_MODULE'] = 'floppyforms.test_settings'


# Adding current directory to ``sys.path``.
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent)


def runtests(*args):
    args = list(args) or [
        'floppyforms',
    ]

    test_coverage = coverage(
        branch=True,
        source=['floppyforms'])
    test_coverage.start()

    # Run tests.
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'test'] + args)

    test_coverage.stop()

    # Report coverage to commandline.
    test_coverage.report(
        omit='floppyforms/test*',
        file=sys.stdout)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
