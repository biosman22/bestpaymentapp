# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


import datetime

from django.urls import reverse

# Create your models here.


class Account(AbstractBaseUser):
    marital_status_CHOICES = [
        ('married', 'Married'),
        ('single', 'Single'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('cohabiting', 'Cohabiting'),
        ('not_applicable', 'Not_applicable'),
    ]


    contact_type_CHOICES = [
        ('personal', 'Personal'), # A personal wallet only allows one contact per wallet.
        ('business', 'Business'), # A business can allow more than one contact linked to a wallet.
    ]

    
    gender_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('not_applicable', 'Prefer not to tell')
    ]
    

    email = models.CharField(max_length=50, unique=True)
    first_name =  models.CharField(max_length=20)
    last_name =   models.CharField(max_length=20)
    phone_number =  models.CharField(max_length=12)
    
    phone_code =  models.CharField(max_length=7)

    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50,blank=True)
    address_line = models.CharField(max_length=200, blank=True)
    state  = models.CharField(max_length=200, blank=True)
    zip_code  = models.CharField(max_length=200, blank=True)
    address_rapyd_id = models.CharField(max_length=80, blank=True)

    contact_type = models.CharField(max_length=10, choices=contact_type_CHOICES, default="person")
    date_of_birth = models.DateField(blank=True,null=True)
    identification_type = models.CharField(max_length=3, default="PA", blank=True) #PA, DL, ID
    identification_number = models.CharField(max_length=50, blank=True)

    marital_status = models.CharField(max_length=14 , choices=marital_status_CHOICES, default ='not_applicable') # * married, single, divorced, widowed, cohabiting, not_applicable
    gender = models.CharField(max_length=14, choices=gender_CHOICES, default="not_applicable")  #* male, female
    contact_rapyd_id = models.CharField(max_length=50, blank=True)  # returned value
    contact_url = models.CharField(max_length=50, blank=True) # returned value
    verification_status = models.CharField(max_length=50, default='not verified')
    USERNAME_FIELD = 'email'

    def get_absolute_url(self):
        
        return reverse('contact_detail', kwargs={'pk' : self.pk})



class Wallet(models.Model):

    wallet_type_CHOICES = [
        ('person', 'Person'), # One personal contact.
        ('company', 'Company'), # One business contact and multiple personal contacts.
        ('client', 'Client'), #  Each client wallet has one business contact and multiple personal contacts.
    
    ]

    type_of_wallet = models.CharField(max_length=10, choices=wallet_type_CHOICES, default='person')

    ewallet_reference_id = models.CharField(max_length=100)
    ewallet_rapyd_id = models.CharField(max_length=80, blank=True) # returned value

    contact = models.OneToOneField(Account,on_delete=models.CASCADE)
    def set_ref_id(self,):
        ref = self.contact.first_name+"-"+self.contact.last_name+"-"+ str(datetime.datetime.now())
        self.ewallet_reference_id = ref