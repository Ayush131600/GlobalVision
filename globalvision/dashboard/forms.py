from django import forms
from inventory.models import Vehicle, Equipment
from blog.models import BlogPost
from cms.models import TeamMember, AboutPage, SiteSettings
from contacts.models import ContactMessage
from django_summernote.widgets import SummernoteWidget

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'category', 'price_per_day', 'status', 'description', 'image']

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'price_per_day', 'stock', 'status', 'description', 'image']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'cover_image', 'body', 'is_published']
        widgets = {
            'body': SummernoteWidget()
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'favourite_trek', 'photo', 'display_order']

class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = ['mission', 'story', 'stat_years', 'stat_treks', 'stat_clients', 'stat_team']
        widgets = {
            'mission': SummernoteWidget(),
            'story': SummernoteWidget(),
        }

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'