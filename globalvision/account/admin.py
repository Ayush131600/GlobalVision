from django.contrib import admin
from .models import User, Vehicle, Equipment, BlogPost

admin.site.register(User)
admin.site.register(Vehicle)
admin.site.register(Equipment)
admin.site.register(BlogPost)
