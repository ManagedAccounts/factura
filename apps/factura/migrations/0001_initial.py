# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ruc', models.IntegerField(unique=True, max_length=11)),
                ('razon_social', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cantidad', models.IntegerField()),
                ('impuesto', models.DecimalField(max_digits=6, decimal_places=2)),
                ('subtotal', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serie', models.IntegerField(max_length=3)),
                ('numero', models.CharField(unique=True, max_length=6)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.IntegerField(null=True, blank=True)),
                ('cliente', models.ForeignKey(to='factura.Cliente')),
                ('vendedor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.IntegerField()),
                ('number', models.IntegerField()),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.TextField(max_length=300)),
                ('imagen', models.ImageField(null=True, upload_to=b'productos/', blank=True)),
                ('precio', models.DecimalField(max_digits=6, decimal_places=2)),
                ('afecto', models.BooleanField(default=False)),
                ('igv', models.DecimalField(max_digits=6, decimal_places=2)),
                ('stock', models.IntegerField()),
                ('estado', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(to='factura.CategoriaProducto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='factura',
            field=models.ForeignKey(to='factura.Factura', db_column=b'factura_id'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detallefactura',
            name='producto',
            field=models.ForeignKey(to='factura.Producto', db_column=b'producto_id'),
            preserve_default=True,
        ),
    ]
