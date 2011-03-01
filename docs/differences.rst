Differences with django.forms
=============================

So, you have a project already using django.forms, and you're considering a
switch to floppyforms? Here's what you need to know, assuming the only
change you've made to your code is a simple change, from:

.. code-block:: python

    from django import forms


to:

.. code-block:: python

    import floppyforms as forms

Standard forms
--------------

Floppyforms adds a couple of things on top of the standard django widgets:
HTML syntax, more native widget types, the ``required`` attribute and
client-side validation.

HTML syntax
```````````

Floppyforms uses an HTML syntax instead of django's XHTML syntax. You will see
``<input type="text" ... >`` and not ``<input type="text" />``.

Native widget types
```````````````````

Floppyforms tries to use the native HTML5 widgets whenever it's possible. Thus
some widgets which used to be simple ``TextInputs`` in django.forms are now
specific input that will render as ``<input type="...">`` with the HTML5
types such as ``url``, ``email``. See :ref:`widgets` for a detailed list of
specific widgets.

For instance, if you have declared a form using django.forms:

.. code-block:: python

    class ThisForm(forms.Form):
        date = forms.DateField()

The ``date`` field will be rendered as an ``<input type="text">``. However, by
just changing the forms library to floppyforms, the input will be an ``<input
type="date">``.

Required attribute
``````````````````

In addition to the various input types, every required field has the
``required`` attribute set to ``True`` on its widget. That means that every
``<input>`` widget for a required field will be rendered as ``<input
type="..." ... required>``. This is used for client-side validation: for
instance, Firefox 4 won't let the user submit the form unless he's filled the
input. This saves HTTP requests but doesn't mean you can stop validating user
input.

Client-side validation
``````````````````````

Like with the ``required`` attribute, the ``pattern`` attribute is especially
interesting for slightly more complex client-side validation. The SlugField
and the IPAddressField both have a pattern attached to the ``<input>``.

ModelForms
----------

As for ModelForms, all the fields coming from the model still get a widget
from django.form and not from floppyforms, unless the widgets are overridden
in the form's ``Meta`` inner class. For example, if we have a model declared
as such:

.. code-block:: python

    from django.db import models

    class Hi(models.Model):
        name = forms.CharField(max_length=255)
        timestamp = forms.DateTimeField()
        rank = models.PositiveIntegerField()

And a ModelForm written like this:

.. code-block:: python

    import floppyforms as forms

    class HiForm(forms.ModelForm):
        yesno = forms.BooleanField

        class Meta:
            model = Hi
            widgets = {
                'timestamp': forms.DateTimeInput,
            }

With such a ModelForm, the ``yesno`` and ``timestamp`` fields will get a
widget from floppyforms:

* ``yesno`` is an extra field declared using the floppyforms namespace
* ``timestamp`` has an overridden widget coming from floppyforms as well

However, the ``name`` and ``rank`` field will both get a widget from
django.forms, in this case a ``TextInput``.

Getting back django's behaviour
-------------------------------

If you need to get the same output as standard django forms:

* Override ``floppyforms/input.html``, ``floppyforms/radio.html``,
  ``floppyforms/clearable_input.html`` and
  ``floppyforms/checkbox_select.html`` to use an XHTML syntax

* Remove the ``required`` attribute from the templates as well

* Make sure your fields which have HTML5 widgets by default get simple
  ``TextInputs`` instead:

  .. code-block:: python

      class Foo(forms.Form):
          url = forms.URLField(widget=forms.TextInput)


.. note:: On overriding the default templates

    If you override floppyforms' templates in your project-level template
    directory, the floppyforms tests will start failing. You might want to
    define new widgets that extends floppyforms widgets using their own
    templates to avoid this issue.
