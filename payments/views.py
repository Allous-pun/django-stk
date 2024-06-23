from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import TransactionForm
from .models import Transaction
from .services import DarajaAPI
from .serializer import TransactionSerializer

# Existing views for server-side rendering
def initiate_payment(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            response = DarajaAPI.send_stk_push(transaction)
            if response['ResponseCode'] == '0':
                transaction.transaction_id = response['CheckoutRequestID']
                transaction.status = 'Pending'
            else:
                transaction.status = 'Failed'
            transaction.save()
            return redirect('payment_status', transaction_id=transaction.id)
    else:
        form = TransactionForm()
    return render(request, 'payments/initiate_payment.html', {'form': form})

def payment_status(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'payments/payment_status.html', {'transaction': transaction})

@csrf_exempt
def stk_callback(request):
    data = request.json()
    checkout_request_id = data['Body']['stkCallback']['CheckoutRequestID']
    result_code = data['Body']['stkCallback']['ResultCode']
    result_desc = data['Body']['stkCallback']['ResultDesc']

    try:
        transaction = Transaction.objects.get(transaction_id=checkout_request_id)
        if result_code == 0:
            transaction.status = 'Success'
        else:
            transaction.status = 'Failed'
        transaction.save()
    except Transaction.DoesNotExist:
        pass

    return JsonResponse({"ResultDesc": "Success", "ResultCode": 0})

# New views for API endpoints
class TransactionCreateView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
