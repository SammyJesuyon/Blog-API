# Generated by Django 4.0.4 on 2022-05-25 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_blog_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=255),
        ),
    ]
