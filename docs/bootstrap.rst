Layout example with Bootstrap
=============================

If you use Floppyforms with Bootstrap you might be interested in using a
bootstrap layout for your form.

What you have to do is to create those two templates:

**floppyforms/templates/floppyforms/layouts/bootstrap.html**:

.. code-block:: django

    {% load floppyforms %}{% block formconfig %}{% formconfig row using "floppyforms/rows/bootstrap.html" %}{% endblock %}
    
    {% block forms %}{% for form in forms %}
    {% block errors %}
        {% for error in form.non_field_errors %}
            <div class="alert alert-error">
                <a class="close" href="#" data-dismiss="alert">×</a>
                {{ error }}
            </div><!--- .alert.alert-error -->
        {% endfor %}
        {% for error in form|hidden_field_errors %}
            <div class="alert alert-error">
                <a class="close" href="#" data-dismiss="alert">×</a>
                {{ error }}
            </div><!--- .alert.alert-error -->
        {% endfor %}
    {% endblock errors %}
    {% block rows %}
            {% for field in form.visible_fields %}
                {% if forloop.last %}{% formconfig row with hidden_fields=form.hidden_fields %}{% endif %}
                {% block row %}{% formrow field %}{% endblock %}
            {% endfor %}
            {% if not form.visible_fields %}{% for field in form.hidden_fields %}{% formfield field %}{% endfor %}{% endif %}
    {% endblock %}
    {% endfor %}{% endblock %}

**floppyforms/templates/floppyforms/rows/bootstrap.html**:

.. code-block:: django

    {% load floppyforms %}{% block row %}{% for field in fields %}
    <div class="control-group{% if field.errors %} error{% endif %}">
        {% with classes=field.css_classes label=label|default:field.label help_text=help_text|default:field.help_text %}
        {% block label %}{% if field|id %}<label class="control-label" for="{{ field|id }}">{% endif %}{{ label }}{% if field.field.required %} <span class="required">*</span>{% endif %}{% if label|last not in ".:!?" %}:{% endif %}{% if field|id %}</label>{% endif %}{% endblock %}
        {% block field %}
            <div class="controls {{ classes }} field-{{ field.name }}">
                {% block widget %}{% formfield field %}{% endblock %}
                {% block errors %}{% include "floppyforms/errors.html" with errors=field.errors %}{% endblock %}
                {% block help_text %}{% if field.help_text %}
                    <p class="help-block">{{ field.help_text }}</p>
                {% endif %}{% endblock %}
                {% block hidden_fields %}{% for field in hidden_fields %}{{ field.as_hidden }}{% endfor %}{% endblock %}
            </div><!--- .controls -->
        {% endblock %}
        {% endwith %}
    </div><!--- .control-group{% if field.errors %}.error{% endif %} -->
    {% endfor %}{% endblock %}

You can also define this layout by default:

**floppyforms/templates/floppyforms/layouts/default.html**:

.. code-block:: django

    {% extends "floppyforms/layouts/bootstrap.html" %}

You can also make a change to the error display:

**floppyforms/templates/floppyforms/errors.html**:

.. code-block:: django

    {% if errors %}<span class="help-inline">{% for error in errors %}{{ error }}{% if not forloop.last %}<br />{% endif %}{% endfor %}</span>{% endif %}

And that's it, you now have a perfect display for your form with bootstrap.
