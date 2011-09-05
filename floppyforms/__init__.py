from django.forms import (Form, ModelForm, BaseModelForm, model_to_dict,
                          fields_for_model, save_instance, ValidationError,
                          Media, MediaDefiningClass)

from django.contrib.localflavor.generic.forms import (
                          DEFAULT_DATE_INPUT_FORMATS,
                          DEFAULT_DATETIME_INPUT_FORMATS,
)

# Import SelectDateWidget from extras
from django.forms.extras import SelectDateWidget

from floppyforms.fields import *
from floppyforms.models import *
from floppyforms.widgets import *
from floppyforms import gis

__version___ = '0.4.7'
