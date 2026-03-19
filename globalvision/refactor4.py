import os
import re

directory = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates\account'
files_to_process = ['rent_vehicle.html', 'rent_equipment.html']

for filename in files_to_process:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else 'Global Vision'

    # Extract CSS
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    css = css_match.group(1) if css_match else ''
    
    # Remove common blocks gently
    css = re.sub(r':root\s*\{.*?\}(?=\s*(?:\*|\.|\n))', '', css, flags=re.DOTALL)
    css = re.sub(r'\*\s*\{\s*box-sizing:\s*border-box;\s*margin:\s*0;\s*padding:\s*0;\s*\}', '', css)
    css = re.sub(r'\*\s*\{\s*margin:\s*0;\s*padding:\s*0;\s*box-sizing:\s*border-box;\s*\}', '', css)
    
    # Find everything between </header> and </body>
    body_match = re.search(r'</header>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
    if not body_match:
        print(f"Failed to find boundary in {filename}")
        continue
    
    body_content = body_match.group(1)

    # scripts
    scripts_match = re.search(r'<script>(.*?)</script>', body_content, re.DOTALL | re.IGNORECASE)
    scripts = scripts_match.group(0) if scripts_match else ''
    # remove scripts from body
    if scripts:
        body_content = body_content.replace(scripts, '')

    new_content = f"""{{% extends 'account/base.html' %}}
{{% load static %}}

{{% block title %}}{title}{{% endblock %}}

{{% block extra_css %}}
{css.strip()}
{{% endblock %}}

{{% block content %}}
{body_content.strip()}
{{% endblock %}}

{{% block extra_scripts %}}
{scripts.strip()}
{{% endblock %}}
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Processed {filename}')
