# Generated by Django 4.2.3 on 2023-11-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Interactions', '0008_follower_travel_mate_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='triplike',
            name='travel_mate_profile',
            field=models.URLField(default='1'),
            preserve_default=False,
        ),
    ]
