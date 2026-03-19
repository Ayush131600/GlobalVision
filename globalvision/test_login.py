import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "globalvision.settings")
django.setup()

from django.test import Client
c = Client(SERVER_NAME='127.0.0.1')
resp = c.post('/admin-login/', {'username': 'spideradmin', 'password': 'password'})
print("ADMIN LOGIN:", resp.status_code, resp.content.decode()[:200])
