Form layouts
============

.. highlight:: html+django
.. versionadded:: 1.0

Form layouts are reusable templates that describe how a form is presented as
HTML. See the :ref:`form templatetags <form>` for more information on how to
use them during form rendering.

Built-in layouts
----------------

django-floppyforms ships with three standard form layouts:

Paragraph
~~~~~~~~~

Renders the form as a ``<p>`` tag using the ``floppyforms/layouts/p.html``
template.

The **default row template** is ``floppyforms/rows/p.html``.

Unordered list
~~~~~~~~~~~~~~

Renders the form as a ``<ul>`` tag using the ``floppyforms/layouts/ul.html``
template.

The **default row template** is ``floppyforms/rows/li.html``.

Table
~~~~~

Renders the form as a ``<table>`` tag using the
``floppyforms/layouts/table.html`` template.

The **default row template** is ``floppyforms/rows/tr.html``.

Default template
~~~~~~~~~~~~~~~~

django-floppyforms uses a default template when rendering a form
called ``floppyforms/layouts/default.html``.

The code of the default layout actually looks like::

    {% extends "floppyforms/layouts/p.html" %}

You can drop in your own default form layout, for use when no specific layout
is defined, by overriding ``floppyforms/layouts/default.html`` in your
templates directory.

The **default row template** is ``floppyforms/rows/default.html``

.. _custom form layouts:

Create custom layouts
---------------------

Sometimes the sample layouts mentioned above just don't meet your needs. In
that case there are some possibilities to customize them.

The simplest way is to use Django's template inheritance, extend a built-in
layout, and only overwrite the bits you want to modify. In this case, use the
layout that matches your needs best and customize it by overriding one of the
following blocks:

* ``formconfig``: In this block are all the ``{% formconfig %}`` tags that are
  used in the layout. The built-in layouts configure their row level template
  here.

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

* ``row``: This block is wrapped around the ``{% formrow %}`` tag.

Alternatively it is of course possible to write your own form layout from
scratch. Have a look at the `existing ones`_ to get an idea what is possible,
what cases to take into account and how the template code could look like.

.. _`existing ones`: https://github.com/brutasse/django-floppyforms/tree/master/floppyforms/templates/floppyforms/layouts/

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

* ``widget``: This one contains just the ``{% formfield %}`` tag that will
  render the field's widget.

* ``help_text``: Change the help text markup by overriding this block.

* ``hidden_fields``: The built-in row templates allow hidden fields to be
  passed into the row with the template variable named ``hidden_fields``. The
  form layouts pass all the form's hidden fields into the last rendered form
  row.
