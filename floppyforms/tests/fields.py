from .base import FloppyFormsTestCase

import floppyforms as forms


class IntegerFieldTests(FloppyFormsTestCase):
    def test_parse_int(self):
        int_field = forms.IntegerField()
        result = int_field.clean('15')
        self.assertEqual(15, result)
        self.assertIsInstance(result, int)
