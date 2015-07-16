from decimal import Decimal
import django
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import six
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

import floppyforms.__future__ as forms

from .compat import unittest
from .models import Registration


expectedFailure = unittest.expectedFailure
skipIf = unittest.skipIf


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
    height = forms.DecimalField(localize=True, required=False)
    agree_to_terms = forms.BooleanField()

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise ValidationError('Haha, you trapped into the honeypot.')
        return self.cleaned_data['honeypot']

    def clean(self):
        if self.errors:
            raise ValidationError('Please correct the errors below.')


class RegistrationModelForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = (
            'firstname',
            'lastname',
            'username',
            'age',
        )


class FormRenderAsMethodsTests(TestCase):
    def test_default_rendering(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/default.html'):
            with self.assertTemplateUsed('floppyforms/layouts/table.html'):
                rendered = six.text_type(form)
                self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/default.html'):
            with self.assertTemplateUsed('floppyforms/layouts/table.html'):
                rendered = six.text_type(form)
                self.assertTrue(' name="firstname"' in rendered)

    def test_as_p(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/p.html'):
            rendered = form.as_p()
            self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/p.html'):
            rendered = form.as_p()
            self.assertTrue(' name="firstname"' in rendered)

    def test_as_table(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/table.html'):
            rendered = form.as_table()
            self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/table.html'):
            rendered = form.as_table()
            self.assertTrue(' name="firstname"' in rendered)

    def test_as_ul(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/ul.html'):
            rendered = form.as_ul()
            self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/ul.html'):
            rendered = form.as_ul()
            self.assertTrue(' name="firstname"' in rendered)


class FormHasChangedTests(TestCase):
    def test_basic_has_changed(self):
        form = RegistrationForm()
        self.assertFalse(form.has_changed())

        form = RegistrationForm({'height': '1.89'})
        self.assertTrue(form.has_changed())

        form = RegistrationForm({'height': '1.89'},
                                initial={'height': Decimal('1.89')})
        self.assertFalse(form.has_changed())

    def test_custom_has_changed_logic_for_checkbox_input(self):
        form = RegistrationForm({'agree_to_terms': True})
        self.assertTrue(form.has_changed())

        form = RegistrationForm({'agree_to_terms': False},
                                initial={'agree_to_terms': False})
        self.assertFalse(form.has_changed())

        form = RegistrationForm({'agree_to_terms': False},
                                initial={'agree_to_terms': 'False'})
        self.assertFalse(form.has_changed())

    @skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
    def test_widgets_do_not_have_has_changed_method(self):
        self.assertFalse(hasattr(forms.CheckboxInput, '_has_changed'))
        self.assertFalse(hasattr(forms.NullBooleanSelect, '_has_changed'))
        self.assertFalse(hasattr(forms.SelectMultiple, '_has_changed'))
        self.assertFalse(hasattr(forms.FileInput, '_has_changed'))
        self.assertFalse(hasattr(forms.DateInput, '_has_changed'))
        self.assertFalse(hasattr(forms.DateTimeInput, '_has_changed'))
        self.assertFalse(hasattr(forms.TimeInput, '_has_changed'))

    def test_has_changed_logic_with_localized_values(self):
        '''
        See: https://code.djangoproject.com/ticket/16612
        '''
        with translation.override('de-de'):
            form = RegistrationForm({'height': '1,89'},
                                    initial={'height': Decimal('1.89')})
            self.assertFalse(form.has_changed())

    if django.VERSION < (1, 6):
        test_has_changed_logic_with_localized_values = expectedFailure(
            test_has_changed_logic_with_localized_values)
