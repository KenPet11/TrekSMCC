from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
from .models import Twitter_User
from django.utils import timezone
from datetime import datetime
from django.views.generic import ListView
from django.utils.timezone import localtime
import json
from datetime import datetime, timedelta, date
import pytz
import tweepy
import random
from nltk.corpus import stopwords
from dateutil.relativedelta import *
from pytz import common_timezones
from django.http import HttpResponseRedirect
from django.core import serializers
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


auth = tweepy.OAuthHandler("fwrSfG4uSUYv4iE38sMADRXRk", "i41PVv11Eh1wSue3aAhrucPE3Mcye5zRwALvMUikmO3KiwEMqh")
auth.set_access_token("1087756438288719873-qChEYx47VTjmU3POUIrK3WnZQK86NE", "VbyFkxUw8uRYWw3BCmj5EfGw7HxMqJa3yjQtmHZMt9HZp")

api = tweepy.API(auth)

central = pytz.timezone('America/Chicago')

# Create your views here.
def homepage(request):
	tw_created_at = datetime.today() + timedelta(days=1)
	tw_year = tw_created_at.strftime("%Y")
	tw_month = tw_created_at.strftime("%m")
	tw_day = tw_created_at.strftime("%d")
	day_score = []
	day_time = []
	week_score = []
	week_time = []
	month_score = []
	month_time = []
	year_score = []
	year_time = []

	one_day_ago = datetime.now().astimezone(central) - timedelta(days=1)
	tw_y = one_day_ago.strftime("%Y")
	tw_m = one_day_ago.strftime("%m")
	tw_d = one_day_ago.strftime("%d")
	day_tweets = Tweet.objects.filter(tweet_day=tw_d, tweet_month=tw_m, tweet_year=tw_y).order_by('tweet_created_at')
	while (one_day_ago.strftime("%d %m %H") != (datetime.now().astimezone(central).strftime("%d %m %H"))): 
		score = 0
		num = 0
		for t in day_tweets:
			if t.tweet_created_at.astimezone(central).strftime("%H") == one_day_ago.strftime("%H"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			day_score.append(0)
			day_time.append(one_day_ago.astimezone(central).strftime("%a %H:%M"))
			one_day_ago = one_day_ago + timedelta(hours=1)
		else:
			avg = score / num
			day_score.append(avg)
			day_time.append(one_day_ago.astimezone(central).strftime("%a %H:%M"))
			one_day_ago = one_day_ago + timedelta(hours=1)

	#week tweets

	one_week_ago = datetime.today() - timedelta(days=7)
	week_tweets = Tweet.objects.filter(tweet_created_at__gte=one_week_ago).order_by('tweet_created_at')
	while (one_week_ago.strftime("%d %m") != (datetime.today() + timedelta(days=1)).strftime("%d %m")):
		score = 0
		num = 0
		for t in week_tweets:
			if t.tweet_created_at.astimezone(pytz.utc).strftime("%a") == one_week_ago.strftime("%a"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			one_week_ago = one_week_ago + timedelta(days=1)
			continue
		else:
			avg = score / num
		week_score.append(avg)
		week_time.append(one_week_ago.strftime("%a"))
		one_week_ago = one_week_ago + timedelta(days=1)

	#month tweets
	last_month = datetime.today() - relativedelta(months=1)
	month_tweets = Tweet.objects.filter(tweet_created_at__gte=last_month).order_by('tweet_created_at')
	while (last_month.strftime("%d %m") != (datetime.today() + timedelta(days=1)).strftime("%d %m")):
		score = 0
		num = 0
		for t in month_tweets:
			if t.tweet_created_at.astimezone(pytz.utc).strftime("%d %m") == last_month.strftime("%d %m"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			last_month = last_month + timedelta(days=1)
			continue
		else:
			avg = score / num
		month_score.append(avg)
		month_time.append(last_month.strftime("%b %d %Y"))
		last_month = last_month + timedelta(days=1)

	#year tweets
	last_year = datetime.today() - relativedelta(years=1)
	year_tweets = Tweet.objects.filter(tweet_created_at__gte=last_year).order_by('tweet_created_at')
	while (last_year.strftime("%m %Y") != (datetime.today() + relativedelta(months=1)).strftime("%m %Y")):
		score = 0
		num = 0
		for t in year_tweets:
			if t.tweet_created_at.astimezone(pytz.utc).strftime("%m %Y") == last_year.strftime("%m %Y"): 
				score = score + t.tweet_score
				num = num + 1
		if num is 0:
			last_year = last_year + relativedelta(months=1)
			continue
		else:
			avg = score / num
		year_score.append(avg)
		year_time.append(last_year.strftime("%B %Y"))
		last_year = last_year + relativedelta(months=1)

	return render(request = request,
		template_name='main/home.html',
		context = {"today_data":day_score, "today_labels": day_time, "week_data":week_score, "week_labels":week_time, "month_data":month_score, "month_labels":month_time, "year_data":year_score, "year_labels":year_time})

#create method that returns data in json (json python library)
#in java, use tie function to updata data , and rebuid the chart)

def get_latest(request):
	scores = []
	times = []
	tw_created_at = datetime.today().astimezone(central)
	tw_later = datetime.today().astimezone(central) - timedelta(hours=4)
	tw_year = tw_created_at.strftime("%Y")
	tw_month = tw_created_at.strftime("%m")
	tw_day = tw_created_at.strftime("%d")
	latest_tweet_list = Tweet.objects.filter(tweet_created_at__range=(tw_later, tw_created_at)).order_by('tweet_created_at')
	if(len(latest_tweet_list) > 50):
		latest_tweet_list = latest_tweet_list[:50]

	for t in latest_tweet_list:
		scores.append(t.tweet_score)
		times.append(t.tweet_created_at.astimezone(central).strftime("%a %H:%M"))

	return_object = {}
	return_object["scores"] = scores
	return_object["times"] = times
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_latest_feed(request):
	latest_tweet_list = Tweet.objects.order_by('-tweet_created_at')[:5]

	tweetText = []
	tweetCreatedAt = []
	userName = []
	tweetLocation = []
	tweetID = []
	tweetUserDisplay = []

	for tweet in latest_tweet_list:
		tweetText.append(tweet.tweet_text)
		tweetCreatedAt.append(tweet.tweet_created_at.astimezone(central).strftime("%a %m/%d/%Y, %H:%M %p"))
		user = Twitter_User.objects.filter(t_user_name=tweet.tweet_user_user_name).first()
		userName.append(user.t_screen_name)
		tweetLocation.append(tweet.tweet_user_location)
		tweetID.append(tweet.tweet_id)
		tweetUserDisplay.append(tweet.tweet_user_user_name)

	return_object = {}
	return_object["tweetText"] = tweetText
	return_object["tweetCreatedAt"] = tweetCreatedAt
	return_object["userName"] = userName
	return_object['tweetLocation'] = tweetLocation
	return_object["tweetID"] = tweetID
	return_object["tweetUserDisplay"] = tweetUserDisplay
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def send_tweet(request):
	data=json.loads(request.body.decode("utf-8"))
	print(data)
	tweetID = data['tweetID']
	tweetTextToSend = data['tweetTextToSend']
	print(tweetTextToSend, tweetID)
	s = api.update_status(tweetTextToSend, tweetID)
	return_object = {}
	return_object['result'] = 'success'
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_tweet(request, tweetid):
	tid_list = tweetid.split(" ")
	tid = tid_list[0]
	tuid = ('').join(tid_list[1:])
	return_object = {}
	return_object['screenName'] = tuid
	return_object['tweetID'] = tid
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_cloud_text(request):
	latest_tweet_list = Tweet.objects.order_by('-tweet_created_at')[:200]
	stop = stopwords.words('english')
	dataDict = {}
	for tweet in latest_tweet_list:
		stringWordList = tweet.tweet_text.split(" ")
		for word in stringWordList:
			if word not in stop:
				if word in dataDict.keys():
					dataDict[word] += 1
				else:
					dataDict[word] = 1

	return_object = {}
	return_list = []
	for word, value in dataDict.items():
		newDict = {}
		newDict["word"] = word
		newDict["value"] = value
		return_list.append(newDict)
	
	return_object["cloudText"] = return_list[:125]
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_gender_data(request):
	male = 0
	female = 0
	for user in Twitter_User.objects.all():
		if user.t_user_gender == 'male':
			male +=1
		elif user.t_user_gender == 'female':
			female +=1

	return_object = {}
	return_object['male'] = male
	return_object['female'] = female
	return HttpResponse(json.dumps(return_object), content_type='application/json')

def get_map_data(request):
	data = []
	for tweet in Tweet.objects.filter(tweet_longitude__isnull=False).order_by('-tweet_created_at')[:200]:
		newData = {}
		if tweet.tweet_user_location != None and tweet.tweet_user_location != 'tweet_user_location' and tweet.tweet_longitude != None:
			newData['name'] = tweet.tweet_user_location
			newData['latitude'] = tweet.tweet_latitude
			newData['longitude'] = tweet.tweet_longitude
			newData['radius'] = 10
			newData['fillKey'] = 'gt50'
			data.append(newData)

	return_object = {}
	return_object['locations'] = data
	return HttpResponse(json.dumps(return_object), content_type='application/json')