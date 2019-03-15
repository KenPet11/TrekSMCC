from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import tweepy
from afinn import Afinn
from django.utils import timezone

class Command(BaseCommand):
	help = 'Scrapes Twitter for Trek tweets and stores them in database'

	def handle(self, *args, **kwargs):
		auth = tweepy.OAuthHandler("amiKfJygvIY5PKHbrwYWp19YD","vOH7V77acZ6SFUMinAwFj47qWvOPmQgKy9CF8UQkWovEkqtoAp")
		auth.set_access_token("1088541921054806016-MCTqKdD0jS1QfcGGydiPvLgbLiO0Ar","1NCcStbqXWSOHlPvult1G2yN4gP2fhTCw16JwEj6DFlqB")

		api = tweepy.API(auth)
		af = Afinn(emoticons=True)

		class CustomStreamListener(tweepy.StreamListener):
			def on_status(self, status):
				if 'stolen' not in status.text:
					tw_created_at = status.created_at
					tw_id = status.id_str
					try:
						tw_text = status.extended_tweet.full_text
					except:
						tw_text = status.text
					tw_user = status.user.id_str
					try:
						tw_longitude = status.coordinates.coordinates[0]
						tw_latitude = status.coordinates.coordinates[1]
					except:
						tw_longitude = None
						tw_latitude = None
					tw_place = None #status.place.__dict__
					tw_retweet = status.retweeted
					try:
						tw_media = status.entities.media.__dict__
					except:
						tw_media = None
					try:
						tw_hashtags = status.entities.hashtags.__dict__
					except:
						tw_hashtags = None
					try:
						tw_psensitive = status.possibly_sensitive
					except:
						tw_psensitive = 0
					tw_score = af.score(tw_text)
					print(tw_score)
					user_id = status.user.id
					user_screen_name = status.user.screen_name
					user_name = status.user.name
					user_location = status.user.location
					user_description = status.user.description

				if not Tweet.objects.filter(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score):
					t = Tweet(tweet_created_at=tw_created_at, tweet_id=tw_id, tweet_text=tw_text, tweet_user=tw_user, tweet_longitude=tw_longitude, tweet_latitude=tw_latitude, tweet_place=tw_place, tweet_retweeted_status=tw_retweet, tweet_media=tw_media, tweet_hashtags=tw_hashtags, tweet_possibly_sensitive=tw_psensitive, tweet_score=tw_score)
					print(t)
					t.save()

				if not Twitter_User.objects.filter(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description):
					u = Twitter_User(t_id=user_id, t_screen_name=user_screen_name, t_user_name=user_name, t_user_location=user_location, t_user_description = user_description)
					print(u)
					u.save(u)

			def on_error(self, status_code):
				print >> sys.stderr, 'Encountered error with status code:', status_code
				return True # Don't kill the stream

			def on_timeout(self):
				print >> sys.stderr, 'Timeout...'
				return True # Don't kill the stream

		sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
		sapi.filter(track=['Trek bike', 'Trek bicycle', 'Trek bicycle corporation'])