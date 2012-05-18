Template tags
=============

.. highlight:: html+django

To load the floppyforms template library you have to load it on
top of your templates first::

    {% load floppyforms %}

.. _form:

form
----

.. versionadded:: 1.0

The ``form`` tag is used to render one or more form instances using a
template. ::

    {% form myform using "floppyforms/layouts/p.html" %}
    {% form myform another_form form3 using "floppyforms/layouts/p.html" %}

django-floppyforms provides three built-in layouts:

* ``floppyforms/layouts/p.html``: wraps each field in a ``<p>`` tag.
* ``floppyforms/layouts/ul.html``: wraps each field in a ``<li>`` tag.
* ``floppyforms/layouts/table.html``: wraps each form row with a ``<tr>``,
  the label with a ``<th>`` and the widget with a ``<td>`` tag.

See the documentation on :doc:`layouts and how to customize them
</layouts>` for more details.

You can use a default layout by leaving the ``using ...`` out::

    {% form myform %}

In this case the ``floppyforms/layouts/default.html`` template will be used,
which by default is the same as ``floppyforms/layouts/p.html``.

Sometimes it's necessary to pass additional template variables into the
context of a form layout. This can be done in the same way and with the same
syntax as the ``include`` template tag::

    {% form myform using "layout_with_title.html" with title="Please fill in the form" only %}

The ``only`` keyword, as shown in the example above, acts also the same way as
it does in the ``include`` tag. It prevents other, not explicitly
specified, variables from being available in the layout's template context.

Inline layouts
~~~~~~~~~~~~~~

Inlining the form layout is also possible if you don't plan to reuse it
somewhere else. This is done by not specifying a template name after the
``using`` keyword::

    {% form myform using %}
        ... your form layout here ...
    {% endform %}

formconfig
----------

.. versionadded:: 1.0

The ``formconfig`` tag can be used to configure some of the form template
tags arguments upfront so that they don't need to be specified over and over
again.

The first argument specifies which part of the form should be configured:

``row``
~~~~~~~

The ``formrow`` tag takes arguments to specify which template is used to
render the row and whether additional variables are passed into this template.
These parameters can be configured for multiple form rows with a ``{%
formconfig row ... %}`` tag. The syntax is the same as with ``formrow``::

    {% formconfig row using "floppyforms/rows/p.html" %}
    {% formconfig row using "my_form_layout.html" with hide_errors=1 only %}

Please note that form configurations will only be available in a form layout
or wrapped by a ``form`` template tag. They also only apply to all the
form tags that come after the ``formconfig``. It is possible to overwrite
already set options. Here is a valid example::

    {% form myform using %}
    <form action="" method="post" id="signup">{% csrf_token %}
        {% formconfig row using "floppyforms/rows/p.html" %}
        {% formrow form.username %}
        {% formrow form.password %}

        {% formconfig row using "floppyforms/rows/tr.html" %}
        <table>
        {% formrow form.firstname form.lastname %}
        {% formrow form.age %}
        {% formrow form.city form.street %}
        </table>

        <p><input type="submit" value="Signup!" /></p>
    </form>
    {% endform %}

``field``
~~~~~~~~~

A form field takes the same arguments as a form row does, so the same
configuration options are available here, in addition to a ``for`` keyword to
limit which fields the specified configuration will apply to.

List a form field after the ``for`` keyword to only configure the arguments of
that particular field. The following ``formconfig`` example will only affect
the second ``formfield`` tag but the first one will be left untouched::

    {% formconfig field using "input.html" with type="password" for userform.password %}
    {% formfield userform.username %}
    {% formfield userform.password %}

Some more generic field filters are available. A string can be used to limit
configuration either to a specific field name or a field type::

    {% formconfig field with placeholder="Type to search ..." for "search" %}
    {% formfield myform.search %}

    {% formconfig field using "forms/widgets/textarea.html" for "CharField" %}
    {% formfield myform.comment %}

formfield
---------

.. versionadded:: 1.0

Renders a form field using the associated widget. You can specify a widget
template with the ``using`` keyword. Otherwise it will fall back to the
:doc:`widget's default template </widgets-reference>`.

It also accepts ``include``-like parameters::

    {% formfield userform.password using "input.html" with type="password" %}

The ``formfield`` tag should only be used in a form layout, usually in a row
template.

formrow
-------

.. versionadded:: 1.0

The ``formrow`` tag is a quite similar to the ``form`` tag but acts on a
set of form fields instead of complete forms. It takes one or more fields as
arguments and a template which should be used to render those fields::

    {% formrow userform.firstname userform.lastname using "floppyforms/rows/p.html" %}

It also accepts ``include``-like parameters::

    {% formrow myform.field using "my_row_layout.html" with hide_errors=1 only %}

The ``formrow`` tag is usually only used in form layouts.

See the documentation on :doc:`row templates and how they are customized
</layouts>` for more details.

widget
------

.. versionadded:: 1.0

The ``widget`` tag lets you render a widget with the outer template context
available. By default widgets are rendered using a completely isolated
context. In some cases you might want to access the outer context, for
instance for using floppyforms widgets with `django-sekizai`_::

    {% for field in form %}
        {% if not field.is_hidden %}
            {{ field.label_tag }}
            {% widget field %}
            {{ field.errors }}
        {% else %}
            {% widget field %}
        {% endif %}
    {% endfor %}

.. _django-sekizai: http://django-sekizai.readthedocs.org/en/latest/

You can safely use the ``widget`` tag with non-floppyforms widgets, they will
be properly rendered. However, since they're not template-based, they won't be
able to access any template context.
