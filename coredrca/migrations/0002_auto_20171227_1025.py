# Generated by Django 2.0 on 2017-12-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coredrca', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmacia',
            name='idReceita',
            field=models.ManyToManyField(null=True, to='coredrca.Receita'),
        ),
    ]
