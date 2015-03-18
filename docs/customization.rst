Customization
=============

Override default templates
--------------------------

Widgets have a ``template_name`` attribute that points to the template that is
used when rendering the form. Default templates are provided for all
:doc:`built-in widgets </widgets-reference>`. In most cases the default
implementation of these templates have no specific behaviour and simply inherit
from ``floppyforms/input.html``. They are provided mainly to give an easy
way for a site-wide customization of how a specifig widget is rendered.

You can easily override these templates in your project-level
``TEMPLATE_DIRS``, assuming they take precedence over app-level templates.

Custom widgets with custom templates
------------------------------------

If you want to override the rendering behaviour only for a few widgets, you
can extend a ``Widget`` class from FloppyForms and override the
``template_name`` attribute::

    import floppyforms as forms

    class OtherEmailInput(forms.EmailInput):
        template_name = 'path/to/other_email.html'

Then, the output can be customized in ``other_email.html``:

.. code-block:: jinja

    <input type="email"
           name="{{ name }}"
           id="{{ attrs.id }}"
           placeholder="john@example.com"
           {% if value %}value="{{ value }}"{% endif %}>

Here we have a hardcoded placeholder without needing to instantiate the widget
with an ``attrs`` dictionary::

    class EmailForm(forms.Form):
        email = forms.EmailField(widget=OtherEmailInput())

.. _template_name_customization:

You can also customize the ``template_name`` without subclassing, by passing it
as an argument when instantiating the widget::

    class EmailForm(forms.Form):
        email = forms.EmailField(
            widget=forms.EmailInput(template_name='path/to/other_email.html'))

For advanced use, you can even customize the template used per-render, by
passing a ``template_name`` argument to the widget's ``render()`` method.

Adding more template variables
------------------------------

There is also a way to add extra context. This is done by subclassing the
widget class and extending the ``get_context()`` method::

    class OtherEmailInput(forms.EmailInput):
        template_name = 'path/to/other.html'

        def get_context(self, name, value, attrs):
            ctx = super(OtherEmailInput, self).get_context(name, value, attrs)
            ctx['foo'] = 'bar'
            return ctx

And then the ``other.html`` template can make use of the ``{{ foo }}`` context
variable.

``get_context()`` takes ``name``, ``value`` and ``attrs`` as arguments, except
for all ``Select`` widgets which take an additional ``choices`` argument.

In case you don't need the arguments passed to ``get_context()``, you can
extend ``get_context_data()`` which doesn't take any arguments::

    class EmailInput(forms.EmailInput):
        def get_context_data(self):
            ctx = super(EmailInput, self).get_context_data()
            ctx.update({
                'placeholder': 'hello@example.com',
            })
            return ctx

Altering the widget's ``attrs``
-------------------------------

All widget attibutes except for ``type``, ``name``, ``value`` and ``required``
are put in the ``attrs`` context variable, which you can extend in
``get_context()``:

.. code-block:: python

    def get_context(self, name, value, attrs):
        ctx = super(MyWidget, self).get_context(name, value, attrs)
        ctx['attrs']['class'] = 'mywidget'
        return ctx

This will render the widget with an additional ``class="mywidget"`` attribute.

If you want only the attribute's key to be rendered, set it to ``True``:

.. code-block:: python

    def get_context(self, name, value, attrs):
        ctx = super(MyWidget, self).get_context(name, value, attrs)
        ctx['attrs']['awesome'] = True
        return ctx

This will simply add ``awesome`` as a key-only attribute.
