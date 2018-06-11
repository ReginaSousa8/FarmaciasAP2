# Generated by Django 2.0 on 2017-12-27 14:12

import coredrca.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coredrca', '0003_auto_20171227_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aviar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idFarmacia', models.ForeignKey(on_delete=coredrca.models.Farmacia, to='coredrca.Farmacia')),
                ('idReceita', models.ForeignKey(on_delete=coredrca.models.Receita, to='coredrca.Receita')),
            ],
        ),
    ]
