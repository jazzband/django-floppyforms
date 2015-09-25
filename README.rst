django-floppyforms
==================

.. image:: https://api.travis-ci.org/gregmuellegger/django-floppyforms.png
   :alt: Build Status
   :target: https://travis-ci.org/gregmuellegger/django-floppyforms

Full control of form rendering in the templates.

* Authors: Gregor Müllegger and many many `contributors`_
* Original creator: Bruno Renié started this project and kept it going for many years.
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
install "https://github.com/gregmuellegger/django-floppyforms/tarball/master#egg=django-floppyforms"``.

.. _in-development version: https://github.com/gregmuellegger/django-floppyforms

Help
----

Create a ticket in the `issues section on github`_ or ask your questions on the
#django-floppyforms IRC channel on freenode.

You can get professional consulting regarding django-floppyforms or any other
Django related work from django-floppyforms' maintainer `Gregor Müllegger`_.

.. _issues section on github: https://github.com/gregmuellegger/django-floppyforms/issues
.. _Gregor Müllegger: http://gremu.net/

Bugs
----

Really? Oh well... Please Report. Or better, fix :) We are happy to help you
through the process of fixing and testing a bug. Just get in touch.

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

    pip install "tox>=1.8"

Run the tests::

    tox -e py27-16

You can see all the supported test configurations with ``tox -l``.
