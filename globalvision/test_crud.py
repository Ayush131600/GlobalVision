import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "globalvision.settings")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from dashboard.models import Vehicle

c = Client(SERVER_NAME='127.0.0.1')
User = get_user_model()
admin_user = User.objects.filter(is_staff=True).first()
if admin_user:
    c.force_login(admin_user)

print("Starting Add Vehicle")
# Try adding vehicle without is_available
resp = c.post('/dashboard/vehicles/add/', {
    'name': 'Test Car',
    'type': 'car',
    'description': 'Description',
    'price_per_day': '10',
    'image': ''
})

print("POST Status:", resp.status_code)
if resp.status_code == 200:
    print("Add Vehicle Edit errors:", resp.context['form'].errors)

# count vehicles
print("Count:", Vehicle.objects.count())

# Try updating the vehicle
v = Vehicle.objects.first()
if v:
    print("Starting Edit")
    resp_edit = c.post(f'/dashboard/vehicles/{v.id}/edit/', {
        'name': 'Edited Car',
        'type': 'jeep',
        'description': 'D',
        'price_per_day': '20',
        'is_available': True,
        'image': ''
    })
    print("Edit Status:", resp_edit.status_code)
    
    print("Starting Delete")
    resp_del = c.post(f'/dashboard/vehicles/{v.id}/delete/')
    print("Delete Status:", resp_del.status_code)
