# Generated by Django 2.0.5 on 2018-06-17 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_auto_20180617_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='time',
            field=models.DateTimeField(default='1970-10-10 08:00:00'),
        ),
    ]
