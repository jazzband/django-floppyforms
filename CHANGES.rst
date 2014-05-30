Changelog
---------

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

  This feature will become the default behaviour in floppyforms 1.3.

  See the documentation for more information:
  http://django-floppyforms.readthedocs.org/en/latest/usage.html#modelforms

* If you added an attribute with value 1 to the attrs kwargs (e.g. ``{'value':
  1}``, you would get no attribute value in the rendered html (e.g. ``value``
  instead of ``value="1"``). That's fixed now, thanks to Viktor Ershov for the
  report.
