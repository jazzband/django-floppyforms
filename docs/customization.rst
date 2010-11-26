Customization
=============

Widgets have a ``template_name`` attribute that point to the template to use
when rendering the form. Default templates are provided, for instance the
default template for a ``TextInput`` and other input-type widgets is
``floppyforms/input.html``. You can easily override this template in your
project-level ``TEMPLATE_DIRS``, assuming they take precedence over app-level
templates.

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
           id="{{ id }}"
           placeholder="john@example.com"
           {% if value %}value="{{ value }}"{% endif %} />

Here we have a hardcoded placeholder without needing to instantiate the widget
with an ``attrs`` dictionary::

    class EmailForm(forms.Form):
        email = forms.EmailField(widget=OtherEmailInput())

There is also a way to add extra context. This is done by subclassing the
widget class an extending the ``get_extra_context()`` method::

    class OtherEmailInput(forms.EmailInput):
        template_name = 'path/to/other.html'

        def get_extra_context(self):
            ctx = super(OtherEmailInput, self).get_extra_context()
            ctx['foo'] = 'bar'
            return ctx

And then the ``other.html`` template can make use of the ``{{ foo }}`` context
variable.
