Template tags
=============

.. highlight:: html+django

To load the floppyforms template library you have to load it on
top of your templates first::

    {% load floppyforms %}

.. _form templatetag:

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

Sometimes it is necessary to pass additional template variables into the
context of a form layout. This can be done in the same way and with the same
syntax as django's `include template tag`_::

    {% form myform using "layout_with_title.html" with title="Please fill in the form" only %}

The ``only`` keyword, as shown in the example above, acts also the same way as
it does in the ``include`` tag. It prevents other, not explicitly
specified, variables from being available in the layout's template context.

.. _include template tag: https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatetag-include

Inline layouts
~~~~~~~~~~~~~~

Inlining the form layout is also possible if you don't plan to reuse it
somewhere else. This is done by not specifying a template name after the
``using`` keyword::

    {% form myform using %}
        ... your form layout here ...
    {% endform %}

.. _formconfig templatetag:

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

However a configuration set with ``formconfig`` will only be available inside
the ``form`` tag that it was specified in. This makes it possible to scope the
configuration with an extra use of the ``form`` tag. See this example::

    {% form myform using %}
    <form action="" method="post" id="signup">{% csrf_token %}
        {# will use default row template #}
        {% formrow form.username %}

        {% form form using %}
            <ul>
                {# this config will not be available outside of the wrapping form tag #}
                {% formconfig row using "floppyforms/rows/li.html" %}

                {# will use configured li row template #}
                {% formrow form.password form.password2 %}
            </ul>
        {% endform %}

        {# will use default row template #}
        {% formrow form.firstname form.lastname %}

        <p><input type="submit" value="Signup!" /></p>
    </form>
    {% endform %}

``field``
~~~~~~~~~

A form field takes the same arguments as a form row does, so the same
configuration options are available here, in addition to a ``for`` keyword to
limit which fields the specified configuration will apply to.

Using the ``for`` keyword allows you to limit the configuration to a specific
field or a set of fields. After the ``for`` keyword, you can give:

* a form field, like ``form.field_name``
* the name of a specific field, like ``"username"``
* a class name of a form field, like ``"CharField"``
* a class name of a widget, like ``"Textarea"``

The configuration applied by ``{% formconfig field ... %}`` is then only
available on those fields that match the given criteria.

Here is an example to clarify things. The ``formconfig`` in the snippet below
will only affect the second ``formfield`` tag but the first one will be left
untouched::

    {% formconfig field using "input.html" with type="password" for userform.password %}
    {% formfield userform.username %}
    {% formfield userform.password %}

And some more examples showing the filtering applied on field names, field
types and widget types::

    {% formconfig field with placeholder="Type to search ..." for "search" %}
    {% formfield myform.search %}

    {% formconfig field using "forms/widgets/textarea.html" for "CharField" %}
    {% formfield myform.comment %}

    {% formconfig field using class="text_input" for "TextInput" %}
    {% formfield myform.username %}

.. note:: Please note that the filterings that act on the field class name and
   widget class name (like ``"CharField"``) also match on subclasses of those
   field. This means if your class inherits from
   ``django.forms.fields.CharField`` it will also get the configuration applied
   specified by ``{% formconfig field ... for "CharField" %}``.

.. _formfield templatetag:

formfield
---------

.. versionadded:: 1.0

Renders a form field using the associated widget. You can specify a widget
template with the ``using`` keyword. Otherwise it will fall back to the
:doc:`widget's default template </widgets-reference>`.

It also accepts ``include``-like parameters::

    {% formfield userform.password using "input.html" with type="password" %}

The ``formfield`` tag should only be used inside a form layout, usually in a
row template.

.. _formrow templatetag:

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

.. _widget templatetag:

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
