from django.forms import models

from floppyforms.widgets import Select, SelectMultiple

__all__ = ('ModelChoiceField', 'ModelMultipleChoiceField')


class ModelChoiceField(models.ModelChoiceField):
    widget = Select


class ModelMultipleChoiceField(models.ModelMultipleChoiceField):
    widget = SelectMultiple
