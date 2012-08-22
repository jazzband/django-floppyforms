from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import (TextInput, HiddenInput, CheckboxInput, Select,
                      ClearableFileInput, SelectMultiple, DateInput,
                      DateTimeInput, TimeInput, URLInput, NumberInput,
                      EmailInput, NullBooleanSelect, SlugInput, IPAddressInput,
                      SplitDateTimeWidget, SplitHiddenDateTimeWidget,
                      FILE_INPUT_CONTRADICTION)

__all__ = (
    'Field', 'CharField', 'IntegerField', 'DateField', 'TimeField',
    'DateTimeField', 'EmailField', 'FileField', 'ImageField', 'URLField',
    'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
    'FloatField', 'DecimalField', 'SlugField', 'RegexField', 'IPAddressField',
    'TypedChoiceField', 'FilePathField', 'TypedMultipleChoiceField',
    'ComboField', 'MultiValueField', 'SplitDateTimeField',
)


class Field(forms.Field):
    widget = TextInput
    hidden_widget = HiddenInput

    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
        self.widget.is_required = self.required  # fallback to support
                                                 # is_required with
                                                 # Django < 1.3


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
    default_error_messages = {
        'invalid': _(u"No file was submitted. Check the encoding type on the form."),
        'missing': _(u"No file was submitted."),
        'empty': _(u"The submitted file is empty."),
        'max_length': _(u'Ensure this filename has at most %(max)d characters (it has %(length)d).'),
        'contradiction': _(u'Please either submit a file or check the clear checkbox, not both.')
    }

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop('max_length', None)
        self.allow_empty_file = kwargs.pop('allow_empty_file', False)
        super(FileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if data is FILE_INPUT_CONTRADICTION:
            raise forms.ValidationError(self.error_messages['contradiction'])
        if data is False:
            if not self.required:
                return False
            data = None
        if not data and initial:
            return initial
        return super(FileField, self).clean(data)


class ImageField(Field, forms.ImageField):
    widget = ClearableFileInput


class MultipleChoiceField(Field, forms.MultipleChoiceField):
    widget = SelectMultiple


class TypedMultipleChoiceField(MultipleChoiceField,
                               forms.TypedMultipleChoiceField):
    pass


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


class IntegerField(Field, forms.IntegerField):
    widget = NumberInput


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


class IPAddressField(Field, forms.IPAddressField):
    widget = IPAddressInput


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
