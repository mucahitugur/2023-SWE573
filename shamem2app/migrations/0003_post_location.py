# Generated by Django 4.2 on 2023-05-26 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shamem2app', '0002_post_created_at_post_decade_post_exact_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]