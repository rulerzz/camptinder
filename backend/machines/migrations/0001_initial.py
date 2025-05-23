# Generated by Django 5.1.6 on 2025-03-25 10:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        ('organizations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('battery_level', models.IntegerField(blank=True, null=True)),
                ('alarm_battery_level', models.IntegerField(blank=True, null=True)),
                ('temp_level', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('serial_number', models.CharField(max_length=100, unique=True)),
                ('last_maintenance', models.DateField(blank=True, null=True)),
                ('production_data', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('area_code', models.CharField(blank=True, max_length=20)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.location')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('area_code', 'serial_number'), name='uq_area_code_serial_number')],
            },
        ),
    ]
