from django.db import models

from django_unsigned_fields.fields import (
    UnsignedManyToManyField,
    UnsignedAutoField,
)


class UnsignedModel(models.Model):
    id = UnsignedAutoField(primary_key=True)


class SignedModel(models.Model):
    pass


class SignedToUnsignedModel(models.Model):
    rel = UnsignedManyToManyField(UnsignedModel, from_unsigned=False)


class UnsignedToSignedModel(models.Model):
    id = UnsignedAutoField(primary_key=True)
    rel = UnsignedManyToManyField(SignedModel, to_unsigned=False)


class UnsignedToUnsignedModel(models.Model):
    id = UnsignedAutoField(primary_key=True)
    rel = UnsignedManyToManyField(UnsignedModel)
