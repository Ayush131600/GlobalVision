import os
import re

SETTINGS_PATH = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\globalvision\settings.py'
URLS_PATH = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\globalvision\urls.py'

# Update URLs
with open(URLS_PATH, 'r', encoding='utf-8') as f:
    urls_content = f.read()

if 'path(\\'admin-login/\\'' not in urls_content:
    # Need to add to urlpatterns and imports
    # Safely insert imports
    if 'from dashboard.views import admin_login_view' not in urls_content:
        import_str = "\\nfrom dashboard.views import admin_login_view\\nfrom django.conf import settings\\nfrom django.conf.urls.static import static\\n"
        urls_content = urls_content.replace('from django.urls import path, include', 'from django.urls import path, include' + import_str)
    
    # Safely insert url patterns
    new_urls = """
    path('admin-login/', admin_login_view, name='admin_login'),
    path('dashboard/', include('dashboard.urls')),
"""
    # find where urlpatterns = [ ends or just append to urlpatterns
    urls_content += "\\nurlpatterns += [" + new_urls + "]\\n"
    urls_content += "urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\\n"

    with open(URLS_PATH, 'w', encoding='utf-8') as f:
        f.write(urls_content)


# Update Settings
with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
    settings_content = f.read()

app_str = "\\n    'dashboard',\\n    'django_summernote',"
if "\\'dashboard\\'" not in settings_content and '"dashboard"' not in settings_content:
    # Add to INSTALLED_APPS
    settings_content = settings_content.replace("INSTALLED_APPS = [", "INSTALLED_APPS = [" + app_str)

summernote_config = """

MEDIA_URL = '/media/'
import os
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'height': '400px',
        'toolbar': [
            ['style', ['bold', 'italic', 'underline', 'clear']],
            ['font', ['strikethrough']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen', 'codeview']],
        ],
    }
}
"""

if 'SUMMERNOTE_CONFIG' not in settings_content:
    settings_content += summernote_config

with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
    f.write(settings_content)

