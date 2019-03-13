# Generated by Django 2.1.5 on 2019-03-12 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190220_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='tweet_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_id',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='twitter_user',
            name='t_id',
            field=models.CharField(max_length=60),
        ),
    ]
