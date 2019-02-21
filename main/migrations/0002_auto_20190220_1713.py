# Generated by Django 2.1.5 on 2019-02-20 22:13

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_created_at',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_hashtags',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_latitude',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_longitude',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_media',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_place',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_possibly_sensitive',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_retweeted_status',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='twitter_user',
            name='t_user_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='twitter_user',
            name='t_user_location',
            field=models.CharField(blank=True, max_length=240),
        ),
    ]
