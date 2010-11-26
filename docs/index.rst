Django-floppyforms
==================

Django-foppyforms is an application that gives you full control of the output
of forms rendering. This is more a **widgets** library than a forms library
but form fields are provided for convenience. The forms API and features are
exactly the same as Django's, the key difference is that widgets are rendered
in templates instead of using string interpolation.

The widgets API allows you to customize and extend the widgets behaviour,
making it very easy to define custom widgets. The default widgets are very
similar to the default Django widgets, except that they implement some nice
features of HTML5 forms, such as the ``placeholder`` and ``required``
attribute, as well as the new ``<input>`` types. For more information, read
`this`_ if you haven't yet.

.. _this: http://diveintohtml5.org/forms.html

The source code is hosted on `github`_.

.. _github: https://github.com/brutasse/django-floppyforms

Installation
-------------

Django 1.2 or greater is required because of the smart *if* template tag.
Two-step process:

* ``pip install -e git+git://github.com/brutasse/django-floppyforms.git#egg=floppyforms``
* Add ``floppyforms`` to your ``INSTALLED_APPS``

When you're done you can jump to the :doc:`usage <usage>` section.

.. toctree::
   :maxdepth: 2

   usage
   widgets
   customization
   widgets-reference

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

