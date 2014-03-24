from django.db import models as db_models
from django.forms import models
from django.utils import six

from .fields import (Field, CharField, IntegerField, DateField, TimeField,
                     DateTimeField, EmailField, FileField, ImageField,
                     URLField, BooleanField, NullBooleanField, FloatField,
                     DecimalField, SlugField, IPAddressField,
                     GenericIPAddressField, TypedChoiceField, FilePathField)
from .forms import LayoutRenderer
from .widgets import Select, SelectMultiple, Textarea


__all__ = ('ModelForm', 'ModelChoiceField', 'ModelMultipleChoiceField',
           'modelformset_factory', 'inlineformset_factory')


class ModelChoiceField(Field, models.ModelChoiceField):
    widget = Select


class ModelMultipleChoiceField(Field, models.ModelMultipleChoiceField):
    widget = SelectMultiple


FORMFIELD_OVERRIDES = {
    db_models.BooleanField: {'form_class': BooleanField},
    db_models.CharField: {'form_class': CharField},
    db_models.CommaSeparatedIntegerField: {'form_class': CharField},
    db_models.DateField: {'form_class': DateField},
    db_models.DateTimeField: {'form_class': DateTimeField},
    db_models.DecimalField: {'form_class': DecimalField},
    db_models.EmailField: {'form_class': EmailField},
    db_models.FilePathField: {'form_class': FilePathField},
    db_models.FloatField: {'form_class': FloatField},
    db_models.IntegerField: {'form_class': IntegerField},
    db_models.BigIntegerField: {'form_class': IntegerField},
    db_models.IPAddressField: {'form_class': IPAddressField},
    db_models.GenericIPAddressField: {'form_class': GenericIPAddressField},
    db_models.NullBooleanField: {'form_class': NullBooleanField},
    db_models.PositiveIntegerField: {'form_class': IntegerField},
    db_models.PositiveSmallIntegerField: {'form_class': IntegerField},
    db_models.SlugField: {'form_class': SlugField},
    db_models.SmallIntegerField: {'form_class': IntegerField},
    db_models.TextField: {'form_class': CharField, 'widget': Textarea},
    db_models.TimeField: {'form_class': TimeField},
    db_models.URLField: {'form_class': URLField},
    db_models.BinaryField: {'form_class': CharField},

    db_models.FileField: {'form_class': FileField},
    db_models.ImageField: {'form_class': ImageField},

    db_models.ForeignKey: {'form_class': ModelChoiceField},
    db_models.ManyToManyField: {'form_class': ModelMultipleChoiceField},
    db_models.OneToOneField: {'form_class': ModelChoiceField},
}


for value in FORMFIELD_OVERRIDES.values():
    value['choices_form_class'] = TypedChoiceField


def formfield_callback(db_field, **kwargs):
    defaults = FORMFIELD_OVERRIDES.get(db_field.__class__, {}).copy()
    defaults.update(kwargs)
    return db_field.formfield(**defaults)


class ModelFormMetaclass(models.ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        if not attrs.get('formfield_callback'):
            attrs['formfield_callback'] = formfield_callback
        return super(ModelFormMetaclass, mcs).__new__(mcs, name, bases, attrs)


class ModelForm(six.with_metaclass(ModelFormMetaclass, LayoutRenderer, models.ModelForm)):
    pass


def modelform_factory(model, form=ModelForm, *args, **kwargs):
    return models.modelform_factory(model, form, *args, **kwargs)


def modelformset_factory(model, form=ModelForm, *args, **kwargs):
    return models.modelformset_factory(model, form, *args, **kwargs)


def inlineformset_factory(parent_model, model, form=ModelForm,
                          *args, **kwargs):
    return models.inlineformset_factory(parent_model, model, form,
                                        *args, **kwargs)
