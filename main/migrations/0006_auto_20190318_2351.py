# Generated by Django 2.1.5 on 2019-03-19 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190318_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_created_at',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]