from django import forms, VERSION
from django.template import loader
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext, ugettext_lazy

__all__ = (
    'TextInput', 'PasswordInput', 'HiddenInput', 'ClearableFileInput',
    'FileInput', 'DateInput', 'DateTimeInput', 'TimeInput', 'Textarea',
    'CheckboxInput', 'Select', 'NullBooleanSelect', 'SelectMultiple',
    'RadioSelect', 'CheckboxSelectMultiple', 'SearchInput', 'RangeInput',
    'ColorInput', 'EmailInput', 'URLInput', 'PhoneNumberInput', 'NumberInput',
    'IPAddressInput', 'MultiWidget', 'Widget', 'SplitDateTimeWidget',
    'SplitHiddenDateTimeWidget', 'MultipleHiddenInput',
)


class Widget(forms.Widget):
    pass


class Input(forms.TextInput):
    input_type = None
    template_name = 'floppyforms/input.html'
    is_required = False

    def get_context_data(self):
        return {}

    def get_context(self, name, value, attrs=None, extra_context={}):
        context = {
            'type': self.input_type,
            'name': name,
            'hidden': self.is_hidden,
            'required': self.is_required,
            'value': '',
        }
        context.update(extra_context)

        if value:
            context['value'] = value

        context.update(self.get_context_data())

        attrs.update(self.attrs)

        # for things like "checked", set the value to False so that the
        # template doesn't render checked="".
        for key, value in attrs.items():
            if value == True:
                attrs[key] = False
        context['attrs'] = attrs
        return context

    def render(self, name, value, attrs=None, extra_context={}):
        context = self.get_context(name, value, attrs=attrs,
                                   extra_context=extra_context)
        return loader.render_to_string(self.template_name, context)


class TextInput(Input):
    input_type = 'text'


class PasswordInput(Input):
    input_type = 'password'

    def __init__(self, attrs=None, render_value=False):
        super(PasswordInput, self).__init__(attrs)
        self.render_value = render_value

    def render(self, name, value, attrs=None):
        if not self.render_value:
            value = None
        return super(PasswordInput, self).render(name, value, attrs)


class HiddenInput(Input):
    input_type = 'hidden'
    is_hidden = True

    def get_context_data(self):
        ctx = super(HiddenInput, self).get_context_data()
        ctx['hidden'] = True
        return ctx


class SlugInput(TextInput):

    def get_context_data(self):
        self.attrs['pattern'] = "[-\w]+"
        return super(SlugInput, self).get_context_data()


class IPAddressInput(TextInput):

    def get_context_data(self):
        self.attrs['pattern'] = ("(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|"
                                 "2[0-4]\d|[0-1]?\d?\d)){3}")
        return super(IPAddressInput, self).get_context_data()


class Textarea(Input):
    template_name = 'floppyforms/textarea.html'
    rows = 10
    cols = 40

    def __init__(self, attrs=None):
        default_attrs = {'cols': self.cols, 'rows': self.rows}
        if attrs:
            default_attrs.update(attrs)
        super(Textarea, self).__init__(default_attrs)


class FileInput(forms.FileInput, Input):
    input_type = 'file'

    def render(self, name, value, attrs=None):
        return super(FileInput, self).render(name, None, attrs=attrs)

if VERSION >= (1, 3):
    class ClearableFileInput(FileInput, forms.ClearableFileInput):
        template_name = 'floppyforms/clearable_input.html'
        initial_text = ugettext_lazy('Currently')
        input_text = ugettext_lazy('Change')
        clear_checkbox_label = ugettext_lazy('Clear')

        def get_context_data(self):
            ctx = super(ClearableFileInput, self).get_context_data()
            ctx['initial_text'] = self.initial_text
            ctx['input_text'] = self.input_text
            ctx['clear_checkbox_label'] = self.clear_checkbox_label
            return ctx

        def render(self, name, value, attrs=None, extra_context={}):
            context = self.get_context(name, value, attrs=attrs,
                                       extra_context=extra_context)
            ccb_name = self.clear_checkbox_name(name)
            context['checkbox_name'] = ccb_name
            context['checkbox_id'] = self.clear_checkbox_id(ccb_name)
            return loader.render_to_string(self.template_name, context)
else:
    class ClearableFileInput(FileInput):
        pass


class DateInput(forms.DateInput, Input):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput, Input):
    input_type = 'datetime'


class TimeInput(forms.TimeInput, Input):
    input_type = 'time'


class SearchInput(Input):
    input_type = 'search'


class EmailInput(Input):
    input_type = 'email'


class URLInput(Input):
    input_type = 'url'


class ColorInput(Input):
    input_type = 'color'


class NumberInput(Input):
    input_type = 'number'
    min = None
    max = None
    step = None

    def __init__(self, attrs=None):
        default_attrs = {'min': self.min, 'max': self.max, 'step': self.step}
        if attrs:
            default_attrs.update(attrs)
        super(NumberInput, self).__init__(default_attrs)


class RangeInput(NumberInput):
    input_type = 'range'


class PhoneNumberInput(Input):
    input_type = 'tel'


class CheckboxInput(forms.CheckboxInput, Input):
    input_type = 'checkbox'

    def render(self, name, value, attrs=None):
        try:
            result = self.check_test(value)
            if result:
                self.attrs['checked'] = ''
        except:  # That bare except is in the Django code...
            pass
        if value not in ('', True, False, None):
            value = force_unicode(value)
        return Input.render(self, name, value, attrs=attrs)


class Select(forms.Select, Input):
    template_name = 'floppyforms/select.html'

    def render(self, name, value, attrs=None, choices=()):
        if choices:
            self.choices = choices
        extra = {'choices': self.choices}
        return Input.render(self, name, value, attrs=attrs,
                            extra_context=extra)


class NullBooleanSelect(forms.NullBooleanSelect, Select):

    def render(self, name, value, attrs=None, choices=()):
        choices = ((u'1', ugettext('Unknown')),
                   (u'2', ugettext('Yes')),
                   (u'3', ugettext('No')))
        try:
            value = {True: u'2', False: u'3', u'2': u'2', u'3': u'3'}[value]
        except KeyError:
            value = u'1'
        return Select.render(self, name, value, attrs, choices=choices)


class SelectMultiple(forms.SelectMultiple, Select):

    def get_context_data(self):
        ctx = super(SelectMultiple, self).get_context_data()
        ctx['multiple'] = True
        return ctx

    def render(self, name, value, attrs=None, choices=()):
        return Select.render(self, name, value, attrs=attrs, choices=choices)


class CheckboxSelectMultiple(SelectMultiple):
    template_name = 'floppyforms/checkbox_select.html'


class RadioSelect(forms.RadioSelect, Select):
    template_name = 'floppyforms/radio.html'

    def render(self, name, value, attrs=None, choices=()):
        return Select.render(self, name, value, attrs=attrs, choices=choices)


class MultiWidget(forms.MultiWidget):
    pass


class SplitDateTimeWidget(MultiWidget):

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (DateInput(attrs=attrs, format=date_format),
                   TimeInput(attrs=attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microseconds=0)]
        return [None, None]


class SplitHiddenDateTimeWidget(SplitDateTimeWidget):
    is_hidden = True

    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(SplitHiddenDateTimeWidget, self).__init__(attrs, date_format,
                                                        time_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class MultipleHiddenInput(HiddenInput):
    """<input type="hidden"> for fields that have a list of values"""
    def __init__(self, attrs=None, choices=()):
        super(MultipleHiddenInput, self).__init__(attrs)
        self.choices = choices

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        id_ = final_attrs.get('id', None)
        inputs = []
        for i, v in enumerate(value):
            input_attrs = dict(value=force_unicode(v), **final_attrs)
            if id_:
                input_attrs['id'] = '%s_%s' % (id_, i)
            del input_attrs['type']
            del input_attrs['value']
            input_ = HiddenInput()
            input_.is_required = self.is_required
            inputs.append(input_.render(name, force_unicode(v), input_attrs))
        return "\n".join(inputs)

