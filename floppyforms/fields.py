import django
from django import forms
import decimal

from .widgets import (TextInput, HiddenInput, CheckboxInput, Select,
                      ClearableFileInput, SelectMultiple, DateInput,
                      DateTimeInput, TimeInput, URLInput, NumberInput,
                      EmailInput, NullBooleanSelect, SlugInput, IPAddressInput,
                      SplitDateTimeWidget, SplitHiddenDateTimeWidget,
                      MultipleHiddenInput)

__all__ = (
    'Field', 'CharField', 'IntegerField', 'DateField', 'TimeField',
    'DateTimeField', 'EmailField', 'FileField', 'ImageField', 'URLField',
    'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
    'FloatField', 'DecimalField', 'SlugField', 'RegexField',
    'GenericIPAddressField', 'TypedChoiceField', 'FilePathField',
    'TypedMultipleChoiceField', 'ComboField', 'MultiValueField',
    'SplitDateTimeField',
)
if django.VERSION < (1, 9):
    __all__ += ('IPAddressField',)


class Field(forms.Field):
    widget = TextInput
    hidden_widget = HiddenInput


class CharField(Field, forms.CharField):
    widget = TextInput

    def widget_attrs(self, widget):
        attrs = super(CharField, self).widget_attrs(widget)
        if attrs is None:
            attrs = {}
        if self.max_length is not None and isinstance(widget, (TextInput, HiddenInput)):
            # The HTML attribute is maxlength, not max_length.
            attrs.update({'maxlength': str(self.max_length)})
        return attrs


class BooleanField(Field, forms.BooleanField):
    widget = CheckboxInput


class NullBooleanField(Field, forms.NullBooleanField):
    widget = NullBooleanSelect


class ChoiceField(Field, forms.ChoiceField):
    widget = Select


class TypedChoiceField(ChoiceField, forms.TypedChoiceField):
    widget = Select


class FilePathField(ChoiceField, forms.FilePathField):
    widget = Select


class FileField(Field, forms.FileField):
    widget = ClearableFileInput


class ImageField(Field, forms.ImageField):
    widget = ClearableFileInput


class MultipleChoiceField(Field, forms.MultipleChoiceField):
    widget = SelectMultiple
    hidden_widget = MultipleHiddenInput


class TypedMultipleChoiceField(MultipleChoiceField,
                               forms.TypedMultipleChoiceField):
    pass


class DateField(Field, forms.DateField):
    widget = DateInput


class DateTimeField(Field, forms.DateTimeField):
    widget = DateTimeInput


class TimeField(Field, forms.TimeField):
    widget = TimeInput


class FloatField(Field, forms.FloatField):
    widget = NumberInput

    def widget_attrs(self, widget):
        attrs = super(FloatField, self).widget_attrs(widget) or {}
        if self.min_value is not None:
            attrs['min'] = self.min_value
        if self.max_value is not None:
            attrs['max'] = self.max_value
        if 'step' not in widget.attrs:
            attrs.setdefault('step', 'any')
        return attrs


class IntegerField(Field, forms.IntegerField):
    widget = NumberInput

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', NumberInput if not kwargs.get('localize') else self.widget)
        super(IntegerField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(IntegerField, self).widget_attrs(widget) or {}
        if self.min_value is not None:
            attrs['min'] = self.min_value
        if self.max_value is not None:
            attrs['max'] = self.max_value
        return attrs


class DecimalField(Field, forms.DecimalField):
    widget = NumberInput

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', NumberInput if not kwargs.get('localize') else self.widget)
        super(DecimalField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(DecimalField, self).widget_attrs(widget) or {}
        if self.min_value is not None:
            attrs['min'] = self.min_value
        if self.max_value is not None:
            attrs['max'] = self.max_value
        if self.decimal_places is not None:
            attrs['step'] = decimal.Decimal('0.1') ** self.decimal_places
        return attrs


class EmailField(Field, forms.EmailField):
    widget = EmailInput


class URLField(Field, forms.URLField):
    widget = URLInput


class SlugField(Field, forms.SlugField):
    widget = SlugInput


class RegexField(Field, forms.RegexField):
    widget = TextInput

    def __init__(self, regex, js_regex=None, max_length=None, min_length=None,
                 error_message=None, *args, **kwargs):
        self.js_regex = js_regex
        super(RegexField, self).__init__(regex, max_length, min_length,
                                         *args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(RegexField, self).widget_attrs(widget) or {}
        if self.js_regex is not None:
            attrs['pattern'] = self.js_regex
        return attrs


if django.VERSION < (1, 9):
    class IPAddressField(Field, forms.IPAddressField):
        widget = IPAddressInput


class GenericIPAddressField(Field, forms.GenericIPAddressField):
    pass


class ComboField(Field, forms.ComboField):
    pass


class MultiValueField(Field, forms.MultiValueField):
    pass


class SplitDateTimeField(forms.SplitDateTimeField):
    widget = SplitDateTimeWidget
    hidden_widget = SplitHiddenDateTimeWidget

    def __init__(self, *args, **kwargs):
        super(SplitDateTimeField, self).__init__(*args, **kwargs)
        for widget in self.widget.widgets:
            widget.is_required = self.required
