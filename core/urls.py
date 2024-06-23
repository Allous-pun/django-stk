from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.package_list, name='package_list'),
    path('packages/select/<int:package_id>/', views.select_package, name='select_package'),
    path('api/packages/', views.package_list, name='package_list'),
    path('api/transactions/', views.select_package, name= "select_package" )
    
]