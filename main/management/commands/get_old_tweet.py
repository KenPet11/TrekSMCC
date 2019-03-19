from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import tweepy
from afinn import Afinn
from django.utils import timezone
from datetime import datetime
import GetOldTweets3 as got3
import pytz

class Command(BaseCommand):
	help = 'Scrapes Twitter for Trek tweets and stores them in database'

	def handle(self, *args, **kwargs):
		tweetCriteria = got3.manager.TweetCriteria().setQuerySearch('Trek bike', 'Trek bicycle', 'Trek bicycle corporation', 'Trek bikes', 'trekbikes', 'trekbike').setSince("2017-01-01").setUntil("2019-03-18").setMaxTweets(100)
		tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
		af = Afinn(emoticons=True)

		for tweet in tweets:
			if 'stolen' not in tweet.text and 'star' not in tweet.text and 'Star' not in tweet.text and 'Stolen' not in tweet.text and 'Ad' not in tweet.text:
				if hasattr(tweet, 'created at'):
					tw_created_at = tweet.created_at.astimezone(pytz.utc) 
					tw_year = tw_created_at.strftime("%Y")
					tw_month = tw_created_at.strftime("%m")
					tw_day = tw_created_at.strftime("%d")
				else:
					tw_created_at = 0
				if not hasattr(tweet, 'id_str'):
					continue
				tw_id = tweet.id_str
				try:
					tw_text = tweet.extended_tweet['full_text']
				except:
					tw_text = tweet.text
				if hasattr(tweet, 'retweeted_status'):
					try:
						tw_text = tweet.retweeted_status.full_text
					except:
						tw_text = tweet.retweeted_status.text
				if(tw_text.split()[0] == 'RT'):
					tw_text = ' '.join(tw_text.split()[1:])
				wlist = tw_text.split()
				for word in wlist:
					if word[0] == '@':
						wlist.remove(word)
				tw_text = ' '.join(wlist)
				for word in wlist:
					if word.split(':')[0] == 'https':
						wlist.remove(word)
				tw_text = ' '.join(wlist)
				tw_user = tweet.user.id_str
				try:
					tw_longitude = tweet.coordinates.coordinates[0]
					tw_latitude = tweet.coordinates.coordinates[1]
				except:
					tw_longitude = None
					tw_latitude = None
				tw_place = None 
				tw_retweet = tweet.retweeted_status
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
				tweet_user_user_name = tweet.user.name
				tweet_user_location = tweet.user.location
				user_id = tweet.user.id
				user_screen_name = tweet.user.screen_name
				user_name = tweet.user.name
				user_location = tweet.user.location
				user_description = tweet.user.description

				if not Tweet.objects.filter(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day):
					t = Tweet(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score, tweet_user_user_name=tweet_user_user_name, tweet_user_location=tweet_user_location, tweet_year=tw_year, tweet_month=tw_month, tweet_day=tw_day)
					t.save()

					if not Twitter_User.objects.filter(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description):
						u = Twitter_User(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description)
						u.save(u)