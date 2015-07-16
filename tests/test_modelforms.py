import django
from django.db import models
from django.test import TestCase
from django.utils.encoding import python_2_unicode_compatible

import floppyforms.__future__ as forms
from floppyforms.__future__.models import modelform_factory, modelformset_factory, inlineformset_factory

from .compat import unittest
from .models import Registration, AllFields


skipIf = unittest.skipIf


@python_2_unicode_compatible
class SomeModel2(models.Model):
    some_field = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.some_field


class BaseModelFormFieldRewritingTests(object):
    '''
    A base class to mixin generic tests to check if the form fields on a
    modelform where set correctly to their floppyformic brother.

    A subclass must implement the ``get_test_object``, ``check_field`` and ``check_widget`` methods.
    '''

    def test_auto_boolean(self):
        form_obj = self.get_test_object('boolean')
        self.check_field(form_obj, 'boolean', forms.BooleanField)

    def test_auto_char(self):
        form_obj = self.get_test_object('char')
        self.check_field(form_obj, 'char', forms.CharField)

    def test_auto_comma_separated(self):
        form_obj = self.get_test_object('comma_separated')
        self.check_field(form_obj, 'comma_separated', forms.CharField)

    def test_auto_date(self):
        form_obj = self.get_test_object('date')
        self.check_field(form_obj, 'date', forms.DateField)

    def test_auto_datetime(self):
        form_obj = self.get_test_object('datetime')
        self.check_field(form_obj, 'datetime', forms.DateTimeField)

    def test_auto_decimal(self):
        form_obj = self.get_test_object('decimal')
        self.check_field(form_obj, 'decimal', forms.DecimalField)

    def test_auto_email(self):
        form_obj = self.get_test_object('email')
        self.check_field(form_obj, 'email', forms.EmailField)

    def test_auto_file_path(self):
        form_obj = self.get_test_object('file_path')
        self.check_field(form_obj, 'file_path', forms.FilePathField)

    def test_auto_float_field(self):
        form_obj = self.get_test_object('float_field')
        self.check_field(form_obj, 'float_field', forms.FloatField)

    def test_auto_integer(self):
        form_obj = self.get_test_object('integer')
        self.check_field(form_obj, 'integer', forms.IntegerField)

    def test_auto_big_integer(self):
        form_obj = self.get_test_object('big_integer')
        self.check_field(form_obj, 'big_integer', forms.IntegerField)

    @skipIf(django.VERSION >= (1, 8), 'IPAddressField is deprecated with Django >= 1.8')
    def test_auto_ip_address(self):
        form_obj = self.get_test_object('ip_address')
        self.check_field(form_obj, 'ip_address', forms.IPAddressField)

    def test_auto_generic_ip_address(self):
        form_obj = self.get_test_object('generic_ip_address')
        self.check_field(form_obj, 'generic_ip_address', forms.GenericIPAddressField)

    def test_auto_null_boolean(self):
        form_obj = self.get_test_object('null_boolean')
        self.check_field(form_obj, 'null_boolean', forms.NullBooleanField)

    def test_auto_positive_integer(self):
        form_obj = self.get_test_object('positive_integer')
        self.check_field(form_obj, 'positive_integer', forms.IntegerField)

    def test_auto_positive_small_integer(self):
        form_obj = self.get_test_object('positive_small_integer')
        self.check_field(form_obj, 'positive_small_integer', forms.IntegerField)

    def test_auto_slug(self):
        form_obj = self.get_test_object('slug')
        self.check_field(form_obj, 'slug', forms.SlugField)

    def test_auto_small_integer(self):
        form_obj = self.get_test_object('small_integer')
        self.check_field(form_obj, 'small_integer', forms.IntegerField)

    def test_auto_text(self):
        form_obj = self.get_test_object('text')
        self.check_field(form_obj, 'text', forms.CharField)
        self.check_widget(form_obj, 'text', forms.Textarea)

    def test_auto_time(self):
        form_obj = self.get_test_object('time')
        self.check_field(form_obj, 'time', forms.TimeField)

    def test_auto_url(self):
        form_obj = self.get_test_object('url')
        self.check_field(form_obj, 'url', forms.URLField)

    def test_auto_file_field(self):
        form_obj = self.get_test_object('file_field')
        self.check_field(form_obj, 'file_field', forms.FileField)

    def test_auto_image(self):
        form_obj = self.get_test_object('image')
        self.check_field(form_obj, 'image', forms.ImageField)

    def test_auto_fk(self):
        form_obj = self.get_test_object('fk')
        self.check_field(form_obj, 'fk', forms.ModelChoiceField)

    def test_auto_m2m(self):
        form_obj = self.get_test_object('m2m')
        self.check_field(form_obj, 'm2m', forms.ModelMultipleChoiceField)

    def test_auto_one(self):
        form_obj = self.get_test_object('one')
        self.check_field(form_obj, 'one', forms.ModelChoiceField)

    def test_auto_choices(self):
        form_obj = self.get_test_object('choices')
        self.check_field(form_obj, 'choices', forms.TypedChoiceField)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class ModelFormTests(BaseModelFormFieldRewritingTests, TestCase):
    def get_test_object(self, field_name):
        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = (field_name,)
        return Form

    def check_field(self, Form, field_name, field_class):
        self.assertIsInstance(Form.base_fields[field_name], field_class)

    def check_widget(self, Form, field_name, widget_class):
        self.assertIsInstance(Form.base_fields[field_name].widget, widget_class)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class ModelFormFactoryTests(BaseModelFormFieldRewritingTests, TestCase):
    def get_test_object(self, field_name):
        return modelform_factory(AllFields, form=forms.ModelForm,
            fields=(field_name,))

    def check_field(self, Form, field_name, field_class):
        self.assertIsInstance(Form.base_fields[field_name], field_class)

    def check_widget(self, Form, field_name, widget_class):
        self.assertIsInstance(Form.base_fields[field_name].widget, widget_class)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class ModelFormSetFactoryTests(BaseModelFormFieldRewritingTests, TestCase):
    def get_test_object(self, field_name):
        return modelformset_factory(
            AllFields,
            form=forms.ModelForm,
            fields=(field_name,))

    def check_field(self, Formset, field_name, field_class):
        self.assertIsInstance(Formset.form.base_fields[field_name], field_class)

    def check_widget(self, Formset, field_name, widget_class):
        self.assertIsInstance(Formset.form.base_fields[field_name].widget, widget_class)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class InlineFormSetFactoryTests(BaseModelFormFieldRewritingTests, TestCase):
    def get_test_object(self, field_name):
        return inlineformset_factory(
            Registration,
            AllFields,
            fk_name='fk',
            form=forms.ModelForm,
            fields=(field_name,))

    def check_field(self, Formset, field_name, field_class):
        self.assertIsInstance(Formset.form.base_fields[field_name], field_class)

    def check_widget(self, Formset, field_name, widget_class):
        self.assertIsInstance(Formset.form.base_fields[field_name].widget, widget_class)


class ModelMultipleChoiceFieldTests(TestCase):
    def test_model_choice_field(self):
        """ModelChoiceField and ModelMultipleChoiceField"""
        SomeModel2.objects.create(some_field='Meh')
        SomeModel2.objects.create(some_field='Bah')

        class MultiModelForm(forms.Form):
            mods = forms.ModelMultipleChoiceField(queryset=SomeModel2.objects.all())

        rendered = MultiModelForm(data={'mods': [1, 2]})['mods'].as_hidden()
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="mods" value="1" id="id_mods_0">
        <input type="hidden" name="mods" value="2" id="id_mods_1">
        """)
