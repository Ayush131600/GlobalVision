from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
