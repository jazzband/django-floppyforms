# -*- coding: utf-8 -*-
import codecs
import re
from os import path
from distutils.core import setup
from setuptools import find_packages


def read(*parts):
    return codecs.open(path.join(path.dirname(__file__), *parts),
                       encoding='utf-8').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-floppyforms',
    version=find_version('floppyforms', '__init__.py'),
    author=u'Bruno Renié',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/gregmuellegger/django-floppyforms',
    license='BSD licence, see LICENSE file',
    description='Full control of form rendering in the templates',
    long_description=u'\n\n'.join((
        read('README.rst'),
        read('CHANGES.rst'))),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False,
)
