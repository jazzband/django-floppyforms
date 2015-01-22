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


class MyRegexForm(forms.Form):
    name = forms.RegexField(r'[a-zA-Z]')


class MyField(forms.CharField):
    pass


class MyCustomFieldForm(forms.Form):
    name = MyField()


class MyWidget(forms.TextInput):
    pass


class MyCustomWidgetForm(forms.Form):
    name = forms.CharField(widget=MyWidget())


class OtherClass(object):
    pass


class MakeFloppyTestCase(TestCase):

    def test_make_basic_form_floppy(self):

        NewClass = make_floppy(MyForm)

        new_form = NewClass()

        self.assertIsInstance(new_form, floppyforms.Form)

    def test_make_form_with_arg_floppy(self):

        NewClass = make_floppy(MyRegexForm)

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

    def test_try_to_make_custom_field_floppy(self):

        with warnings.catch_warnings(record=True) as w:

            NewClass = make_floppy(MyCustomFieldForm)

            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[-1].category(), RuntimeWarning)
            self.assertIs(NewClass.base_fields['name'],
                          MyCustomFieldForm.base_fields['name'])

    def test_try_to_make_custom_widget_floppy(self):

        with warnings.catch_warnings(record=True) as w:

            NewClass = make_floppy(MyCustomWidgetForm)

            self.assertEqual(len(w), 1)
            self.assertIsInstance(w[-1].category(), RuntimeWarning)
            self.assertIs(NewClass.base_fields['name'].widget,
                          MyCustomWidgetForm.base_fields['name'].widget)

    def test_try_to_make_instance_floppy(self):

        form = MyForm()

        with self.assertRaises(TypeError):
            make_floppy(form)

    def test_try_to_make_non_form_floppy(self):

        with self.assertRaises(TypeError):
            make_floppy(OtherClass)
