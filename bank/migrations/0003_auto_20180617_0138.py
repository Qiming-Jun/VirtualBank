# Generated by Django 2.0.5 on 2018-06-16 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_crashcard_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tranfer',
            new_name='Transfer',
        ),
    ]
