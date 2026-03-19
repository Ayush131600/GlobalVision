import re

base_path = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates\dashboard\base_dashboard.html'
with open(base_path, 'r', encoding='utf-8') as f:
    text = f.read()

replacement = '<link rel="stylesheet" href="{% static ' + "'" + 'css/dashboard.css' + "'" + ' %}">\n<style>\n{% block extra_css'

text = re.sub(r'<style>.*?\{%\s*block\s+extra_css', replacement, text, flags=re.DOTALL)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Done")
