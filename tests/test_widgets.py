import datetime
import decimal
import os
import sys

import django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.dates import MONTHS
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now

import floppyforms as forms

from .base import InvalidVariable
from .compat import force_str
from .compat import unittest


skipIf = unittest.skipIf
skipUnless = unittest.skipUnless


@python_2_unicode_compatible
class SomeModel(models.Model):
    some_field = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.some_field


class WidgetRenderingTest(TestCase):
    """Testing the rendering of the different widgets."""
    maxDiff = None

    def test_text_input(self):
        """<input type="text">"""
        class TextForm(forms.Form):
            text = forms.CharField(label='My text field')

        rendered = TextForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">My text field:</label>
            <input type="text" name="text" id="id_text" required>
        </p>""")

        form = TextForm(data={'text': ''})
        self.assertFalse(form.is_valid())

        form = TextForm(data={'text': 'some text'})
        self.assertTrue(form.is_valid())

        class TextForm(forms.Form):
            text = forms.CharField(required=False)

        rendered = TextForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input type="text" name="text" id="id_text">
        </p>""")

        class TextForm(forms.Form):
            text = forms.CharField(
                widget=forms.TextInput(attrs={'placeholder': 'Heheheh'})
            )

        rendered = TextForm(initial={'text': 'some initial text'}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input type="text" name="text" id="id_text" value="some initial text" placeholder="Heheheh" required>
        </p>""")

        invalid = lambda: forms.CharField(max_length=5).clean('foo bar')
        self.assertRaises(forms.ValidationError, invalid)

        class TextForm(forms.Form):
            text = forms.CharField(max_length=2)

        self.assertFalse(TextForm(data={'text': 'foo'}).is_valid())

        # Bug #7 - values should be passed as unicode strings
        rendered = TextForm(data={'text': 0}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input type="text" name="text" id="id_text" value="0" required maxlength="2">
        </p>""")

    def test_password(self):
        """<input type="password">"""
        class PwForm(forms.Form):
            pw = forms.CharField(widget=forms.PasswordInput)

        rendered = PwForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_pw">Pw:</label>
            <input type="password" name="pw" id="id_pw" required>
        </p>""")

        class PwForm(forms.Form):
            text = forms.CharField()
            pw = forms.CharField(widget=forms.PasswordInput)

        form = PwForm(data={'pw': 'some-pwd'})
        self.assertFalse(form.is_valid())  # missing text
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_text">Text:</label>
            <input type="text" name="text" id="id_text" required>
        </p>
        <p>
            <label for="id_pw">Pw:</label>
            <input type="password" name="pw" id="id_pw" required>
        </p>""")

        class PwForm(forms.Form):
            text = forms.CharField()
            pw = forms.CharField(
                widget=forms.PasswordInput(render_value=True)
            )

        form = PwForm(data={'pw': 'some-pwd'})
        self.assertFalse(form.is_valid())  # missing text
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_text">Text:</label>
            <input type="text" name="text" id="id_text" required>
        </p>
        <p>
            <label for="id_pw">Pw:</label>
            <input type="password" name="pw" id="id_pw" required value="some-pwd">
        </p>""")

    def test_hidden(self):
        """<input type="hidden">"""
        class HiddenForm(forms.Form):
            hide = forms.CharField(widget=forms.HiddenInput())

        rendered = HiddenForm().as_p()
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="hide" id="id_hide" required>
        """)

        form = HiddenForm(data={'hide': 'what for?'})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="hide" id="id_hide" required value="what for?">
        """)

    def test_textarea(self):
        """<textarea>"""

        class TextForm(forms.Form):
            text = forms.CharField(widget=forms.Textarea)

        rendered = TextForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <textarea name="text" id="id_text" cols="40" rows="10" required></textarea>
        </p>
        """)

        class TextForm(forms.Form):
            text = forms.CharField(
                widget=forms.Textarea(attrs={'rows': 42, 'cols': 55})
            )

        rendered = TextForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <textarea name="text" id="id_text" rows="42" cols="55" required></textarea>
        </p>
        """)

    def test_file(self):
        """"<input type="file">"""
        class FileForm(forms.Form):
            file_ = forms.FileField()

        rendered = FileForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            <input type="file" name="file_" id="id_file_" required>
        </p>
        """)

        class FileForm(forms.Form):
            file_ = forms.FileField(required=False)

        rendered = FileForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            <input type="file" name="file_" id="id_file_">
        </p>
        """)

    def test_date(self):
        """<input type="date">"""
        class DateForm(forms.Form):
            date = forms.DateField()

        rendered = DateForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_date">Date:</label>
            <input type="date" name="date" id="id_date" required>
        </p>
        """)

    def test_datetime(self):
        """<input type="datetime">"""
        class DateTimeForm(forms.Form):
            date = forms.DateTimeField()

        rendered = DateTimeForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_date">Date:</label>
            <input type="datetime" name="date" id="id_date" required>
        </p>
        """)

    def test_time(self):
        """<input type="time">"""
        class TimeForm(forms.Form):
            date = forms.TimeField()

        rendered = TimeForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_date">Date:</label>
            <input type="time" name="date" id="id_date" required>
        </p>
        """)

    @override_settings(LANGUAGE_CODE='sl', USE_I18n=True)
    def test_date_with_locale(self):
        """<input type="date">"""
        class DateForm(forms.Form):
            date = forms.DateField(initial=datetime.date(2014, 1, 31))

        rendered = DateForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_date">Date:</label>
            <input type="date" value="2014-01-31" name="date" id="id_date" required>
        </p>
        """)

    def test_search(self):
        """<input type="search">"""
        class SearchForm(forms.Form):
            query = forms.CharField(widget=forms.SearchInput)

        rendered = SearchForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_query">Query:</label>
            <input type="search" name="query" id="id_query" required>
        </p>
        """)

    def test_email(self):
        """<input type="email">"""
        class EmailForm(forms.Form):
            email = forms.EmailField()

        rendered = EmailForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_email">Email:</label>
            <input type="email" name="email" id="id_email" required>
        </p>
        """)

        form = EmailForm(data={'email': 'foo@bar.com'})
        self.assertTrue(form.is_valid())
        form = EmailForm(data={'email': 'lol'})
        self.assertFalse(form.is_valid())

    def test_url(self):
        """<input type="url">"""
        class URLForm(forms.Form):
            url = forms.URLField()

        rendered = URLForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_url">Url:</label>
            <input type="url" name="url" id="id_url" required>
        </p>
        """)

        form = URLForm(data={'url': 'http://example.com'})
        self.assertTrue(form.is_valid())
        form = URLForm(data={'url': 'com'})
        self.assertFalse(form.is_valid())

    def test_color(self):
        """<input type="color">"""
        class ColorForm(forms.Form):
            color = forms.CharField(widget=forms.ColorInput)

        rendered = ColorForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_color">Color:</label>
            <input type="color" name="color" id="id_color" required>
        </p>
        """)

    def test_number(self):
        """<input type="number">"""
        class NumberForm(forms.Form):
            num = forms.DecimalField()

        rendered = NumberForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input type="number" name="num" id="id_num" required>
        </p>
        """)

        form = NumberForm(data={'num': 10})
        self.assertTrue(form.is_valid())
        form = NumberForm(data={'num': 'meh'})
        self.assertFalse(form.is_valid())

        class NumberForm(forms.Form):
            num = forms.DecimalField(
                widget=forms.NumberInput(attrs={'min': 5, 'max': 10})
            )

        rendered = NumberForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input type="number" name="num" id="id_num" required min="5" max="10">
        </p>
        """)

        class NumInput(forms.NumberInput):
            min = 9
            max = 99
            step = 10

        class NumberForm(forms.Form):
            num = forms.DecimalField(widget=NumInput)

        rendered = NumberForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input type="number" name="num" id="id_num" required min="9" max="99" step="10">
        </p>
        """)

        class NumberForm(forms.Form):
            num = forms.DecimalField(widget=NumInput(attrs={'step': 12}))
        rendered = NumberForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_num">Num:</label>
            <input type="number" name="num" id="id_num" required min="9" max="99" step="12">
        </p>
        """)

    def test_range(self):
        """<input type="range">"""
        class RangeForm(forms.Form):
            range_ = forms.DecimalField(widget=forms.RangeInput)

        rendered = RangeForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_range_">Range :</label>
            <input type="range" name="range_" id="id_range_" required>
        </p>
        """)

    def test_phone(self):
        """<input type="tel">"""
        class PhoneForm(forms.Form):
            tel = forms.CharField(widget=forms.PhoneNumberInput)

        rendered = PhoneForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_tel">Tel:</label>
            <input type="tel" name="tel" id="id_tel" required>
        </p>
        """)

    def test_checkbox(self):
        """<input type="checkbox">"""
        class CBForm(forms.Form):
            cb = forms.BooleanField()

        rendered = CBForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" required>
        </p>
        """)

        form = CBForm(data={'cb': False})
        self.assertFalse(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" required>
        </p>
        """)

        form = CBForm(data={'cb': 1})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" required checked>
        </p>
        """)

        form = CBForm(data={'cb': True})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" required checked>
        </p>
        """)

        form = CBForm(data={'cb': 'on'})
        self.assertTrue(form.is_valid())
        rendered = form.as_p()

        # The behaviour of the value attribute changed with Django 1.5. Prior
        # it was included as given in ``data``. Now it's always excluded as the
        # value is casted to a bool. See #167 for more details.
        if django.VERSION < (1, 5):
            self.assertHTMLEqual(rendered, """
            <p>
                <label for="id_cb">Cb:</label>
                <input type="checkbox" name="cb" id="id_cb" required checked value="on">
            </p>
            """)
        else:
            self.assertHTMLEqual(rendered, """
            <p>
                <label for="id_cb">Cb:</label>
                <input type="checkbox" name="cb" id="id_cb" required checked>
            </p>
            """)

    @skipUnless(sys.version_info[0] < 3, 'Only applies to Python 2')
    def test_checkbox_string_values(self):
        class CBForm(forms.Form):
            cb = forms.BooleanField()

        form = CBForm(data={'cb': unicode('False')})
        self.assertFalse(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" required>
        </p>
        """)

        form = CBForm(data={'cb': 'False'})
        self.assertFalse(form.is_valid())
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li>This field is required.</li>
        </ul>
        <p>
            <label for="id_cb">Cb:</label>
            <input type="checkbox" name="cb" id="id_cb" required>
        </p>
        """)

    def test_select(self):
        """<select>"""
        CHOICES = (
            ('en', 'English'),
            ('de', 'Deutsch'),
        )

        class SelectForm(forms.Form):
            select = forms.ChoiceField(choices=CHOICES)

        rendered = SelectForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_select">Select:</label>
            <select name="select" id="id_select" required>
                <option value="en">English</option>
                <option value="de">Deutsch</option>
            </select>
        </p>
        """)

        rendered = SelectForm(initial={'select': 'en'}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_select">Select:</label>
            <select name="select" id="id_select" required>
                <option value="en" selected>English</option>
                <option value="de">Deutsch</option>
            </select>
        </p>
        """)

    def test_nbselect(self):
        """NullBooleanSelect"""
        class NBForm(forms.Form):
            nb = forms.NullBooleanField()

        rendered = NBForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_nb">Nb:</label>
            <select name="nb" id="id_nb" required>
                <option value="1" selected>Unknown</option>
                <option value="2">Yes</option>
                <option value="3">No</option>
            </select>
        </p>
        """)

        rendered = NBForm(data={'nb': True}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_nb">Nb:</label>
            <select name="nb" id="id_nb" required>
                <option value="1">Unknown</option>
                <option value="2" selected>Yes</option>
                <option value="3">No</option>
            </select>
        </p>
        """)

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
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select name="multi" id="id_multi" required multiple>
                <option value="en">English</option>
                <option value="de">Deutsch</option>
                <option value="fr">Francais</option>
            </select>
        </p>
        """)

        rendered = MultiForm(data={'multi': ['fr', 'en']}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select name="multi" id="id_multi" required multiple>
                <option value="en" selected>English</option>
                <option value="de">Deutsch</option>
                <option value="fr" selected>Francais</option>
            </select>
        </p>
        """)

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
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select name="multi" id="id_multi" required multiple>
                <option value="1">English</option>
                <option value="12">Deutsch</option>
                <option value="123">Francais</option>
            </select>
        </p>
        """)

        rendered = MultiForm(data={'multi': ['123']}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <select name="multi" id="id_multi" required multiple>
                <option value="1">English</option>
                <option value="12">Deutsch</option>
                <option value="123" selected>Francais</option>
            </select>
        </p>
        """)

    def test_optgroup(self):
        """<optgroup> in select widgets"""
        CHOICES = (
            (None, (
                ('en', 'English'),
                ('de', 'Deutsch'),
                ('fr', 'Francais'),
            )),
            ("Asian", (
                ('jp', 'Japanese'),
                ('bn', 'Bengali'),
            )),
        )

        class LangForm(forms.Form):
            lang = forms.ChoiceField(choices=CHOICES)

        rendered = LangForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_lang">Lang:</label>
            <select name="lang" id="id_lang" required>
                <option value="en">English</option>
                <option value="de">Deutsch</option>
                <option value="fr">Francais</option>
                <optgroup label="Asian">
                    <option value="jp">Japanese</option>
                    <option value="bn">Bengali</option>
                </optgroup>
            </select>
        </p>""")

        rendered = LangForm(data={'lang': 'jp'}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_lang">Lang:</label>
            <select name="lang" id="id_lang" required>
                <option value="en">English</option>
                <option value="de">Deutsch</option>
                <option value="fr">Francais</option>
                <optgroup label="Asian">
                    <option value="jp" selected>Japanese</option>
                    <option value="bn">Bengali</option>
                </optgroup>
            </select>
        </p>""")

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
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <ul>
                <li><label for="id_multi_1"><input type="checkbox" id="id_multi_1" name="multi" value="en">English</label></li>
                <li><label for="id_multi_2"><input type="checkbox" id="id_multi_2" name="multi" value="de">Deutsch</label></li>
                <li><label for="id_multi_3"><input type="checkbox" id="id_multi_3" name="multi" value="fr">Francais</label></li>
            </ul>
        </p>
        """)
        rendered = MultiForm(data={'multi': ['fr', 'en']}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_multi">Multi:</label>
            <ul>
                <li><label for="id_multi_1"><input type="checkbox" id="id_multi_1" name="multi" value="en" checked>English</label></li>
                <li><label for="id_multi_2"><input type="checkbox" id="id_multi_2" name="multi" value="de">Deutsch</label></li>
                <li><label for="id_multi_3"><input type="checkbox" id="id_multi_3" name="multi" value="fr" checked>Francais</label></li>
            </ul>
        </p>
        """)

    def test_checkbox_select_multiple_with_iterable_initial(self):
        """Passing iterable objects to initial data, not only lists or tuples.
        This is useful for ValuesQuerySet for instance."""
        choices = (
            ('en', 'En'),
            ('fr', 'Fr'),
            ('de', 'De'),
        )

        class iterable_choices(object):
            def __init__(self, choices):
                self.choices = choices

            def __iter__(self):
                for choice in self.choices:
                    yield choice

            def __len__(self):
                return len(self.choices)

        class Form(forms.Form):
            key = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple,
                choices=choices,
            )

        form = Form(initial={'key': iterable_choices(['fr', 'en'])})
        self.assertHTMLEqual(form.as_p(), """
            <p><label for="id_key">Key:</label><ul>
                <li><label for="id_key_1"><input id="id_key_1" name="key" type="checkbox" value="en" checked="checked">En</label></li>
                <li><label for="id_key_2"><input id="id_key_2" name="key" type="checkbox" value="fr" checked="checked">Fr</label></li>
                <li><label for="id_key_3"><input id="id_key_3" name="key" type="checkbox" value="de">De</label></li>
            </ul></p>
        """)

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
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_radio">Radio:</label>
            <ul>
                <li><label for="id_radio_1"><input type="radio" name="radio" id="id_radio_1" value="en" required>English</label></li>
                <li><label for="id_radio_2"><input type="radio" name="radio" id="id_radio_2" value="de" required>Deutsch</label></li>
                <li><label for="id_radio_3"><input type="radio" name="radio" id="id_radio_3" value="fr" required>Francais</label></li>
            </ul>
        </p>""")

        rendered = RadioForm(data={'radio': 'fr'}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_radio">Radio:</label>
            <ul>
                <li><label for="id_radio_1"><input type="radio" name="radio" id="id_radio_1" value="en" required>English</label></li>
                <li><label for="id_radio_2"><input type="radio" name="radio" id="id_radio_2" value="de" required>Deutsch</label></li>
                <li><label for="id_radio_3"><input type="radio" name="radio" id="id_radio_3" value="fr" required checked>Francais</label></li>
            </ul>
        </p>""")

    def test_slug(self):
        """<input type="text" pattern="[-\w]+">"""
        class SlugForm(forms.Form):
            slug = forms.SlugField()

        rendered = SlugForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_slug">Slug:</label>
            <input type="text" name="slug" id="id_slug" pattern="[-\w]+" required>
        </p>""")
        self.assertFalse(SlugForm(data={'slug': '123 foo'}).is_valid())
        self.assertTrue(SlugForm(data={'slug': '123-foo'}).is_valid())

    def test_regex(self):
        """<input type="text" pattern="...">"""
        class RegexForm(forms.Form):
            re_field = forms.RegexField(r'^\d{3}-[a-z]+$',
                                        '\d{3}-[a-z]+')
            re_field_ = forms.RegexField(r'^[a-z]{2}$')

        rendered = RegexForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_re_field">Re field:</label>
            <input type="text" name="re_field" id="id_re_field" pattern="\d{3}-[a-z]+" required>
        </p><p>
            <label for="id_re_field_">Re field :</label>
            <input type="text" name="re_field_" id="id_re_field_" required>
        </p>""")

        self.assertFalse(RegexForm(data={'re_field': 'meh',
                                         're_field_': 'fr'}).is_valid())
        self.assertTrue(RegexForm(data={'re_field': '123-python',
                                        're_field_': 'fr'}).is_valid())

    @skipIf(django.VERSION >= (1, 8), 'IPAddressField is deprecated with Django >= 1.8')
    def test_ip_address(self):
        """<input pattern="<IPv4 re>">"""
        class IPv4Form(forms.Form):
            ip = forms.IPAddressField()

        rendered = IPv4Form().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_ip">Ip:</label>
            <input type="text" name="ip" pattern="%s" id="id_ip" required>
        </p>""" % forms.IPAddressInput.ip_pattern)

        self.assertFalse(IPv4Form(data={'ip': '500.500.1.1'}).is_valid())
        self.assertTrue(IPv4Form(data={'ip': '250.100.1.8'}).is_valid())

    def test_generic_ip_address(self):
        """<input type=text>"""
        class GenericIPForm(forms.Form):
            ip = forms.GenericIPAddressField()

        with self.assertTemplateUsed('floppyforms/input.html'):
            rendered = GenericIPForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_ip">Ip:</label>
            <input type="text" name="ip" id="id_ip" required>
        </p>""")

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
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_typed">Typed:</label>
            <select name="typed" id="id_typed" required>
                <option value="0">Some value</option>
                <option value="1">Other value</option>
                <option value="2">A third one</option>
            </select>
        </p>""")

        form = TypedForm(data={'typed': '0'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['typed'], False)

    def test_file_path_field(self):
        """foo = forms.FilePathField()"""
        parent = os.path.dirname(os.path.abspath(__file__))

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
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_thing">Thing:</label>
            <select name="thing" id="id_thing" required multiple>
                <option value="0">Some value</option>
                <option value="1">Other value</option>
                <option value="2">A third one</option>
            </select>
        </p>""")

    def test_model_choice_field(self):
        """ModelChoiceField and ModelMultipleChoiceField"""
        SomeModel.objects.create(some_field='Meh')
        SomeModel.objects.create(some_field='Bah')

        class ModelChoiceForm(forms.Form):
            mod = forms.ModelChoiceField(queryset=SomeModel.objects.all())

        rendered = ModelChoiceForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mod">Mod:</label>
            <select name="mod" id="id_mod" required>
                <option value="">---------</option>
                <option value="1">Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")

        rendered = ModelChoiceForm(data={'mod': 1}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mod">Mod:</label>
            <select name="mod" id="id_mod" required>
                <option value="">---------</option>
                <option value="1" selected>Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")

        class MultiModelForm(forms.Form):
            mods = forms.ModelMultipleChoiceField(queryset=SomeModel.objects.all())

        rendered = MultiModelForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mods">Mods:</label>
            <select name="mods" id="id_mods" required multiple>
                <option value="1">Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")
        rendered = MultiModelForm(data={'mods': [1]}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_mods">Mods:</label>
            <select name="mods" id="id_mods" required multiple>
                <option value="1" selected>Meh</option>
                <option value="2">Bah</option>
            </select>
        </p>""")

    def test_combo_field(self):
        """Combo field"""
        class ComboForm(forms.Form):
            combo = forms.ComboField(fields=[forms.EmailField(),
                                             forms.CharField(max_length=10)])

        rendered = ComboForm().as_p()
        self.assertTrue(' required ' in rendered, rendered)
        self.assertFalse(ComboForm(data={'combo': 'bob@exmpl.com'}).is_valid())
        self.assertTrue(ComboForm(data={'combo': 'bob@ex.com'}).is_valid())

    def test_split_datetime(self):
        """Split date time widget"""
        class SplitForm(forms.Form):
            split = forms.SplitDateTimeField()

        rendered = SplitForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_split_0">Split:</label>
            <input type="date" name="split_0" required id="id_split_0">
            <input type="time" name="split_1" required id="id_split_1">
        </p>""")

        class SplitForm(forms.Form):
            split = forms.SplitDateTimeField(required=False)

        rendered = SplitForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_split_0">Split:</label>
            <input type="date" name="split_0" id="id_split_0">
            <input type="time" name="split_1" id="id_split_1">
        </p>""")

        valid = {'split_0': '2011-02-06', 'split_1': '12:12'}
        self.assertTrue(SplitForm(data=valid).is_valid())

        invalid = {'split_0': '2011-02-06', 'split_1': ''}
        self.assertFalse(SplitForm(data=invalid).is_valid())

        class SplitForm(forms.Form):
            split = forms.SplitDateTimeField(
                widget=forms.SplitHiddenDateTimeWidget,
            )

        rendered = SplitForm().as_p()
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="split_0" required id="id_split_0">
        <input type="hidden" name="split_1" required id="id_split_1">
        """)

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
        self.assertHTMLEqual(rendered, """
        <input type="hidden" name="multi" value="heh" required id="id_multi_0">
        <input type="hidden" name="multi" value="foo" required id="id_multi_1">
        """)

    def test_datetime_with_initial(self):
        """SplitDateTimeWidget with an initial value"""
        value = now()

        class DateTimeForm(forms.Form):
            dt = forms.DateTimeField(initial=value,
                                     widget=forms.SplitDateTimeWidget)

        rendered = DateTimeForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_dt_0">Dt:</label>
            <input type="date" name="dt_0" value="%s" id="id_dt_0">
            <input type="time" name="dt_1" value="%s" id="id_dt_1">
        </p>""" % (value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")))

    def test_select_date_widget(self):
        """SelectDateWidget"""
        today = datetime.date.today()

        class SelectDateForm(forms.Form):
            dt = forms.DateField(initial=today,
                                 widget=forms.SelectDateWidget)

        rendered = SelectDateForm().as_p()
        option_year = ('<option value="%(year)d" selected="selected">'
                       '%(year)d</option>') % {'year': today.year}
        self.assertTrue(option_year in rendered, rendered)

        option_month = ('<option value="%d" selected="selected">%s'
                        '</option>') % (
                            today.month,
                            force_str(MONTHS[today.month]))
        self.assertTrue(option_month in rendered, rendered)

        option_day = ('<option value="%(day)d" selected="selected">%(day)d'
                      '</option>') % {'day': today.day}
        self.assertTrue(option_day in rendered, rendered)

        self.assertFalse(' id="id_dt"' in rendered, rendered)

        self.assertTrue(' id="id_dt_year"' in rendered, rendered)
        self.assertTrue(' id="id_dt_month"' in rendered, rendered)
        self.assertTrue(' id="id_dt_day"' in rendered, rendered)
        self.assertEqual(rendered.count('<option value="0">---</option>'), 0)

        class SelectDateForm(forms.Form):
            dt = forms.DateField(initial='%s-09-09' % today.year,
                                 widget=forms.SelectDateWidget)
        rendered = SelectDateForm().as_p()
        self.assertTrue(str(today.year) in rendered, rendered)
        self.assertEqual(rendered.count('<option value="0">---</option>'), 0)

        class SelectDateForm(forms.Form):
            dt = forms.DateField(widget=forms.SelectDateWidget(required=False))
        rendered = SelectDateForm().as_p()
        self.assertEqual(rendered.count('<option value="0">---</option>'), 3)

    def test_no_attrs_rendering(self):
        widget = forms.TextInput()
        try:
            rendered = widget.render('name', 'value')
            self.assertEqual(
                rendered,
                '<input type="text" name="name" value="value">\n',
            )
        except AttributeError:
            self.fail("Rendering with no attrs should work")

    def test_required_select(self):
        """The 'required' attribute on the Select widget"""
        choices = (('foo', 'foo'),
                   ('bar', 'bar'))

        class SelectForm(forms.Form):
            foo = forms.CharField(widget=forms.Select(choices=choices))

        rendered = SelectForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_foo">Foo:</label>
            <select name="foo" required id="id_foo">
                <option value="foo">foo</option>
                <option value="bar">bar</option>
            </select>
        </p>""")

        class SelectForm(forms.Form):
            foo = forms.CharField(widget=forms.Select(choices=choices),
                                  required=False)

        rendered = SelectForm().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_foo">Foo:</label>
            <select name="foo" id="id_foo">
                <option value="foo">foo</option>
                <option value="bar">bar</option>
            </select>
        </p>""")

    def test_clearable_file_input(self):
        class Form(forms.Form):
            file_ = forms.FileField(required=False)

        fake_instance = {'url': 'test test'}
        rendered = Form(initial={'file_': fake_instance}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            Currently: <a target="_blank" href="test test">{&#39;url&#39;: &#39;test test&#39;}</a>
            <input type="checkbox" name="file_-clear" id="file_-clear_id">
            <label for="file_-clear_id">Clear</label><br>Change:
            <input type="file" name="file_" id="id_file_">
        </p>""")

        form = Form(initial={'file_': fake_instance},
                    data={'file_-clear': True})
        self.assertTrue(form.is_valid())
        # file_ has been cleared
        self.assertFalse(form.cleaned_data['file_'])

    def test_clearable_file_input_with_none_value(self):
        class Form(forms.Form):
            file_ = forms.FileField(required=False)

        rendered = Form(initial={'file_': None}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            <input type="file" name="file_" id="id_file_">
        </p>""")

    def test_clearable_file_input_with_custom_labels(self):
        class MyFileInput(forms.ClearableFileInput):
            initial_text = 'INITIAL_TEXT'
            input_text = 'INPUT_TEXT'
            clear_checkbox_label = 'CLEAR_CHECKBOX_LABEL'

        class Form(forms.Form):
            file_ = forms.FileField(required=False, widget=MyFileInput)

        fake_instance = {'url': 'test test'}
        rendered = Form(initial={'file_': fake_instance}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            INITIAL_TEXT: <a target="_blank" href="test test">{&#39;url&#39;: &#39;test test&#39;}</a>
            <input type="checkbox" name="file_-clear" id="file_-clear_id">
            <label for="file_-clear_id">CLEAR_CHECKBOX_LABEL</label><br>INPUT_TEXT:
            <input type="file" name="file_" id="id_file_">
        </p>""")

        form = Form(initial={'file_': fake_instance},
                    data={'file_-clear': True})
        self.assertTrue(form.is_valid())
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_file_">File :</label>
            INITIAL_TEXT: <a target="_blank" href="test test">{&#39;url&#39;: &#39;test test&#39;}</a>
            <input type="checkbox" name="file_-clear" id="file_-clear_id">
            <label for="file_-clear_id">CLEAR_CHECKBOX_LABEL</label><br>INPUT_TEXT:
            <input type="file" name="file_" id="id_file_">
        </p>""")

    def test_rendered_file_input(self):
        class Form(forms.Form):
            file_ = forms.FileField()

            def clean_file_(self):
                raise forms.ValidationError('Some error')

        file_ = SimpleUploadedFile('name', b'some contents')

        form = Form(files={'file_': file_})
        valid = form.is_valid()
        self.assertFalse(valid)
        rendered = form.as_p()
        self.assertHTMLEqual(rendered, """
        <ul class="errorlist">
            <li>Some error</li>
        </ul>
        <p>
            <label for="id_file_">File :</label>
            <input type="file" name="file_" id="id_file_" required>
        </p>""")

    def test_true_attr(self):
        """widgets with attrs={'foo': True} should render as <input foo>"""
        class Form(forms.Form):
            text = forms.CharField(widget=forms.TextInput(attrs={
                'foo': True,
                'bar': False,
            }))

        rendered = Form().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_text">Text:</label>
            <input type="text" foo bar="False" id="id_text" name="text" required>
        </p>""")

    def test_range_input(self):
        class Form(forms.Form):
            foo = forms.CharField(widget=forms.RangeInput(attrs={
                'min': 1, 'max': 10, 'step': 1, 'bar': 1.0
            }))

        rendered = Form(initial={'foo': 5}).as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_foo">Foo:</label>
            <input type="range" name="foo" value="5" required max="10" step="1" bar="1.0" id="id_foo" min="1">
        </p>""")

    def test_datalist(self):
        class Form(forms.Form):
            foo = forms.CharField(widget=forms.TextInput(
                datalist=['Foo', 'Bar', 'Baz'],
            ))

        rendered = Form().as_p()
        self.assertHTMLEqual(rendered, """
        <p>
            <label for="id_foo">Foo:</label>
            <input type="text" name="foo" required id="id_foo" list="id_foo_list">
            <datalist id="id_foo_list">
                <option value="Foo">
                <option value="Bar">
                <option value="Baz">
            </datalist>
        </p>""")

    def test_specify_template_at_init(self):
        """Can customize the template used when instantiating the widget."""
        widget = forms.TextInput(template_name='custom.html')

        rendered = widget.render('text', 'value')
        self.assertHTMLEqual(rendered, '<input type="custom" name="text" />')

    def test_specify_template_at_init_as_None(self):
        """Can give an explicit template_name=None without overriding."""
        widget = forms.TextInput(template_name=None)

        self.assertIsNot(widget.template_name, None)

    def test_specify_template_in_render(self):
        """Can customize the template used at render time."""
        widget = forms.TextInput()

        rendered = widget.render('text', 'value', template_name='custom.html')
        self.assertHTMLEqual(rendered, '<input type="custom" name="text" />')

        # Can explicitly give None and will not override
        rendered = widget.render('text', 'value', template_name=None)
        self.assertHTMLEqual(
            rendered, '<input type="text" name="text" value="value" />')


class WidgetRenderingTestWithTemplateStringIfInvalidSet(WidgetRenderingTest):
    pass

WidgetRenderingTestWithTemplateStringIfInvalidSet = override_settings(TEMPLATE_STRING_IF_INVALID=InvalidVariable('INVALID'))(WidgetRenderingTestWithTemplateStringIfInvalidSet)


class WidgetContextTests(TestCase):
    def test_widget_render_method_should_not_clutter_the_context(self):
        '''
        Make sure that the widget rendering pops the context as often as it
        pushed onto it. Otherwise this would lead to leaking variables into
        outer scopes.

        See issue #43 for more information.
        '''
        context = Context({
            'one': 1,
        })
        context_levels = len(context.dicts)
        widget = forms.TextInput()
        widget.context_instance = context
        widget.render('text', '')
        self.assertEqual(len(context.dicts), context_levels)

    def test_widget_should_not_clutter_the_context(self):
        class TextForm(forms.Form):
            text = forms.CharField(label='My text field')
        context = Context({
            'form': TextForm(),
        })
        context_levels = len(context.dicts)
        rendered = Template('''
            {% load floppyforms %}
            {% form form using %}
                {% formrow form.text with label="Textfield" %}
                {% formrow form.text %}
            {% endform %}
        ''').render(context)
        self.assertEqual(len(context.dicts), context_levels)
        self.assertHTMLEqual(rendered, '''
            <p>
                <label for="id_text">Textfield:</label>
                <input type="text" name="text" id="id_text" required />
            </p>
            <p>
                <label for="id_text">My text field:</label>
                <input type="text" name="text" id="id_text" required />
            </p>
        ''')


class AttrsTemplateTests(TestCase):
    def render_attrs(self, attrs):
        return render_to_string('floppyforms/attrs.html', {
            'attrs': attrs,
        })

    def test_attrs_with_one_item(self):
        rendered = self.render_attrs({
            'name': 'fieldname'
        })
        self.assertEqual(rendered, ' name="fieldname"')

    def test_attrs_with_value_is_true(self):
        rendered = self.render_attrs({
            'required': True
        })
        self.assertEqual(rendered, ' required')

    def test_attrs_with_value_is_one(self):
        '''
        Regression test for #88.
        '''
        rendered = self.render_attrs({
            'value': True
        })
        self.assertEqual(rendered, ' value')
        rendered = self.render_attrs({
            'value': 1
        })
        self.assertEqual(rendered, ' value="1"')
        rendered = self.render_attrs({
            'value': False
        })
        self.assertEqual(rendered, ' value="False"')

    def test_attrs_with_multiple_values(self):
        rendered = self.render_attrs({
            'required': True,
            'format': 'dd.mm.yyyy',
        })
        # We cannot predict the ordering...
        self.assertTrue(rendered in [
            ' required format="dd.mm.yyyy"',
            ' format="dd.mm.yyyy" required',
        ])

        rendered = self.render_attrs({
            'value': 'Hello World',
            'id': 'id_name',
            'name': 'name',
            'disabled': True,
        })
        self.assertTrue(' value="Hello World"' in rendered)
        self.assertTrue(' id="id_name"' in rendered)
        self.assertTrue(' name="name"' in rendered)

        # disabled shouldn't have a value
        self.assertTrue(' disabled' in rendered)
        self.assertTrue(' disabled=' not in rendered)

    def test_attrs_not_localized(self):

        # We should got 0.01, not 0,01.
        with override_settings(USE_L10N=True, LANGUAGE_CODE='fr-fr'):
            rendered = self.render_attrs({'step': decimal.Decimal('0.01')})
            self.assertTrue(rendered in [
                ' step="0.01"',
            ])
