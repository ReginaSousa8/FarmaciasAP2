# Generated by Django 2.0 on 2017-12-27 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coredrca', '0004_aviar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmacia',
            name='idReceita',
        ),
    ]