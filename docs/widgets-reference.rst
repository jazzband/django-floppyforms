Widgets reference
=================

For each widgets, the default class attributes.

.. module:: floppyforms.widgets
   :synopsis: FloppyForm's form widgets

.. class:: TextInput

    .. attribute:: TextInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: TextInput.input_type
    
        ``text``

.. class:: PasswordInput

    .. attribute:: PasswordInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: PasswordInput.input_type
    
        ``password``

.. class:: HiddenInput

    .. attribute:: HiddenInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: HiddenInput.input_type
    
        ``hidden``

.. class:: FileInput

    .. attribute:: FileInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: FileInput.input_type
    
        ``file``

.. class:: ClearableFileInput

    .. attribute:: ClearableFileInput.template_name
    
        ``'floppyforms/input.html'``

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
    
        ``'floppyforms/input.html'``

    .. attribute:: EmailInput.input_type
    
        ``email``

.. class:: URLInput

    .. attribute:: URLInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: URLInput.input_type
    
        ``url``

.. class:: SearchInput

    .. attribute:: SearchInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: SearchInput.input_type
    
        ``search``

.. class:: ColorInput

    .. attribute:: ColorInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: ColorInput.input_type
    
        ``color``

.. class:: PhoneNumberInput

    .. attribute:: PhoneNumberInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: PhoneNumberInput.input_type
    
        ``tel``

.. class:: DateInput

    .. attribute:: DateInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: DateInput.input_type
    
        ``date``

.. class:: DateTimeInput

    .. attribute:: DateTimeInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: DateTimeInput.input_type
    
        ``datetime``

.. class:: TimeInput

    .. attribute:: TimeInput.template_name
    
        ``'floppyforms/input.html'``

    .. attribute:: TimeInput.input_type
    
        ``time``

.. class:: NumberInput

    .. attribute:: NumberInput.template_name
    
        ``'floppyforms/number_input.html'``

    .. attribute:: NumberInput.input_type
    
        ``number``

    .. attribute:: NumberInput.min

        None

    .. attribute:: NumberInput.max

        None

    .. attribute:: NumberInput.step

        None

    ``min``, ``max`` and ``step`` are available in the template context if
    they are not None.

.. class:: RangeInput

    .. attribute:: NumberInput.template_name
    
        ``'floppyforms/number_input.html'``

    .. attribute:: RangeInput.input_type
    
        ``range``

    .. attribute:: RangeInput.min

        None

    .. attribute:: RangeInput.max

        None

    .. attribute:: RangeInput.step

        None

    ``min``, ``max`` and ``step`` are available in the template context if
    they are not None.

.. class:: Textarea

    .. attribute:: Textarea.template_name
    
        ``'floppyforms/textarea.html'``

    .. attribute:: Textarea.rows
    
        10

    .. attribute:: Textarea.cols

        40

    ``rows`` and ``cols`` are available in the template context.

.. class:: CheckboxInput

    .. attribute:: CheckboxInput.template_name
    
        ``'floppyforms/input.html'``

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
    
        ``'floppyforms/select.html'``

.. class:: CheckboxSelectMultiple

    .. attribute:: CheckboxSelectMultiple.template_name
    
        ``'floppyforms/checkbox_select.html'``
