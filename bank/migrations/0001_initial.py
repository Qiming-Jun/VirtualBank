# Generated by Django 2.0.5 on 2018-06-15 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aname', models.CharField(max_length=32)),
                ('apasswd', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='CrashCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DrawDeposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=16)),
                ('datafrom', models.CharField(default='自动取款机', max_length=64, null=True)),
                ('time', models.DateTimeField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bank.CrashCard')),
            ],
        ),
        migrations.CreateModel(
            name='Tranfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('scbalance', models.IntegerField()),
                ('dcbalance', models.IntegerField()),
                ('remark', models.CharField(default='无', max_length=128, null=True)),
                ('dcard', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='dcid', to='bank.CrashCard')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=32)),
                ('uidcard', models.CharField(max_length=32)),
                ('uphone', models.CharField(max_length=32)),
                ('uemail', models.CharField(max_length=32)),
                ('upasswd', models.CharField(max_length=128)),
                ('paypasswd', models.CharField(max_length=128, null=True)),
                ('time', models.DateTimeField()),
                ('status', models.CharField(default='正常', max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='tranfer',
            name='duser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='did', to='bank.Users'),
        ),
        migrations.AddField(
            model_name='tranfer',
            name='scard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='scid', to='bank.CrashCard'),
        ),
        migrations.AddField(
            model_name='tranfer',
            name='suser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sid', to='bank.Users'),
        ),
        migrations.AddField(
            model_name='crashcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='bank.Users'),
        ),
    ]
