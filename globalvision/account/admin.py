from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    model_icon = 'person'
    fieldsets = (
        ("Authentication", {"fields": ("user_name", "password")}),
        ("Personal Profile", {"fields": ("email", "phone_no", "dob", "address", "profile_photo")}),
        ("Governance & Roles", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("System Permissions", {"fields": ("groups", "user_permissions")}),
        ("Audit Logs", {"fields": ("last_login", "created_at")}),
    )
    re0adonly_fields = ("created_at", "last_login")
    list_display = ("user_name", "email", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("user_name", "email")
    ordering = ("user_name",)
    filter_horizontal = ("groups", "user_permissions")
