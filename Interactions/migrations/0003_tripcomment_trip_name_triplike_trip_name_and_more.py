# Generated by Django 4.2.6 on 2023-10-29 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Interactions', '0002_triprequest_is_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripcomment',
            name='trip_name',
            field=models.CharField(default='a', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triplike',
            name='trip_name',
            field=models.CharField(default='a', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triprequest',
            name='trip_name',
            field=models.CharField(default='a', max_length=30),
            preserve_default=False,
        ),
    ]
