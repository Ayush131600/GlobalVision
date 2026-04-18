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
        fields = ['user_name', 'email', 'phone_no', 'dob', 'address', 'profile_photo']
        widgets = {
            'phone_no': forms.TextInput(attrs={'type': 'tel', 'pattern': '[0-9]{10,15}', 'title': 'Please enter 10 to 15 digits'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'profile_photo': forms.FileInput(attrs={'class': 'd-none', 'id': 'profilePhotoUpload', 'accept': 'image/*'}),
        }

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if not phone_no.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if not (10 <= len(phone_no) <= 15):
            raise forms.ValidationError("Phone number should be between 10 and 15 digits.")
        return phone_no
