from __future__ import unicode_literals

from django.conf import settings
from django.core import exceptions
from django.db import connection as default_connection
from django.db.models import fields
from django.db.models.fields.related import (
    OneToOneField,
    ManyToManyField,
    add_lazy_relation,
    ReverseManyRelatedObjectsDescriptor,
    RECURSIVE_RELATIONSHIP_CONSTANT,
)
from django.utils.translation import ugettext as _
from django.utils.functional import curry

from django_unsigned_fields.compat import six

KILOBYTES = 1024
MEGABYTES = 1024 * KILOBYTES
GIGABYTES = 1024 * MEGABYTES

REWARDS_IMAGE_MAX_UPLOAD_SIZE = 5 * MEGABYTES


def create_many_to_many_intermediary_model(field, klass):
    """
    This function is a large copy/paste from django in order to construct
    correct through tables for `ManyToManyField` relationships.
    """
    from django.db import models
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
    # Construct and return the new class.
    return type(str(name), (models.Model,), {
        'Meta': meta,
        '__module__': klass.__module__,
        from_: models.UnsignedForeignKey(klass, related_name='%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint),
        to: models.UnsignedForeignKey(to_model, related_name='%s+' % name, db_tablespace=field.db_tablespace, db_constraint=field.rel.db_constraint)
    })


class UnsignedManyToManyField(ManyToManyField):
    def contribute_to_class(self, cls, name):
        # To support multiple relations to self, it's useful to have a non-None
        # related name on symmetrical relations for internal reasons. The
        # concept doesn't make a lot of sense externally ("you want me to
        # specify *what* on my non-reversible relation?!"), so we set it up
        # automatically. The funky name reduces the chance of an accidental
        # clash.
        if self.rel.symmetrical and (self.rel.to == "self" or self.rel.to == cls._meta.object_name):
            self.rel.related_name = "%s_rel_+" % name

        super(UnsignedManyToManyField, self).contribute_to_class(cls, name)

        # The intermediate m2m model is not auto created if:
        #  1) There is a manually specified intermediate, or
        #  2) The class owning the m2m field is abstract.
        #  3) The class owning the m2m field has been swapped out.
        if not self.rel.through and not cls._meta.abstract and not cls._meta.swapped:
            self.rel.through = create_many_to_many_intermediary_model(self, cls)

        # Add the descriptor for the m2m relation
        setattr(cls, self.name, ReverseManyRelatedObjectsDescriptor(self))

        # Set up the accessor for the m2m table name for the relation
        self.m2m_db_table = curry(self._get_m2m_db_table, cls._meta)

        # Populate some necessary rel arguments so that cross-app relations
        # work correctly.
        if isinstance(self.rel.through, six.string_types):
            def resolve_through_model(field, model, cls):
                field.rel.through = model
            add_lazy_relation(cls, self, self.rel.through, resolve_through_model)


class UnsignedIntegerField(fields.IntegerField):
    def db_type(self, connection=None):
        connection = connection or default_connection
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
            return "integer UNSIGNED"
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            return 'integer'
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return 'bigint'
        else:
            raise NotImplementedError

    def get_internal_type(self):
        return "UnsignedIntegerField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return value
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be an unsigned integer."))


class UnsignedAutoField(fields.AutoField):
    def db_type(self, connection=None):
        connection = connection or default_connection
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
            return "integer UNSIGNED AUTO_INCREMENT"
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            return 'integer'
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
            return 'bigserial'
        else:
            raise NotImplementedError

    def get_internal_type(self):
        return "UnsignedAutoField"

    def to_python(self, value):
        if value is None:
            return value
        try:
            return value
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                _("This value must be a long integer."))


class UnsignedForeignKey(fields.related.ForeignKey):
    def db_type(self, connection=None):
        connection = connection or default_connection
        rel_field = self.rel.get_related_field()
        # next lines are the "bad tooth" in the original code:
        if (isinstance(rel_field, UnsignedAutoField) or
            (not connection.features.related_fields_match_type and
             isinstance(rel_field, UnsignedIntegerField))):
            # because it continues here in the django code:
            # return IntegerField().db_type()
            # thereby fixing any AutoField as IntegerField
            return UnsignedIntegerField().db_type()
        return rel_field.db_type(connection)


class UnsignedOneToOneField(UnsignedForeignKey, OneToOneField):
    """
    If you use subclass model, you might need to name
    the `ptr` field explicitly. This is the field type you
    might want to use. Here is an example:

    class Base(models.Model):
        title = models.CharField(max_length=40, verbose_name='Title')

    class Concrete(Base):
        base_ptr = fields.BigOneToOneField(Base)
        ext = models.CharField(max_length=12, null=True, verbose_name='Ext')
    """
    pass


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedIntegerField$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedAutoField$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedForeignKey$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedOneToOneField$'],
    )
    add_introspection_rules(
        rules=[],
        patterns=[r'^django_unsigned_fields\.fields\.UnsignedManyToManyField$'],
    )
except ImportError:
    pass
