from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
from .models import Twitter_User

# Create your views here.
def homepage(request):
	latest_tweet_list = Tweet.objects.order_by('tweet_created_at')[:5]
	return render(request = request,
		template_name='main/home.html',
		context = {"Tweets": latest_tweet_list})