=============================
django-unsigned-fields
=============================

.. image:: https://badge.fury.io/py/django-unsigned-fields.png
    :target: https://badge.fury.io/py/django-unsigned-fields

.. image:: https://travis-ci.org/simpleenergy/django-unsigned-fields.png?branch=master
    :target: https://travis-ci.org/simpleenergy/django-unsigned-fields

.. image:: https://coveralls.io/repos/simpleenergy/django-unsigned-fields/badge.png?branch=master
    :target: https://coveralls.io/r/simpleenergy/django-unsigned-fields?branch=master

Django fields for using unsigned integers for relationships"

Documentation
-------------

The full documentation is at https://django-unsigned-fields.readthedocs.org.

Quickstart
----------

Install django-unsigned-fields::

    pip install django-unsigned-fields

Then use it in a project::

    import django-unsigned-fields

Features
--------

- :class:`django_unsigned_fields.fields.UnsignedAutoField`
- :class:`django_unsigned_fields.fields.UnsignedForeignKey`
- :class:`django_unsigned_fields.fields.UnsignedOneToOneField`
- :class:`django_unsigned_fields.fields.UnsignedManyToManyField`
