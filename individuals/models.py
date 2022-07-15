# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


import datetime

# Create your models here.


class Account(AbstractBaseUser):
    marital_status_CHOICES = [
        ('Married', 'Married'),
        ('Single', 'Single'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        ('Cohabiting', 'Cohabiting'),
        ('Not_applicable', 'Not_applicable'),
    ]


    contact_type_CHOICES = [
        ('Personal', 'Personal'),
        ('Business', 'Business'),
    ]

    
    gender_CHOICES = [
        ('Personal', 'Personal'),
        ('Business', 'Business'),
    ]
    

    email = models.CharField(max_length=50, unique=True)
    first_name =  models.CharField(max_length=20)
    last_name =   models.CharField(max_length=20)
    phone_number =  models.CharField(max_length=15)

    country =  models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address_line = models.CharField(max_length=200)
    state  = models.CharField(max_length=200)
    zip_code  = models.CharField(max_length=200)

    contact_type = models.CharField(max_length=10, choices=contact_type_CHOICES, default="personal")
    date_of_birth = models.DateField()
    identification_type = models.CharField(max_length=3, default="PA") #PA, DL, ID
    identification_number = models.CharField(max_length=50)

    marital_status = models.CharField(max_length=20 , choices=marital_status_CHOICES, default ='Single') # * married, single, divorced, widowed, cohabiting, not_applicable
    gender = models.CharField(max_length=6, choices=gender_CHOICES, default="male")  #* male, female
    contact_id = models.CharField(max_length=50)  # returned value
    contact_url = models.CharField(max_length=50)
    verification_status = models.CharField(max_length=50,default='not verified')
    USERNAME_FIELD = 'email'



class Wallet(models.Model):
    type_of_wallet = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    first_name =  models.CharField(max_length=20)
    last_name =   models.CharField(max_length=20)
    phone_number =  models.CharField(max_length=15)
    ewallet_reference_id = first_name+"-"+last_name+"-"+ datatime.date.today()
    contact = models.OneToOneField(Account,on_delete=models.CASCADE)