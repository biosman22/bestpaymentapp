
import hashlib
import base64
import json
import requests
from datetime import datetime
import calendar
import string
from random import *
import hmac
from django.conf import settings


def get_countries():
    http_method = 'get'                   # get|put|post|delete - must be lowercase
    base_url = 'https://sandboxapi.rapyd.net'
    path = '/v1/data/countries'           # Portion after the base URL. Hardkeyed for this example.

    # salt: randomly generated for each request.
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.punctuation + string.digits
    salt = "".join(choice(allchar)for x in range(randint(min_char, max_char)))

    # Current Unix time (seconds).
    d = datetime.utcnow()
    timestamp = calendar.timegm(d.utctimetuple())

    access_key = settings.RAPYD_ACCESS_KEY        # The access key received from Rapyd.
    secret_key = settings.RAPYD_SECRET_KEY       # Never transmit the secret key by itself.

    body = ''                             # JSON body goes here. Always empty string for GET; 
                                          # strip nonfunctional whitespace.

    to_sign = http_method + path + salt + str(timestamp) + access_key + secret_key + body

    h = hmac.new(bytes(secret_key, 'utf-8'), bytes(to_sign, 'utf-8'), hashlib.sha256)

    signature = base64.urlsafe_b64encode(str.encode(h.hexdigest()))

    url = base_url + path

    headers = {
        'access_key': access_key,
        'signature': signature,
        'salt': salt,
        'timestamp': str(timestamp),
        'Content-Type': "application\/json"
    }

    print(url)

    r = requests.get(url, headers = headers)
    all_countries = r['data']
    print(all_countries)

    print(len(all_countries))




def get_signature(http_method, path, body="" ):
    # http_method    get|put|post|delete - must be lowercase
    base_url = settings.RAPYD_API_URL
    #path = '/v1/data/countries'           # Portion after the base URL. Hardkeyed for this example.

    # salt: randomly generated for each request.
    min_char = 8
    max_char = 12
    allchar = string.ascii_letters + string.punctuation + string.digits
    salt = "".join(choice(allchar)for x in range(randint(min_char, max_char)))

    # Current Unix time (seconds).
    d = datetime.utcnow()
    timestamp = calendar.timegm(d.utctimetuple())

    access_key = settings.RAPYD_ACCESS_KEY        # The access key received from Rapyd.
    secret_key = settings.RAPYD_SECRET_KEY       # Never transmit the secret key by itself.

    #body= ''                             # JSON body goes here. Always empty string for GET; 
                                          # strip nonfunctional whitespace.
    # print("-------------- body inside signature -----------------")
    # print(body)
    to_sign = http_method + path + salt + str(timestamp) + access_key + secret_key + body

    h = hmac.new(bytes(secret_key, 'utf-8'), bytes(to_sign, 'utf-8'), hashlib.sha256)

    signature = base64.urlsafe_b64encode(str.encode(h.hexdigest()))

    # return {"sinature": signature,
            # "salt": salt,
            # "timestamp":timestamp,}

    headers = {
        'access_key': access_key,
        'signature': signature,
        'salt': salt,
        'timestamp': str(timestamp),
        'Content-Type': "application\/json"
    }

    return headers