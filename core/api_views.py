# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Package
from .serializer import PackageSerializer

# Existing views remain as is
from django.shortcuts import render, get_object_or_404
from payments.forms import TransactionForm

def package_list(request):
    packages = Package.objects.all()
    return render(request, 'core/package_list.html', {'packages': packages})

def select_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    initial_data = {
        'package': package.name,
        'amount': package.price,
    }
    form = TransactionForm(initial=initial_data)
    return render(request, 'payments/initiate_payment.html', {'form': form, 'package': package})

def home(request):
    return render(request, 'core/home.html')

# New API views
class PackageListView(APIView):
    def get(self, request):
        packages = Package.objects.all()
        serializer = PackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
