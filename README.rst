Django-floppyforms
==================

Full control of form rendering in the templates.

* Author: Bruno Renié
* Licence: BSD
* Compatibility: Django 1.2+ (smart *if* template tag needed)
* Requirements: homework -- read `this`_.

.. _this: http://diveintohtml5.org/forms.html

Installation
------------

* ``pip install -e git+git://github.com/brutasse/django-floppyforms.git#egg=floppyforms``
* Add ``floppyforms`` to your ``INSTALLED_APPS``

Usage
-----

Forms
`````

FloppyForms are supposed to work just like Django forms::

    import floppyforms as forms

    class FlopForm(forms.Form):
        name = forms.CharField()
        email = forms.EmailField()
        url = forms.URLField()

With some template code::

    <form method="post" action="/some-action/">
        {% csrf_token %}
        {{ form.as_p }}
        <p><input type="submit" value="Yay!" /></p>
    </form>

Each field has a default widget and widgets are rendered using a template.
Each widget is rendered using an isolated context containing all the relevant
information.

Default templates are provided and their output is relatively similar to
Django widgets, with a few minor differences:

* HTML5 ``<input>`` types are supported: ``url``, ``email``, ``date``,
  ``datetime``, ``time``, ``number``, ``range``, ``search``, ``color``,
  ``tel``.

* The ``required`` and ``placeholder`` attributes are also supported.

Widgets are rendered with the following context variables:

* ``hidden``: set to ``True`` if the field is hidden.
* ``required``: set to ``True`` if the field is required.
* ``type``: the input type. Can be ``text``, ``password``, etc. etc.
* ``name``: the name of the input.
* ``id``: the if of the input.

Each widget has a ``template_name`` attribute which points to the template to
use when rendering the widget. A basic template for an ``<input>`` widget may
look like::

    <input id="{{ id }}"
           type="{{ type }}"
           name="{{ name }}"
           {% if value %}value="{{ value }}"{% endif %} />

The default FloppyForms template for an ``<input>`` widget is slightly more
complex.

Some widgets may provide extra context variables:

============== ===============================
Widget         Extra context
============== ===============================
Textarea       ``rows``, ``cols``
NumberInput    ``min``, ``max``,  ``step``
RangeInput     ``min``, ``max``, ``step``
SelectMultiple ``multiple`` is set to ``True``
============== ===============================

Furthermore, the ``attrs`` dictionary is added to the template context. For
instance, with a field created this way::

    bar = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'john@example.com'}))

Then the ``placeholder`` variable is available in the template context.

ModelForms
``````````

With ``ModelForms``, you need to override the widgets to pick FloppyForms'
widgets. Say we have a ``Flop`` model::

    class Flop(models.Model):
        name = models.CharField(max_length=255)
        url = models.URLField()

Creating a ``ModelForm`` with widgets from FloppyForms is easy::

    import floppyforms as forms

    class FlopForm(forms.ModelForm):
        class Meta:
            model = Flop
            widgets = {
                'name': forms.TextInput,
                'url': forms.URLInput,
            }

Widget reference
----------------

The first column represents the name of a django.forms field. FloppyForms aims
to implement all the Django fields with the same class name, in the
``floppyforms`` namespace. Some widgets are missing but you can safely use the
widgets from ``django.forms`` if you need them.

======================== ================
Fields                   Widgets
======================== ================
BooleanField             CheckboxInput
CharField                TextInput
ChoiceField              Select
TypedChoiceField         Not implemented
DateField                DateInput
DateTimeField            DateTimeInput
DecimalField             NumberInput
EmailField               EmailInput
FileField                FileInput
FilePathField            Not implemented
FloatField               NumberInput
ImageField               Not implemented
IntegerField             NumberInput
IPAddressField           Not implemented
MultipleChoiceField      SelectMultiple
NullBooleanField         NullBooleanInput
RegexField               Not implemented
SlugField                Not implemented
TimeField                TimeInput
URLField                 URLInput
ComboField               Not implemented
MultiValueField          Not implemented
SplitDateTimeField       Not implemented
ModelChoiceField         Not implemented
ModelMultipleChoiceField Not implemented
======================== ================

Customization
-------------

The first way of customizing a widget is to define a custom template::

    import floppyforms as forms

    class GenericEmailInput(forms.EmailInput):
        template_name = 'path/to/generic_email.html'

Then, the output can be customized in ``generic_email.html``::

    <input type="email"
           name="{{ name }}"
           id="{{ id }}"
           placeholder="john@example.com"
           {% if value %}value="{{ value }}"{% endif %} />

Here we have a generic placeholder without needing to instantiate the widget
with an ``attrs`` dictionary::

    class EmailForm(forms.Form):
        email = forms.EmailField(widget=GenericEmailInput())

There is also a way to add extra context. This is done by subclassing the
widget class an extending the ``get_extra_context()`` method::


    class OtheEmailInput(forms.EmailInput):
        template_name = 'path/to/other.html'

        def get_extra_context(self):
            ctx = super(OtheEmailInput, self).get_extra_context()
            ctx['foo'] = 'bar'
            return ctx

And then the ``other.html`` template can make use of the ``{{ bar }}`` context
variable.

Bugs
----

Really? Oh well... Please Report. Or better, fix :)
