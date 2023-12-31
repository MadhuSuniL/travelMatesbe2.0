# Generated by Django 4.2.6 on 2023-10-29 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Interactions', '0003_tripcomment_trip_name_triplike_trip_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripCommentReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_comment', to='Interactions.tripcomment', to_field='comment_id')),
                ('reply_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment', to='Interactions.tripcomment', to_field='comment_id')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
