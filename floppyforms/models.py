import warnings

from django.forms import models

from .fields import Field
from .forms import LayoutRenderer
from .widgets import Select, SelectMultiple, MultipleHiddenInput

__all__ = ('ModelForm', 'ModelChoiceField', 'ModelMultipleChoiceField')


class ModelForm(LayoutRenderer, models.ModelForm):
    def __new__(cls, *args, **kwargs):
        url = 'https://github.com/gregmuellegger/django-floppyforms/tree/1.2.0/CHANGES.rst'
        warnings.warn(
            'The behaviour of subclasses of floppyforms.models.ModelForm will '
            'change with django-floppyforms 2.0. '
            'Use `import floppyforms.__future__ as forms` instead of '
            '`import floppyforms as forms` to use the new behaviour now. '
            'See announcement here: %s' % url,
            FutureWarning)
        return super(ModelForm, cls).__new__(cls, *args, **kwargs)


class ModelChoiceField(Field, models.ModelChoiceField):
    widget = Select


class ModelMultipleChoiceField(Field, models.ModelMultipleChoiceField):
    widget = SelectMultiple
    hidden_widget = MultipleHiddenInput
