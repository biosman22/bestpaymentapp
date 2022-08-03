# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from .lazy_encoder import LazyEncoder
from django.core.serializers import serialize
import datetime

from django.urls import reverse
import json
# Create your models here.



class AccountsManager(BaseUserManager):
    def create_user(self, email=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            #date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            #date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    #def get_by_natural_key(self, email):
    #     return self.get(email=email)






class Wallet(models.Model):

    wallet_type_CHOICES = [
        ('person', 'Person'), # One personal contact.
        ('company', 'Company'), # One business contact and multiple personal contacts.
        ('client', 'Client'), #  Each client wallet has one business contact and multiple personal contacts.
    
    ]

    type_of_wallet = models.CharField(max_length=10, choices=wallet_type_CHOICES, default='person')

    ewallet_reference_id = models.CharField(max_length=100)
    ewallet_rapyd_id = models.CharField(max_length=100, blank=True) # returned value
    

    def set_ref_id(self,first_name, last_name):
        #ref = self.contact.first_name+"-"+self.contact.last_name+"-"+ str(datetime.datetime.now())
        ref = first_name+"-"+last_name+"-"+ str(self.id)
        self.ewallet_reference_id = ref




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
    currency_code =  models.CharField(max_length=5, default='GBP')
    
    objects = AccountsManager()
    USERNAME_FIELD = 'email'
    wallets = models.ManyToManyField(Wallet)

    REQUIRED_FIELDS =[]  
    #                    ['first_name', 
    #                     'last_name',
    #                     'phone_number',
    #                     'phone_code', 
    #                     'country_name'
                        #'contact_type',
                        #'marital_status',
                        #'gender',
                        #'verification_status']
    
    def __str__(self):
        #ser_obj =  json.loads(serialize('json', [self], cls=LazyEncoder))[0]['fields']
        #return  json.dumps( ser_obj)
        return self.email
    class Meta:
        pass
        #ordering = ('-country_code')#, '-updated_at', )
    def get_full_name(self):
        if self.first_name:
            return f'{self.first_name}  {self.last_name}'
        return self.email.split('@')[0]
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    

    # def get_absolute_url(self):
        
    #     return reverse('contact_detail', kwargs={'pk' : self.pk})




class Vbank_account(models.Model):
    rapyd_id =  models.CharField(max_length=100 )
    merchant_reference_id = models.CharField(max_length=100 )
    ewallet_rapyd_id = models.CharField(max_length=100)
    #account in response
    beneficiary_name = models.CharField(max_length=100 )
    address = models.CharField(max_length=100, blank=True)
    country_iso = models.CharField(max_length=5)
    iban = models.CharField(max_length=100, blank=True)
    sort_code = models.CharField(max_length=20, blank=True)
    account_no =  models.CharField(max_length=20)
    bic = models.CharField(max_length=20, blank=True)
    #--- end account
    status = models.CharField(max_length=5)
    currency = models.CharField(max_length=5)
    #transactions still not here

    wallet =  models.ForeignKey(Wallet, on_delete=models.CASCADE)






class Transaction(models.Model):
    vbank_account =  models.ForeignKey(Wallet, on_delete=models.CASCADE)
    
    rapyd_id =  models.CharField(max_length=100 )
    amount =  models.CharField(max_length=10)
    currency = models.CharField(max_length=5)


    #{'id': 'issuing_348351c6c69bbacb9c8425082cc2378c', 'merchant_reference_id': 'issuing_348351c6c69bbacb9c8425082cc2378c', 'ewallet': 'ewallet_adab89ee81d8091f3f918f86fe64eefa', 'bank_account': {'beneficiary_name': 'CashDash UK Limited', 'address': 'Northwest House, 119 Marylebone Road NW1 5PU', 'country_iso': 'GB', 'iban': 'GB36SAPY60838292780648', 'sort_code': '608382', 'account_no': '0092780648', 'bic': 'SAPYGB2L'}, 'metadata': {}, 'status': 'ACT', 'description': 'Issue test bank account', 'funding_instructions': None, 'currency': 'GBP', 'transactions': [{'id': 'isutran_e3d96e453e20b7c4a21aecca73351ce0', 'amount': 100, 'currency': 'GBP', 'created_at': 1659108204}]}



# wallet transaction
# {
#             "id": "wt_71dfe7cafb8504c8d623e76577247b87",
#             "amount": 120,
#             "currency": "MXN",
#             "ewallet_id": "ewallet_95feaa629caa5ef64c49e5c24b29171d",
#             "type": "payment_funds_in",
#             "balance_type": "available_balance",
#             "balance": 455719,
#             "created_at": 1653218443,
#             "status": "CLOSED",
#             "reason": "",
#             "metadata": {
#                 "merchant-defined": true
#             }
#         },


# # vbank transactions 
# {
#                 "id": "isutran_38be3b9c019f337a5a12bd47eb0fd3bd",
#                 "amount": 23,
#                 "currency": "EUR",
#                 "created_at": 1547376134
#             },


