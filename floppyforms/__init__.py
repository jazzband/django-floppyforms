from django.forms import (BaseForm, Form, ModelForm, BaseModelForm,
                          model_to_dict, fields_for_model, save_instance,
                          ValidationError, Media, MediaDefiningClass)

from django.contrib.localflavor.generic.forms import (
                          DEFAULT_DATE_INPUT_FORMATS,
                          DEFAULT_DATETIME_INPUT_FORMATS,
)

from floppyforms.fields import *
from floppyforms.models import *
from floppyforms.widgets import *
from floppyforms import gis

__version__ = '0.4.7'
