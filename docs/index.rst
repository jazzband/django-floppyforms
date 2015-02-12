django-floppyforms
==================

**django-floppyforms** is an application that gives you full control of the
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

.. _github: https://github.com/gregmuellegger/django-floppyforms

Installation
------------

As a requirement of django-floppyforms, you will need to have Django in
version 1.4 or higher installed and use Python 2.6 or newer.  Python 3 and
PyPy are supported!

Two-step process to install django-floppyforms:

* ``pip install django-floppyforms``
* Add ``'floppyforms'`` to your ``INSTALLED_APPS``

When you're done you can jump to the :doc:`usage <usage>` section. For the
impatient reader, there's also an :doc:`examples <examples>` section.

Using ``django-floppyforms``
----------------------------

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

.. toctree::
   :maxdepth: 2

   changelog

Getting help
------------

Feel free to join the ``#django-floppyforms`` IRC channel on freenode.

Why the name?
-------------

* There aren't enough packages with silly names in the Django community. So,
  here's one more.
* The name reflects the idea that a widget can take any kind of shape, if that
  makes any sense.

Performance
-----------

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
    print "django-floppyforms:", time(flop)

The result varies if you're doing template caching or not. To put it simply,
here is the average time for a single iteration on a MacBookPro @ 2.53GHz.

================== ============================= ===========================
Method             Time without template caching Time with template caching
================== ============================= ===========================
Plain Django       1.63973999023 msec            1.6320669651 msec
django-floppyforms 9.05481505394 msec            3.0161819458 msec
================== ============================= ===========================

Even with template caching, the rendering time is doubled. However the impact
is probably not noticeable since rendering the form above takes 3
milliseconds instead of 1.6: **it still takes no time :)**. The use of
template caching in production is, of course, encouraged.
