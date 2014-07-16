from __future__ import unicode_literals

from django.test import TestCase

from tests.models import (
    SourceModel, TargetModel, OneToOneModel, ManyToManyModel,
)


class UnsignedForeignKeyTest(TestCase):
    def test_relationship(self):
        target = TargetModel.objects.create()

        source_a = SourceModel.objects.create(target=target)
        source_b = SourceModel.objects.create(target=target)
        # no target
        source_c = SourceModel.objects.create()

        self.assertEqual(source_a.target, target)
        self.assertEqual(source_b.target, target)

        self.assertEqual(target.sources.count(), 2)

        self.assertIn(source_a, target.sources.all())
        self.assertIn(source_b, target.sources.all())
        self.assertNotIn(source_c, target.sources.all())


class OneToOneTest(TestCase):
    def test_relationship(self):
        source = SourceModel.objects.create()
        o2o = OneToOneModel.objects.create(source=source)

        self.assertEqual(o2o.source, source)
        # test reverse
        self.assertEqual(source.onetoonemodel, o2o)

    def test_no_one_to_one(self):
        source = SourceModel.objects.create()

        with self.assertRaises(OneToOneModel.DoesNotExist):
            source.onetoonemodel


class UnsignedManyToManyFieldTest(TestCase):
    def test_relationship(self):
        source = SourceModel.objects.create()

        m2m_a = ManyToManyModel.objects.create()
        m2m_b = ManyToManyModel.objects.create()

        source.manys.add(m2m_a)

        self.assertIn(m2m_a, source.manys.all())
        self.assertNotIn(m2m_b, source.manys.all())

        # test other side of the m2m
        self.assertIn(source, m2m_a.sources.all())
        self.assertNotIn(source, m2m_b.sources.all())
