Provided widgets
================

Default widgets for form fields
-------------------------------

The first column represents the name of a django.forms field. FloppyForms aims
to implement all the Django fields with the same class name, in the
``floppyforms`` namespace. Some widgets and fields are missing but the appropriate
fields and widgets have been imported from the ``django.forms`` namespace.

======================== =================== ========================
Fields                   Widgets             Specificities
======================== =================== ========================
BooleanField             CheckboxInput
CharField                TextInput
ComboField               TextInput
ChoiceField              Select
TypedChoiceField         Select
FilePathField            Select
ModelChoiceField         Select
DateField                DateInput           <input type="date">
DateTimeField            DateTimeInput       <input type="datetime">
DecimalField             NumberInput         <input type="number">
EmailField               EmailInput          <input type="email">
FileField                ClearableFileInput
FloatField               NumberInput         <input type="number">
ImageField               ClearableFileInput
IntegerField             NumberInput         <input type="number">
MultipleChoiceField      SelectMultiple
TypedMultipleChoiceField SelectMultiple
ModelMultipleChoiceField SelectMultiple
NullBooleanField         NullBooleanSelect
TimeField                TimeInput           <input type="time">
URLField                 URLInput            <input type="url">
SlugField                SlugInput           <input pattern="[-\\w]+">
RegexField               TextInput           <input [pattern=...]>
IPAddressField           IPAddressInput      <input pattern=...>
MultiValueField          None (*abstract*)
SplitDateTimeField       SplitDateTimeWidget
======================== =================== ========================

.. note:: ClearableFileInput

    The ``ClearableFileInput`` widget has been added in Django 1.3. If you use
    django-floppyforms with Django 1.2, the ClearableFileInput will behave
    just like a traditional FileInput.


.. note:: TypedMultipleChoiceField

    The ``TypedMultipleChoiceField`` has also been added in Django 1.3, it
    will behave like a normal ``MultipleChoiceField`` on Django 1.2.


.. note:: RegexField

    In Django, ``RegexField`` takes a required ``regex`` argument. The version
    shipped in floppyforms also takes an optional ``js_regex`` argument, for
    client-side validation of the regex. The ``js_regex`` must be a regex
    written in javascript syntax. Example::

        class RegexForm(forms.Form):
            re_field = forms.RegexField(r'^\d{3}-[a-z]+$',  # regex
                                        '\d{3}-[a-z]+')     # js_regex

    If you don't provide the ``js_regex`` argument, there will be no
    client-side validation of the field. Although the the two versions of the
    regex may be identical, the distinction allows you to pass compiled
    regexes as a ``regex`` argument.


The following widgets have not yet been implemented:

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
