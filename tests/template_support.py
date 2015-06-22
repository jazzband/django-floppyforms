"""
Tests related about integrating with other template libraries.
"""

from django.test import TestCase
from django.template import Context
from django.template import Template
import floppyforms as forms
from floppyforms.widgets import TextInput


class ForeignInclusionTagInWidgetTests(TestCase):
    def test_inclusion_tag_in_widget_template(self):
        widget = TextInput(template_name='widget_with_inclusion_tag.html')
        rendered = widget.render('field', 'value')
        self.assertTrue('take this' in rendered)

    def test_inclusion_tag_in_form_tag(self):
        widget = TextInput(template_name='widget_with_inclusion_tag.html')

        class InclusionTagForm(forms.Form):
            field = forms.CharField(widget=widget)

        form = InclusionTagForm()
        template = Template('{% load floppyforms %}{% form form %}')
        rendered = template.render(Context({'form': form}))
        self.assertTrue('take this' in rendered)
