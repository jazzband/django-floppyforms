import sys

from django.utils import six


class InvalidVariable(six.text_type):
    if sys.version_info[0] >= 3:
        def __bool__(self):
            return False
    else:
        def __nonzero__(self):
            return False
