from django.core.management.base import BaseCommand
from main.models import Twitter_User, Tweet
import tweepy
from afinn import Afinn
from django.utils import timezone
from datetime import datetime
import pytz
import requests
import json
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		geopy.geocoders.options.default_timeout = None
		geolocator = Nominatim(user_agent="trek_smcc")

		for tweet in Tweet.objects.all():
			if tweet.tweet_user_location != None:
				location = geolocator.geocode(tweet.tweet_user_location)
				if location != None:
					tweet.tweet_longitude = location.longitude
					tweet.tweet_latitude = location.latitude
					tweet.save()
			