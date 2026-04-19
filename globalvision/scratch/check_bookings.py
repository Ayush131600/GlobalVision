import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(r'c:\Users\Acer\Desktop\GlobalVision\globalvision')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalvision.settings')
django.setup()

from bookings.models import Booking
from inventory.models import Vehicle, Equipment
from django.contrib.contenttypes.models import ContentType

print("--- Bookings ---")
for b in Booking.objects.all():
    print(f"ID: {b.id}, Item: {b.item}, Dates: {b.start_date} to {b.end_date}, Status: {b.status}, Stock check: {b.item.stock if b.item else 'N/A'}")

print("\n--- Vehicles ---")
for v in Vehicle.objects.all():
    print(f"ID: {v.id}, Name: {v.name}, Stock: {v.stock}")
