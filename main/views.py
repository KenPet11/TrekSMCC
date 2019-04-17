from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Tweet
from .models import Twitter_User
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

#json_serializer = serializers.get_serializer("json")()
#users = json_serializer.serialize(Twitter_User.objects.all(),ensure_ascii=False)

#users = Twitter_User.objects.values_list('t_user_gender')
# Create your views here.
def homepage(request):
	latest_tweet_list = Tweet.objects.order_by('-tweet_created_at')[:5]
	users = list(Twitter_User.objects.values_list('t_user_gender'))
	locations = list(Tweet.objects.values_list('tweet_place'))
	print(users)
	#user_list = Twitter_User.objects.order_by('-t_id').values('t_user_gender')[:]
	#for i in user_list:
		#print(i)
	#print(user_list)
	context = {"Tweets":latest_tweet_list}
	context["Twitter_Users"] = json.dumps({'data':users})
	context["tweet_place"] = json.dumps({'places':locations})
	return render(request = request,
		template_name='main/home.html',
		context = context)

def ajaxtest(request):
	print("helloworld")
	return homepage(request)
