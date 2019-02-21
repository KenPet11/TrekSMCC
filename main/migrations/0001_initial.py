# Generated by Django 2.1.5 on 2019-02-20 21:53

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_created_at', models.CharField(max_length=60)),
                ('tweet_id', models.BigIntegerField(default=0)),
                ('tweet_text', models.TextField()),
                ('tweet_user', models.CharField(max_length=60)),
                ('tweet_longitude', models.FloatField()),
                ('tweet_latitude', models.FloatField()),
                ('tweet_place', jsonfield.fields.JSONField()),
                ('tweet_retweeted_status', models.BooleanField(default=False)),
                ('tweet_media', jsonfield.fields.JSONField()),
                ('tweet_hashtags', jsonfield.fields.JSONField()),
                ('tweet_possibly_sensitive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Twitter_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_id', models.BigIntegerField(default=0)),
                ('t_screen_name', models.CharField(max_length=20)),
                ('t_user_name', models.CharField(max_length=60)),
                ('t_user_location', models.CharField(max_length=240)),
                ('t_user_description', models.TextField()),
            ],
        ),
    ]
