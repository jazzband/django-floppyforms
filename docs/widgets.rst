Provided widgets
================

Default widgets for form fields
-------------------------------

The first column represents the name of a django.forms field. FloppyForms aims
to implement all the Django fields with the same class name, in the
``floppyforms`` namespace. Some widgets and fields are missing but the appropriate
fields and widgets have been imported from the ``django.forms`` namespace.

======================== ================== ========================
Fields                   Widgets            Specificities
======================== ================== ========================
BooleanField             CheckboxInput
CharField                TextInput
ChoiceField              Select
DateField                DateInput          <input type="date">
DateTimeField            DateTimeInput      <input type="datetime">
DecimalField             NumberInput        <input type="number">
EmailField               EmailInput         <input type="email">
FileField                ClearableFileInput
FloatField               NumberInput        <input type="number">
ImageField               ClearableFileInput
IntegerField             NumberInput        <input type="number">
MultipleChoiceField      SelectMultiple
NullBooleanField         NullBooleanSelect
TimeField                TimeInput          <input type="time">
URLField                 URLInput           <input type="url">
======================== ================== ========================

.. note:: ClearableFileInput

    The ``ClearableFileInput`` widget has been added in Django 1.3. If you use
    django-floppyforms with Django 1.2, the ClearableFileInput will behave
    just like a traditional FileInput.

    The ``TypedMultipleChoiceField`` has also been added in Django 1.3 and is
    imported into the namespace if it is available.

The following fields have not yet been implemented:

* TypedChoiceField
* FilePathField
* IPAddressField
* TypedMultipleChoiceField
* RegexField
* SlugField
* ComboField
* MultiValueField
* SplitDateTimeField
* ModelChoiceField
* ModelMultipleChoiceField

The following widgets have not yet been implemented:

* MultiWidget
* MultipleHiddenInput
* SplitDateTimeWidget
* SelectDateWidget

Fields and widgets that are not implemented are aliased from ``django.forms``.
They are still usable from the ``floppyforms`` namespace but their rendering
can't be customized using the floppyforms concepts.


Other (HTML5) widgets
---------------------

Some HTML5 widgets are also provided, although browser support may not be
there yet:

* ``SearchInput``: a widget that renders ``<input type="search">``.
* ``ColorInput``: ``<input type="color">`` (not implemented in any browser
  yet).
* ``RangeInput``: ``<input type="range">``, for sliders instead of spinboxes
  for numbers.
* ``PhoneNumberInput``: ``<input type="tel">``. For phone numbers.
