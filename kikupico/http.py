import urequests
import ujson
from . import logging

def get_json(url):
    try:
        res = urequests.get(url)
        ret = res.json()
        res.close()
        return ret
    except Exception as e:
        logging.error(e)
        return None

def post_json(url, json):
    try:
        res = urequests.post(url, data = ujson.dumps(json))
        ret = res.json()
        res.close()
        return ret
    except Exception as e:
        logging.error(e)
        return None
