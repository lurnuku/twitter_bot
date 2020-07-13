import tweepy
import re
import json
import time
import sched
# NOTE: I put my keys.py in the keys.py.py to separate them
# from this main file.
# Please refer to keys_format.py to see the format.
from keys import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

replied_helpdays_filename = 'replied.json'
medu_paypal = 'http://paypal.me/lurnuku'

def get_replied_helpday_numbers():
    file = open(replied_helpdays_filename, 'r')
    data = file.read()
    json_data = json.loads(data)
    file.close()

    return json_data

def store_replied_helpday_number(modified_json):
    file = open(replied_helpdays_filename, 'w')
    file.seek(0)
    json.dump(modified_json, file, indent=4)
    file.close()

    return

def find_and_retweet_last_tweet(target):
    h3h3 = api.get_user(target)

    tweet = api.user_timeline(id=h3h3.id, count=1)[0]
    tweet_text = tweet.text
    tweet_id = tweet.id

    # https://regex101.com/r/Tc68WX/1
    help_day_regex = 'H.E.L.P. Day #\d+'
    # https://regex101.com/r/gjYUlR/1
    help_day_number_extract_regex = '#\d+'


    if (re.search(help_day_regex, tweet_text)):
        match = re.search(help_day_number_extract_regex, tweet_text)
        help_day_number = match.group(0)

        replied_helpdays = get_replied_helpday_numbers()

        if help_day_number in replied_helpdays['helpday_numbers']:
            print('I already replied to this tweet BAKA!')
            return

        try:
            api.update_status('@' + target + ' ' + medu_paypal, tweet_id)
            api.retweet(tweet_id)

            replied_helpdays['helpday_numbers'].append(help_day_number)
            store_replied_helpday_number(replied_helpdays)
        except ValueError:
            print('Something went wrong and I couldn\'t tweet for you my flesh overlord')
    else:
        print('Helpday tweet not found :(')
    return

find_and_retweet_last_tweet('h3h3productions')