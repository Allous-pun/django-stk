from django.urls import path
from . import views
from .views import TransactionCreateView


urlpatterns = [
    path('initiate/', views.initiate_payment, name='initiate_payment'),
    path('status/<int:transaction_id>/', views.payment_status, name='payment_status'),
    path('callback/', views.stk_callback, name='stk_callback'),
    path('api/transactions/', TransactionCreateView.as_view(), name='transaction-create'),
]
