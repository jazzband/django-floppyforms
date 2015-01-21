# flake8: noqa
from django.forms import (BaseModelForm, model_to_dict, fields_for_model,
                          save_instance, ValidationError, Media,
                          MediaDefiningClass)

from .fields import *
from .forms import *
from .models import *
from .widgets import *

try:
    from . import gis
except Exception:
    import warnings
    warnings.warn(
        "Unable to import floppyforms.gis, geometry widgets not available")

__version__ = '1.3.0'
