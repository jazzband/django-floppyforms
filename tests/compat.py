import sys


if sys.version_info >= (2, 7):
    import unittest
else:
    from django.utils import unittest


try:
    from django.utils.encoding import force_str
except ImportError:
    # Required for Django < 1.5
    from django.utils.encoding import force_unicode as force_str
