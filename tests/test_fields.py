import django
import decimal
from datetime import datetime
from django.test import TestCase

import floppyforms.__future__ as forms

from .compat import unittest
from .models import ImageFieldModel


skipIf = unittest.skipIf


class ImageFieldModelForm(forms.ModelForm):
    class Meta:
        model = ImageFieldModel
        fields = ('image_field',)


class DateTimeFieldTests(TestCase):
    def test_parse_datetime(self):
        field = forms.DateTimeField()
        result = field.clean('2000-01-01')
        self.assertEqual(result, datetime(2000, 1, 1))

    def test_data_is_being_parsed(self):
        class SampleForm(forms.Form):
            datetime_field = forms.DateTimeField()

        form = SampleForm({'datetime_field': '2099-12-31'})
        form.full_clean()
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data['datetime_field'],
            datetime(2099, 12, 31))


class FloatFieldTests(TestCase):
    def test_parse(self):
        float_field = forms.FloatField()
        result = float_field.clean('1.5')
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.5)

    def test_pass_values(self):
        class FloatForm(forms.Form):
            no_options = forms.FloatField()
            min_value = forms.FloatField(min_value=1.234)
            step_attr = forms.FloatField(widget=forms.NumberInput(attrs={
                'step': '0.01'
            }))

        rendered = str(FloatForm()['no_options'])
        self.assertHTMLEqual(rendered, """
            <input type="number" name="no_options" id="id_no_options"
                step="any" required>
        """)
        rendered = str(FloatForm()['min_value'])
        self.assertHTMLEqual(rendered, """
            <input type="number" name="min_value" id="id_min_value"
                min="1.234" step="any" required>
        """)
        rendered = str(FloatForm()['step_attr'])
        self.assertHTMLEqual(rendered, """
            <input type="number" name="step_attr" id="id_step_attr"
                step="0.01" required>
        """)


class IntegerFieldTests(TestCase):
    def test_parse_int(self):
        int_field = forms.IntegerField()
        result = int_field.clean('15')
        self.assertEqual(15, result)
        self.assertIsInstance(result, int)

    def test_pass_values(self):
        class IntForm(forms.Form):
            num = forms.IntegerField(max_value=10)
            other = forms.IntegerField()
            third = forms.IntegerField(min_value=10, max_value=150)

        rendered = IntForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input type="number" name="num" id="id_num" max="10" required>
        </p>
        <p>
            <label for="id_other">Other:</label>
            <input type="number" name="other" id="id_other" required>
        </p>
        <p>
            <label for="id_third">Third:</label>
            <input type="number" name="third" id="id_third" min="10" max="150" required>
        </p>""")


class DecimalFieldTests(TestCase):
    def test_parse_decimal(self):
        decimal_field = forms.DecimalField(decimal_places=2)
        result = decimal_field.clean('1.5')
        self.assertEqual(decimal.Decimal('1.5'), result)
        self.assertIsInstance(result, decimal.Decimal)

    def test_pass_values(self):
        class DecimalForm(forms.Form):
            num = forms.DecimalField(decimal_places=2, max_value=10.5)
            other = forms.DecimalField(decimal_places=1)
            third = forms.DecimalField(decimal_places=3, min_value=-10, max_value=15)

        rendered = DecimalForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input type="number" name="num" id="id_num" max="10.5" step="0.01" required>
        </p>
        <p>
            <label for="id_other">Other:</label>
            <input type="number" name="other" id="id_other" step="0.1" required>
        </p>
        <p>
            <label for="id_third">Third:</label>
            <input type="number" name="third" id="id_third" min="-10" max="15" step="0.001" required>
        </p>""")


class ImageFieldTests(TestCase):
    @skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
    def test_model_field_set_to_none(self):
        # ``models.ImageField``s return a file object with no associated file.
        # These objects raise errors if you try to access the url etc. So we
        # test here that this does not raise any errors.
        # See: https://github.com/gregmuellegger/django-floppyforms/issues/128
        instance = ImageFieldModel.objects.create(image_field=None)
        form = ImageFieldModelForm(instance=instance)
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
            <p>
            <label for="id_image_field">Image field:</label>
            <input id="id_image_field" name="image_field" type="file" />
            </p>""")

        context = form.fields['image_field'].widget.get_context(
            name='image_field',
            value=instance.image_field,
            attrs={})
        self.assertEqual(context['value'], None)


class MultipleChoiceFieldTests(TestCase):
    def test_as_hidden(self):
        some_choices = (
            ('foo', 'bar'),
            ('baz', 'meh'),
            ('heh', 'what?!'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(choices=some_choices)

        rendered = MultiForm(data={'multi': ['heh', 'foo']})['multi'].as_hidden()
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="multi" value="heh" id="id_multi_0">
        <input type="hidden" name="multi" value="foo" id="id_multi_1">
        """)
