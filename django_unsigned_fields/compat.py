import django

try:
    from django.utils import six
except ImportError:
    from . import six  # NOQA

RECURSIVE_RELATIONSHIP_CONSTANT = 'self'

if django.VERSION[1] == 7:
    def create_many_to_many_intermediary_model(field, klass):
        """
        This function is a large copy/paste from django in order to construct
        correct through tables for `ManyToManyField` relationships.
        """
        from django.db import models
        from django_unsigned_fields.fields import UnsignedForeignKey
        from django.db.models.fields.related import (
            add_lazy_relation,
            RECURSIVE_RELATIONSHIP_CONSTANT,
        )
        managed = True
        if isinstance(field.rel.to, six.string_types) and field.rel.to != RECURSIVE_RELATIONSHIP_CONSTANT:
            to_model = field.rel.to
            to = to_model.split('.')[-1]

            def set_managed(field, model, cls):
                field.rel.through._meta.managed = model._meta.managed or cls._meta.managed
            add_lazy_relation(klass, field, to_model, set_managed)
        elif isinstance(field.rel.to, six.string_types):
            to = klass._meta.object_name
            to_model = klass
            managed = klass._meta.managed
        else:
            to = field.rel.to._meta.object_name
            to_model = field.rel.to
            managed = klass._meta.managed or to_model._meta.managed
        name = '%s_%s' % (klass._meta.object_name, field.name)
        if field.rel.to == RECURSIVE_RELATIONSHIP_CONSTANT or to == klass._meta.object_name:
            from_ = 'from_%s' % to.lower()
            to = 'to_%s' % to.lower()
        else:
            from_ = klass._meta.model_name
            to = to.lower()
        meta = type(str('Meta'), (object,), {
            'db_table': field._get_m2m_db_table(klass._meta),
            'managed': managed,
            'auto_created': klass,
            'app_label': klass._meta.app_label,
            'db_tablespace': klass._meta.db_tablespace,
            'unique_together': (from_, to),
            'verbose_name': '%(from)s-%(to)s relationship' % {'from': from_, 'to': to},
            'verbose_name_plural': '%(from)s-%(to)s relationships' % {'from': from_, 'to': to},
            'apps': field.model._meta.apps,
        })
        to_field_klass = UnsignedForeignKey if field.to_unsigned else models.ForeignKey
        from_field_klass = UnsignedForeignKey if field.from_unsigned else models.ForeignKey
        # Construct and return the new class.
        return type(str(name), (models.Model,), {
            'Meta': meta,
            '__module__': klass.__module__,
            from_: from_field_klass(klass, related_name='%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint),
            to: to_field_klass(to_model, related_name='%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint)
        })
elif django.VERSION[1] == 6:
    def create_many_to_many_intermediary_model(field, klass):
        from django.db import models
        from django_unsigned_fields.fields import UnsignedForeignKey
        from django.db.models.fields.related import (
            add_lazy_relation,
            RECURSIVE_RELATIONSHIP_CONSTANT,
        )
        managed = True
        if isinstance(field.rel.to, six.string_types) and field.rel.to != RECURSIVE_RELATIONSHIP_CONSTANT:
            to_model = field.rel.to
            to = to_model.split('.')[-1]

            def set_managed(field, model, cls):
                field.rel.through._meta.managed = model._meta.managed or cls._meta.managed
            add_lazy_relation(klass, field, to_model, set_managed)
        elif isinstance(field.rel.to, six.string_types):
            to = klass._meta.object_name
            to_model = klass
            managed = klass._meta.managed
        else:
            to = field.rel.to._meta.object_name
            to_model = field.rel.to
            managed = klass._meta.managed or to_model._meta.managed
        name = '%s_%s' % (klass._meta.object_name, field.name)
        if field.rel.to == RECURSIVE_RELATIONSHIP_CONSTANT or to == klass._meta.object_name:
            from_ = 'from_%s' % to.lower()
            to = 'to_%s' % to.lower()
        else:
            from_ = klass._meta.model_name
            to = to.lower()
        meta = type('Meta', (object,), {
            'db_table': field._get_m2m_db_table(klass._meta),
            'managed': managed,
            'auto_created': klass,
            'app_label': klass._meta.app_label,
            'db_tablespace': klass._meta.db_tablespace,
            'unique_together': (from_, to),
            'verbose_name': '%(from)s-%(to)s relationship' % {'from': from_, 'to': to},
            'verbose_name_plural': '%(from)s-%(to)s relationships' % {'from': from_, 'to': to},
        })
        # Construct and return the new class.
        to_field_klass = UnsignedForeignKey if field.to_unsigned else models.ForeignKey
        from_field_klass = UnsignedForeignKey if field.from_unsigned else models.ForeignKey
        return type(str(name), (models.Model,), {
            'Meta': meta,
            '__module__': klass.__module__,
            from_: from_field_klass(klass, related_name='%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint),
            to: to_field_klass(to_model, related_name='%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint)
        })
elif django.VERSION[1] <= 5:
    def create_many_to_many_intermediary_model(field, klass):
        from django.db import models
        from django_unsigned_fields.fields import UnsignedForeignKey
        from django.db.models.fields.related import (
            add_lazy_relation,
            RECURSIVE_RELATIONSHIP_CONSTANT,
        )
        managed = True
        if isinstance(field.rel.to, six.string_types) and field.rel.to != RECURSIVE_RELATIONSHIP_CONSTANT:
            to_model = field.rel.to
            to = to_model.split('.')[-1]

            def set_managed(field, model, cls):
                field.rel.through._meta.managed = model._meta.managed or cls._meta.managed
            add_lazy_relation(klass, field, to_model, set_managed)
        elif isinstance(field.rel.to, six.string_types):
            to = klass._meta.object_name
            to_model = klass
            managed = klass._meta.managed
        else:
            to = field.rel.to._meta.object_name
            to_model = field.rel.to
            managed = klass._meta.managed or to_model._meta.managed
        name = '%s_%s' % (klass._meta.object_name, field.name)
        if field.rel.to == RECURSIVE_RELATIONSHIP_CONSTANT or to == klass._meta.object_name:
            from_ = 'from_%s' % to.lower()
            to = 'to_%s' % to.lower()
        else:
            from_ = klass._meta.object_name.lower()
            to = to.lower()
        meta = type('Meta', (object,), {
            'db_table': field._get_m2m_db_table(klass._meta),
            'managed': managed,
            'auto_created': klass,
            'app_label': klass._meta.app_label,
            'db_tablespace': klass._meta.db_tablespace,
            'unique_together': (from_, to),
            'verbose_name': '%(from)s-%(to)s relationship' % {'from': from_, 'to': to},
            'verbose_name_plural': '%(from)s-%(to)s relationships' % {'from': from_, 'to': to},
        })
        # Construct and return the new class.
        to_field_klass = UnsignedForeignKey if field.to_unsigned else models.ForeignKey
        from_field_klass = UnsignedForeignKey if field.from_unsigned else models.ForeignKey
        return type(str(name), (models.Model,), {
            'Meta': meta,
            '__module__': klass.__module__,
            from_: from_field_klass(klass, related_name='%s+' % name, db_tablespace=field.db_tablespace),
            to: to_field_klass(to_model, related_name='%s+' % name, db_tablespace=field.db_tablespace)
        })
