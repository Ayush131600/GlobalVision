from django.urls import path
from . import views

urlpatterns = [
    path('esewa/pay/<int:transaction_id>/', views.initiate_esewa_payment, name='initiate_esewa_payment'),
    path('esewa/success/', views.esewa_success, name='esewa_success'),
    path('esewa/failure/', views.esewa_failure, name='esewa_failure'),
]
