from django.shortcuts import render, redirect

from .forms import NewUserForm
from django.contrib import messages

from django.contrib.auth import login, authenticate ,logout #add this
from django.contrib.auth.forms import AuthenticationForm #add this

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, FileResponse

from .payments.rapyd import *

# Create your views here.



def homepage(request):
	get_countries()
	#create_wallet()
	#country_required_documents()
	#verify_identity()
	#create_virtual_bank_account()
	#list_virtual_accounts()
	#bank_deposit()
	return render(request,'home.html')


def country_documents(request):
	country_required_documents()
	return 


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
	all_countries = get_countries()
	#create_wallet()
	#country_required_documents()
	#verify_identity()
	#create_virtual_bank_account()
	#list_virtual_accounts()
	#bank_deposit()
	return render(request,'soft/sign_up.html', {"countries": all_countries['data']})