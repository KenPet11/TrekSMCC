# Generated by Django 2.1.7 on 2019-03-30 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_twitter_user_t_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter_user',
            name='t_user_gender',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
