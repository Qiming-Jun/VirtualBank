# Generated by Django 2.0.5 on 2018-06-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_auto_20180619_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='drawdeposit',
            name='type',
            field=models.CharField(default='存款', max_length=32),
        ),
    ]
