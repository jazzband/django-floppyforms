from django import forms

from .widgets import (TextInput, HiddenInput, CheckboxInput, Select,
                      ClearableFileInput, SelectMultiple, DateInput,
                      DateTimeInput, TimeInput, URLInput, NumberInput,
                      EmailInput, NullBooleanSelect, SlugInput, IPAddressInput,
                      SplitDateTimeWidget, SplitHiddenDateTimeWidget)

__all__ = (
    'Field', 'CharField', 'IntegerField', 'DateField', 'TimeField',
    'DateTimeField', 'EmailField', 'FileField', 'ImageField', 'URLField',
    'BooleanField', 'NullBooleanField', 'ChoiceField', 'MultipleChoiceField',
    'FloatField', 'DecimalField', 'SlugField', 'RegexField', 'IPAddressField',
    'GenericIPAddressField', 'TypedChoiceField', 'FilePathField',
    'TypedMultipleChoiceField', 'ComboField', 'MultiValueField',
    'SplitDateTimeField',
)


class FieldMixin(object):
    widget = TextInput
    hidden_widget = HiddenInput


class Field(FieldMixin, forms.Field):
    pass


class CharField(FieldMixin, forms.CharField):
    widget = TextInput

    def widget_attrs(self, widget):
        attrs = super(CharField, self).widget_attrs(widget)
        if attrs is None:
            attrs = {}
        if self.max_length is not None and isinstance(widget, (TextInput, HiddenInput)):
            # The HTML attribute is maxlength, not max_length.
            attrs.update({'maxlength': str(self.max_length)})
        return attrs


class BooleanField(FieldMixin, forms.BooleanField):
    widget = CheckboxInput


class NullBooleanField(FieldMixin, forms.NullBooleanField):
    widget = NullBooleanSelect


class ChoiceFieldMixin(FieldMixin):
    widget = Select


class ChoiceField(ChoiceFieldMixin, forms.ChoiceField):
    pass


class TypedChoiceField(ChoiceFieldMixin, forms.TypedChoiceField):
    widget = Select


class FilePathField(ChoiceFieldMixin, forms.FilePathField):
    widget = Select


class FileField(FieldMixin, forms.FileField):
    widget = ClearableFileInput


class ImageField(FieldMixin, forms.ImageField):
    widget = ClearableFileInput


class MultipleChoiceFieldMixin(FieldMixin):
    widget = SelectMultiple


class MultipleChoiceField(MultipleChoiceFieldMixin, forms.MultipleChoiceField):
    pass


class TypedMultipleChoiceField(MultipleChoiceField,
                               forms.TypedMultipleChoiceField):
    pass


class DateField(FieldMixin, forms.DateField):
    widget = DateInput


class DateTimeField(FieldMixin, forms.DateTimeField):
    widget = DateTimeInput


class TimeField(FieldMixin, forms.TimeField):
    widget = TimeInput


class FloatField(FieldMixin, forms.FloatField):
    widget = NumberInput


class IntegerField(FieldMixin, forms.IntegerField):
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


class DecimalField(FieldMixin, forms.DecimalField):
    widget = NumberInput

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', NumberInput if not kwargs.get('localize') else self.widget)
        super(DecimalField, self).__init__(*args, **kwargs)


class EmailField(FieldMixin, forms.EmailField):
    widget = EmailInput


class URLField(FieldMixin, forms.URLField):
    widget = URLInput


class SlugField(FieldMixin, forms.SlugField):
    widget = SlugInput


class RegexField(FieldMixin, forms.RegexField):
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


class IPAddressField(FieldMixin, forms.IPAddressField):
    widget = IPAddressInput


class GenericIPAddressField(FieldMixin, forms.GenericIPAddressField):
    pass


class ComboField(FieldMixin, forms.ComboField):
    pass


class MultiValueField(FieldMixin, forms.MultiValueField):
    pass


class SplitDateTimeField(forms.SplitDateTimeField):
    widget = SplitDateTimeWidget
    hidden_widget = SplitHiddenDateTimeWidget

    def __init__(self, *args, **kwargs):
        super(SplitDateTimeField, self).__init__(*args, **kwargs)
        for widget in self.widget.widgets:
            widget.is_required = self.required
