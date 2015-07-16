import warnings

import django.forms
from django.test import TestCase

import floppyforms as forms
from .models import Registration


class ModelFormDeprecationTests(TestCase):
    def test_model_form_is_deprecated(self):
        class RegistrationModelForm(forms.ModelForm):
            class Meta:
                model = Registration
                fields = (
                    'firstname',
                    'lastname',
                    'username',
                    'age',
                )

        with warnings.catch_warnings(record=True) as w:
            modelform = RegistrationModelForm()
            self.assertEqual(len(w), 1)
            self.assertTrue(w[0].category is FutureWarning)

        self.assertFalse(isinstance(modelform.base_fields['firstname'], forms.CharField))
        self.assertIsInstance(modelform.base_fields['firstname'], django.forms.CharField)
