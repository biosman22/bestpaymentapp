import requests, json
from datetime import datetime, timedelta 
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils import timezone
from django.conf import settings
from .signature import get_signature
from .api_call import call_api




def create_virtual_bank_account(ewallet_rapyd_id, country_code,currency):
    
    body = json.dumps({
        "currency": currency,
        "country": country_code,
        "description": "Issuing bank account number to wallet",
        "ewallet": ewallet_rapyd_id,
    }, separators=(',', ':'))

    results = call_api('post', path=f'/v1/issuing/bankaccounts', body=body)

    print(results.json())
    print("virtual account created ")

    return results.json()




def list_virtual_accounts(wallet_id):

    results = call_api('get', path=f'/v1/issuing/bankaccounts/list?ewallet='+ wallet_id)
    
    print("all virtual accouns")

    print(results.json())

    return results.json()


def bank_deposit(issuing_id):
    body = json.dumps({
	"issued_bank_account": issuing_id,
	"amount": "100",
	"currency": "GBP"
    }, separators=(',', ':'))
   
    results = call_api('post', path=f'/v1/issuing/bankaccounts/bankaccounttransfertobankaccount', body=body)
    
    print("bank deposit")

    print(results.json())

    return results.json()
