from __future__ import unicode_literals

from django.test import TestCase

from tests_with_migrations.models import (
    UnsignedModel, SignedModel,
    UnsignedToSignedModel,
    SignedToUnsignedModel,
    UnsignedToUnsignedModel,
)


class NormalToUnsignedTest(TestCase):
    def test_relationship(self):
        unsigned = UnsignedModel.objects.create()
        signed = SignedToUnsignedModel.objects.create()

        self.assertFalse(SignedToUnsignedModel.objects.filter(
            rel=unsigned,
        ).exists())

        signed.rel.add(unsigned)

        self.assertTrue(SignedToUnsignedModel.objects.filter(
            rel=unsigned,
        ).exists())


class UnsignedToNormalTest(TestCase):
    def test_relationship(self):
        signed = SignedModel.objects.create()
        unsigned = UnsignedToSignedModel.objects.create()

        self.assertFalse(UnsignedToSignedModel.objects.filter(
            rel=signed,
        ).exists())

        unsigned.rel.add(signed)

        self.assertTrue(UnsignedToSignedModel.objects.filter(
            rel=signed,
        ).exists())


class UnsignedToUnsignedTest(TestCase):
    def test_relationship(self):
        unsigned = UnsignedModel.objects.create()
        other_unsigned = UnsignedToUnsignedModel.objects.create()

        self.assertFalse(UnsignedToUnsignedModel.objects.filter(
            rel=unsigned,
        ).exists())

        other_unsigned.rel.add(unsigned)

        self.assertTrue(UnsignedToUnsignedModel.objects.filter(
            rel=unsigned,
        ).exists())
