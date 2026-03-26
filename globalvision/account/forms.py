from django import forms
from inventory.models import Vehicle, Equipment
from blog.models import BlogPost
from .models import User

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'image', 'price_per_day', 'description', 'category', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'image', 'price_per_day', 'description', 'category', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'cover_image']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 10}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email', 'phone_no', 'dob', 'address']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
