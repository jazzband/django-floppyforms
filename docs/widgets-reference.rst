Widgets reference
=================

For each widgets, the default class attributes.

.. module:: floppyforms.widgets
   :synopsis: FloppyForm's form widgets

.. class:: Input

    .. attribute:: Input.datalist

        A list of possible values, which will be rendered as a ``<datalist>``
        element tied to the input. Note that the list of options passed as
        ``datalist`` elements are only **suggestions** and are not related to
        form validation.

    .. attribute:: Input.template_name

       A path to a template that should be used to render this widget. You can
       change the template name per instance by passing in a keyword argument
       called ``template_name``. This will override the default that is set by
       the widget class. You can also change the template used for rendering by
       an argument to the ``Input.render()`` method. See more about exchanging
       the templates in the :doc:`documentation about customization <customization>`.

.. class:: TextInput

    .. attribute:: TextInput.template_name

        ``'floppyforms/text.html'``

    .. attribute:: TextInput.input_type

        ``text``

.. class:: PasswordInput

    .. attribute:: PasswordInput.template_name

        ``'floppyforms/password.html'``

    .. attribute:: PasswordInput.input_type

        ``password``

.. class:: HiddenInput

    .. attribute:: HiddenInput.template_name

        ``'floppyforms/hidden.html'``

    .. attribute:: HiddenInput.input_type

        ``hidden``

.. class:: SlugInput

    .. attribute:: SlugInput.template_name

        ``'floppyforms/slug.html'``

    .. attribute:: SlugInput.input_type

        ``text``

    An text input that renders as ``<input pattern="[-\w]+" ...>`` for
    client-side validation of the slug.

.. class:: IPAddressInput

    .. attribute:: IPAddressInput.template_name

        ``'floppyforms/ipaddress.html'``

    .. attribute:: IPAddressInput.input_type

        ``text``

    An text input that renders as ``<input pattern="..." ...>`` for
    client-side validation. The pattern checks that the entered value is a
    valid IPv4 address.

.. class:: FileInput

    .. attribute:: FileInput.template_name

        ``'floppyforms/file.html'``

    .. attribute:: FileInput.input_type

        ``file``

.. class:: ClearableFileInput

    .. attribute:: ClearableFileInput.template_name

        ``'floppyforms/clearable_input.html'``

    .. attribute:: ClearableFileInput.input_type

        ``file``

    .. attribute:: ClearableFileInput.initial_text

        ``_('Currently')``

    .. attribute:: ClearableFileInput.input_text

        ``_('Change')``

    .. attribute:: ClearableFileInput.clear_checkbox_label

        ``_('Clear')``

    The ``initial_text``, ``input_text`` and ``clear_checkbox_label``
    attributes are provided in the template context.

.. class:: EmailInput

    .. attribute:: EmailInput.template_name

        ``'floppyforms/email.html'``

    .. attribute:: EmailInput.input_type

        ``email``

.. class:: URLInput

    .. attribute:: URLInput.template_name

        ``'floppyforms/url.html'``

    .. attribute:: URLInput.input_type

        ``url``

.. class:: SearchInput

    .. attribute:: SearchInput.template_name

        ``'floppyforms/search.html'``

    .. attribute:: SearchInput.input_type

        ``search``

.. class:: ColorInput

    .. attribute:: ColorInput.template_name

        ``'floppyforms/color.html'``

    .. attribute:: ColorInput.input_type

        ``color``

.. class:: PhoneNumberInput

    .. attribute:: PhoneNumberInput.template_name

        ``'floppyforms/phonenumber.html'``

    .. attribute:: PhoneNumberInput.input_type

        ``tel``

.. class:: DateInput

    .. attribute:: DateInput.template_name

        ``'floppyforms/date.html'``

    .. attribute:: DateInput.input_type

        ``date``

    A widget that renders as ``<input type="date" value="...">``. Value
    is rendered in ISO-8601 format (i.e. ``YYYY-MM-DD``) regardless of
    localization settings.


.. class:: DateTimeInput

    .. attribute:: DateTimeInput.template_name

        ``'floppyforms/datetime.html'``

    .. attribute:: DateTimeInput.input_type

        ``datetime``

.. class:: TimeInput

    .. attribute:: TimeInput.template_name

        ``'floppyforms/time.html'``

    .. attribute:: TimeInput.input_type

        ``time``

.. class:: NumberInput

    .. attribute:: NumberInput.template_name

        ``'floppyforms/number.html'``

    .. attribute:: NumberInput.input_type

        ``number``

    .. attribute:: NumberInput.min

        None

    .. attribute:: NumberInput.max

        None

    .. attribute:: NumberInput.step

        None

    ``min``, ``max`` and ``step`` are available in the ``attrs`` template
    variable if they are not None.

.. class:: RangeInput

    .. attribute:: NumberInput.template_name

        ``'floppyforms/range.html'``

    .. attribute:: RangeInput.input_type

        ``range``

    .. attribute:: RangeInput.min

        None

    .. attribute:: RangeInput.max

        None

    .. attribute:: RangeInput.step

        None

    ``min``, ``max`` and ``step`` are available in the ``attrs`` template
    variable if they are not None.

.. class:: Textarea

    .. attribute:: Textarea.template_name

        ``'floppyforms/textarea.html'``

    .. attribute:: Textarea.rows

        10

    .. attribute:: Textarea.cols

        40

    ``rows`` and ``cols`` are available in the ``attrs`` variable.

.. class:: CheckboxInput

    .. attribute:: CheckboxInput.template_name

        ``'floppyforms/checkbox.html'``

    .. attribute:: CheckboxInput.input_type

        ``checkbox``

.. class:: Select

    .. attribute:: Select.template_name

        ``'floppyforms/select.html'``

.. class:: NullBooleanSelect

    .. attribute:: NullBooleanSelect.template_name

        ``'floppyforms/select.html'``

.. class:: RadioSelect

    .. attribute:: RadioSelect.template_name

        ``'floppyforms/radio.html'``

.. class:: SelectMultiple

    .. attribute:: SelectMultiple.template_name

        ``'floppyforms/select_multiple.html'``

.. class:: CheckboxSelectMultiple

    .. attribute:: CheckboxSelectMultiple.template_name

        ``'floppyforms/checkbox_select.html'``

.. class:: MultiWidget

   The same as ``django.forms.widgets.MultiWidget``. The rendering can be
   customized by overriding ``format_output``, which joins all the rendered
   widgets.

.. class:: SplitDateTimeWidget

    Displays a ``DateInput`` and a ``TimeInput`` side by side.

.. class:: MultipleHiddenInput

    A multiple <input type="hidden"> for fields that have several values.

.. class:: SelectDateWidget

    A widget that displays three ``<select>`` boxes, for the year, the month
    and the date.

    Available context:

    * ``year_field``: the name for the year's ``<select>`` box.
    * ``month_field``: the name for the month's ``<select>`` box.
    * ``day_field``: the name for the day's ``<select>`` box.

    .. attribute:: SelectDateWidget.template_name

        The template used to render the widget. Default:
        ``'floppyforms/select_date.html'``.

    .. attribute:: SelectDateWidget.none_value

        A tuple representing the value to display when there is no initial
        value. Default: ``(0, '---')``.

    .. attribute:: SelectDateWidget.day_field

        The way the day field's name is derived from the widget's name.
        Default: ``'%s_day'``.

    .. attribute:: SelectDateWidget.month_field

        The way the month field's name is derived. Default: ``'%s_month'``.

    .. attribute:: SelectDateWidget.year_field

        The way the year field's name is derived. Default: ``'%s_year'``.
