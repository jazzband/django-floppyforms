Django-floppyforms
==================

Django-floppyforms is an application that gives you full control of the
output of forms rendering. The forms API and features are exactly the same
as Django's, the key difference is that fields and widgets are rendered in
templates instead of using string interpolation, giving you full control of
the output using Django templates.

The widgets API allows you to customize and extend the widgets behaviour,
making it very easy to define custom widgets. The default widgets are very
similar to the default Django widgets, except that they implement some nice
features of HTML5 forms, such as the ``placeholder`` and ``required``
attribute, as well as the new ``<input>`` types. For more information, read
`this`_ if you haven't yet.

.. _this: http://diveintohtml5.info/forms.html

The form rendering API is a set of template tags that lets you render forms
using custom layouts. This is very similar to Django's ``as_p``, ``as_ul`` or
``as_table``, except that you can customize and add layouts to your
convenience.

The source code is hosted on `github`_.

.. _github: https://github.com/brutasse/django-floppyforms

Installation
------------

Django 1.3 or greater is required. Two-step process to install
django-floppyforms:

* ``pip install -U django-floppyforms``
* Add ``'floppyforms'`` to your ``INSTALLED_APPS``

When you're done you can jump to the :doc:`usage <usage>` section. For the
impatient reader, there's also an :doc:`examples <examples>` section.

.. toctree::
   :maxdepth: 2

   usage
   widgets
   customization
   widgets-reference
   geodjango
   layouts
   templatetags
   differences
   examples
   bootstrap

Additional notes
----------------

Help
````

Feel free to join the ``#django-floppyforms`` IRC channel on freenode.

Changelog
`````````

* **v1.0.1**:

  * Fixed ``Textarea`` widget template to work with a non-empty
    ``TEMPLATE_STRING_IF_INVALID`` setting. Thanks to Leon Matthews for the
    report.
  * Fixed context handling in widget rendering. It didn't take care of popping
    the context as often as it was pushed onto. This could cause strange
    behaviour in the template by leaking variables into outer scopes. Thanks to
    David Danier for the report.

* **v1.0**:

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

* **v0.4**:

  * All widgets from Django have their floppyforms equivalent
  * Added widgets for GeoDjango

Why the name?
`````````````

* There aren't enough packages with silly names in the Django community. So,
  here's one more.
* The name reflects the idea that a widget can take any kind of shape, if that
  makes any sense.

Performance
```````````

Each time a widget is rendered, there is a template inclusion. To what extent
does it affect performance? You can try with this little script:

.. code-block:: python

    import timeit

    django = """from django import forms

    class DjangoForm(forms.Form):
        text = forms.CharField()
        slug = forms.SlugField()
        some_bool = forms.BooleanField()
        email = forms.EmailField()
        date = forms.DateTimeField()
        file_ = forms.FileField()

    rendered = DjangoForm().as_p()"""

    flop = """import floppyforms as forms

    class FloppyForm(forms.Form):
        text = forms.CharField()
        slug = forms.SlugField()
        some_bool = forms.BooleanField()
        email = forms.EmailField()
        date = forms.DateTimeField()
        file_ = forms.FileField()

    rendered = FloppyForm().as_p()"""

    def time(stmt):
        t = timeit.Timer(stmt=stmt)
        return t.timeit(number=1000)

    print "Plain django:", time(django)
    print "Django-floppyforms:", time(flop)

The result varies if you're doing template caching or not. To put it simply,
here is the average time for a single iteration on a MacBookPro @ 2.53GHz.

================== ============================= ===========================
Method             Time without template caching Time with template caching
================== ============================= ===========================
Plain Django       1.63973999023 msec            1.6320669651 msec
Django-floppyforms 9.05481505394 msec            3.0161819458 msec
================== ============================= ===========================

Even with template caching, the rendering time is doubled. However the impact
is probably not noticeable since rendering the form above takes 3
milliseconds instead of 1.6: **it still takes no time :)**. The use of
template caching in production is, of course, encouraged.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

