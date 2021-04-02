# Generated by Django 3.1.7 on 2021-04-02 14:59

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('campaign', '0005_auto_20210402_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
