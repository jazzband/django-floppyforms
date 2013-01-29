from django.test import TestCase

import floppyforms as forms


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
