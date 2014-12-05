from datetime import datetime
from django.test import TestCase

import floppyforms as forms


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
