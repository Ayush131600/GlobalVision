from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('review/add/<str:product_type>/<int:product_id>/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', views.delete_review, name='delete_review'),
]
