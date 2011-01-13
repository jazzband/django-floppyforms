from django import forms, VERSION
from django.template import loader
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext, ugettext_lazy


class FloppyInput(forms.TextInput):
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


class TextInput(FloppyInput):
    input_type = 'text'


class PasswordInput(forms.PasswordInput, FloppyInput):
    input_type = 'password'


class HiddenInput(FloppyInput):
    input_type = 'hidden'
    is_hidden = True

    def get_context_data(self):
        ctx = super(HiddenInput, self).get_context_data()
        ctx['hidden'] = True
        return ctx


class Textarea(FloppyInput):
    template_name = 'floppyforms/textarea.html'
    rows = 10
    cols = 40

    def get_context_data(self):
        ctx = super(Textarea, self).get_context_data()
        self.attrs['rows'] = self.rows
        self.attrs['cols'] = self.cols
        return ctx


class FileInput(forms.FileInput, FloppyInput):
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
            context['checkbox_name'] = self.clear_checkbox_name(name)
            context['checkbox_id'] = self.clear_checkbox_id(context['checkbox_name'])
            return loader.render_to_string(self.template_name, context)
else:
    class ClearableFileInput(FileInput):
        pass


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

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        for attr in ('min', 'max', 'step'):
            if getattr(self, attr) is not None:
                attrs[attr] = getattr(self, attr)

        return super(NumberInput, self).render(name, value, attrs=attrs)


class RangeInput(NumberInput):
    input_type = 'range'


class PhoneNumberInput(FloppyInput):
    input_type = 'tel'


class CheckboxInput(forms.CheckboxInput, FloppyInput):
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
        return FloppyInput.render(self, name, value, attrs=attrs)


class Select(forms.Select, FloppyInput):
    template_name = 'floppyforms/select.html'

    def render(self, name, value, attrs=None, choices=()):
        if choices:
            self.choices = choices
        extra = {'choices': self.choices}
        return FloppyInput.render(self, name, value, attrs=attrs,
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
