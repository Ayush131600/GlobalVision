import os
import re

BASE_DIR = r'c:\Users\Acer\Desktop\GlobalVision\globalvision'
STATIC_CSS = os.path.join(BASE_DIR, 'static', 'css')
os.makedirs(STATIC_CSS, exist_ok=True)

# 1. admin_login.html
login_path = os.path.join(BASE_DIR, 'templates', 'auth', 'admin_login.html')
with open(login_path, 'r', encoding='utf-8') as f:
    admin_login_content = f.read()

style_match = re.search(r'<style>(.*?)</style>', admin_login_content, re.DOTALL)
if style_match:
    css_content = style_match.group(1).strip()
    with open(os.path.join(STATIC_CSS, 'admin_login.css'), 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    css_link = '<link rel="stylesheet" href="{% static \'css/admin_login.css\' %}">'
    if '{% load static %}' not in admin_login_content:
        admin_login_content = '{% load static %}\n' + admin_login_content
    
    admin_login_content = admin_login_content.replace(style_match.group(0), css_link)
    with open(login_path, 'w', encoding='utf-8') as f:
        f.write(admin_login_content)

# 2. base_dashboard.html
base_path = os.path.join(BASE_DIR, 'templates', 'dashboard', 'base_dashboard.html')
with open(base_path, 'r', encoding='utf-8') as f:
    base_dashboard_content = f.read()

# We need to extract the CSS up to {% block extra_css %}
style_match = re.search(r'<style>(.*?)\{%\s*block\s+extra_css', base_dashboard_content, re.DOTALL)
if style_match:
    css_content = style_match.group(1).strip()
    with open(os.path.join(STATIC_CSS, 'dashboard.css'), 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    # We replace from <style> to {% block extra_css %} inclusive
    new_style_block = '<link rel="stylesheet" href="{% static \'css/dashboard.css\' %}">\n<style>\n{% block extra_css'
    
    base_dashboard_content = base_dashboard_content.replace('<style>\\n' + style_match.group(1) + '{% block extra_css', new_style_block)
    
    with open(base_path, 'w', encoding='utf-8') as f:
        f.write(base_dashboard_content)

# 3. forms.py validation
forms_path = os.path.join(BASE_DIR, 'dashboard', 'forms.py')
with open(forms_path, 'r', encoding='utf-8') as f:
    forms_content = f.read()

VALIDATOR_CODE = """
from django.core.exceptions import ValidationError
import os

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, PNG, and WEBP files are allowed.')
"""

# add validation method cleanly if not exist
if 'def validate_image_extension' not in forms_content:
    forms_content = VALIDATOR_CODE + "\\n" + forms_content
    # now append validator to the fields
    # It's cleaner to inject "clean_image" and "clean_cover_image" in the forms.
    clean_image_method = """
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image_extension(image)
        return image
"""
    clean_cover_image_method = """
    def clean_cover_image(self):
        image = self.cleaned_data.get('cover_image')
        if image:
            validate_image_extension(image)
        return image
"""

    forms_content = forms_content.replace('    class Meta:\\n        model = Vehicle', clean_image_method + '    class Meta:\\n        model = Vehicle')
    forms_content = forms_content.replace('    class Meta:\\n        model = Equipment', clean_image_method + '    class Meta:\\n        model = Equipment')
    forms_content = forms_content.replace('    class Meta:\\n        model = BlogPost', clean_cover_image_method + '    class Meta:\\n        model = BlogPost')

    with open(forms_path, 'w', encoding='utf-8') as f:
        f.write(forms_content)

print('Update successful.')
