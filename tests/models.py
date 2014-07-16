from __future__ import unicode_literals

from django.db import models

from django_unsigned_fields.fields import (
    UnsignedManyToManyField, UnsignedForeignKey,
    UnsignedOneToOneField, UnsignedAutoField,
)


class ManyToManyModel(models.Model):
    id = UnsignedAutoField(primary_key=True)


class TargetModel(models.Model):
    id = UnsignedAutoField(primary_key=True)


class SourceModel(models.Model):
    id = UnsignedAutoField(primary_key=True)
    target = UnsignedForeignKey(TargetModel, null=True, related_name='sources',
                                blank=True)

    manys = UnsignedManyToManyField(ManyToManyModel, related_name='sources',
                                    blank=True)


class OneToOneModel(models.Model):
    id = UnsignedAutoField(primary_key=True)
    source = UnsignedOneToOneField(SourceModel)
