from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Vehicle, Equipment

@admin.register(Vehicle)
class VehicleAdmin(ModelAdmin):
    model_icon = 'directions_car'
    list_display = ('name', 'category', 'price_per_day', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ("General Details", {
            "fields": ("name", "category", "description", "image"),
        }),
        ("Rental Options", {
            "fields": ("price_per_day", "status", "created_at"),
        }),
    )

@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    model_icon = 'hiking'
    list_display = ('name', 'category', 'price_per_day', 'stock', 'status')
    list_filter = ('category', 'status')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

    fieldsets = (
        ("Item Specifications", {
            "fields": ("name", "category", "description", "image"),
        }),
        ("Inventory & Pricing", {
            "fields": ("price_per_day", "stock", "status", "created_at"),
        }),
    )
