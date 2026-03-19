from django import forms
from .models import Vehicle, Equipment, BlogPost
from django.core.exceptions import ValidationError
import os
from django_summernote.widgets import SummernoteWidget

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, PNG, and WEBP files are allowed.')

class VehicleForm(forms.ModelForm):
    image = forms.ImageField(validators=[validate_image_extension], required=False)
    class Meta:
        model = Vehicle
        fields = ['name', 'type', 'description', 'price_per_day', 'is_available', 'image']

class EquipmentForm(forms.ModelForm):
    image = forms.ImageField(validators=[validate_image_extension], required=False)
    class Meta:
        model = Equipment
        fields = ['name', 'category', 'description', 'price_per_day', 'stock', 'image']

class BlogPostForm(forms.ModelForm):
    cover_image = forms.ImageField(validators=[validate_image_extension], required=False)
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'cover_image', 'status']
        widgets = {
            'content': SummernoteWidget()
        }