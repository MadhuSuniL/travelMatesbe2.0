# Generated by Django 4.2.6 on 2023-12-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelMates', '0009_alter_travelmate_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelmate',
            name='is_online',
            field=models.BooleanField(default=False),
        ),
    ]