from django.shortcuts import render, redirect

from .forms import NewUserForm, AccountForm
from django.contrib import messages

from django.contrib.auth import login, authenticate ,logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.core.serializers import serialize

from .payments import rapyd, wallet, vbank

from .models import *


from .lazy_encoder import LazyEncoder

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

import json
# Create your views here.



def homepage(request):
	rapyd.get_countries()
	#create_wallet()
	#country_required_documents()
	#verify_identity()
	#create_virtual_bank_account()
	#list_virtual_accounts()
	#bank_deposit()
	return render(request,'home.html')




def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request,"register.html", context={"register_form":form})


    
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "login.html", context={"login_form":form})



def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("homepage")



def sign_up_req(request):
	all_countries = rapyd.get_countries()
	#create_wallet()
	#country_required_documents()
	#verify_identity()
	#create_virtual_bank_account()
	#list_virtual_accounts()
	#bank_deposit()
	return render(request,'soft/sign_up.html', {"countries": all_countries['data']})




def country_documents(request):
	country = request.GET.get('c')
	response = rapyd.country_required_documents(country)
	return JsonResponse(response)

def create_wallet(request):
	print("request body")
	request_body = request.POST

	print(request_body)
	#print(request.data)
	
	account_form = AccountForm(request.POST)
	#print(account_form)

	#account = account_form.save()
	print(account_form.errors)
	if account_form.is_valid():
		print("saved to the database")
		#rapyd.create_wallet()
		account = account_form.save()
		account.set_password(account.password)
		print("the_pass_word")
		print(account.password)
		a_wallet =  Wallet()
		
		
		a_wallet.save()

		a_wallet.set_ref_id(account.first_name, account.last_name)
		a_wallet.save()
		rapyd_response = rapyd.create_wallet(account, a_wallet)
		print(rapyd_response)
		if rapyd_response['status']['status'] == 'SUCCESS':
			a_wallet.ewallet_rapyd_id = rapyd_response['data']['id'] 
			account.address_rapyd_id = rapyd_response['data']['contacts']['data'][0]['address']['id']
			account.contact_rapyd_id = rapyd_response['data']['contacts']['data'][0]['id']
			account.contact_url = rapyd_response['data']['contacts']['url']
			a_wallet.save()
			account.save()
			account.wallets.add(a_wallet)
			verification_response = rapyd.verify_identity(a_wallet.ewallet_rapyd_id ,account.country_code, account.identification_type, account.id)
			print(verification_response)
			if verification_response['status']['status'] == 'SUCCESS':
				account.verification_status = 'KYCd'
				vbank_response = vbank.create_virtual_bank_account(a_wallet.ewallet_rapyd_id, account.country_code, account.currency_code)
				vbank_account = create_vbank_account_process(a_wallet, vbank_response)
	
				
				#{'status': {'error_code': '', 'status': 'SUCCESS', 'message': '', 'response_code': '', 'operation_id': '83a0b678-d7f9-427e-9b14-a56817ed4471'}, 'data': {'id': 'issuing_38b0e01d5173fabf8d9204499c845353', 'merchant_reference_id': 'issuing_38b0e01d5173fabf8d9204499c845353', 'ewallet': 'ewallet_b2249378547497bd26a4eb5403f9fb3e', 'bank_account': {'beneficiary_name': 'CashDash UK Limited', 'address': 'Northwest House, 119 Marylebone Road NW1 5PU', 'country_iso': 'GB', 'iban': 'GB36SAPY60838292780648', 'sort_code': '608382', 'account_no': '0092780648', 'bic': 'SAPYGB2L'}, 'metadata': {}, 'status': 'ACT', 'description': 'Issue test bank account', 'funding_instructions': None, 'currency': 'GBP', 'transactions': []}}

			login(request, account)
			

			#ser_obj =  serialize('json', [account], cls=LazyEncoder)

			#print(ser_obj)

			request.session['account_id'] = account.id
			#request.session['wallet_id'] = wallet.id
		
			messages.success(request, "Registration successful." )
			return redirect("main_page")


	messages.error(request, "Unsuccessful registration. Invalid information.")
	return redirect("sign_up")
	
	
	
	#return JsonResponse({"id":ewallet_rapyd_id})
	#return render(request,'soft/profile.html', {})




	#{'status': {'error_code': '', 'status': 'SUCCESS', 'message': '', 'response_code': '', 'operation_id': '31f8f6a9-0ea2-477f-a14d-54bc62ccc8bb'}, 'data': {'phone_number': '+14155551233', 'email': 'eeysdfteyt@loook.com', 'first_name': 'bob', 'last_name': 'tabor', 'id': 'ewallet_cd86354398b399f53f3eff6cefcde394', 'status': 'ACT', 'accounts': [], 'verification_status': 'not verified', 'type': 'person', 'metadata': {'merchant_defined': True}, 'ewallet_reference_id': 'bob-tabor-2022-07-26 10:34:45.901185', 'category': None, 'contacts': {'data': [{'id': 'cont_82c3f65396018151b52fc9996548fecf', 'first_name': 'bob', 'last_name': 'tabor', 'middle_name': '', 'second_last_name': '', 'gender': 'not_applicable', 'marital_status': 'not_applicable', 'house_type': '', 'contact_type': 'personal', 'phone_number': '+14155551233', 'email': 'eeysdfteyt@loook.com', 'identification_type': 'DL', 'identification_number': '252736576', 'issued_card_data': {'preferred_name': '', 'transaction_permissions': '', 'role_in_company': ''}, 'date_of_birth': None, 'country': 'US', 'nationality': None, 'address': {'id': 'address_42b8b38b631899c3b3152892b9e312d1', 'name': 'bob tabor', 'line_1': 'United States of America', 'line_2': '', 'line_3': '', 'city': '', 'state': '', 'country': '', 'zip': '', 'phone_number': '', 'metadata': {}, 'canton': '', 'district': '', 'created_at': 1658824487}, 'ewallet': 'ewallet_cd86354398b399f53f3eff6cefcde394', 'created_at': 1658824487, 'metadata': {'merchant_defined': True}, 'business_details': None, 'compliance_profile': 0, 'verification_status': 'not verified', 'send_notifications': False, 'mothers_name': ''}], 'has_more': False, 'total_count': 1, 'url': '/v1/ewallets/ewallet_cd86354398b399f53f3eff6cefcde394/contacts'}}}


# the_one = Account.objects.get(pk=10)
# print(the_one)
# print(the_one.password)
# ewallet = the_one.wallets.all()[0]
# print(ewallet)
# ewallet_ref = ewallet.ewallet_rapyd_id
# vbank.create_virtual_bank_account(ewallet_ref, 'GB', 'GBP')


def main_page(request):
	request_body = request.POST
	account_id = request.session.get('account_id', None)
	if account_id != None:
		print(account_id)
		account = Account.objects.get(pk=account_id)
		all_wallets = []
		wallets = account.wallets.all()
		vbank_accounts = set()
		for a_wallet in wallets:
			#Rapyd Api
			#wallet_details = wallet.list_wallets(a_wallet.ewallet_reference_id)['data'][0]
			#print(wallet_details)
			#all_wallets.append(wallet_details)

			
			for a_vbank in a_wallet.vbank_account_set.all():
				vbank_accounts.add(a_vbank)
				vbank_history = vbank.retrieve_history( a_vbank.rapyd_id)
				#print('vbank_history')
				#print(vbank_history)
			

			#print(	a_wallet.vbank_account_set.all())
		print("----------------- virtual bank accounts----------------")
		print(vbank_accounts)

		balances  = wallet.retrive_balances(a_wallet.ewallet_rapyd_id)
		print('---------------balances------------------')
		print(balances)
		

		all_wallet_transactions =  wallet.list_transactions(a_wallet.ewallet_rapyd_id, 5)

		print('-----------------all_wallet_transactions---------------------')
		print(all_wallet_transactions)
		#account = json.loads(account_text)[0]
		#print(account)
		#print(request.account)
		#vbank.bank_deposit("issuing_348351c6c69bbacb9c8425082cc2378c")
		all_countries = rapyd.get_countries()
		context = { 'account':account,
					'wallets': wallets,
					'vbank_accounts':vbank_accounts,
					'balances':balances['data'],
					'transactions':all_wallet_transactions['data'][:5],
					"countries": all_countries['data'],}

		return render(request,'soft/profilev2.html', context)
	
	return render(request,'soft/main.html')
		


def contact_detail(request, pk):
	account = Account.objects.get(pk=1)
	return redirect(account)



def log_me_in(request):
	if request.method == "POST":
		request_body = request.POST
		print(request_body)

		email = request_body.get('email', None)
		password = request_body.get('password',None)
		
		print("NEW SHIT")
		#print(Account.objects.get(id=60))
		print(Account.objects.all())

		if email is not None and password is not None:

			try:
				the_account = Account.objects.get(email=email.lower())
				print(the_account.is_active )
				account = authenticate(email=email, password=password)
			except ObjectDoesNotExist :
				account = None
			if account is not None:
				login(request, account)
				
				#ser_obj =  serialize('json', [account], cls=LazyEncoder)

				#print(ser_obj)

				#request.session['account'] = ser_obj
				request.session['account_id'] =account.id 
				messages.info(request, f"You are now logged in as {account}.")
				return redirect("main_page")
			else:
				messages.error(request,"Invalid username or password.")
				print("not authorized")
		else:
			messages.error(request,"Invalid username or password.")
	
	return render(request, "soft/login.html")






def log_me_out(request):
	#request.session['account_id'] =None
	
	logout(request)
	request.session['account_id'] =None
	return redirect("main_page")



def retrive_wallet(request):
	request_body = request.POST
	print(request_body)
	wallet_rapyd_id = request_body.get('ewallet_rapyd_id')
	print(wallet_rapyd_id)
	return JsonResponse(wallet.retrive_wallet(wallet_rapyd_id))
	# context = {"a_wallet" : wallet.retrive_wallet(wallet_rapyd_id)['data']}
	# print(context)
	# return render(request, "soft/wallet.html", context )



def list_vbank(request):
	request_body = request.POST
	print(request_body)
	wallet_rapyd_id = request_body.get('ewallet_rapyd_id')
	print(wallet_rapyd_id)

	return JsonResponse(vbank.list_virtual_accounts(wallet_rapyd_id))


def get_vbank(request):
	request_body = request.POST
	print(request_body)
	# wallet_rapyd_id = request_body.get('ewallet_rapyd_id')
	# print(wallet_rapyd_id)
	
	vbank_rapyd_id = request_body.get('vbank_rapyd_id')
	print(vbank_rapyd_id)

	
	a_vbank =  Vbank_account.objects.get(rapyd_id = vbank_rapyd_id)
	ser_obj =  json.loads(serialize('json', [a_vbank], cls=LazyEncoder))[0]['fields']

	context = {"vbank":ser_obj }
	return render(request, "soft/vbank.html", context)
	#return JsonResponse(vbank.list_virtual_accounts(wallet_rapyd_id))


def make_deposit(request):
	request_body = request.POST
	print(request_body)
	vbank_id = request_body.get('vbank_rapyd_id')
	amount = request_body.get('amount')
	currency = request_body.get('currency')
	print(vbank_id)
	deposit_response =  vbank.bank_deposit(vbank_id, amount, currency)
	
	print("-----------------bank deposit---------------")

	print(deposit_response)
	
	print("-----------------bank deposit end---------------")
	
	return JsonResponse(deposit_response)


def test_vbank(request):
	request_body = request.POST
	print("--------------------test vbank request ---------------")
	print(request_body)
	wallet_rapyd_id = request_body.get('ewallet_rapyd_id')
	
	try:
		a_wallet = Wallet.objects.get(ewallet_rapyd_id=wallet_rapyd_id)
	except ObjectDoesNotExist:
		a_wallet = None
		print("internal DB error")
		return JsonResponse({"server":"error"})


	country_iso = request_body.get('country_iso')
	currency_code = request_body.get('currency_code')

	print(wallet_rapyd_id)
	#all_vbanks = vbank.list_virtual_accounts(wallet_rapyd_id)
	all_vbanks = a_wallet.vbank_account_set.all()

	the_bank_number = None
	
	for a_vbank in all_vbanks:
		
		if a_vbank.country_iso== country_iso:
			print("---------------matched-------------------")
			if a_vbank.iban:
				the_bank_number = a_vbank.iban
			elif  a_vbank.account_no:
				ser_obj =  json.loads(serialize('json', [a_vbank], cls=LazyEncoder))[0]['fields']
        #return  json.dumps( ser_obj)
				the_bank_number = json.dumps( ser_obj)
	
	if the_bank_number == None :
		vbank_response = vbank.create_virtual_bank_account(a_wallet.ewallet_rapyd_id, country_iso, currency_code )
		if vbank_response['status']['status'] =="SUCCESS":
			vbank_account = create_vbank_account_process(a_wallet, vbank_response)
			
			the_bank_number = vbank_response['data']
	
			#country_capabilities = vbank.list_capabilities(country_iso)
				

			return JsonResponse({"account_data": the_bank_number })
		return  JsonResponse({'error': 'currency not supported'})

	return JsonResponse({"account_data": the_bank_number })

{'status': {'error_code': '', 'status': 'SUCCESS', 'message': '', 'response_code': '', 'operation_id': '1dc9e2c9-ec4a-46a0-b133-ab395f1e4d59'}, 'data': {'id': 'issuing_812a6bcb62847b8f713a9029348ce1b4', 'merchant_reference_id': 'issuing_812a6bcb62847b8f713a9029348ce1b4', 'ewallet': 'ewallet_b6ec3fe7475a2595f4e9d05b0cc37a9e', 'bank_account': {'beneficiary_name': 'Rapyd Financial Technology US Inc', 'address': '701 Villa Ave, Mountain View, CA 94041', 'country_iso': 'US', 'country': 'United States', 'aba_routing_number': '051504597', 'account_number': '5002001485351098'}, 'metadata': {}, 'status': 'ACT', 'description': 'Issue test bank account', 'funding_instructions': None, 'currency': 'USD', 'transactions': []}}


def list_capabilities(request):
	
	request_body = request.POST
	print(request_body)
	country_code = request_body.get('country_code')
	print(country_code)

	cpa_response  = vbank.list_capabilities(country_code)
	return JsonResponse(cpa_response)




def create_vbank_account_process(a_wallet, vbank_response):
	vbank_account = Vbank_account()
	vbank_account.rapyd_id = vbank_response['data']['id']
	Vbank_account.merchant_reference_id = vbank_response['data']['merchant_reference_id']
	vbank_account.ewallet_rapyd_id = vbank_response['data']['ewallet']
	vbank_account.beneficiary_name = vbank_response['data']['bank_account']['beneficiary_name']
	vbank_account.country_iso = vbank_response['data']['bank_account']['country_iso']

	if  "account_no" in vbank_response['data']['bank_account']:
		vbank_account.account_no = vbank_response['data']['bank_account']['account_no']
	elif 'account_number' in vbank_response['data']['bank_account']:
		vbank_account.account_no = vbank_response['data']['bank_account']['account_number']


	if  'address' in vbank_response['data']['bank_account']:
		vbank_account.address = vbank_response['data']['bank_account']['address']

	if  'iban' in vbank_response['data']['bank_account'] :
		vbank_account.iban = vbank_response['data']['bank_account']['iban']

	if  'sort_code' in vbank_response['data']['bank_account']:
		vbank_account.sort_code = vbank_response['data']['bank_account']['sort_code']

	if  'bic' in vbank_response['data']['bank_account']:
		vbank_account.bic = vbank_response['data']['bank_account']['bic']


	vbank_account.status = vbank_response['data']['status']
	vbank_account.currency = vbank_response['data']['currency']
	vbank_account.wallet = a_wallet
	vbank_account.save()

	return vbank_account