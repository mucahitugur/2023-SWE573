# Generated by Django 4.2 on 2023-04-09 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shamem2app', '0003_post_created_at_post_image_post_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
