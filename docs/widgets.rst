Provided widgets
================

Default widgets for form fields
-------------------------------

The first column represents the name of a django.forms field. FloppyForms aims
to implement all the Django fields with the same class name, in the
``floppyforms`` namespace. Some widgets are missing but you can safely use the
widgets from ``django.forms`` if you need them.

======================== =================
Fields                   Widgets
======================== =================
BooleanField             CheckboxInput
CharField                TextInput
ChoiceField              Select
TypedChoiceField         Not implemented
DateField                DateInput
DateTimeField            DateTimeInput
DecimalField             NumberInput
EmailField               EmailInput
FileField                FileInput
FilePathField            Not implemented
FloatField               NumberInput
ImageField               Not implemented
IntegerField             NumberInput
IPAddressField           Not implemented
MultipleChoiceField      SelectMultiple
NullBooleanField         NullBooleanSelect
RegexField               Not implemented
SlugField                Not implemented
TimeField                TimeInput
URLField                 URLInput
ComboField               Not implemented
MultiValueField          Not implemented
SplitDateTimeField       Not implemented
ModelChoiceField         Not implemented
ModelMultipleChoiceField Not implemented
======================== =================

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
