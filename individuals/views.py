from django.shortcuts import render, redirect

from .forms import NewUserForm, AccountForm
from django.contrib import messages

from django.contrib.auth import login, authenticate ,logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse
from django.core.serializers import serialize

from .payments import rapyd

from .models import *


from .lazy_encoder import LazyEncoder


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
		print(account.password)
		a_wallet =  Wallet()
		
		a_wallet.contact = account
		a_wallet.save()
		a_wallet.set_ref_id()
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
			login(request, account)
			

			ser_obj =  serialize('json', [account], cls=LazyEncoder)

			#print(ser_obj)

			request.session['account'] = ser_obj
		
			messages.success(request, "Registration successful." )
			return redirect("main_page")


	messages.error(request, "Unsuccessful registration. Invalid information.")
	return redirect("sign_up")
	
	
	
	#return JsonResponse({"id":ewallet_rapyd_id})
	#return render(request,'soft/profile.html', {})




	#{'status': {'error_code': '', 'status': 'SUCCESS', 'message': '', 'response_code': '', 'operation_id': '31f8f6a9-0ea2-477f-a14d-54bc62ccc8bb'}, 'data': {'phone_number': '+14155551233', 'email': 'eeysdfteyt@loook.com', 'first_name': 'bob', 'last_name': 'tabor', 'id': 'ewallet_cd86354398b399f53f3eff6cefcde394', 'status': 'ACT', 'accounts': [], 'verification_status': 'not verified', 'type': 'person', 'metadata': {'merchant_defined': True}, 'ewallet_reference_id': 'bob-tabor-2022-07-26 10:34:45.901185', 'category': None, 'contacts': {'data': [{'id': 'cont_82c3f65396018151b52fc9996548fecf', 'first_name': 'bob', 'last_name': 'tabor', 'middle_name': '', 'second_last_name': '', 'gender': 'not_applicable', 'marital_status': 'not_applicable', 'house_type': '', 'contact_type': 'personal', 'phone_number': '+14155551233', 'email': 'eeysdfteyt@loook.com', 'identification_type': 'DL', 'identification_number': '252736576', 'issued_card_data': {'preferred_name': '', 'transaction_permissions': '', 'role_in_company': ''}, 'date_of_birth': None, 'country': 'US', 'nationality': None, 'address': {'id': 'address_42b8b38b631899c3b3152892b9e312d1', 'name': 'bob tabor', 'line_1': 'United States of America', 'line_2': '', 'line_3': '', 'city': '', 'state': '', 'country': '', 'zip': '', 'phone_number': '', 'metadata': {}, 'canton': '', 'district': '', 'created_at': 1658824487}, 'ewallet': 'ewallet_cd86354398b399f53f3eff6cefcde394', 'created_at': 1658824487, 'metadata': {'merchant_defined': True}, 'business_details': None, 'compliance_profile': 0, 'verification_status': 'not verified', 'send_notifications': False, 'mothers_name': ''}], 'has_more': False, 'total_count': 1, 'url': '/v1/ewallets/ewallet_cd86354398b399f53f3eff6cefcde394/contacts'}}}



def main_page(request):
	request_body = request.POST
	#print(request_body)
	#print(request.GET)
	account_text = request.session.get('account', None)
	if account != None
		print(account_text)
		account = json.loads(account_text)[0]
		print(account)
		#print(request.account)
	return render(request,'soft/profile.html', account)


def contact_detail(request, pk):
	account = Account.objects.get(pk=1)
	return redirect(account)

