import os
import time
import lib
import tweepy
import json

try:
    os.mkdir("data")
except:
    pass

while True:
    try:
        api = lib.get_api()
        id = int(time.time()*1000)
        old_id = lib.old_id(id)
        if old_id != None:
            old_data = lib.Data.load(old_id)
            users = list(old_data.followers |
                         old_data.friends | old_data.outgoing)
            actives = []
            for x in lib.list_split(100, users):
                actives.extend([x.id for x in api.lookup_users(user_ids=x)])
        else:
            actives = []

        data = lib.Data(id=id, friends=list(tweepy.Cursor(api.friends_ids, count=5000).items()), followers=list(tweepy.Cursor(
            api.followers_ids, count=5000).items()), outgoing=[int(x) for x in tweepy.Cursor(api.friendships_outgoing).items()], actives=actives)

        data.save()
    except:
        print("エラー")

    time.sleep(60*60)
