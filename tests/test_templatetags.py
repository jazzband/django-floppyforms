import django
from django.forms import TextInput
from django.forms.formsets import formset_factory
from django.template import Context, Template, TemplateSyntaxError
from django.test import TestCase

import floppyforms as forms
from floppyforms.templatetags.floppyforms import (FormConfig, ConfigFilter,
                                                  FormNode, RowModifier,
                                                  FieldModifier)


_TEMPLATE_PREAMBLE = '{% load floppyforms %}'
if (1, 6) <= django.VERSION <= (1, 7):
    _TEMPLATE_PREAMBLE += '{% load firstof from future %}'
    _TEMPLATE_PREAMBLE += '{% load cycle from future %}'


def render(template, context=None, config=None):
    if context is None:
        context = {}
    if not hasattr(context, 'dicts'):
        context = Context(context)
    if config is not None:
        setattr(context, FormNode.CONFIG_CONTEXT_ATTR, config)
    t = Template(_TEMPLATE_PREAMBLE + template)
    return t.render(context)


def render_in_form(template, context=None):
    template = '{% load floppyforms %}{% form myform using %}' + template + '{% endform %}'
    return render(template, context)


def compile_to_nodelist(template):
    rendered_template = Template(
        '{% load floppyforms %}{% form myform using %}' + template + '{% endform %}')
    form_node = rendered_template.nodelist[1]
    return form_node.options['nodelist'][0]


class SimpleForm(forms.Form):
    name = forms.CharField()


class PersonForm(forms.Form):
    firstname = forms.CharField()
    lastname = forms.CharField()
    age = forms.IntegerField()
    bio = forms.CharField(widget=forms.Textarea)


class HardcodedWidget(forms.Widget):
    def render(self, *args, **kwargs):
        return 'Hardcoded widget.'


class HardcodedForm(forms.Form):
    name = forms.CharField(widget=HardcodedWidget())


class FormConfigNodeTests(TestCase):
    def test_enforce_form_tag(self):
        render('{% form myform using %}{% formconfig row using "my_row_template.html" %}{% endform %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formconfig row using "my_row_template.html" %}')
        render('{% form myform using %}{% formconfig field using "my_row_template.html" %}{% endform %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formconfig field using "my_row_template.html" %}')

    def test_valid_syntax(self):
        render_in_form('{% formconfig row using "my_row_template.html" %}')
        render_in_form('{% formconfig row using "my_row_template.html" with myarg="bar" %}')
        render_in_form('{% formconfig row with myarg="bar" %}')

        render_in_form('{% formconfig field using "field.html" %}')
        render_in_form('{% formconfig field using "field.html" with myarg="bar" %}')
        render_in_form('{% formconfig field with myarg="bar" %}')
        render_in_form('{% formconfig field using "field.html" for "spam" %}')
        render_in_form('{% formconfig field using "field.html" for myvar %}')
        render_in_form('{% formconfig field using template %}')

    def test_invalid_syntax(self):
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig row %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig row myarg="bar" %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig row with %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig row with only %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig row using "my_row_template.html" for "spam" %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig field %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig field myarg="bar" %}')
        with self.assertRaises(TemplateSyntaxError):
            # wrong argument order
            render_in_form('{% formconfig field with myarg="bar" using "field.html" %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig non_existent_modifier %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig non_existent_modifier with option=1 %}')

        # only is not allowed in formconfig
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig row with myarg="bar" only %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig row using "my_row_template.html" only %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig field with myarg="bar" only %}')
        with self.assertRaises(TemplateSyntaxError):
            render_in_form('{% formconfig field using "field.html" only %}')

    def test_row_config(self):
        rowconfig = compile_to_nodelist('{% formconfig row using "my_row_template.html" %}')
        self.assertTrue(isinstance(rowconfig, RowModifier))

        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        rowconfig.render(context)
        self.assertTrue(hasattr(context, '_form_config'))

    def test_row_config_using(self):
        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        node = compile_to_nodelist(
            '{% formconfig row using "my_row_template.html" %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(config.retrieve('row_template'), 'my_row_template.html')

        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        node = compile_to_nodelist('{% formconfig row using empty_var %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(config.retrieve('row_template'), 'floppyforms/rows/default.html')

    def test_row_config_with(self):
        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        node = compile_to_nodelist('{% formconfig row with extra_class="fancy" %}')
        node.render(context)
        config = node.get_config(context)
        extra_context = config.retrieve('row_context')
        self.assertTrue(extra_context)
        self.assertTrue(extra_context['extra_class'], 'fancy')

    def test_field_config(self):
        rowconfig = compile_to_nodelist(
            '{% formconfig field with extra_class="fancy" %}')
        self.assertTrue(isinstance(rowconfig, FieldModifier))

        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        rowconfig.render(context)
        self.assertTrue(hasattr(context, '_form_config'))

    def test_field_config_using(self):
        form = SimpleForm()

        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        node = compile_to_nodelist('{% formconfig field using "field.html" %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['name']),
            'field.html')

        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        node = compile_to_nodelist('{% formconfig field using empty_var %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['name']),
            'floppyforms/text.html')

    def test_field_config_with(self):
        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True})
        node = compile_to_nodelist('{% formconfig field with type="email" %}')
        node.render(context)
        config = node.get_config(context)
        extra_context = config.retrieve('widget_context')
        self.assertTrue(extra_context)
        self.assertTrue(extra_context['type'], 'email')

    def test_field_config_for_bound_field(self):
        form = PersonForm()
        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True, 'form': form})

        node = compile_to_nodelist('{% formconfig field using "field.html" for form.lastname %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['firstname']),
            'floppyforms/text.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['lastname']),
            'field.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['age']),
            'floppyforms/number.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['bio']),
            'floppyforms/textarea.html')

    def test_field_config_for_field_name(self):
        form = PersonForm()
        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True, 'form': form})

        node = compile_to_nodelist('{% formconfig field using "field.html" for "firstname" %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['firstname']),
            'field.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['lastname']),
            'floppyforms/text.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['age']),
            'floppyforms/number.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['bio']),
            'floppyforms/textarea.html')

    def test_field_config_for_field_type(self):
        form = PersonForm()
        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True, 'form': form})

        node = compile_to_nodelist('{% formconfig field using "field.html" for "IntegerField" %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['firstname']),
            'floppyforms/text.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['lastname']),
            'floppyforms/text.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['age']),
            'field.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['bio']),
            'floppyforms/textarea.html')

    def test_field_config_for_widget_type(self):
        form = PersonForm()
        context = Context({FormNode.IN_FORM_CONTEXT_VAR: True, 'form': form})

        node = compile_to_nodelist('{% formconfig field using "field.html" for "Textarea" %}')
        node.render(context)
        config = node.get_config(context)
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['firstname']),
            'floppyforms/text.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['lastname']),
            'floppyforms/text.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['age']),
            'floppyforms/number.html')
        self.assertEqual(
            config.retrieve('widget_template', bound_field=form['bio']),
            'field.html')


class FormTagTests(TestCase):
    def test_valid_syntax(self):
        render('{% form myform %}')
        render('{% form myform using "myform_layout.html" %}')
        render('{% form myform secondform %}')
        render('{% form myform using %}{% endform %}')
        render('{% form myform secondform using %}{% endform %}')
        render('{% form myform secondform thirdform %}')
        render('{% form myform secondform thirdform using "myform_layout.html" with arg=value %}')
        render('{% form myform secondform thirdform using "myform_layout.html" only %}')
        render('{% form myform secondform thirdform using "myform_layout.html" with arg=value only %}')

    def test_invalid_syntax(self):
        with self.assertRaises(TemplateSyntaxError):
            render('{% form %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form using %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform using "myform_layout.html" with %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform using "myform_layout.html" with only %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform using "myform_layout.html" only with arg=value %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form using %}{% endform %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform using "myform_layout.html" too_many_arguments %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform %}{% endform %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform using "myform_layout.html" %}{% endform %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform using "myform_layout.html" only %}{% endform %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% form myform using "myform_layout.html" with arg=value %}{% endform %}')

    def test_inline_content(self):
        self.assertHTMLEqual(
            render('{% form myform using %}foo{% endform %}'), 'foo')
        self.assertHTMLEqual(render("""
            {% form myform using %}
                {% if 1 %}True{% else %}False{% endif %}
            {% endform %}
            """), 'True')
        # don't leak variables into outer scope
        self.assertHTMLEqual(render("""
            {% form myform using %}
                <ins>{% cycle "foo" "bar" as value %}</ins>
            {% endform %}
            <del>{% firstof value "NO VALUE" %}</del>
            """), '<ins>foo</ins><del>NO VALUE</del>')
        # form variable equals the first argument in form tag
        self.assertHTMLEqual(render("""
            {% form myform using %}{% if myform == form %}Equals!{% endif %}{% endform %}
            """, {'myform': SimpleForm()}), 'Equals!')
        self.assertHTMLEqual(render("""
            {% form f1 f2 using %}
                {% if f1 == forms.0 and f2 == forms.1 and f1 != f2 %}
                    Equals!
                {% endif %}
            {% endform %}
            """, {'f1': SimpleForm(), 'f2': SimpleForm()}), 'Equals!')

        # none forms are not included in form list
        self.assertHTMLEqual(
            render("""
            {% form f1 nothing f2 more_of_nothing using %}
                {% if f1 == forms.0 and f2 == forms.1 %}
                {% if forms.2 == None and more_of_nothing == None %}
                    Equals!
                {% endif %}
                {% endif %}
                Length: {{ forms|length }}
            {% endform %}""", {
                'f1': SimpleForm(),  # noqa
                'f2': SimpleForm()
            }), 'Equals! Length: 2')

    def test_include_content(self):
        with self.assertTemplateUsed('simple_form_tag.html'):
            self.assertHTMLEqual(
                render('{% form myform using "simple_form_tag.html" %}', {
                    'myform': PersonForm(),
                }), """
                Forms: 1
                1. Form Fields: firstname lastname age bio
                """)
        with self.assertTemplateUsed('simple_form_tag.html'):
            self.assertHTMLEqual(
                render('{% form f1 non f2 using "simple_form_tag.html" %}', {
                    'f1': SimpleForm(),
                    'f2': PersonForm(),
                }), """
                Forms: 2
                1. Form Fields: name
                2. Form Fields: firstname lastname age bio
                """)

    def test_include_content_with_extra_arguments(self):
        with self.assertTemplateUsed('simple_form_tag.html'):
            self.assertHTMLEqual(
                render('{% form myform using "simple_form_tag.html" with extra_argument="spam" %}', {
                    'myform': PersonForm(),
                }), """
                Forms: 1
                1. Form Fields: firstname lastname age bio
                Extra argument: spam
                """)
        with self.assertTemplateUsed('simple_form_tag.html'):
            self.assertHTMLEqual(
                render('{% form myform using "simple_form_tag.html" with extra_argument=0 %}', {
                    'myform': PersonForm(),
                }), """
                Forms: 1
                1. Form Fields: firstname lastname age bio
                """)
        with self.assertTemplateUsed('simple_form_tag.html'):
            self.assertHTMLEqual(
                render("""
                    {% with extra_argument="ham" %}
                        {% form myform using "simple_form_tag.html" %}
                    {% endwith %}
                    """, {'myform': PersonForm()}),
                """
                Forms: 1
                1. Form Fields: firstname lastname age bio
                Extra argument: ham
                """)
        with self.assertTemplateUsed('simple_form_tag.html'):
            self.assertHTMLEqual(
                render("""
                    {% with extra_argument="ham" %}
                        {% form myform using "simple_form_tag.html" only %}
                    {% endwith %}
                    """, {'myform': PersonForm()}),
                """
                Forms: 1
                1. Form Fields: firstname lastname age bio
                """)
        with self.assertTemplateUsed('simple_form_tag.html'):
            self.assertHTMLEqual(
                render("""
                    {% with extra_argument="spam" %}
                        {% form myform using "simple_form_tag.html" with extra_argument=0 %}
                    {% endwith %}
                    """, {'myform': PersonForm()}),
                """
                Forms: 1
                1. Form Fields: firstname lastname age bio
                """)

    def test_default_template(self):
        with self.assertTemplateUsed('floppyforms/layouts/default.html'):
            render('{% form myform %}')

    def test_form_list_as_argument(self):
        form1 = PersonForm()
        form2 = SimpleForm()
        form_list = [form1, form2, form2]
        self.assertHTMLEqual(
            render('{% form forms using "simple_form_tag.html" %}', {
                'forms': form_list,
            }), """
            Forms: 3
            1. Form Fields: firstname lastname age bio
            2. Form Fields: name
            3. Form Fields: name
            """)

    def test_formset_rendering(self):
        PersonFormSet = formset_factory(PersonForm, extra=3)
        formset = PersonFormSet()
        self.assertHTMLEqual(
            render('{% form formset using "simple_form_tag.html" %}', {
                'formset': formset,
            }), """
            Forms: 3
            1. Form Fields: firstname lastname age bio
            2. Form Fields: firstname lastname age bio
            3. Form Fields: firstname lastname age bio
            """)

        formset = PersonFormSet(initial=[{}, {}])
        self.assertHTMLEqual(
            render('{% form formset using "simple_form_tag.html" %}', {
                'formset': formset,
            }), """
            Forms: 5
            1. Form Fields: firstname lastname age bio
            2. Form Fields: firstname lastname age bio
            3. Form Fields: firstname lastname age bio
            4. Form Fields: firstname lastname age bio
            5. Form Fields: firstname lastname age bio
            """)

    def test_formconfig_gets_popped_after_form_tag(self):
        form = PersonForm()
        rendered = render('''{% form form using %}
            {% formconfig row with extra_argument="first argument" %}
            {% formrow form.firstname using "simple_formrow_tag.html" %}
            {% form form using %}
                {% formconfig row with extra_argument="pop me" %}
                {% formrow form.lastname using "simple_formrow_tag.html" %}
                {% formrow argument|if:forloop.last|else:None %}
            {% endform %}
            {% formrow form.lastname using "simple_formrow_tag.html" %}
        {% endform %}''', {'form': form})
        self.assertHTMLEqual(rendered, '''
        Fields: 1
        1. Field: firstname Extra argument: first argument

        Fields: 1
        1. Field: lastname Extra argument: pop me

        Fields: 1
        1. Field: lastname Extra argument: first argument
        ''')

    def test_formconfig_inside_only(self):
        form = PersonForm()
        rendered = render('''{% form form using "formconfig_inside_only.html" with form=form only  %}''', {'form': form})
        self.assertHTMLEqual(rendered, '''
        Fields: 1
        1. Field: firstname Extra argument: first argument
        ''')


class FormRowTagTests(TestCase):
    def test_valid_syntax(self):
        render('{% formrow myform.field %}')
        render('{% formrow myform.field using "myrow_layout.html" %}')
        render('{% formrow myform.field secondfield %}')
        render('{% formrow myform.field secondfield thirdfield %}')
        render('{% formrow myform.field secondfield thirdfield using "myform_layout.html" with arg=value %}')
        render('{% formrow myform.field secondfield thirdfield using "myform_layout.html" only %}')
        render('{% formrow myform.field secondfield thirdfield using "myform_layout.html" with arg=value only %}')

    def test_invalid_syntax(self):
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow using %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow myform.name using %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow myform.name using "myform_layout.html" with %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow myform.name using "myform_layout.html" with only %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow myform.name using "myform_layout.html" only with arg=value %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow myform.name using "myform_layout.html" too_many_arguments %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow myform.name using %}{% endformrow %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formrow myform.name using %}{% endform %}')

    def test_include_content(self):
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(
                render('{% formrow myform.lastname using "simple_formrow_tag.html" %}', {
                    'myform': PersonForm(),
                }), """
                Fields: 1
                1. Field: lastname
                """)
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(
                render('{% formrow person.age simple.non simple.name using "simple_formrow_tag.html" %}', {
                    'simple': SimpleForm(),
                    'person': PersonForm(),
                }), """
                Fields: 2
                1. Field: age
                2. Field: name
                """)

    def test_include_content_with_extra_arguments(self):
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(
                render('{% formrow myform.firstname using "simple_formrow_tag.html" with extra_argument="spam" %}', {
                    'myform': PersonForm(),
                }), """
                Fields: 1
                1. Field: firstname
                Extra argument: spam
                """)
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(
                render('{% formrow myform.age using "simple_formrow_tag.html" with extra_argument=0 %}', {
                    'myform': PersonForm(),
                }), """
                Fields: 1
                1. Field: age
                """)
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(
                render("""
                    {% with extra_argument="ham" %}
                        {% formrow myform.lastname using "simple_formrow_tag.html" %}
                    {% endwith %}
                    """, {'myform': PersonForm()}),
                """
                Fields: 1
                1. Field: lastname
                Extra argument: ham
                """)
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(
                render("""
                    {% with extra_argument="ham" %}
                        {% formrow myform.firstname using "simple_formrow_tag.html" only %}
                    {% endwith %}
                    """, {'myform': PersonForm()}),
                """
                Fields: 1
                1. Field: firstname
                """)
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(
                render("""
                    {% with extra_argument="spam" %}
                        {% formrow myform.firstname using "simple_formrow_tag.html" with extra_argument=0 %}
                    {% endwith %}
                    """, {'myform': PersonForm()}),
                """
                Fields: 1
                1. Field: firstname
                """)

    def test_default_template(self):
        with self.assertTemplateUsed('floppyforms/rows/default.html'):
            render('{% formrow myform.name %}')

    def test_configure_template(self):
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            render("""{% form myform using %}
                {% formconfig row using "simple_formrow_tag.html" %}
                {% formrow form.name %}
            {% endform %}""")

    def test_configure_template_with_extra_context(self):
        with self.assertTemplateUsed('simple_formrow_tag.html'):
            self.assertHTMLEqual(render("""{% form myform using %}
                {% formconfig row using "simple_formrow_tag.html" %}
                {% formrow form.name with extra_argument="I want ham!" %}
            {% endform %}"""), "Fields: 0 Extra argument: I want ham!")

    def test_configure_extra_context(self):
        self.assertHTMLEqual(render("""{% form myform using %}
            {% formconfig row with extra_argument="I want spam!" %}
            {% formconfig row with extra_argument="I want ham!" %}
            {% formrow form.name using "simple_formrow_tag.html" %}
        {% endform %}"""), "Fields: 0 Extra argument: I want ham!")

        self.assertHTMLEqual(render("""{% form myform using %}
            {% formconfig row using "simple_formrow_tag.html" with extra_argument="I want ham!" %}
            {% formrow form.name %}
        {% endform %}"""), "Fields: 0 Extra argument: I want ham!")

    def test_field_list_as_argument(self):
        form = PersonForm()
        self.assertHTMLEqual(render("""{% form myform using %}
            {% formrow form using "simple_formrow_tag.html" %}
        {% endform %}""", {'myform': form}), """
            Fields: 4
            1. Field: firstname
            2. Field: lastname
            3. Field: age
            4. Field: bio
        """)

        form = PersonForm()
        self.assertHTMLEqual(render("""{% form myform using %}
            {% formrow form.lastname form None form.firstname using "simple_formrow_tag.html" %}
        {% endform %}""", {'myform': form}), """
            Fields: 6
            1. Field: lastname
            2. Field: firstname
            3. Field: lastname
            4. Field: age
            5. Field: bio
            6. Field: firstname
        """)

    def test_formconfig_gets_popped_after_formrow_tag(self):
        '''
        Tests that the form config will be reseted after being set in a
        ``formrow`` tag.
        '''
        form = SimpleForm()
        rendered = render('''{% form form using %}
            {% formconfig row with extra_argument="first argument" %}
            {% formrow form.name using "simple_formrow_tag_with_config.html" %}
            {% formrow form.name using "simple_formrow_tag.html" %}
        {% endform %}''', {'form': form})
        self.assertHTMLEqual(rendered, '''
        Fields: 1
        1. Field: name argument: defined inline
        Extra argument: first argument

        Fields: 1
        1. Field: name
        Extra argument: first argument
        ''')


class FormFieldTagTests(TestCase):
    def test_valid_syntax(self):
        render('{% formfield myform.name %}')

    def test_unvalid_syntax(self):
        with self.assertRaises(TemplateSyntaxError):
            render('{% formfield %}')
        with self.assertRaises(TemplateSyntaxError):
            render('{% formfield myform.firstname myform.lastname %}')

    def test_render_empty_value(self):
        self.assertEqual(render('{% formfield myform.name %}'), '')

    def test_widget_template(self):
        with self.assertTemplateUsed('floppyforms/input.html'):
            render('{% formfield myform.name %}', {'myform': SimpleForm()})
        with self.assertTemplateUsed('simple_formfield_tag.html'):
            render('{% formfield myform.name using "simple_formfield_tag.html" %}', {'myform': SimpleForm()})

    def test_outer_scope(self):
        self.assertHTMLEqual(render("""
            {% with "yepyep" as extra_argument %}
            {% formfield myform.name using "simple_formfield_tag.html" %}
            {% endwith %}
        """, {'myform': SimpleForm()}), 'Type: text Extra argument: yepyep')

    def test_only_option(self):
        self.assertHTMLEqual(render("""
            {% with "yepyep" as extra_argument %}
            {% formfield myform.name using "simple_formfield_tag.html" only %}
            {% endwith %}
        """, {'myform': SimpleForm()}), 'Type: text')

    def test_configure_template_with_extra_context(self):
        form = SimpleForm()
        with self.assertTemplateUsed('simple_formfield_tag.html'):
            self.assertHTMLEqual(
                render("""{% form myform using %}
                {% formconfig field using "simple_formfield_tag.html" %}
                {% formfield form.name with extra_argument="I want bacon!" %}
            {% endform %}""", {'myform': form}),
                "Type: text Extra argument: I want bacon!")

    def test_configure_extra_context(self):
        form = SimpleForm()
        self.assertHTMLEqual(
            render("""{% form myform using %}
            {% formconfig field with extra_argument="I want spam!" %}
            {% formconfig field with extra_argument="I want ham!" %}
            {% formfield form.name using "simple_formfield_tag.html" %}
        {% endform %}""", {'myform': form}),
            "Type: text Extra argument: I want ham!")

        context = Context({'myform': form})
        self.assertHTMLEqual(
            render("""{% form myform using %}
            {% formconfig field using "simple_formfield_tag.html" with extra_argument="I want ham!" %}
            {% formfield form.name %}
        {% endform %}""", context),
            "Type: text Extra argument: I want ham!")

    def test_change_widget(self):
        form = SimpleForm()
        config = FormConfig()
        config.configure('widget', forms.PasswordInput(), filter=ConfigFilter(form['name']))

        self.assertHTMLEqual(render("""{% form myform using %}
            {% formfield form.name %}
        {% endform %}""", {'myform': form}, config), """<input type="password" name="name" id="id_name" />""")

    def test_hardcoded_widget(self):
        form = HardcodedForm()
        self.assertHTMLEqual(render("""{% form myform using %}
            {% formfield form.name %}
        {% endform %}""", {'myform': form}), """Hardcoded widget.""")

    def test_formconfig_gets_popped_after_formfield_tag(self):
        '''
        Tests that the form config will be reseted after being set in a
        ``formfield`` tag.
        '''
        form = SimpleForm()
        rendered = render('''{% form form using %}
            {% formconfig field with extra_argument="first argument" %}
            {% formfield form.name using "extra_argument_with_config.html" with prefix="1." %}
            {% formfield form.name using "extra_argument.html" with prefix="2." %}
        {% endform %}''', {'form': form})
        self.assertHTMLEqual(rendered, '''
        1. argument: first argument
        2. argument: first argument
        ''')


class WidgetTagTest(TestCase):
    def test_widget_tag(self):
        class MediaWidget(forms.TextInput):
            template_name = 'media_widget.html'

        class TestForm(forms.Form):
            test = forms.CharField(widget=MediaWidget)
            test2 = forms.CharField(widget=TextInput)

        self.assertHTMLEqual(render("""
        {% for field in form %}
            {% widget field %}
        {% endfor %}""", {'form': TestForm(), 'STATIC_URL': '/static/'}), """
        <input type="text" name="test" id="id_test" required>
        <script type="text/javascript" src="/static/foo.js"></script>
        <input type="text" name="test2" id="id_test2">""")

        with self.assertRaises(TemplateSyntaxError):
            render("""{% widget %}""")

        with self.assertRaises(TemplateSyntaxError):
            render("""{% widget stuff 12 %}""")
