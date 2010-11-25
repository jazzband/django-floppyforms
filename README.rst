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

====================== ============================================
Widget                 Extra context
====================== ============================================
Textarea               ``rows``, ``cols``
NumberInput            ``min``, ``max``,  ``step``
RangeInput             ``min``, ``max``, ``step``
Select                 ``choices``
RadioSelect            ``choices``
NullBooleanSelect      ``choices``
SelectMultiple         ``choices``, ``multiple`` is set to ``True``
CheckboxSelectMultiple ``choices``, ``multiple`` is set to ``True``
====================== ============================================

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

Provided widgets
----------------

Default widgets for form fields
```````````````````````````````

The first column represents the name of a django.forms field. FloppyForms aims
to implement all the Django fields with the same class name, in the
``floppyforms`` namespace. Some widgets are missing but you can safely use the
widgets from ``django.forms`` if you need them.

======================== =================
Fields                   Widgets
======================== =================
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
NullBooleanField         NullBooleanSelect
RegexField               Not implemented
SlugField                Not implemented
TimeField                TimeInput
URLField                 URLInput
ComboField               Not implemented
MultiValueField          Not implemented
SplitDateTimeField       Not implemented
ModelChoiceField         Not implemented
ModelMultipleChoiceField Not implemented
======================== =================

Other widgets
`````````````

Some HTML5 widgets are also provided, although browser support may not be
there yet:

* ``SearchInput``: a widget that renders ``<input type="search">``.
* ``ColorInput``: ``<input type="color">`` (not implemented in any browser
  yet).
* ``RangeInput``: ``<input type="range">``, for sliders instead of spinboxes
  for numbers.
* ``PhoneNumberInput``: ``<input type="tel">``. For phone numbers.

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

You can also override the default templates in your project's templates,
assuming they take precedence on the app-provided templates (this is the
default behaviour).

There is also a way to add extra context. This is done by subclassing the
widget class an extending the ``get_extra_context()`` method::


    class OtheEmailInput(forms.EmailInput):
        template_name = 'path/to/other.html'

        def get_extra_context(self):
            ctx = super(OtheEmailInput, self).get_extra_context()
            ctx['foo'] = 'bar'
            return ctx

And then the ``other.html`` template can make use of the ``{{ foo }}`` context
variable.

Widgets reference
-----------------

For each widgets, the default class attributes.

TextInput
`````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: text

PasswordInput
`````````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: password

HiddenInput
```````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: hidden

FileInput
`````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: file

ClearableFileInput
``````````````````

* ``template_name``: ``'floppyforms/clearable_input.html'``
* ``initial_text``: ``_('Currently')``
* ``input_text``: ``_('Change')``
* ``clear_checkbox_label``: ``_('Clear')``

The ``initial_text``, ``input_text`` and ``clear_checkbox_label`` attributes
are provided in the template context.

EmailInput
``````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: email

URLInput
````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: url

SearchInput
```````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: search

ColorInput
``````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: color

PhoneNumberInput
````````````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: tel

DateInput
`````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_text``: date

DateTimeInput
`````````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: datetime

TimeInput
`````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: time

NumberInput
```````````

* ``template_name``: ``'floppyforms/number_input.html'``
* ``input_type``: number
* ``min``: None
* ``max``: None
* ``step``: None

``min``, ``max`` and ``step`` are available in the template context if they
are not None.

RangeInput
``````````

* ``template_name``: ``'floppyforms/number_input.html'``
* ``input_type``: range
* ``min``: None
* ``max``: None
* ``step``: None

``min``, ``max`` and ``step`` are available in the template context if they
are not None.

Textarea
````````

* ``template_name``: ``'floppyforms/textarea.html'``
* ``rows``: 10
* ``cols``: 40

CheckboxInput
`````````````

* ``template_name``: ``'floppyforms/input.html'``
* ``input_type``: checkbox

Select
``````

* ``template_name``: ``'floppyforms/select.html'``

NullBooleanSelect
`````````````````

* ``template_name``: ``'floppyforms/select.html'``

RadioSelect
```````````

* ``template_name``: ``'floppyforms/radio.html'``

SelectMultiple
``````````````

* ``template_name``: ``'floppyforms/select.html'``

CheckboxSelectMultiple
``````````````````````

* ``template_name``: ``'floppyforms/checkbox_select.html'``


Bugs
----

Really? Oh well... Please Report. Or better, fix :)
