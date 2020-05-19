#!/usr/bin/env python
import argparse
import logging

import os, sys

log = logging.getLogger(__name__)


os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'


# Adding current directory to ``sys.path``.
parent = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent)


def runtests(*argv):
    argv = list(argv) or [
        'floppyforms',
        'tests',
    ]
    opts = argparser.parse_args(argv)

    is_py38 = sys.version_info.major == 3 and sys.version_info.minor == 8
    if is_py38:
        log.warning("Coverage is currently broken in Python 3.8, coveragfe option ignored")
        use_coverage = False
    else:
        use_coverage = opts.coverage
    if use_coverage:
        from coverage import coverage
        test_coverage = coverage(
            branch=True,
            source=['floppyforms'])
        test_coverage.start()

    # Run tests.
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], 'test'] + opts.appname)

    if use_coverage:
        test_coverage.stop()

        # Report coverage to commandline.
        test_coverage.report(file=sys.stdout)


argparser = argparse.ArgumentParser(description='Process some integers.')
argparser.add_argument('appname', nargs='*')
argparser.add_argument('--no-coverage', dest='coverage', action='store_const',
    const=False, default=True, help='Do not collect coverage data.')


if __name__ == '__main__':
    runtests(*sys.argv[1:])
