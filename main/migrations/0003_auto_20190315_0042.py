# Generated by Django 2.1.5 on 2019-03-15 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_tweet_tweet_user_screen_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_user_location',
            field=models.CharField(blank=True, default='', max_length=240, null=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_user_user_name',
            field=models.CharField(default='', max_length=60),
        ),
    ]
