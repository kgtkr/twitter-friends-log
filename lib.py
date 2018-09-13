import tweepy
import os
import time
import json
import typing


def get_api():
    CK = os.environ.get("CK")
    CS = os.environ.get("CS")
    TK = os.environ.get("TK")
    TS = os.environ.get("TS")

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(TK, TS)

    return tweepy.API(auth)


def logging():
    try:
        os.mkdir("data")
    except:
        pass

    api = get_api()
    now = int(time.time()*1000)

    data = {}
    data["friends"] = list(tweepy.Cursor(api.friends_ids, count=5000).items())
    data["followers"] = list(tweepy.Cursor(
        api.followers_ids, count=5000).items())
    data["outgoing"] = [int(x) for x in tweepy.Cursor(
        api.friendships_outgoing).items()]

    data_s = json.dumps(data)
    path = f"data/{now}.json"

    with open(path, mode='w') as f:
        f.write(data_s)


def list_split(n: int, list):
    return [list[i:i+n] for i in range(0, len(list), n)]


def name_to_id(name):
    return int(name.replace(".json", ""))


def old_id(val: int):
    ids = [name_to_id(x) for x in os.listdir("data")]
    ids = [x for x in ids if x < val]
    ids.sort()
    ids.reverse()
    if len(ids) != 0:
        return ids[0]
    else:
        return None


class Data:
    def __init__(self, id: int, friends: typing.List[int], followers: typing.List[int], outgoing: typing.List[int], actives: typing.List[int]):
        self.id = id
        self.friends = set(friends)
        self.followers = set(followers)
        self.outgoing = set(outgoing)
        self.actives = set(actives)

    def save(self):
        data = {}
        data["friends"] = list(self.friends)
        data["followers"] = list(self.followers)
        data["outgoing"] = list(self.outgoing)
        data["actives"] = list(self.actives)

        with open(f"data/{self.id}.json", mode='w') as f:
            f.write(json.dumps(data))

    @staticmethod
    def load(id: int):
        with open(f"data/{id}.json") as f:
            s = f.read()
            data = json.loads(s)
            return Data(id=id, friends=data["friends"], followers=data["followers"], outgoing=data["outgoing"], actives=data["actives"])
