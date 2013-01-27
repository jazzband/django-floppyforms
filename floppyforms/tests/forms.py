from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import six
from django.utils.translation import ugettext_lazy as _

import floppyforms as forms

from .models import Registration


class RegistrationForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    firstname = forms.CharField(label=_(u'Your first name?'))
    lastname = forms.CharField(label=_(u'Your last name:'))
    username = forms.CharField(max_length=30)
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text=_(u'Make sure to use a secure password.'),
    )
    password2 = forms.CharField(label=_(u'Retype password'), widget=forms.PasswordInput)
    age = forms.IntegerField(required=False)

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise ValidationError(u'Haha, you trapped into the honeypot.')
        return self.cleaned_data['honeypot']

    def clean(self):
        if self.errors:
            raise ValidationError(u'Please correct the errors below.')


class RegistrationModelForm(forms.ModelForm):
    class Meta:
        model = Registration


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
