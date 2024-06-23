
# payments/services.py

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

class DarajaAPI:
    @staticmethod
    def get_access_token():
        
        consumer_key = settings.DARAJA_CONSUMER_KEY
        consumer_secret = settings.DARAJA_CONSUMER_SECRET
        authorization_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(authorization_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        json_response = response.json()
        return json_response['access_token']

    @staticmethod
    def generate_password():
        
        shortcode = settings.BUSINESS_SHORT_CODE
        lipa_na_mpesa_online_passkey = settings.LIPA_NA_MPESA_ONLINE_PASSKEY
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = shortcode + lipa_na_mpesa_online_passkey + timestamp
        encoded_string = base64.b64encode(data_to_encode.encode())
        return encoded_string.decode('utf-8')

    @staticmethod
    def send_stk_push(transaction):
         
        access_token = DarajaAPI.get_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer " + access_token}
        payload = {
            "BusinessShortCode": settings.BUSINESS_SHORT_CODE,
            "Password": DarajaAPI.generate_password(),
            "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": transaction.amount,
            "PartyA": transaction.phone_number,
            "PartyB": settings.BUSINESS_SHORT_CODE,
            "PhoneNumber": transaction.phone_number,
            "CallBackURL": settings.CALLBACK_URL,
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": f"Payment for {transaction.package}"
        }
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()