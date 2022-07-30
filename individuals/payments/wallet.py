import requests, json
from datetime import datetime, timedelta 
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
from django.conf import settings
from .signature import get_signature
from .api_call import call_api


def list_wallets( ewallet_reference_id):

    http_method = 'get'                   # get|put|post|delete - must be lowercase
    path = '/v1/user/wallets' 
    
    results = call_api(http_method, path=path+"?ewallet_reference_id="+ewallet_reference_id)

    #print(results.json())
    return results.json()


def retrive_wallet(wallet_id):
    http_method = 'get'                   # get|put|post|delete - must be lowercase
    path = '/v1/user/'

    results = call_api(http_method, path=path + wallet_id)

    #print(results.json())
    return results.json()


def enable_wallet(wallet_id):
    path = "/v1/user/enable"
    http_method = "post"
    
    d = json.dumps({"ewallet": wallet_id}, separators=(',', ':'))

    
    r= call_api(http_method, path, body=d)

    #print(r.json())

    return r.json()


def disable_wallet(wallet_id):
    path = "/v1/user/disable"
    http_method = "post"
    
    d = json.dumps({"ewallet": wallet_id}, separators=(',', ':'))

    
    r= call_api(http_method, path, body=d)

    #print(r.json())

    return r.json()




def update_wallet(wallet_id, ewallet_reference_id, email, first_name, last_name, phone_number):
    path = "/v1/user"
    http_method = "put"
    main_dict = {"ewallet": wallet_id}
    if ewallet_reference_id:
        main_dict['ewallet_reference_id'] =ewallet_reference_id
    
    if email:
        main_dict['email'] = email

    if first_name:
        main_dict['first_name'] = first_name

    if last_name:
        main_dict['last_name'] = last_name

    if phone_number:
        main_dict['phone_number'] = phone_number
    
    d = json.dumps(main_dict , separators=(',', ':'))

    
    r= call_api(http_method, path, body=d)

    #print(r.json())

    return r.json()




def delete_wallet(wallet_id):
    path = "/v1/user/"
    http_method = "delete"
    

    r= call_api(http_method, path + wallet_id)

    #print(r.json())

    return r.json()




def retrive_balances(wallet_id):
    http_method = 'get'                   # get|put|post|delete - must be lowercase
    path = '/v1/user/'+wallet_id+'/accounts'

    results = call_api(http_method, path=path )

    #print(results.json())
    return results.json()


def list_transactions(wallet_id):
    http_method = 'get'                   # get|put|post|delete - must be lowercase
    path = '/v1/user/'+wallet_id+'/transactions'

    results = call_api(http_method, path=path )

    #print(results.json())
    return results.json()


