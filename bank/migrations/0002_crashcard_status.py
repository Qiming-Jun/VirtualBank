# Generated by Django 2.0.5 on 2018-06-16 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crashcard',
            name='status',
            field=models.CharField(default='正常', max_length=32),
        ),
    ]
