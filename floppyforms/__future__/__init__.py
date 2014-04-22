# flake8: noqa
from floppyforms import *

import django

if django.VERSION < (1, 6):
    import warnings
    warnings.warn("floppyforms.__future__ features are only available in "
                  "django 1.6+")
else:
    from .models import *
