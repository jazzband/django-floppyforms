import django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.template import Context, Template
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

import floppyforms as forms

from .base import InvalidVariable
from .compat import unittest


skipIf = unittest.skipIf


def render(template, context=None):
    if context is None:
        context = {}
    c = Context(context)
    t = Template('{% load floppyforms %}' + template)
    return t.render(c)


class HiddenForm(forms.Form):
    hide = forms.CharField(widget=forms.HiddenInput())


class OneFieldForm(forms.Form):
    text = forms.CharField()

    def clean(self):
        if self.errors:
            raise ValidationError('Please correct the errors below.')


class ShortForm(forms.Form):
    name = forms.CharField(label=_('Your first name?'))
    age = forms.IntegerField(required=False)
    metadata = forms.CharField(required=False, widget=forms.HiddenInput)


class RegistrationForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    firstname = forms.CharField(label=_('Your first name?'))
    lastname = forms.CharField(label=_('Your last name:'))
    username = forms.CharField(max_length=30)
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text=_('Make sure to use a secure password.'),
    )
    password2 = forms.CharField(label=_('Retype password'), widget=forms.PasswordInput)
    age = forms.IntegerField(required=False)

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise ValidationError('Haha, you trapped into the honeypot.')
        return self.cleaned_data['honeypot']

    def clean(self):
        if self.errors:
            raise ValidationError('Please correct the errors below.')


class PLayoutTests(TestCase):
    def test_layout(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/p.html'):
            with self.assertTemplateUsed('floppyforms/rows/p.html'):
                layout = render('{% form form using "floppyforms/layouts/p.html" %}', {'form': form})
        self.maxDiff = None
        self.assertHTMLEqual(layout, """
        <p><label for="id_firstname">Your first name?</label> <input type="text" name="firstname" id="id_firstname" required />
        </p>
        <p><label for="id_lastname">Your last name:</label> <input type="text" name="lastname" id="id_lastname" required />
        </p>
        <p><label for="id_username">Username:</label> <input type="text" name="username" id="id_username" maxlength="30" required />
        </p>
        <p><label for="id_password">Password:</label> <input type="password" name="password" id="id_password" required />
         <span class="helptext">Make sure to use a secure password.</span></p>
        <p><label for="id_password2">Retype password:</label> <input type="password" name="password2" id="id_password2" required />
        </p>
        <p><label for="id_age">Age:</label> <input type="number" name="age" id="id_age" />
        <input type="hidden" name="honeypot" id="id_honeypot" />
        </p>
        """)

    def test_layout_with_errors(self):
        form = RegistrationForm({'non_field_errors': True})
        layout = render('{% form form using "floppyforms/layouts/p.html" %}', {'form': form})
        self.maxDiff = None
        self.assertHTMLEqual(layout, """
        <ul class="errorlist"><li>Please correct the errors below.</li></ul>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_firstname">Your first name?</label> <input type="text" name="firstname" id="id_firstname" required /></p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_lastname">Your last name:</label> <input type="text" name="lastname" id="id_lastname" required /></p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_username">Username:</label> <input type="text" name="username" id="id_username" maxlength="30" required /></p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p>
            <label for="id_password">Password:</label> <input type="password" name="password" id="id_password" required />
            <span class="helptext">Make sure to use a secure password.</span>
        </p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_password2">Retype password:</label> <input type="password" name="password2" id="id_password2" required /></p>
        <p><label for="id_age">Age:</label> <input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" id="id_honeypot" /></p>
        """)

        form = RegistrationForm({'non_field_errors': True, 'honeypot': 1})
        layout = render('{% form form using "floppyforms/layouts/p.html" %}', {'form': form})
        self.assertHTMLEqual(layout, """
        <ul class="errorlist">
            <li>Please correct the errors below.</li>
            <li>Haha, you trapped into the honeypot.</li>
        </ul>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_firstname">Your first name?</label> <input type="text" name="firstname" id="id_firstname" required /></p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_lastname">Your last name:</label> <input type="text" name="lastname" id="id_lastname" required /></p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_username">Username:</label> <input type="text" name="username" id="id_username" maxlength="30" required /></p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p>
            <label for="id_password">Password:</label> <input type="password" name="password" id="id_password" required />
            <span class="helptext">Make sure to use a secure password.</span>
        </p>
        <ul class="errorlist"><li>This field is required.</li></ul>
        <p><label for="id_password2">Retype password:</label> <input type="password" name="password2" id="id_password2" required /></p>
        <p><label for="id_age">Age:</label> <input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" id="id_honeypot" value="1" /></p>
        """)

    def test_layout_with_custom_label(self):
        form = OneFieldForm()
        layout = render("""
            {% form form using %}
                {% formrow form.text using "floppyforms/rows/p.html" with label="Custom label" %}
            {% endform %}
        """, {'form': form})
        self.assertHTMLEqual(layout, """
        <p><label for="id_text">Custom label:</label> <input type="text" name="text" id="id_text" required /></p>
        """)

    def test_layout_with_custom_help_text(self):
        form = OneFieldForm()
        layout = render("""
            {% form form using %}
                {% formrow form.text using "floppyforms/rows/p.html" with help_text="Would you mind entering text here?" %}
            {% endform %}
        """, {'form': form})
        self.assertHTMLEqual(layout, """
        <p>
            <label for="id_text">Text:</label> <input type="text" name="text" id="id_text" required />
            <span class="helptext">Would you mind entering text here?</span>
        </p>
        """)

    def test_hidden_only_fields(self):
        form = HiddenForm()
        rendered = render("""{% form form using "floppyforms/layouts/p.html" %}""", {'form': form})
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="hide" id="id_hide" required>
        """)

    def test_formsets_with_hidden_fields(self):
        ShortFormset = formset_factory(form=ShortForm, extra=1)
        formset = ShortFormset(initial=[{'name': 'Johnson', 'age': 23, 'metadata': 'Hidden details'}])
        rendered = render("""{% form formset using "floppyforms/layouts/p.html" %}""", {'formset': formset})
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_form-0-name">Your first name?</label>
            <input type="text" name="form-0-name" value="Johnson" required id="id_form-0-name">
        </p>
        <p>
            <label for="id_form-0-age">Age:</label>
            <input type="number" name="form-0-age" value="23" id="id_form-0-age">
            <input type="hidden" name="form-0-metadata" value="Hidden details" id="id_form-0-metadata">
        </p>
        <p>
            <label for="id_form-1-name">Your first name?</label>
            <input type="text" name="form-1-name" required id="id_form-1-name">
        </p>
        <p>
            <label for="id_form-1-age">Age:</label>
            <input type="number" name="form-1-age" id="id_form-1-age">
            <input type="hidden" name="form-1-metadata" id="id_form-1-metadata">
        </p>
        """)


class TableLayoutTests(TestCase):
    def test_default_layout_is_same_as_table_layout(self):
        form = RegistrationForm()
        default = render('{% form form %}', {'form': form})
        layout = render('{% form form using "floppyforms/layouts/table.html" %}', {'form': form})
        self.assertEqual(default, layout)

    def test_layout(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/table.html'):
            with self.assertTemplateUsed('floppyforms/rows/tr.html'):
                layout = render('{% form form using "floppyforms/layouts/table.html" %}', {'form': form})
        self.assertHTMLEqual(layout, """
        <tr><th><label for="id_firstname">Your first name?</label></th><td><input type="text" name="firstname" id="id_firstname" required /></td></tr>
        <tr><th><label for="id_lastname">Your last name:</label></th><td><input type="text" name="lastname" id="id_lastname" required /></td></tr>
        <tr><th><label for="id_username">Username:</label></th><td><input type="text" name="username" id="id_username" maxlength="30" required /></td></tr>
        <tr><th>
            <label for="id_password">Password:</label></th><td><input type="password" name="password" id="id_password" required />
            <br /><span class="helptext">Make sure to use a secure password.</span></td></tr>
        <tr><th><label for="id_password2">Retype password:</label></th><td><input type="password" name="password2" id="id_password2" required /></td></tr>
        <tr><th>
            <label for="id_age">Age:</label></th><td><input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" id="id_honeypot" />
        </td></tr>
        """)

    def test_layout_with_errors(self):
        form = RegistrationForm({'non_field_errors': True})
        layout = render('{% form form using "floppyforms/layouts/table.html" %}', {'form': form})
        self.assertHTMLEqual(layout, """
        <tr><td colspan="2"><ul class="errorlist"><li>Please correct the errors below.</li></ul></td></tr>
        <tr><th><label for="id_firstname">Your first name?</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="firstname" id="id_firstname" required /></td></tr>
        <tr><th><label for="id_lastname">Your last name:</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="lastname" id="id_lastname" required /></td></tr>
        <tr><th><label for="id_username">Username:</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="username" id="id_username" maxlength="30" required /></td></tr>
        <tr>
            <th><label for="id_password">Password:</label></th>
            <td>
                <ul class="errorlist"><li>This field is required.</li></ul>
                <input type="password" name="password" id="id_password" required />
                <br /><span class="helptext">Make sure to use a secure password.</span>
            </td>
        </tr>
        <tr>
            <th><label for="id_password2">Retype password:</label></th>
            <td><ul class="errorlist"><li>This field is required.</li></ul><input type="password" name="password2" id="id_password2" required /></td>
        </tr>
        <tr><th><label for="id_age">Age:</label></th><td><input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" id="id_honeypot" /></td></tr>
        """)

        form = RegistrationForm({'non_field_errors': True, 'honeypot': 1})
        layout = render('{% form form using "floppyforms/layouts/table.html" %}', {'form': form})
        self.assertHTMLEqual(layout, """
        <tr><td colspan="2"><ul class="errorlist"><li>Please correct the errors below.</li><li>Haha, you trapped into the honeypot.</li></ul></td></tr>
        <tr><th><label for="id_firstname">Your first name?</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="firstname" id="id_firstname" required /></td></tr>
        <tr><th><label for="id_lastname">Your last name:</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="lastname" id="id_lastname" required /></td></tr>
        <tr><th><label for="id_username">Username:</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="text" name="username" id="id_username" maxlength="30" required /></td></tr>
        <tr><th><label for="id_password">Password:</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="password" name="password" id="id_password" required /><br /><span class="helptext">Make sure to use a secure password.</span></td></tr>
        <tr><th><label for="id_password2">Retype password:</label></th><td><ul class="errorlist"><li>This field is required.</li></ul><input type="password" name="password2" id="id_password2" required /></td></tr>
        <tr><th><label for="id_age">Age:</label></th><td><input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" value="1" id="id_honeypot" /></td></tr>
        """)

    def test_layout_with_custom_label(self):
        form = OneFieldForm()
        layout = render("""
            {% form form using %}
                {% formrow form.text using "floppyforms/rows/tr.html" with label="Custom label" %}
            {% endform %}
        """, {'form': form})
        self.assertHTMLEqual(layout, """
        <tr><th><label for="id_text">Custom label:</label></th><td><input type="text" name="text" id="id_text" required /></td></tr>
        """)

    def test_layout_with_custom_help_text(self):
        form = OneFieldForm()
        layout = render("""
            {% form form using %}
                {% formrow form.text using "floppyforms/rows/tr.html" with help_text="Would you mind entering text here?" %}
            {% endform %}
        """, {'form': form})
        self.assertHTMLEqual(layout, """
        <tr><th>
            <label for="id_text">Text:</label>
        </th><td>
            <input type="text" name="text" id="id_text" required />
            <br /><span class="helptext">Would you mind entering text here?</span>
        </td></tr>
        """)

    def test_hidden_only_fields(self):
        form = HiddenForm()
        rendered = render("""{% form form using "floppyforms/layouts/table.html" %}""", {'form': form})
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="hide" id="id_hide" required>
        """)

    def test_formsets_with_hidden_fields(self):
        ShortFormset = formset_factory(form=ShortForm, extra=1)
        formset = ShortFormset(initial=[{'name': 'Johnson', 'age': 23, 'metadata': 'Hidden details'}])
        rendered = render("""{% form formset using "floppyforms/layouts/table.html" %}""", {'formset': formset})
        self.assertHTMLEqual(rendered, """
        <tr>
            <th><label for="id_form-0-name">Your first name?</label></th>
            <td>
                <input type="text" name="form-0-name" value="Johnson" required id="id_form-0-name">
            </td>
        </tr>
        <tr>
            <th><label for="id_form-0-age">Age:</label></th>
            <td>
                <input type="number" name="form-0-age" value="23" id="id_form-0-age">
                <input type="hidden" name="form-0-metadata" value="Hidden details" id="id_form-0-metadata">
            </td>
        </tr>
        <tr>
            <th><label for="id_form-1-name">Your first name?</label></th>
            <td>
                <input type="text" name="form-1-name" required id="id_form-1-name">
            </td>
        </tr>
        <tr>
            <th><label for="id_form-1-age">Age:</label></th>
            <td>
                <input type="number" name="form-1-age" id="id_form-1-age">
                <input type="hidden" name="form-1-metadata" id="id_form-1-metadata">
            </td>
        </tr>
        """)


class UlLayoutTests(TestCase):
    def test_layout(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/ul.html'):
            with self.assertTemplateUsed('floppyforms/rows/li.html'):
                layout = render('{% form form using "floppyforms/layouts/ul.html" %}', {'form': form})
        self.assertHTMLEqual(layout, """
        <li><label for="id_firstname">Your first name?</label> <input type="text" name="firstname" id="id_firstname" required /></li>
        <li><label for="id_lastname">Your last name:</label> <input type="text" name="lastname" id="id_lastname" required /></li>
        <li><label for="id_username">Username:</label> <input type="text" name="username" id="id_username" maxlength="30" required /></li>
        <li><label for="id_password">Password:</label> <input type="password" name="password" id="id_password" required />
            <span class="helptext">Make sure to use a secure password.</span></li>
        <li><label for="id_password2">Retype password:</label> <input type="password" name="password2" id="id_password2" required /></li>
        <li><label for="id_age">Age:</label> <input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" id="id_honeypot" /></li>
        """)

    def test_layout_with_errors(self):
        form = RegistrationForm({'non_field_errors': True})
        layout = render('{% form form using "floppyforms/layouts/ul.html" %}', {'form': form})
        self.assertHTMLEqual(layout, """
        <li><ul class="errorlist"><li>Please correct the errors below.</li></ul></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_firstname">Your first name?</label> <input type="text" name="firstname" id="id_firstname" required /></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_lastname">Your last name:</label> <input type="text" name="lastname" id="id_lastname" required /></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_username">Username:</label> <input type="text" name="username" id="id_username" maxlength="30" required /></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_password">Password:</label> <input type="password" name="password" id="id_password" required />
            <span class="helptext">Make sure to use a secure password.</span></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_password2">Retype password:</label> <input type="password" name="password2" id="id_password2" required /></li>
        <li><label for="id_age">Age:</label> <input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" id="id_honeypot" /></li>
        """)

        form = RegistrationForm({'non_field_errors': True, 'honeypot': 1})
        layout = render('{% form form using "floppyforms/layouts/ul.html" %}', {'form': form})
        self.assertHTMLEqual(layout, """
        <li><ul class="errorlist"><li>Please correct the errors below.</li><li>Haha, you trapped into the honeypot.</li></ul></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_firstname">Your first name?</label> <input type="text" name="firstname" id="id_firstname" required /></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_lastname">Your last name:</label> <input type="text" name="lastname" id="id_lastname" required /></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_username">Username:</label> <input type="text" name="username" id="id_username" maxlength="30" required /></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_password">Password:</label> <input type="password" name="password" id="id_password" required />
            <span class="helptext">Make sure to use a secure password.</span></li>
        <li><ul class="errorlist"><li>This field is required.</li></ul><label for="id_password2">Retype password:</label> <input type="password" name="password2" id="id_password2" required /></li>
        <li><label for="id_age">Age:</label> <input type="number" name="age" id="id_age" />
            <input type="hidden" name="honeypot" value="1" id="id_honeypot" /></li>
        """)

    def test_layout_with_custom_label(self):
        form = OneFieldForm()
        layout = render("""
            {% form form using %}
                {% formrow form.text using "floppyforms/rows/li.html" with label="Custom label" %}
            {% endform %}
        """, {'form': form})
        self.assertHTMLEqual(layout, """
        <li><label for="id_text">Custom label:</label><input type="text" name="text" id="id_text" required /></li>
        """)

    def test_layout_with_custom_help_text(self):
        form = OneFieldForm()
        layout = render("""
            {% form form using %}
                {% formrow form.text using "floppyforms/rows/li.html" with help_text="Would you mind entering text here?" %}
            {% endform %}
        """, {'form': form})
        self.assertHTMLEqual(layout, """
        <li>
            <label for="id_text">Text:</label>
            <input type="text" name="text" id="id_text" required />
            <span class="helptext">Would you mind entering text here?</span>
        </li>
        """)

    def test_hidden_only_fields(self):
        form = HiddenForm()
        rendered = render("""{% form form using "floppyforms/layouts/ul.html" %}""", {'form': form})
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="hide" id="id_hide" required>
        """)

    def test_formsets_with_hidden_fields(self):
        ShortFormset = formset_factory(form=ShortForm, extra=1)
        formset = ShortFormset(initial=[{'name': 'Johnson', 'age': 23, 'metadata': 'Hidden details'}])
        rendered = render("""{% form formset using "floppyforms/layouts/ul.html" %}""", {'formset': formset})
        self.assertHTMLEqual(rendered, """
        <li>
            <label for="id_form-0-name">Your first name?</label>
            <input type="text" name="form-0-name" value="Johnson" required id="id_form-0-name">
        </li>
        <li>
            <label for="id_form-0-age">Age:</label>
            <input type="number" name="form-0-age" value="23" id="id_form-0-age">
            <input type="hidden" name="form-0-metadata" value="Hidden details" id="id_form-0-metadata">

        </li>
        <li>
            <label for="id_form-1-name">Your first name?</label>
            <input type="text" name="form-1-name" required id="id_form-1-name">
        </li>
        <li>
            <label for="id_form-1-age">Age:</label>
            <input type="number" name="form-1-age" id="id_form-1-age">
            <input type="hidden" name="form-1-metadata" id="id_form-1-metadata">
        </li>
        """)


class LabelSuffixTests(TestCase):
    def assertInHTML(self, *args, **kwargs):
        if not hasattr(super(LabelSuffixTests, self), 'assertInHTML'):
            # Fallback to simple contains check. That is enough in our case.
            needle, haystack = args[:2]
            return needle in haystack
        return super(LabelSuffixTests, self).assertInHTML(*args, **kwargs)

    def layout_test_form_label_suffix(self, layout):
        form = RegistrationForm()
        rendered = render('{% form form using "floppyforms/layouts/' + layout + '.html" %}', {'form': form})
        self.assertInHTML('<label for="id_username">Username:</label>', rendered)

        form = RegistrationForm(label_suffix=' = ')
        rendered = render('{% form form using "floppyforms/layouts/' + layout + '.html" %}', {'form': form})
        self.assertInHTML('<label for="id_username">Username = </label>', rendered)

        form = RegistrationForm(label_suffix='')
        rendered = render('{% form form using "floppyforms/layouts/' + layout + '.html" %}', {'form': form})
        self.assertInHTML('<label for="id_username">Username</label>', rendered)

    def layout_test_field_label_suffix(self, layout):
        class UserForm(forms.Form):
            username = forms.CharField(label_suffix='!')
            no_suffix = forms.CharField(label_suffix='')
            password = forms.CharField()

        form = UserForm()
        rendered = render('{% form form using "floppyforms/layouts/' + layout + '.html" %}', {'form': form})
        self.assertInHTML('<label for="id_username">Username!</label>', rendered)
        self.assertInHTML('<label for="id_no_suffix">No suffix</label>', rendered)
        self.assertInHTML('<label for="id_password">Password:</label>', rendered)

        form = UserForm(label_suffix='#')
        rendered = render('{% form form using "floppyforms/layouts/' + layout + '.html" %}', {'form': form})
        self.assertInHTML('<label for="id_username">Username!</label>', rendered)
        self.assertInHTML('<label for="id_no_suffix">No suffix</label>', rendered)
        self.assertInHTML('<label for="id_password">Password#</label>', rendered)

    def test_form_label_suffix_with_p_layout(self):
        self.layout_test_form_label_suffix('p')

    def test_form_label_suffix_with_ul_layout(self):
        self.layout_test_form_label_suffix('ul')

    def test_form_label_suffix_with_table_layout(self):
        self.layout_test_form_label_suffix('table')

    @skipIf(django.VERSION < (1, 8), 'Only applies to Django >= 1.8')
    def test_field_label_suffix_with_p_layout(self):
        self.layout_test_field_label_suffix('p')

    @skipIf(django.VERSION < (1, 8), 'Only applies to Django >= 1.8')
    def test_field_label_suffix_with_ul_layout(self):
        self.layout_test_field_label_suffix('ul')

    @skipIf(django.VERSION < (1, 8), 'Only applies to Django >= 1.8')
    def test_field_label_suffix_with_table_layout(self):
        self.layout_test_field_label_suffix('table')


class TemplateStringIfInvalidTests(TestCase):
    '''
    Regression tests for issue #37.
    '''
    def setUp(self):
        self.original_TEMPLATE_STRING_IF_INVALID = settings.TEMPLATE_STRING_IF_INVALID

    def tearDown(self):
        settings.TEMPLATE_STRING_IF_INVALID = self.original_TEMPLATE_STRING_IF_INVALID

    def test_none(self):
        settings.TEMPLATE_STRING_IF_INVALID = None

        layout = OneFieldForm().as_p()
        self.assertHTMLEqual(layout, """
        <p><label for="id_text">Text:</label> <input type="text" name="text" id="id_text" required /></p>
        """)

    def test_non_empty(self):
        settings.TEMPLATE_STRING_IF_INVALID = InvalidVariable('INVALID')

        layout = OneFieldForm().as_p()
        self.assertHTMLEqual(layout, """
        <p><label for="id_text">Text:</label> <input type="text" name="text" id="id_text" required /></p>
        """)
