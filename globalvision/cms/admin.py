from django.contrib import admin
from unfold.admin import ModelAdmin
from django_summernote.admin import SummernoteModelAdmin
from .models import SiteSettings, AboutPage, TeamMember

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    model_icon = 'settings'
    fieldsets = (
        ("Contact Information", {
            "fields": ("phone", "whatsapp", "email", "address"),
        }),
        ("Operating Hours & Location", {
            "fields": ("hours", "maps_embed"),
        }),
        ("Social Presence", {
            "fields": ("facebook_url", "instagram_url", "tripadvisor_url"),
        }),
    )

@admin.register(AboutPage)
class AboutPageAdmin(ModelAdmin, SummernoteModelAdmin):
    model_icon = 'info'
    summernote_fields = ('mission', 'story')
    readonly_fields = ('updated_at',)
    
    fieldsets = (
        ("Our Core", {
            "fields": ("mission", "story"),
        }),
        ("Growth Metrics", {
            "fields": ("stat_years", "stat_treks", "stat_clients", "stat_team"),
        }),
        ("Metadata", {
            "fields": ("updated_at",),
        }),
    )

@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    model_icon = 'groups'
    list_display = ('name', 'role', 'display_order')
