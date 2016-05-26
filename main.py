from requests_oauthlib import OAuth1Session
from collections import ChainMap
import json
import os
import sys
import urllib

consumer_key_file = "config/consumer.json"
access_token_file = "config/access_token.json"
screen_name_fiile = "config/screen_name.json"

def return_json_important_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as json_object:
         important_json_data = json.load(json_object)

    return important_json_data

key_dict = dict(ChainMap(*[return_json_important_file(consumer_key_file), return_json_important_file(access_token_file)]))

save_path = os.path.abspath(os.path.dirname(__file__)+'/image')

screen_name = return_json_important_file(screen_name_fiile)
image_number = 0
get_pages = 10
count = 8

def create_oauth_session(key_dict):
    oauth = OAuth1Session(
        key_dict["consumer_key"],
        key_dict["consumer_secret"],
        key_dict["access_token"],
        key_dict["access_token_secret"]
    )

    return oauth

def favorite_tweets_get(page, key_dict):
    url = "https://api.twitter.com/1.1/favorites/list.json?"
    params = {
        "screen_name": screen_name["screen_name"],
        "page": page,
        "count": count,
        "include_entities": 1
    }
    oauth = create_oauth_session(key_dict)
    response = oauth.get(url, params=params)

    if response.status_code != 200:
        print("Error code: {0}".format(response.status_code))
        return None

    tweets = json.loads(response.text)
    return tweets

def image_serve(tweets):
    global image_number
    for tweet in tweets:
        try:
            image_list = tweet["extended_entities"]["media"]
            for image_dict in image_list:
                url = image_dict["media_url"]
                with open(save_path + '/' + str(image_number) + "_" + os.path.basename(url), mode='wb') as f:
                    img = urllib.request.urlopen(url, timeout=5).read()
                    f.write(img)
                print("Done")
                image_number += 1
        except KeyError:
            print("KeyError: 画像がないツイート")
        except:
            print("Unexcepted error: ", sys.exc_info()[0])

if __name__ == "__main__":
    for i in range(1, get_pages):
        tweets = favorite_tweets_get(i, key_dict)
        image_serve(tweets)
