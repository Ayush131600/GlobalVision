from django.contrib import admin
from .models import SiteSettings, AboutPage, TeamMember

admin.site.register(SiteSettings)
admin.site.register(AboutPage)
admin.site.register(TeamMember)
