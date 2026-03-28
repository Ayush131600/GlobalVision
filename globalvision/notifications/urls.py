from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.notification_list, name='notification_list'),
    path('api/get/', views.get_notifications, name='get_notifications'),
    path('api/mark-read/<int:notification_id>/', views.mark_read, name='mark_read'),
    path('api/mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('admin/send/', views.send_admin_notification, name='admin_notifications'),
]
