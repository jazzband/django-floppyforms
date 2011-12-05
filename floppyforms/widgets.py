from itertools import chain
import re
import datetime

from django import forms
from django.conf import settings
from django.template import loader
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.utils import datetime_safe
from django.utils.dates import MONTHS
from django.utils import formats

try:
    from django.forms.util import to_current_timezone
except ImportError:
    # Dummy timzone converter
    to_current_timezone = lambda value: value

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')


__all__ = (
    'TextInput', 'PasswordInput', 'HiddenInput', 'ClearableFileInput',
    'FileInput', 'DateInput', 'DateTimeInput', 'TimeInput', 'Textarea',
    'CheckboxInput', 'Select', 'NullBooleanSelect', 'SelectMultiple',
    'RadioSelect', 'CheckboxSelectMultiple', 'SearchInput', 'RangeInput',
    'ColorInput', 'EmailInput', 'URLInput', 'PhoneNumberInput', 'NumberInput',
    'IPAddressInput', 'MultiWidget', 'Widget', 'SplitDateTimeWidget',
    'SplitHiddenDateTimeWidget', 'MultipleHiddenInput', 'SelectDateWidget',
)


class Widget(forms.Widget):
    is_required = False


class Input(Widget):
    template_name = 'floppyforms/input.html'
    input_type = None

    def get_context_data(self):
        return {}

    def _format_value(self, value):
        if self.is_localized:
            value = formats.localize_input(value)
        return force_unicode(value)

    def get_context(self, name, value, attrs=None):
        context = {
            'type': self.input_type,
            'name': name,
            'hidden': self.is_hidden,
            'required': self.is_required,
            'True': True,
        }
        # True is injected in the context to allow stricter comparisons
        # for widget attrs. See #25.
        if self.is_hidden:
            context['hidden'] = True

        if value is None:
            value = ''

        if value != '':
            # Only add the value if it is non-empty
            context['value'] = self._format_value(value)

        context.update(self.get_context_data())
        context['attrs'] = self.build_attrs(attrs)

        for key in context['attrs']:
            attr = context['attrs'][key]
            if attr == 1:
                # 1 == True so 'key="1"' will show up only as 'key'
                # Casting to a string so that it doesn't equal to True
                # See #25.
                if not isinstance(attr, bool):
                    context['attrs'][key] = str(attr)
        return context

    def render(self, name, value, attrs=None, **kwargs):
        context = self.get_context(name, value, attrs=attrs or {}, **kwargs)
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


class MultipleHiddenInput(HiddenInput):
    """<input type="hidden"> for fields that have a list of values"""
    def __init__(self, attrs=None, choices=()):
        super(MultipleHiddenInput, self).__init__(attrs)
        self.choices = choices

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []

        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        inputs = []
        for i, v in enumerate(value):
            input_attrs = final_attrs.copy()
            if id_:
                input_attrs['id'] = '%s_%s' % (id_, i)
            input_ = HiddenInput()
            input_.is_required = self.is_required
            inputs.append(input_.render(name, force_unicode(v), input_attrs))
        return "\n".join(inputs)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)


class SlugInput(TextInput):
    """<input type="text"> validating slugs with a pattern"""
    def get_context(self, name, value, attrs):
        context = super(SlugInput, self).get_context(name, value, attrs)
        context['attrs']['pattern'] = "[-\w]+"
        return context


class IPAddressInput(TextInput):
    """<input type="text"> validating IP addresses with a pattern"""
    def get_context(self, name, value, attrs):
        context = super(IPAddressInput, self).get_context(name, value, attrs)
        context['attrs']['pattern'] = ("(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25"
                                       "[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}")
        return context


class FileInput(Input):
    input_type = 'file'
    needs_multipart_form = True
    omit_value = True

    def render(self, name, value, attrs=None):
        if self.omit_value:
            # File inputs can't render an existing value if it's not saved
            value = None
        return super(FileInput, self).render(name, value, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        return files.get(name, None)

    def _has_changed(self, initial, data):
        if data is None:
            return False
        return True


FILE_INPUT_CONTRADICTION = object()


class ClearableFileInput(FileInput):
    template_name = 'floppyforms/clearable_input.html'
    omit_value = False

    def clear_checkbox_name(self, name):
        return name + '-clear'

    def clear_checkbox_id(self, name):
        return name + '_id'

    def get_context(self, name, value, attrs):
        context = super(ClearableFileInput, self).get_context(name, value,
                                                              attrs)
        ccb_name = self.clear_checkbox_name(name)
        context.update({
            'checkbox_name': ccb_name,
            'checkbox_id': self.clear_checkbox_id(ccb_name),
        })
        return context

    def value_from_datadict(self, data, files, name):
        upload = super(ClearableFileInput, self).value_from_datadict(
            data, files, name
        )
        if not self.is_required and CheckboxInput().value_from_datadict(
            data, files, self.clear_checkbox_name(name)
        ):
            if upload:
                return FILE_INPUT_CONTRADICTION
            return False
        return upload

    def _format_value(self, value):
        return value


class Textarea(Input):
    template_name = 'floppyforms/textarea.html'
    rows = 10
    cols = 40

    def __init__(self, attrs=None):
        default_attrs = {'cols': self.cols, 'rows': self.rows}
        if attrs:
            default_attrs.update(attrs)
        super(Textarea, self).__init__(default_attrs)

    def _format_value(self, value):
        return conditional_escape(force_unicode(value))


class DateInput(Input):
    input_type = 'date'

    def __init__(self, attrs=None, format=None):
        super(DateInput, self).__init__(attrs)
        if format:
            self.format = format
            self.manual_format = True
        else:
            self.format = formats.get_format('DATE_INPUT_FORMATS')[0]
            self.manual_format = False

    def _format_value(self, value):
        if self.is_localized and not self.manual_format:
            return formats.localize_input(value)
        elif hasattr(value, 'strftime'):
            value = datetime_safe.new_date(value)
            return value.strftime(self.format)
        return value

    def _has_changed(self, initial, data):
        try:
            input_format = formats.get_format('DATE_INPUT_FORMATS')[0]
            initial = datetime.datetime.strptime(initial, input_format).date()
        except (TypeError, ValueError):
            pass
        return super(DateInput, self)._has_changed(
            self._format_value(initial), data
        )


class DateTimeInput(Input):
    input_type = 'datetime'

    def __init__(self, attrs=None, format=None):
        super(DateTimeInput, self).__init__(attrs)
        if format:
            self.format = format
            self.manual_format = True
        else:
            self.format = formats.get_format('DATETIME_INPUT_FORMATS')[0]
            self.manual_format = False

    def _format_value(self, value):
        if self.is_localized and not self.manual_format:
            return formats.localize_input(value)
        elif hasattr(value, 'strftime'):
            value = datetime_safe.new_datetime(value)
            return value.strftime(self.format)
        return value

    def _has_changed(self, initial, data):
        try:
            input_format = formats.get_format('DATETIME_INPUT_FORMATS')[0]
            initial = datetime.datetime.strptime(initial, input_format)
        except (TypeError, ValueError):
            pass
        return super(DateTimeInput, self)._has_changed(
            self._format_value(initial), data
        )


class TimeInput(Input):
    input_type = 'time'

    def __init__(self, attrs=None, format=None):
        super(TimeInput, self).__init__(attrs)
        if format:
            self.format = format
            self.manual_format = True
        else:
            self.format = formats.get_format('TIME_INPUT_FORMATS')[0]
            self.manual_format = False

    def _format_value(self, value):
        if self.is_localized and not self.manual_format:
            return formats.localize_input(value)
        elif hasattr(value, 'strftime'):
            return value.strftime(self.format)
        return value

    def _has_changed(self, initial, data):
        try:
            input_format = formats.get_format('TIME_INPUT_FORMATS')[0]
            initial = datetime.datetime.strptime(initial, input_format).time()
        except (TypeError, ValueError):
            pass
        return super(TimeInput, self)._has_changed(
            self._format_value(initial), data
        )


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


class CheckboxInput(Input, forms.CheckboxInput):
    input_type = 'checkbox'

    def __init__(self, attrs=None, check_test=None):
        super(CheckboxInput, self).__init__(attrs)
        if check_test is None:
            self.check_test = lambda v: not (v is False or
                                             v is None or
                                             v == '')
        else:
            self.check_test = check_test

    def get_context(self, name, value, attrs):
        result = False
        try:
            result = self.check_test(value)
        except:  # That bare except is in the Django code...
            pass
        context = super(CheckboxInput, self).get_context(name, value, attrs)
        if result:
            context['attrs']['checked'] = True
        return context

    def _format_value(self, value):
        if value in ('', True, False, None):
            value = None
        else:
            value = force_unicode(value)
        return value

    def value_from_datadict(self, data, files, name):
        if name not in data:
            return False
        value = data.get(name)
        values = {'true': True, 'false': False}
        if isinstance(value, basestring):
            value = values.get(value.lower(), value)
        return value

    def _has_changed(self, initial, data):
        return bool(initial) != bool(data)


class Select(Input):
    allow_multiple_selected = False
    template_name = 'floppyforms/select.html'

    def __init__(self, attrs=None, choices=()):
        super(Select, self).__init__(attrs)
        self.choices = list(choices)

    def get_context(self, name, value, attrs=None, choices=()):
        if not isinstance(value, (list, tuple)):
            value = [value]
        context = super(Select, self).get_context(name, value, attrs)

        if self.allow_multiple_selected:
            context['attrs']['multiple'] = "multiple"

        # 'groups' look like this:
        # (
        #   ("Optgroup name", (
        #       (value1, label1),
        #       (value2, label2),
        #   )),
        #   (None, [
        #       (value3, label3),
        #       (value4, label4),
        #   ]),
        # )
        groups = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                group = []
                for val, lab in option_label:
                    group.append((force_unicode(val), lab))
                groups.append((option_value, group))
            else:
                option_value = force_unicode(option_value)
                if groups and groups[-1][0] is None:
                    groups[-1][1].append((option_value, option_label))
                else:
                    groups.append((None, [(option_value, option_label)]))
        context["optgroups"] = groups
        return context

    def _format_value(self, value):
        if len(value) == 1 and value[0] is None:
            return []
        return set(force_unicode(v) for v in value)


class NullBooleanSelect(Select):
    def __init__(self, attrs=None):
        choices = ((u'1', _('Unknown')),
                   (u'2', _('Yes')),
                   (u'3', _('No')))
        super(NullBooleanSelect, self).__init__(attrs, choices)

    def _format_value(self, value):
        value = value[0]
        try:
            value = {True: u'2', False: u'3', u'2': u'2', u'3': u'3'}[value]
        except KeyError:
            value = u'1'
        return value

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        return {u'2': True,
                True: True,
                'True': True,
                u'3': False,
                'False': False,
                False: False}.get(value, None)

    def _has_changed(self, initial, data):
        if initial is not None:
            initial = bool(initial)
        if data is not None:
            data = bool(data)
        return initial != data


class SelectMultiple(Select):
    allow_multiple_selected = True

    def _format_value(self, value):
        if value is None:
            value = []
        return [force_unicode(v) for v in value]

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = set([force_unicode(value) for value in initial])
        data_set = set([force_unicode(value) for value in data])
        return data_set != initial_set


class RadioSelect(Select):
    template_name = 'floppyforms/radio.html'


class CheckboxSelectMultiple(SelectMultiple):
    template_name = 'floppyforms/checkbox_select.html'


class MultiWidget(forms.MultiWidget):
    pass


class SplitDateTimeWidget(MultiWidget):
    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (DateInput(attrs=attrs, format=date_format),
                   TimeInput(attrs=attrs, format=time_format))
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]


class SplitHiddenDateTimeWidget(SplitDateTimeWidget):
    is_hidden = True

    def __init__(self, attrs=None, date_format=None, time_format=None):
        super(SplitHiddenDateTimeWidget, self).__init__(attrs, date_format,
                                                        time_format)
        for widget in self.widgets:
            widget.input_type = 'hidden'
            widget.is_hidden = True


class SelectDateWidget(forms.Widget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = (0, '---')
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'
    template_name = 'floppyforms/select_date.html'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the
        # "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 10)

    def get_context_data(self):
        return {}

    def get_context(self, name, value, attrs=None, extra_context={}):
        context = {
            'year_field': self.year_field % name,
            'month_field': self.month_field % name,
            'day_field': self.day_field % name
        }
        context.update(extra_context)

        if value is None:
            value = ''

        context.update(self.get_context_data())
        attrs.update(self.attrs)

        # for things like "checked", set the value to False so that the
        # template doesn't render checked="".
        for key, value in attrs.items():
            if value == True:
                attrs[key] = False
        context['year_id'] = self.year_field % attrs['id']
        context['month_id'] = self.month_field % attrs['id']
        context['day_id'] = self.day_field % attrs['id']
        del attrs['id']

        context['attrs'] = attrs
        return context

    def render(self, name, value, attrs=None, extra_context={}):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, basestring):
                if settings.USE_L10N:
                    try:
                        input_format = formats.get_format(
                            'DATE_INPUT_FORMATS'
                        )[0]
                        v = datetime.datetime.strptime(value, input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = map(int, match.groups())

        context = self.get_context(name, value, attrs=attrs,
                                   extra_context=extra_context)

        context['year_choices'] = [(i, i) for i in self.years]
        context['year_val'] = year_val

        context['month_choices'] = MONTHS.items()
        context['month_val'] = month_val

        context['day_choices'] = [(i, i) for i in range(1, 32)]
        context['day_val'] = day_val

        return loader.render_to_string(self.template_name, context)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None
        if y and m and d:
            if settings.USE_L10N:
                input_format = formats.get_format('DATE_INPUT_FORMATS')[0]
                try:
                    date_value = datetime.date(int(y), int(m), int(d))
                except ValueError:
                    return '%s-%s-%s' % (y, m, d)
                else:
                    date_value = datetime_safe.new_date(date_value)
                    return date_value.strftime(input_format)
            else:
                return '%s-%s-%s' % (y, m, d)
        return data.get(name, None)
