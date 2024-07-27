import redis
from dotenv import load_dotenv
import os
import pandas as pd
import pickle

load_dotenv()

r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0)


def redis_connect():
    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379, db=0)
    return r


def set_redis_dict(phone, mydict, ttl_time):
    p_mydict = pickle.dumps(mydict)
    r.set(str(phone), p_mydict, keepttl=ttl_time)
    print("__dict__added__")


def get_redis_dict(phone):
    read_dict = r.get(phone)
    if read_dict:
        yourdict = pickle.loads(read_dict)
        return yourdict
    else:
        return None



if __name__=="__main__":
    a=get_redis_dict(7986640195)
    print(a)
    # r=redis_connect()
    # mydict = {1: 2, 2: 3, 3: 4}
