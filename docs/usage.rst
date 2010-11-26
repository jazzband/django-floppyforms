Usage
=====

Forms
`````

FloppyForms are supposed to work just like Django forms::

    import floppyforms as forms

    class FlopForm(forms.Form):
        name = forms.CharField()
        email = forms.EmailField()
        url = forms.URLField()

With some template code:

.. code-block:: jinja

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
look like:

.. code-block:: jinja

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
