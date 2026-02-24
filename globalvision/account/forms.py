from django import forms
from .models import Vehicle, Equipment, BlogPost, User

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['name', 'image', 'price_per_day', 'description', 'category', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'image', 'price_per_day', 'description', 'category', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'email', 'phone_no', 'dob', 'address']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
