# Generated by Django 5.1.7 on 2025-03-19 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_remove_table_is_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]
