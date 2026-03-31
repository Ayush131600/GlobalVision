from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    model_icon = 'event_available'
    list_display = ('id', 'user', 'item', 'start_date', 'end_date', 'status', 'total_price')
    list_filter = ('status', 'start_date')
    search_fields = ('user__username', 'user__email')
