from .signature import get_signature
import requests
from django.conf import settings

def call_api(http_method, path, body=""):
    
    h = get_signature(http_method, path, body)
    url = settings.RAPYD_API_URL + path
    d= body
    if http_method == 'post':
        r = requests.post(url, headers=h, data=d)
    elif http_method == 'get':
        r = requests.get(url, headers=h )
    elif http_method == 'put':
        r = requests.put(url, headers=h, data=d)

    return r