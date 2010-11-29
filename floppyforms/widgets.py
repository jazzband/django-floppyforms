from django import forms
from django.template import loader
from django.utils.translation import ugettext, ugettext_lazy


class FloppyInput(forms.TextInput):
    input_type = None
    template_name = 'floppyforms/input.html'

    def get_extra_context(self):
        return {}

    def render(self, name, value, attrs=None):
        context = {
            'type': self.input_type,
            'name': name,
            'hidden': self.is_hidden,
            'required': self.is_required,
        }
        if value:
            context['value'] = value

        context.update(self.attrs)
        if attrs:
            context.update(attrs)

        context.update(self.get_extra_context())
        return loader.render_to_string(self.template_name, context)


class TextInput(FloppyInput):
    input_type = 'text'


class PasswordInput(FloppyInput):
    input_type = 'password'


class HiddenInput(FloppyInput):
    input_type = 'hidden'
    is_hidden = True

    def get_extra_context(self):
        ctx = super(HiddenInput, self).get_extra_context()
        ctx['hidden'] = True
        return ctx


class Textarea(FloppyInput):
    template_name = 'floppyforms/textarea.html'
    rows = 10
    cols = 40

    def get_extra_context(self):
        ctx = super(Textarea, self).get_extra_context()
        ctx['rows'] = self.rows
        ctx['cols'] = self.cols
        return ctx


class FileInput(forms.FileInput, FloppyInput):
    input_type = 'file'

    def render(self, name, value, attrs=None):
        return super(FileInput, self).render(name, None, attrs=attrs)


class ClearableFileInput(FileInput):
    template_name = 'floppyforms/clearable_input.html'
    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')

    def get_extra_context(self):
        ctx = super(ClearableFileInput, self).get_extra_context()
        ctx['initial'] = self.initial_text
        ctx['input_text'] = self.input_text
        ctx['clear_checkbox_label'] = self.clear_checkbox_label
        return ctx


class DateInput(forms.DateInput, FloppyInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput, FloppyInput):
    input_type = 'datetime'


class TimeInput(forms.TimeInput, FloppyInput):
    input_type = 'time'


class SearchInput(FloppyInput):
    input_type = 'search'


class EmailInput(FloppyInput):
    input_type = 'email'


class URLInput(FloppyInput):
    input_type = 'url'


class ColorInput(FloppyInput):
    input_type = 'color'


class NumberInput(FloppyInput):
    input_type = 'number'
    min = None
    max = None
    step = None
    template_name = 'floppyforms/number_input.html'

    def get_extra_context(self):
        ctx = super(NumberInput, self).get_extra_context()
        for attr in ('min', 'max', 'step'):
            if getattr(self, attr) is not None:
                ctx[attr] = getattr(self, attr)
        return ctx


class RangeInput(NumberInput):
    input_type = 'range'


class PhoneNumberInput(FloppyInput):
    input_type = 'tel'


class CheckboxInput(forms.CheckboxInput, FloppyInput):
    input_type = 'checkbox'

    def render(self, name, value, attrs=None):
        try:
            result = self.check_test(value)
        except:
            result = False
        self.attrs['checked'] = result
        return FloppyInput.render(self, name, value, attrs=attrs)


class Select(forms.Select, FloppyInput):
    template_name = 'floppyforms/select.html'

    def render(self, name, value, attrs=None, choices=()):
        if choices:
            self.choices = choices
        self.attrs['choices'] = self.choices
        return FloppyInput.render(self, name, value, attrs=attrs)


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
    template_name = 'floppyforms/select_multiple.html'

    def get_extra_context(self):
        ctx = super(SelectMultiple, self).get_extra_context()
        ctx['multiple'] = True
        return ctx

    def render(self, name, value, attrs=None, choices=()):
        return Select.render(self, name, value, attrs=attrs, choices=choices)


class CheckboxSelectMultiple(SelectMultiple):
    template_name  = 'floppyforms/checkbox_select.html'


class RadioSelect(forms.RadioSelect, Select):
    template_name = 'floppyforms/radio.html'

    def render(self, name, value, attrs=None, choices=()):
        return Select.render(self, name, value, attrs=attrs, choices=choices)
