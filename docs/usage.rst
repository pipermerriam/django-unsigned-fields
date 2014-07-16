========
Usage
========

To use django-unsigned-fields in a project::


.. code-block:: python

    from django_unsigned_fields.fields import UnsignedForeignKey

    class TargetModel(models.Model):
        id = UnsignedAutoField(primary_key=True)


    class SourceModel(models.Model):
        id = UnsignedAutoField(primary_key=True)
        target = UnsignedForeignKey(TargetModel)
