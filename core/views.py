
from django.shortcuts import render, get_object_or_404
from .models import Package
from payments.forms import TransactionForm
from django.http import JsonResponse

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