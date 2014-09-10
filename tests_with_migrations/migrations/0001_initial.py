# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_unsigned_fields.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignedModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignedToUnsignedModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnsignedModel',
            fields=[
                ('id', django_unsigned_fields.fields.UnsignedAutoField(serialize=False, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnsignedToSignedModel',
            fields=[
                ('id', django_unsigned_fields.fields.UnsignedAutoField(serialize=False, primary_key=True)),
                ('rel', django_unsigned_fields.fields.UnsignedManyToManyField(to_unsigned=False, to='tests_with_migrations.SignedModel', from_unsigned=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UnsignedToUnsignedModel',
            fields=[
                ('id', django_unsigned_fields.fields.UnsignedAutoField(serialize=False, primary_key=True)),
                ('rel', django_unsigned_fields.fields.UnsignedManyToManyField(to_unsigned=True, to='tests_with_migrations.UnsignedModel', from_unsigned=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='signedtounsignedmodel',
            name='rel',
            field=django_unsigned_fields.fields.UnsignedManyToManyField(to_unsigned=True, to='tests_with_migrations.UnsignedModel', from_unsigned=False),
            preserve_default=True,
        ),
    ]
