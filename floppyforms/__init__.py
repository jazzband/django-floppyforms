# flake8: noqa
from django.forms import (BaseModelForm, model_to_dict, fields_for_model,
                          ValidationError, Media, MediaDefiningClass)

from .fields import *
from .forms import *
from .models import *
from .widgets import *

try:
    # Django < 1.9
    from django.forms import save_instance
except ImportError:
    pass

try:
    from . import gis
except Exception:
    import warnings
    warnings.warn(
        "Unable to import floppyforms.gis, geometry widgets not available")

__version__ = '1.6.1'
