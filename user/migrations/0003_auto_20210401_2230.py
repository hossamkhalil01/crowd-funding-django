# Generated by Django 3.1.7 on 2021-04-01 22:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210401_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^01[0-2][0-9]{8}$', 'Egyptian phone number is required')]),
        ),
    ]
