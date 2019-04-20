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
		url = "https://gender-api.com/get?name="
		key = "&key=946d64a0022933dec936848d4e68fb30c588ddd8e1d19292603b709ce0be2539"

		for tweet in Tweet.objects.all():
			first_name = tweet.tweet_user_user_name.split()[0]
			URL = url+str(first_name)+key
			response = requests.get(URL)
			response = response.json()
			tweet.t_user_gender = response["gender"]
			if tweet.tweet_created_at != None:
				tweet.save()