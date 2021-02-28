# Generated by Django 3.1.7 on 2021-02-26 15:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.SlugField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.SlugField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.carmake')),
            ],
        ),
        migrations.CreateModel(
            name='CarSubmodel',
            fields=[
                ('id', models.SlugField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.carmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2050)])),
                ('mileage', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('body_type', models.PositiveIntegerField(blank=True, null=True)),
                ('transmission', models.PositiveIntegerField(blank=True, null=True)),
                ('fuel_type', models.PositiveIntegerField(blank=True, null=True)),
                ('exterior_color', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.carmake')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.carmodel')),
                ('submodel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.carsubmodel')),
            ],
        ),
    ]
