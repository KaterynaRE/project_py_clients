# Generated by Django 5.2 on 2025-05-17 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_medicalhistory_treatment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='qualifications', to='core.doctor'),
        ),
    ]
