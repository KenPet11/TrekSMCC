# Generated by Django 2.1.5 on 2019-03-27 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190319_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter_user',
            name='t_screen_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]