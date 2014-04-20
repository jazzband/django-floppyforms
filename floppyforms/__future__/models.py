from django.db import models as db_models
from django.forms.models import (ModelFormMetaclass as _ModelFormMetaclass,
                                 modelform_factory as _modelform_factory,
                                 modelformset_factory as _modelformset_factory,
                                 inlineformset_factory as _inlineformset_factory,
                                 model_to_dict, fields_for_model, BaseModelForm,
                                 save_instance, ALL_FIELDS, BaseModelFormSet,
                                 BaseInlineFormSet)
from django.utils import six

from floppyforms import fields
from floppyforms.models import (ModelForm as _ModelForm,
                                ModelChoiceField, ModelMultipleChoiceField)
from floppyforms.widgets import Textarea


__all__ = (
    'ModelForm', 'BaseModelForm', 'model_to_dict', 'fields_for_model',
    'save_instance', 'ModelChoiceField', 'ModelMultipleChoiceField',
    'ALL_FIELDS', 'BaseModelFormSet', 'modelformset_factory',
    'BaseInlineFormSet', 'inlineformset_factory',
)


FORMFIELD_OVERRIDES = {
    db_models.BooleanField: {'form_class': fields.BooleanField},
    db_models.CharField: {'form_class': fields.CharField},
    db_models.CommaSeparatedIntegerField: {'form_class': fields.CharField},
    db_models.DateField: {'form_class': fields.DateField},
    db_models.DateTimeField: {'form_class': fields.DateTimeField},
    db_models.DecimalField: {'form_class': fields.DecimalField},
    db_models.EmailField: {'form_class': fields.EmailField},
    db_models.FilePathField: {'form_class': fields.FilePathField},
    db_models.FloatField: {'form_class': fields.FloatField},
    db_models.IntegerField: {'form_class': fields.IntegerField},
    db_models.BigIntegerField: {'form_class': fields.IntegerField},
    db_models.IPAddressField: {'form_class': fields.IPAddressField},
    db_models.GenericIPAddressField: {'form_class': fields.GenericIPAddressField},
    db_models.NullBooleanField: {'form_class': fields.NullBooleanField},
    db_models.PositiveIntegerField: {'form_class': fields.IntegerField},
    db_models.PositiveSmallIntegerField: {'form_class': fields.IntegerField},
    db_models.SlugField: {'form_class': fields.SlugField},
    db_models.SmallIntegerField: {'form_class': fields.IntegerField},
    db_models.TextField: {'form_class': fields.CharField, 'widget': Textarea},
    db_models.TimeField: {'form_class': fields.TimeField},
    db_models.URLField: {'form_class': fields.URLField},
    db_models.BinaryField: {'form_class': fields.CharField},

    db_models.FileField: {'form_class': fields.FileField},
    db_models.ImageField: {'form_class': fields.ImageField},

    db_models.ForeignKey: {'form_class': ModelChoiceField},
    db_models.ManyToManyField: {'form_class': ModelMultipleChoiceField},
    db_models.OneToOneField: {'form_class': ModelChoiceField},
}

for value in FORMFIELD_OVERRIDES.values():
    value['choices_form_class'] = fields.TypedChoiceField


def formfield_callback(db_field, **kwargs):
    defaults = FORMFIELD_OVERRIDES.get(db_field.__class__, {}).copy()
    defaults.update(kwargs)
    return db_field.formfield(**defaults)


class ModelFormMetaclass(_ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        if not attrs.get('formfield_callback'):
            attrs['formfield_callback'] = formfield_callback
        return super(ModelFormMetaclass, mcs).__new__(mcs, name, bases, attrs)


class ModelForm(six.with_metaclass(ModelFormMetaclass, _ModelForm)):
    pass


def modelform_factory(model, form=ModelForm, *args, **kwargs):
    return _modelform_factory(model, form, *args, **kwargs)


def modelformset_factory(model, form=ModelForm, *args, **kwargs):
    return _modelformset_factory(model, form, *args, **kwargs)


def inlineformset_factory(parent_model, model, form=ModelForm,
                          *args, **kwargs):
    return _inlineformset_factory(parent_model, model, form,
                                  *args, **kwargs)
