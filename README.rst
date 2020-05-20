django-floppyforms
==================

.. image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband

.. image:: https://api.travis-ci.org/jazzband/django-floppyforms.png
   :alt: Build Status
   :target: https://travis-ci.org/jazzband/django-floppyforms

Full control of form rendering in the templates.

* Authors: Gregor Müllegger and many many `contributors`_
* Original creator: Bruno Renié started this project and kept it going for many years.
* Licence: BSD
* Requirements: homework -- read `this`_.

.. _contributors: https://github.com/jazzband/django-floppyforms/contributors
.. _this: http://diveintohtml5.info/forms.html

Installation
------------

* ``pip install -U django-floppyforms``
* Add ``floppyforms`` to your ``INSTALLED_APPS``

For those who want to mix and match with vanilla Django widgets, it is also recommended
to put Django's form template directory into your template directories::

    # in your template configuration
    TEMPLATES = [{
        ...,
        # inside the directories parameter
        'DIRS': [
            # include django's form templates
            os.path.join(
                os.path.dirname(django.__file__), "forms/templates/"
            ),
            ... # the rest of your template directories
    }]

For extensive documentation see the ``docs`` folder or `read it on
readthedocs`_

.. _read it on readthedocs: http://django-floppyforms.readthedocs.org/

To install the `in-development version`_ of django-floppyforms, run ``pip
install "https://github.com/jazzband/django-floppyforms/tarball/master#egg=django-floppyforms"``.

.. _in-development version: https://github.com/jazzband/django-floppyforms

Help
----

Create a ticket in the `issues section on github`_ or ask your questions on the
#django-floppyforms IRC channel on freenode.

You can get professional consulting regarding django-floppyforms or any other
Django related work from django-floppyforms' maintainer `Gregor Müllegger`_.

.. _issues section on github: https://github.com/jazzband/django-floppyforms/issues
.. _Gregor Müllegger: http://gremu.net/

Bugs
----

Really? Oh well... Please Report. Or better, fix :) We are happy to help you
through the process of fixing and testing a bug. Just get in touch.

Development
-----------

Thanks for asking!

Get the code::

    git clone git@github.com:jazzband/django-floppyforms.git
    cd django-floppyforms
    virtualenv env
    source env/bin/activate
    add2virtualenv .

Install the development requirements::

    pip install "tox>=1.8"


Currently, you'll need to `install the GeoDjango requirements`_ when running tests.

.. _install the GeoDjango requirements: https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/geolibs/

Run the tests::

    tox
    tox -e py36-22

You can see all the supported test configurations with ``tox -l``.
