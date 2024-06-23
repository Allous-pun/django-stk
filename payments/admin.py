from django.contrib import admin
from .models import Transaction

#register the transaction model with the admin site 
admin.site.register(Transaction)
