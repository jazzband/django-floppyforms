Usage
=====

Forms
`````

Floppyforms are supposed to work just like Django forms::

    import floppyforms as forms

    class ProfileForm(forms.Form):
        name = forms.CharField()
        email = forms.EmailField()
        url = forms.URLField()

With some template code:

.. code-block:: jinja

    <form method="post" action="/some-action/">
        {% csrf_token %}
        {{ form.as_p }}
        <p><input type="submit" value="Yay!"></p>
    </form>

The form will be rendered using the ``floppyforms/layouts/p.html`` template.
See the :doc:`documentation about layouts <layouts>` for details.

Each field has a default widget and widgets are rendered using templates.

Default templates are provided and their output is relatively similar to
Django widgets, with a few :doc:`minor differences</differences>`:

* HTML5 ``<input>`` types are supported: ``url``, ``email``, ``date``,
  ``datetime``, ``time``, ``number``, ``range``, ``search``, ``color``,
  ``tel``.

* The ``required`` and ``placeholder`` attributes are also supported.

Widgets are rendered with the following context variables:

* ``hidden``: set to ``True`` if the field is hidden.
* ``required``: set to ``True`` if the field is required.
* ``type``: the input type. Can be ``text``, ``password``, etc. etc.
* ``name``: the name of the input.
* ``attrs``: the dictionnary passed as a keyword argument to the widget. It
  contains the ``id`` attribute of the widget by default.

Each widget has a ``template_name`` attribute which points to the template to
use when rendering the widget. A basic template for an ``<input>`` widget may
look like:

.. code-block:: jinja

    <input {% for key, val in attrs.items %}
             {{ key }}="{{ val }}"
           {% endfor %}
           type="{{ type }}"
           name="{{ name }}"
           {% if value %}value="{{ value }}"{% endif %}>

The default floppyforms template for an ``<input>`` widget is slightly more
complex.

Some widgets may provide extra context variables and extra attributes:

====================== ====================================== ==============
Widget                 Extra context                          Extra ``attrs``
====================== ====================================== ==============
Textarea                                                      ``rows``, ``cols``
NumberInput                                                   ``min``, ``max``,  ``step``
RangeInput                                                    ``min``, ``max``, ``step``
Select                 ``optgroups``, ``multiple``
RadioSelect            ``optgroups``, ``multiple``
NullBooleanSelect      ``optgroups``, ``multiple``
SelectMultiple         ``optgroups``, ``multiple`` (``True``)
CheckboxSelectMultiple ``optgroups``, ``multiple`` (``True``)
====================== ====================================== ==============

Furthermore, you can specify custom ``attrs`` during widget definition. For
instance, with a field created this way::

    bar = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'john@example.com'}))

Then the ``placeholder`` variable is available in the ``attrs`` template
variable.

.. _usage-modelforms:

ModelForms
``````````

You can use ``ModelForms`` with floppyforms as you would use a ordinary django
``ModelForm``.  Here is an example showing it for a basic ``Profile`` model::

    class Profile(models.Model):
        name = models.CharField(max_length=255)
        url = models.URLField()

Now create a ``ModelForm`` using floppyforms::

    import floppyforms.__future__ as forms

    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ('name', 'url')

The ``ProfileForm`` will now have form fields for all the model fields. So
there will be a ``floppyforms.CharField`` used for the ``Profile.name`` model
field and a ``floppyforms.URLField`` for ``Profile.url``.

.. note::

    Please note that you have to import from ``floppyforms.__future__`` to use
    this feature. Here is why:

    This behaviour changed in version 1.2 of **django-floppyforms**. Before,
    no alterations were made to the widgets of a ``ModelForm``. So you had to
    take care of assigning the floppyforms widgets to the django form fields
    yourself to use the template based rendering provided by floppyforms. Here
    is an example of how you would have done it with django-floppyforms 1.1
    and earlier::

        import floppyforms as forms

        class ProfileForm(forms.ModelForm):
            class Meta:
                model = Profile
                fields = ('name', 'url')
                widgets = {
                    'name': forms.TextInput,
                    'url': forms.URLInput,
                }

    Since the change is backwards incompatible, we decided to provide a
    deprecation path. If you create a ``ModelForm`` with django-floppyforms
    1.2 and use ``import floppyforms as forms`` as the import you will get the
    old behaviour and you will see a ``DeprecationWarning``.

    To use the new behaviour, you can use ``import floppyforms.__future__ as
    forms`` as the import.

    Please make sure to test your code if your modelforms work still as
    expected with the new behaviour. The old version's behaviour will be
    removed completely with django-floppyforms 1.4.
