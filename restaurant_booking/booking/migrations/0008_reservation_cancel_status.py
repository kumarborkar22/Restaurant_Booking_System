# Generated by Django 5.1.7 on 2025-03-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_remove_table_is_booked'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='cancel_status',
            field=models.BooleanField(default=False),
        ),
    ]
