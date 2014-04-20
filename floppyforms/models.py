from django.forms import models

from .fields import Field
from .forms import LayoutRenderer
from .widgets import Select, SelectMultiple

__all__ = ('ModelForm', 'ModelChoiceField', 'ModelMultipleChoiceField')


class ModelForm(LayoutRenderer, models.ModelForm):
    pass


class ModelChoiceField(Field, models.ModelChoiceField):
    widget = Select


class ModelMultipleChoiceField(Field, models.ModelMultipleChoiceField):
    widget = SelectMultiple
