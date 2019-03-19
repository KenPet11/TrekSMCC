from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import tweepy
from afinn import Afinn
from django.utils import timezone
from datetime import datetime
import GetOldTweets3 as got3

class Command(BaseCommand):
	help = 'Scrapes Twitter for Trek tweets and stores them in database'

	def handle(self, *args, **kwargs):
		tweetCriteria = got3.manager.TweetCriteria().setQuerySearch('trek').setSince("2017-01-01").setUntil("2019-03-18").setMaxTweets(1000)
		tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
		af = Afinn(emoticons=True)

		for tweet in tweets:
			if 'stolen' not in tweet.text and 'star' and 'Star' not in tweet.text:
				tw_created_at = tweet.date
				tw_year = tw_created_at.strftime("%Y")
				tw_month = tw_created_at.strftime("%m")
				tw_day = tw_created_at.strftime("%d")
				tw_id = tweet.id
				try:
					tw_text = tweet.text
				except:
					tw_text = tweet.text
				try:
					if(tw_text.split()[0] == 'RT'):
						tw_text = ' '.join(tw_text.split()[1:])
					if(tw_text.split()[-1].split(':')[0] == 'https'):
						tw_text = ' '.join(tw_text.split()[:-1])
				except:
					tw_text = tw_text
				tw_user = tweet.username
				try:
					tw_longitude = None
					tw_latitude = None
				except:
					tw_longitude = None
					tw_latitude = None
				tw_place = None #status.place.__dict__
				tw_retweet = False
				try:
					tw_media = tweet.entities.media.__dict__
				except:
					tw_media = None
				try:
					tw_hashtags = tweet.entities.hashtags.__dict__
				except:
					tw_hashtags = None
				try:
					tw_psensitive = tweet.possibly_sensitive
				except:
					tw_psensitive = 0
				tw_score = af.score(tw_text)
				print(tw_score)
				tweet_user_user_name = tweet.username
				tweet_user_location = tweet.geo
				user_id = tweet.id
				user_screen_name = tweet.username
				user_name = tweet.username
				user_location = tweet.geo
				user_description = tweet.username

			if not Tweet.objects.filter(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day):
				t = Tweet(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day)
				try:
					print(t)
				except:
					print('a')
				t.save()

			if not Twitter_User.objects.filter(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description):
				u = Twitter_User(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description)
				try:
					print(u)
				except:
					print('a')
				u.save(u)

