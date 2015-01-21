from floppyforms.forms import Form as FloppyForm
from floppyforms.__future__.models import (ModelFormMetaclass,
                                           ModelForm as FloppyModelForm)
from floppyforms.models import ModelForm as OldFloppyModelForm

from django.forms import Form as DjangoForm, ModelForm as DjangoModelForm
from django.utils import six
import django

import warnings

__all__ = ('make_floppy',)

class TestForm(FloppyForm):
    pass

def make_floppy(form_class):

    form_instance = form_class()
    if (
        isinstance(form_instance, FloppyForm) or
        isinstance(form_instance, FloppyModelForm)
    ):
        warnings.warn(
            "Attempting to reclassify an existing Floppyform as a Floppyform",
            RuntimeWarning)
        return form_class

    if isinstance(form_instance, DjangoForm):
        new_form_class = type(form_class.__name__, (form_class, FloppyForm), {})

    elif isinstance(form_instance, DjangoModelForm):

        if django.VERSION < (1, 6):
            new_form_class = type(form_class.__name__, (
                form_class, OldFloppyModelForm), {})
        else:
            new_form_class = type(form_class.__name__, (
                six.with_metaclass(ModelFormMetaclass,
                form_class, FloppyModelForm),), {})

    new_form_class.__module__ = form_class.__module__

    return new_form_class
