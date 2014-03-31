django-floppyforms
==================

.. image:: https://api.travis-ci.org/gregmuellegger/django-floppyforms.png
   :alt: Build Status
   :target: https://travis-ci.org/gregmuellegger/django-floppyforms

Full control of form rendering in the templates.

* Author: Bruno Renié and `contributors`_
* Licence: BSD
* Requirements: homework -- read `this`_.

.. _contributors: https://github.com/gregmuellegger/django-floppyforms/contributors
.. _this: http://diveintohtml5.info/forms.html

Installation
------------

* ``pip install -U django-floppyforms``
* Add ``floppyforms`` to your ``INSTALLED_APPS``

For extensive documentation see the ``docs`` folder or `read it on
readthedocs`_

.. _read it on readthedocs: http://django-floppyforms.readthedocs.org/

To install the `in-development version`_ of django-floppyforms, run ``pip
install django-floppyforms==dev``.

.. _in-development version: https://github.com/gregmuellegger/django-floppyforms/tarball/master#egg=django-floppyforms-dev

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

    git clone git@github.com:gregmuellegger/django-floppyforms.git
    cd django-floppyforms
    virtualenv -p python2 env
    source env/bin/activate
    add2virtualenv .

Install the development requirements::

    pip install tox

Run the tests::

    tox -e py27-1.6

You can see all the supported test configurations with ``tox -l``.
