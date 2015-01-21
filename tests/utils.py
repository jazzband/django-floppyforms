from django.test import TestCase
from django import forms

from floppyforms.utils import make_floppy
import floppyforms.__future__ as floppyforms

from .models import Registration

import warnings

class MyForm(forms.Form):
    name = forms.CharField()

class MyModelForm(forms.ModelForm):
    class Meta:
        model = Registration

class MyFloppyForm(floppyforms.Form):
    name = floppyforms.CharField()


class MakeFloppyTestCase(TestCase):

    def test_make_basic_form_floppy(self):

        NewClass = make_floppy(MyForm)

        new_form = NewClass()

        self.assertIsInstance(new_form, floppyforms.Form)

    def test_make_model_form_floppy(self):

        NewClass = make_floppy(MyModelForm)

        new_form = NewClass()

        self.assertIsInstance(new_form, floppyforms.ModelForm)

    def test_try_make_existing_floppyform_floppy(self):

        with warnings.catch_warnings(record=True) as w:

            make_floppy(MyFloppyForm)

            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[-1].category(), RuntimeWarning)
