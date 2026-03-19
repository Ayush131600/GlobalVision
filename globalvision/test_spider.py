import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "globalvision.settings")
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
try:
    admin = User.objects.get(user_name='spideradmin')
except User.DoesNotExist:
    admin = User.objects.create_superuser('spideradmin', 'spider@test.com', 'pass')

c = Client(SERVER_NAME='127.0.0.1')
c.force_login(admin)

urls = [
    '/dashboard/',
    '/dashboard/vehicles/',
    '/dashboard/vehicles/add/',
    '/dashboard/equipment/',
    '/dashboard/equipment/add/',
    '/dashboard/blog/',
    '/dashboard/blog/add/',
    '/dashboard/about/',
    '/dashboard/contact/',
]

for u in urls:
    try:
        resp = c.get(u)
        if resp.status_code != 200:
            print(f"STATUS {resp.status_code} ON {u}")
        else:
            print(f"OK: {u}")
    except Exception as e:
        print(f"CRASH ON {u}: {e}")
        import traceback
        traceback.print_exc()
