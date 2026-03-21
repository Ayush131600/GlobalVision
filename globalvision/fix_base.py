import re

base_path = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates\dashboard\base_dashboard.html'
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire style block perfectly
content = re.sub(r'<style>.*?\{%\s*block\s+extra_css', '<link rel="stylesheet" href="{% static \\"css/dashboard.css\\" %}">\\n<style>\\n{% block extra_css', content, flags=re.DOTALL)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed base dash')
