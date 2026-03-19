from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.vehicle_add, name='vehicle_add'),
    path('vehicles/<int:pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/add/', views.equipment_add, name='equipment_add'),
    path('equipment/<int:pk>/edit/', views.equipment_edit, name='equipment_edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='equipment_delete'),
    
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/add/', views.blog_add, name='blog_add'),
    path('blog/<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    
    path('about/', views.about_editor, name='about_editor'),
    path('contact/', views.contact_editor, name='contact_editor'),
    path('logout/', views.admin_logout_view, name='admin_logout'),
]