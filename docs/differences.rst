Differences with django.forms
=============================

So, you have a project already using ``django.forms``, and you're considering
a switch to floppyforms? Here's what you need to know, assuming the only
change you've made to your code is a simple change, from:

.. code-block:: python

    from django import forms


to:

.. code-block:: python

    import floppyforms as forms

.. note:: ``django.forms.*`` modules

    Other modules contained by ``django.forms``, such as ``forms``, ``utils``
    and ``formsets`` have not been aliased.

HTML 5 forms!
-------------

Floppyforms adds a couple of HTML 5 features on top of the standard Django
widgets: HTML syntax, more native widget types, the ``required`` attribute and
client-side validation.

HTML syntax instead of XHTML
````````````````````````````

Floppyforms uses an HTML syntax instead of Django's XHTML syntax. You will see
``<input type="text" ... >`` and not ``<input type="text" />``.

Native widget types
```````````````````

Floppyforms tries to use the native HTML5 widgets whenever it's possible. Thus
some widgets which used to be simple ``TextInputs`` in ``django.forms`` are
now specific input that will render as ``<input type="...">`` with the HTML5
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
interesting for slightly more complex client-side validation. The ``SlugField``
and the ``IPAddressField`` both have a pattern attached to the ``<input>``.

However having these validations backed directly into the HTML and therefore
allowing the browser to validate the user input might not always what you want
to have. Sometimes you just want to have a form where it should be allowed to
submit invalid data. In that case you can use the ``novalidate`` attribute on
the ``<form>`` HTML tag or the ``formnovalidate`` attribute on the submit
button:

.. code-block:: html

    <form action="" novalidate>
        This input will not be validated:
        <input type="text" required />
    </form>

    <form action="">
        Another way to not validate the form in the browser is using the
        formnovalidate attribute on the submit button:
        <input type="submit" value="cancel" formnovalidate>
    </form>

Read the corresponding documentation for `novalidate`_ and `formnovalidate`_ on
the Mozilla Developer Network if you want to know more.

.. _novalidate: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/form#attr-novalidate
.. _formnovalidate: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/button#attr-formnovalidate

ModelForms
----------

Prior to version 1.2 of django-floppyforms, you had to take some manual
efforts to make your modelforms work with floppyforms. This is now done
seemlesly, but since this was introduced a backwards incompatible change, it
was necessary to provde a deprecation path.

So if you start out new with django-floppyforms just use ``import
floppyforms.__future__ as forms`` as your import instead of ``import
floppyforms as forms`` when you want to define modelforms.

For more information see the :ref:`section about modelforms in the usage
documentation <usage-modelforms>`.

``help_text`` values are autoescaped by default
-----------------------------------------------

If you use HTML in the ``help_text`` value for a Django form field and are not
using django-floppyforms, then you will get the correct HTML rendered in the
template. For example you have this form::

    from django import forms

    class DjangoForm(forms.Form):
        myfield = forms.CharField(help_text='A <strong>help</strong> text.')

When you now use this form with ``{{ form.as_p }}`` in the template, you will
get the help text put in the template as it is, with no HTML escaping. That
might imply a security risk if your help text contains content from untrusted
sources. django-floppyforms applies autoescaping by default to the help text.
So if you define::

    import floppyforms as forms

    class FloppyForm(forms.Form):
        myfield = forms.CharField(help_text='A <strong>help</strong> text.')

And then use ``{{ form.as_p }}``, you will get an output that contains ``A
&lt;strong&;gt;help&lt;/strong&gt; text.``. You can disable the autoescaping
of the help text by using Django's ``mark_safe`` helper::

    from django.utils.html import mark_safe
    import floppyforms as forms

    class FloppyForm(forms.Form):
        myfield = forms.CharField(help_text=mark_safe('A <strong>help</strong> text.'))


``TEMPLATE_STRING_IF_INVALID`` caveats
--------------------------------------

The use of a non-empty ``TEMPLATE_STRING_IF_INVALID`` setting can impact
rendering. Missing template variables are rendered using the content of ``TEMPLATE_STRING_IF_INVALID`` but filters used on non-existing variables are not applied (see `django's documentation on how invalid template variables are
handled`__ for more details).

__ https://docs.djangoproject.com/en/dev/ref/templates/api/#invalid-template-variables

django-floppyforms assumes in its predefined form layouts that
all filters are applied. You can work around this by making your
``TEMPLATE_STRING_IF_INVALID`` evaluate to ``False`` but still keep its
string representation. Here is an example how you could achieve this in your
``settings.py``:

.. code-block:: python

    # on Python 2
    class InvalidVariable(unicode):
        def __nonzero__(self):
            return False

    # on Python 3
    class InvalidVariable(str):
        def __bool__(self):
            return False

    TEMPLATE_STRING_IF_INVALID = InvalidVariable(u'INVALID')

Getting back Django's behaviour
-------------------------------

If you need to get the same output as standard Django forms:

* Override ``floppyforms/input.html``, ``floppyforms/radio.html``,
  ``floppyforms/clearable_input.html``,  ``floppyforms/textarea.html`` and
  ``floppyforms/checkbox_select.html`` to use an XHTML syntax

* Remove the ``required`` attribute from the same templates, as well as ``floppyforms/select.html``

* Make sure your fields which have HTML5 widgets by default get simple
  ``TextInputs`` instead:

  .. code-block:: python

      class Foo(forms.Form):
          url = forms.URLField(widget=forms.TextInput)
