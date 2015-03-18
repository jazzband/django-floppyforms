from django.test import TestCase

import floppyforms as forms

from floppyforms import widgets
from floppyforms.templatetags.floppyforms import ConfigFilter, FormConfig


class AgeField(forms.IntegerField):
    pass


class RegistrationForm(forms.Form):
    name = forms.CharField(label='First- and Lastname', max_length=50)
    email = forms.EmailField(max_length=50,
                             help_text='Please enter a valid email.')
    age = AgeField()
    short_biography = forms.CharField(max_length=200)
    comment = forms.CharField(widget=widgets.Textarea)


class FormConfigTests(TestCase):
    def test_default_retrieve(self):
        """
        Test if FormConfig returns the correct default values if no
        configuration was made.
        """
        form = RegistrationForm()
        config = FormConfig()

        # retrieve widget

        widget = config.retrieve('widget', bound_field=form['name'])
        self.assertTrue(isinstance(widget, widgets.TextInput))
        self.assertEqual(widget, form.fields['name'].widget)

        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertTrue(isinstance(widget, widgets.Textarea))
        self.assertEqual(widget, form.fields['comment'].widget)

        # retrieve widget template

        template_name = config.retrieve('widget_template', bound_field=form['name'])
        self.assertEqual(template_name, 'floppyforms/text.html')

        template_name = config.retrieve('widget_template', bound_field=form['comment'])
        self.assertEqual(template_name, 'floppyforms/textarea.html')

        # retrieve label

        label = config.retrieve('label', bound_field=form['email'])
        self.assertEqual(label, 'Email')

        label = config.retrieve('label', bound_field=form['name'])
        self.assertEqual(label, 'First- and Lastname')

        # retrieve help text

        help_text = config.retrieve('help_text', bound_field=form['name'])
        self.assertFalse(help_text)

        help_text = config.retrieve('help_text', bound_field=form['email'])
        self.assertEqual(help_text, 'Please enter a valid email.')

        # retrieve row template

        template = config.retrieve('row_template', fields=(form['name'], form['email'],))
        self.assertEqual(template, 'floppyforms/rows/default.html')

        # retrieve form layout

        template = config.retrieve('layout', forms=(form,))
        self.assertEqual(template, 'floppyforms/layouts/default.html')

    def test_configure_and_retrieve(self):
        form = RegistrationForm()

        config = FormConfig()
        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertEqual(widget.__class__, widgets.Textarea)

        config.configure('widget', widgets.TextInput(), filter=ConfigFilter('comment'))

        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertEqual(widget.__class__, widgets.TextInput)

        widget = config.retrieve('widget', bound_field=form['name'])
        self.assertEqual(widget.__class__, widgets.TextInput)

    def test_retrieve_for_multiple_valid_values(self):
        form = RegistrationForm()
        config = FormConfig()

        config.configure(
            'widget', widgets.Textarea(),
            filter=ConfigFilter('CharField'),
        )
        config.configure(
            'widget', widgets.HiddenInput(),
            filter=ConfigFilter('short_biography'),
        )

        widget = config.retrieve('widget', bound_field=form['name'])
        self.assertEqual(widget.__class__, widgets.Textarea)
        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertEqual(widget.__class__, widgets.Textarea)

        # we get HiddenInput since this was configured last, even the Textarea
        # config applies to ``short_biography``
        widget = config.retrieve('widget', bound_field=form['short_biography'])
        self.assertEqual(widget.__class__, widgets.HiddenInput)

    def test_filter_for_field_class_name(self):
        form = RegistrationForm()

        config = FormConfig()
        config.configure('widget', widgets.TextInput(), filter=ConfigFilter('CharField'))

        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertEqual(widget.__class__, widgets.TextInput)

        widget = config.retrieve('widget', bound_field=form['name'])
        self.assertEqual(widget.__class__, widgets.TextInput)

    def test_filter_for_widget_class_name(self):
        form = RegistrationForm()

        config = FormConfig()
        config.configure('widget', widgets.TextInput(), filter=ConfigFilter('Textarea'))

        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertEqual(widget.__class__, widgets.TextInput)

        widget = config.retrieve('widget', bound_field=form['name'])
        self.assertEqual(widget.__class__, widgets.TextInput)

        # swap widgets TextInput <> Textarea

        config = FormConfig()
        config.configure('widget', widgets.Textarea(), filter=ConfigFilter('TextInput'))
        config.configure('widget', widgets.TextInput(), filter=ConfigFilter('Textarea'))

        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertEqual(widget.__class__, widgets.TextInput)

        widget = config.retrieve('widget', bound_field=form['name'])
        self.assertEqual(widget.__class__, widgets.Textarea)

    def test_filter_for_name_object(self):
        form = RegistrationForm()

        config = FormConfig()
        config.configure('widget', widgets.Textarea(), filter=ConfigFilter('object'))

        widget = config.retrieve('widget', bound_field=form['email'])
        self.assertEqual(widget.__class__, widgets.EmailInput)

        widget = config.retrieve('widget', bound_field=form['name'])
        self.assertEqual(widget.__class__, widgets.TextInput)

        widget = config.retrieve('widget', bound_field=form['comment'])
        self.assertEqual(widget.__class__, widgets.Textarea)

    def test_stacked_config(self):
        form = RegistrationForm()
        config = FormConfig()

        config.push()
        config.configure(
            'widget', widgets.Textarea(),
            filter=ConfigFilter("CharField"),
        )

        config.push()
        config.configure(
            'widget', widgets.HiddenInput(),
            filter=ConfigFilter('short_biography'),
        )

        widget = config.retrieve('widget', bound_field=form['short_biography'])
        self.assertEqual(widget.__class__, widgets.HiddenInput)

        config.pop()
        widget = config.retrieve('widget', bound_field=form['short_biography'])
        self.assertEqual(widget.__class__, widgets.Textarea)

        config.pop()
        widget = config.retrieve('widget', bound_field=form['short_biography'])
        self.assertEqual(widget.__class__, widgets.TextInput)

    def test_field_filter_works_on_subclasses(self):
        form = RegistrationForm()
        config = FormConfig()

        config.configure(
            'widget', widgets.HiddenInput(),
            filter=ConfigFilter("IntegerField"),
        )

        widget = config.retrieve('widget', bound_field=form['age'])
        self.assertEqual(widget.__class__, widgets.HiddenInput)

    def test_retrieve_all(self):
        config = FormConfig()

        config.configure('number', 1)
        config.configure('number', 2)
        self.assertEqual(list(config.retrieve_all('number')), [2, 1])

        config.configure('number', 4, filter=lambda nr=None, **kwargs: nr == 'four')
        self.assertEqual(list(config.retrieve_all('number')), [2, 1])
        self.assertEqual(list(config.retrieve_all('number', nr='four')), [4, 2, 1])

        config.push()
        config.configure('number', 5, filter=lambda nr=None, **kwargs: nr == 'five')
        self.assertEqual(list(config.retrieve_all('number')), [2, 1])
        self.assertEqual(list(config.retrieve_all('number', nr='five')), [5, 2, 1])

        config.configure('number', -1)
        self.assertEqual(list(config.retrieve_all('number')), [-1, 2, 1])
        self.assertEqual(list(config.retrieve_all('number', nr='four')), [-1, 4, 2, 1])
        self.assertEqual(list(config.retrieve_all('number', nr='five')), [-1, 5, 2, 1])

        config.pop()
        self.assertEqual(list(config.retrieve_all('number')), [2, 1])
        self.assertEqual(list(config.retrieve_all('number', nr='four')), [4, 2, 1])
        self.assertEqual(list(config.retrieve_all('number', nr='five')), [2, 1])
