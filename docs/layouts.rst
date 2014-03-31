Form layouts
============

.. highlight:: html+django
.. versionadded:: 1.0

Using form layouts
------------------

django-floppyforms tries to make displaying Django forms in a template a bit
easier by using the concept of a reusable form layout. A layout is basically
just a single template that knows how to render a form into HTML. Here is a
simple example demonstrating how to use a layout::

    <form action="/contact/" method="post">{% csrf_token %}
        {% form contact_form using "floppyforms/layouts/p.html" %}
        <input type="submit" value="Submit" />
    </form>

Usually a form layout doesn't include the surrounding ``<form>`` tags and the
submit button. So you need to take care of that.

``{% form myform using "floppyforms/layouts/p.html" %}`` will output the form
with each field and accompanying label wrapped in a paragraph and is meant as
a replacement for django's ``{{ myform.as_p }}`` method. Here is the possible
output for our example::

    <form action="/contact/" method="post">
        <p>
            <label for="id_subject">Subject:</label>
            <input id="id_subject" type="text" name="subject" maxlength="100" />
        </p>
        <p>
            <label for="id_message">Message:</label>
            <input type="text" name="message" id="id_message" />
        </p>
        <p>
            <label for="id_sender">Sender:</label>
            <input type="text" name="sender" id="id_sender" />
        </p>
        <p>
            <label for="id_cc_myself">Cc myself:</label>
            <input type="checkbox" name="cc_myself" id="id_cc_myself" />
        </p>
        <input type="submit" value="Submit" />
    </form>

You can also use ``floppyforms/layouts/table.html`` to output table rows (you'll
need to provide your own ``<table>`` tags) and ``floppyforms/layouts/ul.html`` to
output list items. See the :ref:`list of built-in form layouts
<built-in layouts>` for more information.

Customizing the layout template
-------------------------------

If the default layouts are not to your taste, you can completely customize the
way a form is presented using the Django template language. Extending the
above example::

    <form action="/contact/" method="post">
        {% form contact_form using "my_layout.html" %}
        <p><input type="submit" value="Send message" /></p>
    </form>

``my_layout.html`` is able to extend one of the built-in layouts, modifying
the parts you want to change::

    {% extends "floppyforms/layouts/table.html" %}

    {% block errors %}
        <p>Following errors occurred that cannot be matched to a field:</p>
        {{ block.super }}
    {% endblock %}

See the :ref:`form layout reference <layout reference>` for a detailed
description on how you can structure your custom layouts.

You can also specify your form layout "inline" rather than in a separate
template file, if you don't plan to reuse it. This is also done with the
:ref:`form <form templatetag>` tag::

    <form action="/signup/" method="post">
        {% form signup_form using %}
        <div><label for="id_username">Username:</label>
            {% formfield form.username %}<div>
        <div><label for="id_password">Password:</label>
            {% formfield form.password %}</div>
        <div>
            <label for="id_firstname">First- and Lastname:</label><br />
            {% formfield form.firstname %}
            {% formfield form.lastname %}
        </div>
        {% endform %}
        <p><input type="submit" value="Send message" /></p>
    </form>

Note that the ``signup_form`` variable will also be available as ``form``
inside the templatetag. This is for convenience and having always the same
memorizable name makes using the same template a lot easier.

Something new in the example is also the :ref:`formfield <formfield
templatetag>` tag. It is used to render the *widget* of a form field so that
you don't have to type out all the ``<input />`` tags yourself.

But just displaying the widget is not all that you need to take into account
when you are creating your own design. You also need to take care where to
display errors if a field's validation fails, how to display the help text
that might be defined for a field, etc. Because of this it is in most cases
easier to split out these *form rows* (containing one or more fields) into
their own templates. They work just like form layouts but for a subset of
fields and taking care of the errors, help text and other HTML that appears
for every field. Here is how it might look like::

    <form action="/signup/" method="post">
        {% form signup_form using %}
            {% formrow form.username using "div_row.html" %}
            {% formrow form.password using "div_row.html" %}
            {% formrow form.firstname form.lastname using "many_fields_div_row.html" with label="First- and Lastname" %}
        {% endform %}
        <p><input type="submit" value="Sign up" /></p>
    </form>

Rendering multiple forms
------------------------

Sometimes you want to render multiple forms at once, all with the same layout
without repeating yourself. You can do that by passing either a list or
multiple single forms into ``{% form %}``::

    <form action="" method="post">
        {% form myform1 myform2 using "floppyforms/layouts/p.html" %}
        <p><input type="submit" value="Submit" /></p>
    </form>

For the built-in layouts, the output is the same as for::

    <form action="" method="post">
        {% form myform1 using "floppyforms/layouts/p.html" %}
        {% form myform2 using "floppyforms/layouts/p.html" %}
        <p><input type="submit" value="Submit" /></p>
    </form>

Your own layouts can change their behaviour depending on how many forms you
have specified, like wrapping them in a fieldset and giving those unique ids
etc.

.. _formsets:

Using layouts with formsets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is how rendering a formset might look like::

    <form action="" method="post">
        {{ formset.management_form }}
        {% form formset.forms %}
        <p><input type="submit" value="submit" /></p>
    </form>

.. _built-in layouts:

Built-in layouts
----------------

django-floppyforms ships with three standard form layouts:

Paragraph
~~~~~~~~~

Renders the form fields in ``<p>`` tags using the
``floppyforms/layouts/p.html`` template.

The **default row template** is ``floppyforms/rows/p.html``.

The recommended way to use layouts is by using the :ref:`{% form %}
templatetag <form templatetag>`.  However django-floppyforms will hook for
your convenience into django's ``as_*`` methods so that they use templates and
can be modified to your needs. The ``p`` layout will be used for all ``{{
form.as_p }}``.

Unordered list
~~~~~~~~~~~~~~

Renders the form fields as ``<li>`` tags using the
``floppyforms/layouts/ul.html`` template. It does not display the surrounding
``<ul>``. So infact you also can use it with a ``<ol>``.

The **default row template** is ``floppyforms/rows/li.html``.

This layout will be used for all ``{{ form.as_ul }}``.

Table
~~~~~

Renders the form fields as ``<tr>`` tags using the
``floppyforms/layouts/table.html`` template. It does not display the
surrounding ``<table>`` or ``<tbody>``. Please take care of that.

The **default row template** is ``floppyforms/rows/tr.html``.

This layout will be used for all ``{{ form.as_table }}``.

Default template
~~~~~~~~~~~~~~~~

django-floppyforms uses the default template layout
``floppyforms/layouts/default.html`` when calling ``{% form myform %}``
without the ``using`` parameter.

The actual code in the default layout looks like::

    {% extends "floppyforms/layouts/table.html" %}

You can drop in your own default form layout, for use when no specific layout
is defined, by placing a ``floppyforms/layouts/default.html`` in your
templates directory.

The **default row template** is ``floppyforms/rows/default.html``

This layout will be used as default for all ``{{ form }}``.

.. _layout reference:

Create custom layouts
---------------------

Sometimes the sample layouts mentioned above just don't meet your needs. In
that case there are some possibilities to customize them.

The simplest way is to use Django's template inheritance to extend a built-in
layout, only overwriting the bits you want to modify. In this case, use the
layout that matches your needs best and customize it by overriding one of the
following blocks:

* ``formconfig``: In this block are all the :ref:`formconfig <formconfig
  templatetag>` templatetags that are used in the layout. The built-in layouts
  configure their row level template here.

* ``forms``: This block wraps all the actual markup output. Use this to add
  markup before or after the rendered forms::

    {% extends "floppyforms/layouts/p.html" %}

    {% block forms %}
        <form action="" method="post">{% csrf_token %}
            {{ block.super }}
            <p><input type="submit" value="submit" /></p>
        </form>
    {% endblock %}

  The preceding example shows a custom form layout that renders all elements
  in a paragraph based layout that also contains the necessary ``<form>`` tag
  and a submit button.

* ``errors``: All non field errors and errors of hidden fields are rendered in
  this block (the default layouts render errors by including the
  ``form/errors.html`` template).

* ``rows``: The ``rows`` block contains a for loop that iterates over all
  visible fields and displays them in the ``row`` block. Hidden fields are
  rendered in the last row.

* ``row``: This block is wrapped around the ``{% formrow %}`` templatetag.

Alternatively it is of course possible to write your own form layout from
scratch. Have a look at the `existing ones`_ to get an idea what is possible,
what cases to take into account and how the template code could look like.

.. _`existing ones`: https://github.com/gregmuellegger/django-floppyforms/tree/master/floppyforms/templates/floppyforms/layouts/

Creating reusable layouts
~~~~~~~~~~~~~~~~~~~~~~~~~

When you try to create reusable layouts, it is in most cases usefull to
provide some configuration options via arguments. In general the global
template context is available to the layout as well as you can pass extra
variables into the :ref:`form templatetag`::

    {% form contact_form using "my_form_layout.html" with headline="Fill in your enquiry" %}

Whereas ``my_form_layout.html`` could look like::

    {% extends "floppyforms/layouts/p.html" %}

    {% block forms %}
        {% if headline %}<h1>{{ headline }}</h1>{% endif %}
        {{ block.super }}
    {% endblock %}

Form rows
~~~~~~~~~

A vital part of any form layout is one or are many templates for form
rows. A row can be used to render one or multiple fields in a repeating
manner.

The built-in row templates render each passed in field in a separate row. You
can extend and override these like you can with complete form layouts as
described above. Use the following blocks to customize them to your needs:

* ``row``: This is the most outer block and wraps all the generated HTML.
  Use it to wrap the row into additional markup.

* ``field``: You can use this block to wrap every single field into additional
  markup.

* ``errors``: Errors are displayed as a ``<ul>`` list. Override the ``errors``
  block to customize their appearance.

* ``label``: Change the label markup by overriding this block.

* ``widget``: This one contains just the ``{% formfield %}`` templatetag that will
  render the field's widget.

* ``help_text``: Change the help text markup by overriding this block.

* ``hidden_fields``: The built-in row templates allow hidden fields to be
  passed into the row with the template variable named ``hidden_fields``. The
  form layouts pass all the form's hidden fields into the last rendered form
  row.
