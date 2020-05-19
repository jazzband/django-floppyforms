import sys
import django

if sys.version_info >= (2, 7):
    import unittest
else:
    from django.utils import unittest

if django.VERSION < (1, 5):
    from django.utils.encoding import force_unicode as force_str
else:
    from django.utils.encoding import force_str
