from django.db import models
from jsonfield import JSONField

# Create your models here.
class Twitter_User(models.Model):
	t_id = models.BigIntegerField(default=0)
	t_screen_name = models.CharField(max_length=20)
	t_user_name = models.CharField(max_length=60)
	t_user_location = models.CharField(max_length=240, blank=True)
	t_user_description = models.TextField(blank=True)

	def __str__(self):
		return self.t_user_name


class Tweet(models.Model):
	tweet_created_at = models.CharField(max_length=60, blank=True)
	tweet_id = models.BigIntegerField(default=0)
	tweet_text = models.TextField()
	tweet_user = models.CharField(max_length=60)
	tweet_longitude = models.FloatField(blank=True, null=True)
	tweet_latitude = models.FloatField(blank=True, null=True)
	tweet_place = JSONField(blank=True)
	tweet_retweeted_status = models.BooleanField(default=False, blank=True)
	tweet_media = JSONField(blank=True)
	tweet_hashtags = JSONField(blank=True)
	tweet_possibly_sensitive = models.BooleanField(default=False, blank=True)

	def __str__(self):
		return self.tweet_text