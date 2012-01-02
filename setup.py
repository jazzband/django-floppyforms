# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

VERSION = __import__('floppyforms').__version__


setup(
    name='django-floppyforms',
    version=VERSION,
    author='Bruno Renie',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/brutasse/django-floppyforms',
    license='BSD licence, see LICENCE file',
    description='Full control of form rendering in the templates',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    test_suite='runtests.runtests',
    zip_safe=False,
)
