# Generated by Django 3.1.7 on 2021-04-05 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20210404_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='profile_images/default-pic.jpeg', upload_to='profile_images', verbose_name='profile picture'),
        ),
    ]
