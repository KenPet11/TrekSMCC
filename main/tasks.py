import numpy as np
from celery import task
import got

@task(name='summary')
def send_import_summary():
	print('hello')
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('trek').setSince("2016-01-01").setMaxTweets(5)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	try:
		print(tweet.text)
	except:
		print('a')
