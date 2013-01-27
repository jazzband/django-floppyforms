Django-floppyforms
==================

.. image:: https://api.travis-ci.org/brutasse/django-floppyforms.png
   :alt: Build Status
   :target: https://travis-ci.org/brutasse/django-floppyforms

Full control of form rendering in the templates.

* Author: Bruno Renié and `contributors`_
* Licence: BSD
* Compatibility: Django 1.3+
* Requirements: homework -- read `this`_.

.. _contributors: https://github.com/brutasse/django-floppyforms/contributors
.. _this: http://diveintohtml5.ep.io/forms.html

Installation
------------

* ``pip install -U django-floppyforms``
* Add ``floppyforms`` to your ``INSTALLED_APPS``

For extensive documentation see the ``docs`` folder or `read it on
readthedocs`_

.. _read it on readthedocs: http://django-floppyforms.readthedocs.org/

To install the `in-development version`_ of django-floppyforms, run ``pip
install django-floppyforms==dev``.

.. _in-development version: https://github.com/brutasse/django-floppyforms/tarball/master#egg=django-floppyforms-dev

Help
----

Ask your questions on the #django-floppyforms IRC channel on freenode.

Bugs
----

Really? Oh well... Please Report. Or better, fix :)

Development
-----------

Thanks for asking!

Get the code::

    git clone git@github.com:brutasse/django-floppyforms.git
    cd django-floppyforms
    virtualenv -p python2 env
    source env/bin/activate
    add2virtualenv .

Install the development requirements::

    pip install -r requirements/tests.txt
    pip install django  # must be django 1.3 or above

Run the tests::

    DJANGO_SETTINGS_MODULE=floppyforms.test_settings make test
