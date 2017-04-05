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

__version__ = '1.7.1.dev1'


def set_template_setting(key, value):
    if django.VERSION < (1, 8):
        settings_key = 'TEMPLATE_' + key
        setattr(settings, settings_key, value)
    else:
        settings_key = key.lower()
        template_settings = settings.TEMPLATES[0]['OPTIONS']
        template_settings[settings_key] = value


def get_template_setting(key, default=None):
    if django.VERSION < (1, 8):
        settings_key = 'TEMPLATE_' + key
        return getattr(settings, settings_key, default)
    else:
        settings_key = key.lower()
        template_settings = settings.TEMPLATES[0]['OPTIONS']
        return template_settings.get(settings_key, default)
