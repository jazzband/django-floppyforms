from django.forms import models

from .fields import Field
from .widgets import Select, SelectMultiple

__all__ = ('ModelChoiceField', 'ModelMultipleChoiceField')


class ModelChoiceField(Field, models.ModelChoiceField):
    widget = Select


class ModelMultipleChoiceField(Field, models.ModelMultipleChoiceField):
    widget = SelectMultiple
