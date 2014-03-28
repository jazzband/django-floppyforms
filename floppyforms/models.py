import django
from django.db import models as db_models
from django.forms import models
from django.utils import six
from django.utils.text import capfirst

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

    db_models.FileField: {'form_class': FileField},
    db_models.ImageField: {'form_class': ImageField},

    db_models.ForeignKey: {'form_class': ModelChoiceField},
    db_models.ManyToManyField: {'form_class': ModelMultipleChoiceField},
    db_models.OneToOneField: {'form_class': ModelChoiceField},
}

# BinaryField added in Django 1.6
if (hasattr(db_models, 'BinaryField')):
    FORMFIELD_OVERRIDES[db_models.BinaryField] = {'form_class': CharField}


for value in FORMFIELD_OVERRIDES.values():
    value['choices_form_class'] = TypedChoiceField


if django.VERSION < (1, 6):
    # Monkeypatch in support for choices_form_class.
    # This is the formfield method from Django 1.6.2 with minor
    # modifications.

    def _formfield(self, form_class=None, choices_form_class=None, **kwargs):
        """
        Returns a django.forms.Field instance for this database Field.
        """
        defaults = {'required': not self.blank,
                    'label': capfirst(self.verbose_name),
                    'help_text': self.help_text}
        if self.has_default():
            if callable(self.default):
                defaults['initial'] = self.default
                defaults['show_hidden_initial'] = True
            else:
                defaults['initial'] = self.get_default()
        if self.choices:
            # Fields with choices get special treatment.
            include_blank = (self.blank or
                             not (self.has_default() or 'initial' in kwargs))
            defaults['choices'] = self.get_choices(include_blank=include_blank)
            defaults['coerce'] = self.to_python
            if self.null:
                defaults['empty_value'] = None
            if choices_form_class is not None:
                form_class = choices_form_class
            else:
                form_class = TypedChoiceField
            # Many of the subclass-specific formfield arguments (min_value,
            # max_value) don't apply for choice fields, so be sure to only pass
            # the values that TypedChoiceField will understand.
            for k in list(kwargs):
                if k not in ('coerce', 'empty_value', 'choices', 'required',
                             'widget', 'label', 'initial', 'help_text',
                             'error_messages', 'show_hidden_initial'):
                    del kwargs[k]
        defaults.update(kwargs)
        if form_class is None:
            form_class = CharField
        return form_class(**defaults)
    db_models.Field.formfield = _formfield


def formfield_callback(db_field, **kwargs):
    defaults = FORMFIELD_OVERRIDES.get(db_field.__class__, {}).copy()
    defaults.update(kwargs)
    return db_field.formfield(**defaults)


class ModelFormMetaclass(models.ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        if not attrs.get('formfield_callback'):
            attrs['formfield_callback'] = formfield_callback
        return super(ModelFormMetaclass, mcs).__new__(mcs, name, bases, attrs)


# Necessary because we use django.utils.six (v 1.5.2), which only
# allows a single parent class for with_metaclass.
class _ModelForm(LayoutRenderer, models.ModelForm):
    pass


class ModelForm(six.with_metaclass(ModelFormMetaclass, _ModelForm)):
    pass


def modelform_factory(model, form=ModelForm, *args, **kwargs):
    return models.modelform_factory(model, form, *args, **kwargs)


def modelformset_factory(model, form=ModelForm, *args, **kwargs):
    return models.modelformset_factory(model, form, *args, **kwargs)


def inlineformset_factory(parent_model, model, form=ModelForm,
                          *args, **kwargs):
    return models.inlineformset_factory(parent_model, model, form,
                                        *args, **kwargs)
