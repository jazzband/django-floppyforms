import datetime
import os

from django.db import models
from django.test import TestCase

import floppyforms as forms
from floppyforms.tests.gis import GisTests


class WidgetRenderingTest(TestCase):
    """Testing the rendering of the different widgets."""

    def test_text_input(self):
        """<input type="text">"""
        class TextForm(forms.Form):
            text = forms.CharField(label='My text field')

        rendered = TextForm().as_p()
        # Checking for ' required ' to make sure it's rendered by floppyforms
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('name="text"' in rendered, rendered)
        self.assertTrue('>My text field:</label>' in rendered, rendered)

        form = TextForm(data={'text': ''})
        self.assertFalse(form.is_valid())

        form = TextForm(data={'text': 'some text'})
        self.assertTrue(form.is_valid())

        class TextForm(forms.Form):
            text = forms.CharField(required=False)

        rendered = TextForm().as_p()
        self.assertFalse(' required ' in rendered, rendered)

        class TextForm(forms.Form):
            text = forms.CharField(
                widget=forms.TextInput(attrs={'placeholder': 'Heheheh'})
            )

        rendered = TextForm(initial={'text': 'some initial text'}).as_p()
        self.assertTrue('placeholder="Heheheh"' in rendered, rendered)
        self.assertTrue('value="some initial text"' in rendered, rendered)

        invalid = lambda: forms.CharField(max_length=5).clean('foo bar')
        self.assertRaises(forms.ValidationError, invalid)

        class TextForm(forms.Form):
            text = forms.CharField(max_length=2)

        self.assertFalse(TextForm(data={'text': 'foo'}).is_valid())

        # Bug #7 - values should be passed as unicode strings
        rendered = TextForm(data={'text': 0}).as_p()
        self.assertTrue(' value="0"' in rendered, rendered)

    def test_password(self):
        """<input type="password">"""
        class PwForm(forms.Form):
            pw = forms.CharField(widget=forms.PasswordInput)

        rendered = PwForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="password"' in rendered, rendered)

        class PwForm(forms.Form):
            text = forms.CharField()
            pw = forms.CharField(widget=forms.PasswordInput)

        form = PwForm(data={'pw': 'some-pwd'})
        self.assertFalse(form.is_valid())  # missing text
        rendered = form.as_p()
        self.assertFalse('some-pwd' in rendered, rendered)

        class PwForm(forms.Form):
            text = forms.CharField()
            pw = forms.CharField(
                widget=forms.PasswordInput(render_value=True)
            )

        form = PwForm(data={'pw': 'some-pwd'})
        self.assertFalse(form.is_valid())  # missing text
        rendered = form.as_p()
        self.assertTrue('some-pwd' in rendered, rendered)

    def test_hidden(self):
        """<input type="hidden">"""
        class HiddenForm(forms.Form):
            hide = forms.CharField(widget=forms.HiddenInput())

        rendered = HiddenForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="hidden"' in rendered, rendered)

        form = HiddenForm(data={'hide': 'what for?'})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertTrue('value="what for?"' in rendered, rendered)

    def test_textarea(self):
        """<textarea>"""

        class TextForm(forms.Form):
            text = forms.CharField(widget=forms.Textarea)

        rendered = TextForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('<textarea ' in rendered, rendered)

        class TextForm(forms.Form):
            text = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 42, 'cols': 55})
            )

        rendered = TextForm().as_p()
        self.assertTrue('rows="42"' in rendered, rendered)
        self.assertTrue('cols="55"' in rendered, rendered)

    def test_file(self):
        """"<input type="file">"""
        class FileForm(forms.Form):
            file_ = forms.FileField()

        rendered = FileForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="file"' in rendered, rendered)

        class FileForm(forms.Form):
            file_ = forms.FileField(required=False)

        rendered = FileForm().as_p()
        self.assertFalse('required' in rendered, rendered)

    def test_date(self):
        """<input type="date">"""
        class DateForm(forms.Form):
            date = forms.DateField()

        rendered = DateForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="date"' in rendered, rendered)

    def test_datetime(self):
        """<input type="datetime">"""
        class DateTimeForm(forms.Form):
            date = forms.DateTimeField()

        rendered = DateTimeForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="datetime"' in rendered, rendered)

    def test_time(self):
        """<input type="time">"""
        class TimeForm(forms.Form):
            date = forms.TimeField()

        rendered = TimeForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="time"' in rendered, rendered)

    def test_search(self):
        """<input type="search">"""
        class SearchForm(forms.Form):
            query = forms.CharField(widget=forms.SearchInput)

        rendered = SearchForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="search"' in rendered, rendered)

    def test_email(self):
        """<input type="email">"""
        class EmailForm(forms.Form):
            email = forms.EmailField()

        rendered = EmailForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="email"' in rendered, rendered)

        form = EmailForm(data={'email': 'foo@bar.com'})
        self.assertTrue(form.is_valid())
        form = EmailForm(data={'email': 'lol'})
        self.assertFalse(form.is_valid())

    def test_url(self):
        """<input type="url">"""
        class URLForm(forms.Form):
            url = forms.URLField()

        rendered = URLForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="url"' in rendered, rendered)

        form = URLForm(data={'url': 'http://example.com'})
        self.assertTrue(form.is_valid())
        form = URLForm(data={'url': 'com'})
        self.assertFalse(form.is_valid())

    def test_color(self):
        """<input type="color">"""
        class ColorForm(forms.Form):
            Color = forms.CharField(widget=forms.ColorInput)

        rendered = ColorForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="color"' in rendered, rendered)

    def test_number(self):
        """<input type="number">"""
        class NumberForm(forms.Form):
            num = forms.DecimalField()

        rendered = NumberForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="number"' in rendered, rendered)

        form = NumberForm(data={'num': 10})
        self.assertTrue(form.is_valid())
        form = NumberForm(data={'num': 'meh'})
        self.assertFalse(form.is_valid())

        class NumberForm(forms.Form):
            num = forms.DecimalField(
                widget=forms.NumberInput(attrs={'min': 5, 'max': 10})
            )

        rendered = NumberForm().as_p()
        self.assertTrue('min="5"' in rendered, rendered)
        self.assertTrue('max="10"' in rendered, rendered)

        class NumInput(forms.NumberInput):
            min = 9
            max = 99
            step = 10

        class NumberForm(forms.Form):
            num = forms.DecimalField(widget=NumInput)

        rendered = NumberForm().as_p()
        self.assertTrue('min="9"' in rendered, rendered)
        self.assertTrue('max="99"' in rendered, rendered)
        self.assertTrue('step="10"' in rendered, rendered)

        class NumberForm(forms.Form):
            num = forms.DecimalField(widget=NumInput(attrs={'step': 12}))
        rendered = NumberForm().as_p()
        self.assertTrue('step="12"' in rendered, rendered)

    def test_range(self):
        """<input type="range">"""
        class RangeForm(forms.Form):
            range_ = forms.DecimalField(widget=forms.RangeInput)

        rendered = RangeForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="range"' in rendered, rendered)

    def test_phone(self):
        """<input type="tel">"""
        class PhoneForm(forms.Form):
            tel = forms.CharField(widget=forms.PhoneNumberInput)

        rendered = PhoneForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="tel"' in rendered, rendered)

    def test_checkbox(self):
        """<input type="checkbox">"""
        class CBForm(forms.Form):
            cb = forms.BooleanField()

        rendered = CBForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="checkbox"' in rendered, rendered)

        form = CBForm(data={'cb': 0})
        self.assertFalse(form.is_valid())
        rendered = form.as_p()
        self.assertFalse('value=' in rendered, rendered)

        form = CBForm(data={'cb': 1})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertFalse('value=' in rendered, rendered)

        form = CBForm(data={'cb': True})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertFalse('value=' in rendered, rendered)

        form = CBForm(data={'cb': 'foo'})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertTrue('value="foo"' in rendered, rendered)

        rendered = CBForm(initial={'cb': True}).as_p()
        self.assertTrue('checked' in rendered, rendered)

    def test_select(self):
        """<select>"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
        )

        class SelectForm(forms.Form):
            select = forms.ChoiceField(choices=CHOICES)

        rendered = SelectForm().as_p()
        self.assertFalse('selected' in rendered, rendered)

        rendered = SelectForm(initial={'select': 'en'}).as_p()
        self.assertTrue('selected' in rendered, rendered)

    def test_nbselect(self):
        """NullBooleanSelect"""
        class NBForm(forms.Form):
            nb = forms.NullBooleanField()

        rendered = NBForm().as_p()
        self.assertTrue('<select ' in rendered, rendered)
        self.assertTrue('value="1" selected' in rendered, rendered)

        rendered = NBForm(data={'nb': True}).as_p()
        self.assertTrue('value="2" selected' in rendered, rendered)

    def test_select_multiple(self):
        """<select multiple>"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
            ('fr', 'Francais'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(choices=CHOICES)

        rendered = MultiForm().as_p()
        self.assertTrue('multiple' in rendered, rendered)

        rendered = MultiForm(data={'multi': ['fr', 'en']}).as_p()
        self.assertTrue('"fr" selected' in rendered, rendered)
        self.assertTrue('"en" selected' in rendered, rendered)


    def test_select_multiple_values(self):
        """<select multiple>"""
        CHOICES = (
            ('1', 'English'),
            ('12', 'Deutsch'),
            ('123', 'Francais'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(choices=CHOICES)

        rendered = MultiForm().as_p()
        self.assertTrue('multiple' in rendered, rendered)

        rendered = MultiForm(data={'multi': ['123']}).as_p()
        self.assertFalse('"1" selected' in rendered, rendered)
        self.assertFalse('"12" selected' in rendered, rendered)
        self.assertTrue('"123" selected' in rendered, rendered)

    def test_cb_multiple(self):
        """CheckboxSelectMultiple"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
            ('fr', 'Francais'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(
                choices=CHOICES,
                widget=forms.CheckboxSelectMultiple,
            )

        rendered = MultiForm().as_p()
        self.assertTrue('checkbox' in rendered, rendered)
        rendered = MultiForm(data={'multi': ['fr', 'en']}).as_p()
        self.assertTrue(len(rendered.split('checked="checked"')), 4)

    def test_radio_select(self):
        """<input type="radio">"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
            ('fr', 'Francais'),
        )

        class RadioForm(forms.Form):
            radio = forms.ChoiceField(
                choices=CHOICES,
                widget=forms.RadioSelect,
            )

        rendered = RadioForm().as_p()
        self.assertTrue(' required>' in rendered, rendered)
        self.assertTrue('type="radio"' in rendered, rendered)
        self.assertFalse('checked' in rendered, rendered)

        rendered = RadioForm(data={'radio': 'fr'}).as_p()
        self.assertTrue('checked> Francais' in rendered, rendered)

    def test_slug(self):
        """<input type="text" pattern="[-\w]+">"""
        class SlugForm(forms.Form):
            slug = forms.SlugField()

        rendered = SlugForm().as_p()
        self.assertTrue(' required' in rendered, rendered)
        self.assertTrue('pattern="[-\w]+"' in rendered, rendered)
        self.assertFalse(SlugForm(data={'slug': '123 foo'}).is_valid())
        self.assertTrue(SlugForm(data={'slug': '123-foo'}).is_valid())

    def test_regex(self):
        """<input type="text" pattern="...">"""
        class RegexForm(forms.Form):
            re_field = forms.RegexField(r'^\d{3}-[a-z]+$',
                                        '\d{3}-[a-z]+')
            re_field_ = forms.RegexField(r'^[a-z]{2}$')

        rendered = RegexForm().as_p()
        self.assertTrue(' required' in rendered, rendered)
        self.assertTrue('pattern="\d{3}-[a-z]+"' in rendered, rendered)

        self.assertFalse(RegexForm(data={'re_field': 'meh',
                                         're_field_': 'fr'}).is_valid())
        self.assertTrue(RegexForm(data={'re_field': '123-python',
                                        're_field_': 'fr'}).is_valid())

    def test_ip_address(self):
        """<input pattern="<IPv4 re>">"""
        class IPv4Form(forms.Form):
            ip = forms.IPAddressField()

        rendered = IPv4Form().as_p()
        self.assertTrue(' required' in rendered, rendered)
        self.assertTrue('pattern="' in rendered, rendered)

        self.assertFalse(IPv4Form(data={'ip': '500.500.1.1'}).is_valid())
        self.assertTrue(IPv4Form(data={'ip': '250.100.1.8'}).is_valid())

    def test_typed_choice_field(self):
        """foo = forms.TypedChoiceField()"""
        TYPE_CHOICES = (
            (0, 'Some value'),
            (1, 'Other value'),
            (2, 'A third one'),
        )
        my_coerce = lambda val: bool(int(val))

        class TypedForm(forms.Form):
            typed = forms.TypedChoiceField(coerce=my_coerce,
                                           choices=TYPE_CHOICES)

        rendered = TypedForm().as_p()
        self.assertTrue('<select ' in rendered, rendered)
        form = TypedForm(data={'typed': '0'})
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['typed'], False)

    def test_file_path_field(self):
        """foo = forms.FilePathField()"""
        parent = os.path.join(os.path.dirname(__file__), '..')

        class PathForm(forms.Form):
            path = forms.FilePathField(path=parent, recursive=True)

        rendered = PathForm().as_p()
        self.assertTrue('<select ' in rendered, rendered)
        self.assertTrue(len(PathForm().fields['path'].choices) > 10)

    def test_typed_multiple_choice(self):
        """foo = forms.TypedMultipleChoiceField()"""
        TYPE_CHOICES = (
            (0, 'Some value'),
            (1, 'Other value'),
            (2, 'A third one'),
        )
        my_coerce = lambda val: bool(int(val))

        class TypedMultiForm(forms.Form):
            thing = forms.TypedMultipleChoiceField(coerce=my_coerce,
                                                   choices=TYPE_CHOICES)

        rendered = TypedMultiForm().as_p()
        self.assertTrue('<select ' in rendered, rendered)
        self.assertTrue(' multiple="multiple"' in rendered, rendered)

    def test_model_choice_field(self):
        """ModelChoiceField and ModelMultipleChoiceField"""

        class SomeModel(models.Model):
            some_field = models.CharField(max_length=255)

            def __unicode__(self):
                return u'%s' % self.some_field

        fake_items = [
            SomeModel(some_field='Meh', pk=1),
            SomeModel(some_field='Bah', pk=2),
        ]

        class HackedQuerySet(models.query.QuerySet):
            """Yield results with no DB"""
            def iterator(self):
                for obj in fake_items:
                    yield obj

            def get(self, *args, **kwargs):
                return fake_items[0]

        queryset = HackedQuerySet(model=SomeModel)

        class ModelChoiceForm(forms.Form):
            mod = forms.ModelChoiceField(queryset=queryset)

        rendered = ModelChoiceForm().as_p()
        self.assertTrue('<option value="1">Meh</option>' in rendered, rendered)

        rendered = ModelChoiceForm(data={'mod': 1}).as_p()
        self.assertTrue('<option value="1" selected' in rendered, rendered)

        class MultiModelForm(forms.Form):
            mods = forms.ModelMultipleChoiceField(queryset=queryset)

        rendered = MultiModelForm().as_p()
        self.assertTrue('<option value="1">Meh</option>' in rendered, rendered)
        self.assertTrue('multiple="multiple"' in rendered, rendered)
        rendered = MultiModelForm(data={'mods': [1]}).as_p()
        self.assertTrue('<option value="1" selected' in rendered, rendered)

    def test_combo_field(self):
        """Combo field"""
        class ComboForm(forms.Form):
            combo = forms.ComboField(fields=[forms.EmailField(),
                                             forms.CharField(max_length=10)])

        rendered = ComboForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        form = ComboForm(data={'combo': 'bob@example.com'})
        f = ComboForm(data={'combo': 'bob@example.com'})
        self.assertFalse(ComboForm(data={'combo': 'bob@exmpl.com'}).is_valid())
        self.assertTrue(ComboForm(data={'combo': 'bob@ex.com'}).is_valid())

    def test_split_datetime(self):
        """Split date time widget"""
        class SplitForm(forms.Form):
            split = forms.SplitDateTimeField()

        rendered = SplitForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue('type="date"' in rendered, rendered)
        self.assertTrue('type="time"' in rendered, rendered)

        class SplitForm(forms.Form):
            split = forms.SplitDateTimeField(required=False)

        rendered = SplitForm().as_p()
        self.assertFalse(' required ' in rendered, rendered)
        self.assertTrue('type="date"' in rendered, rendered)
        self.assertTrue('type="time"' in rendered, rendered)

        valid = {'split_0': '2011-02-06', 'split_1': '12:12'}
        self.assertTrue(SplitForm(data=valid).is_valid())

        invalid = {'split_0': '2011-02-06', 'split_1': ''}
        self.assertFalse(SplitForm(data=invalid).is_valid())

        class SplitForm(forms.Form):
            split = forms.SplitDateTimeField(
                widget=forms.SplitHiddenDateTimeWidget,
            )

        rendered = SplitForm().as_p()
        self.assertEquals(len(rendered.split('type="hidden"')), 3)

    def test_multiple_hidden(self):
        """<input type="hidden"> for fields with a list of values"""

        some_choices = (
            ('foo', 'bar'),
            ('baz', 'meh'),
            ('heh', 'what?!'),
        )

        class MultiForm(forms.Form):
            multi = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput,
                                              choices=some_choices)

        rendered = MultiForm(data={'multi': ['heh', 'foo']}).as_p()
        self.assertEquals(len(rendered.split('type="hidden"')), 3, rendered)
        self.assertTrue(' required ' in rendered, rendered)

    def test_datetime_with_initial(self):
        """SplitDateTimeWidget with an initial value"""
        class DateTimeForm(forms.Form):
            dt = forms.DateTimeField(initial=datetime.datetime.now(),
                                     widget=forms.SplitDateTimeWidget)

        rendered = DateTimeForm().as_p()
        self.assertTrue('value="' in rendered)
