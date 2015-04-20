Changelog
---------

1.4.0
~~~~~

* Every widget is now using its own template. Previously all widgets that are
  based on the HTML ``<input>`` tag used the generic ``floppyforms/input.html``
  template. Now the widgets each have a custom element for easier
  customisation. For example ``CheckboxInput`` now uses
  ``floppyforms/checkbox.html`` instead of ``floppyforms/input.html``. See
  `Widgets reference
  <http://django-floppyforms.readthedocs.org/en/latest/widgets-reference.html>`_
  for a complete list of available widgets and which templates they use.

* Adjusting the SRIDs used in the GeoDjango widgets to conform with
  Django 1.7. Thanks to Tyler Tipton for the patch.

* Python 3.2 is now officially supported.

* Django 1.8 is now officially supported. django-floppyforms no longers
  triggers Django deprecation warnings.

* Adding `OpenLayers`_ distribution to django-floppyforms static files in order
  to better support HTTPS setups when GIS widgets are used (See #15 for more
  details).

* Fix: ``python setup.py bdist_rpm`` failed because of wrong string encodings
  in setup.py. Thanks to Yuki Izumi for the fix.

* Fix: The ``CheckboxInput`` widget did detect different values in Python 2
  when given ``'False'`` and ``u'False'`` as data. Thanks to @artscoop for the
  patch.

* Fix: ``MultipleChoiceField`` can now correctly be rendered as hidden field by
  using the ``as_hidden`` helper in the template. That was not working
  previously as there was no value set for ``MultipleChoiceField.hidden_widget``.

.. _OpenLayers: http://openlayers.org/

1.3.0
~~~~~

* DateInput widget renders hardcoded "%Y-%m-%d" format. We don't allow custom
  formats there since the "%Y-%m-%d" format is what browsers are submitting
  with HTML5 date input fields. Thanks to Bojan Mihelac for the patch.

* Adding ``supports_microseconds`` attribute to all relevant widget classes.
  Thanks to Stephen Burrows for the patch.

* Using a property for ``Widget.is_hidden`` attribute on widgets to be in
  conformance with Django 1.7 default widget implementation.

* The docs mentioned that the current ``ModelForm`` behaviour in
  ``floppyforms.__future__`` will become the default in 1.3. This is postpone
  for one release and will be part of 1.4.

1.2.0
~~~~~

* Subclasses of ``floppyforms.models.ModelForm`` did not convert widgets of
  form fields that were automatically created for the existing model fields
  into the floppyform variants. This is now changed, thanks to a patch by
  Stephen Burrows.

  Previously you had to set the widgets your self in a model form. For example
  you would write::

    import floppyforms as forms

    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            widgets = {
                'name': forms.TextInput,
                'url': forms.URLInput,
                ...
            }

  Now this is done automatically. But since this is a kind-of
  backwardsincompatible change, you need to use a special import::

    import floppyforms.__future__ as forms

    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile

  This feature will become the default behaviour in floppyforms 1.4.

  See the documentation for more information:
  http://django-floppyforms.readthedocs.org/en/latest/usage.html#modelforms

* If you added an attribute with value 1 to the attrs kwargs (e.g. ``{'value':
  1}``, you would get no attribute value in the rendered html (e.g. ``value``
  instead of ``value="1"``). That's fixed now, thanks to Viktor Ershov for the
  report.

* All floppyform widget classes now take a ``template_name`` argument in the
  ``__init__`` and ``render`` method. Thanks to Carl Meyer for the patch.

1.1.1
~~~~~

* Fix for Django 1.6

* Fix for GIS widgets on Django 1.4 and some versions of GEOS.

1.1
~~~

* Added GenericIPAddressField.

* Django 1.5 and Python 3.3 support added.

* Django 1.3 support dropped.

* GIS widgets switched to stable OpenLayers release instead of a dev build.

* Fixed ``Textarea`` widget template to work with a non-empty
  ``TEMPLATE_STRING_IF_INVALID`` setting. Thanks to Leon Matthews for the
  report.

* Fixed context handling in widget rendering. It didn't take care of popping
  the context as often as it was pushed onto. This could cause strange
  behaviour in the template by leaking variables into outer scopes. Thanks to
  David Danier for the report.

* Added missing empty choice for selectboxes in ``SelectDateWidget``. Thanks
  fsx999 for the report.

* ``IntegerField`` now automatically passes its ``min_value`` and
  ``max_value`` (if provided) to the ``NumberInput`` widget.

* Added basic support for ``<datalist>`` elements for suggestions in
  ``Input`` widgets.

* ``date``, ``datetime`` and ``time`` inputs are not localized anymore. The
  HTML5 spec requires the rendered values to be RFC3339-compliant and the
  browsers are in charge of localization. If you still want localized
  date/time inputs, use those provided by Django or override the
  ``_format_value()`` method of the relevant widgets.

1.0
~~~

* cleaned up the behaviour of ``attrs``
* compatible with Django 1.3 and 1.4
* ``<optgroup>`` support in select widgets
* ``Select`` widgets: renamed ``choices`` context variable to ``optgroups``.
  This is **backwards-incompatible**: if you have custom templates for
  ``Select`` widgets, they need to be updated.
* ``get_context()`` is more reliable
* Added ``form``, ``formrow``, ``formfield``, ``formconfig`` and ``widget``
  template tags.
* Added template-based form layout system.
* Added ability to render widgets with the broader page context, for
  instance for django-sekizai compatibility.

0.4
~~~

* All widgets from Django have their floppyforms equivalent
* Added widgets for GeoDjango
