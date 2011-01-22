from django import forms

from floppyforms.widgets import (TextInput, HiddenInput, CheckboxInput, Select,
                                 FileInput, ClearableFileInput, SelectMultiple,
                                 DateInput, DateTimeInput, TimeInput, URLInput,
                                 NumberInput, RangeInput, EmailInput,
                                 NullBooleanSelect, SlugInput)

__all__ = (
    'Field', 'CharField', 'IntegerField', 'DateField', 'TimeField',
    'DateTimeField', 'EmailField', 'FileField', 'ImageField', 'URLField',
    'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
    'FloatField', 'DecimalField', 'SlugField',
)


class Field(forms.Field):
    widget = TextInput
    hidden_widget = HiddenInput

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
        self.widget.is_required = self.required  # fallback to support
                                                 # is_required with
                                                 # Django < 1.3


class CharField(Field):
    widget = TextInput


class BooleanField(Field, forms.BooleanField):
    widget = CheckboxInput


class NullBooleanField(Field, forms.NullBooleanField):
    widget = NullBooleanSelect


class ChoiceField(Field, forms.ChoiceField):
    widget = Select


class FileField(Field, forms.FileField):
    widget = ClearableFileInput


class ImageField(Field, forms.ImageField):
    widget = ClearableFileInput


class MultipleChoiceField(forms.MultipleChoiceField):
    widget = SelectMultiple


class DateField(Field, forms.DateField):
    widget = DateInput


class DateTimeField(Field, forms.DateTimeField):
    widget = DateTimeInput


class TimeField(Field, forms.TimeField):
    widget = TimeInput


class DecimalField(Field, forms.DecimalField):
    widget = NumberInput


class FloatField(Field, forms.FloatField):
    widget = NumberInput


class IntegerField(FloatField, forms.IntegerField):
    widget = NumberInput


class EmailField(Field, forms.EmailField):
    widget = EmailInput


class URLField(Field, forms.URLField):
    widget = URLInput


class SlugField(Field, forms.SlugField):
    widget = SlugInput
