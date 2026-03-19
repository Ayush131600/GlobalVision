import os
import re

directory = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates\account'
files_to_process = ['home.html', 'about.html', 'contact.html', 'rent_vehicle.html', 'rent_equipment.html', 'product_detail.html', 'blog.html']

for filename in files_to_process:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # If already extending, assume it's processed
    if '{% extends' in content:
        print(f"Skipped {filename} (already extends)")
        continue
    
    # Parse title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else 'Global Vision'
    if '{% block title %}' in title:
        title = title.replace('{% block title %}', '').replace('{% endblock %}', '').strip()

    # Parse CSS
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    css = css_match.group(1) if css_match else ''
    
    # We won't eagerly remove CSS via regex to avoid breaking things, 
    # but we can remove the obvious global blocks.
    css = re.sub(r':root\s*\{.*?\}(?=\s*(?:\*|\.|\n))', '', css, flags=re.DOTALL)
    css = re.sub(r'\*\s*\{\s*margin:\s*0;\s*padding:\s*0;\s*box-sizing:\s*border-box;\s*\}', '', css)
    # The body could have specific styles we want to keep, let's keep it but maybe we need it?
    # Actually, for CSS we will just keep everything and let it override if needed, or remove what we know.
    # It's safer to keep the CSS, but it might duplicate. This is fine since it's scoped properly.

    # Extract body content (between </header> and <footer>)
    body_match = re.search(r'</header>\s*(.*?)\s*<footer', content, re.DOTALL)
    body_content = body_match.group(1) if body_match else ''

    # Extract scripts
    scripts_match = re.search(r'</footer>\s*(<script>.*?</script>)?', content, re.DOTALL)
    scripts = scripts_match.group(1) if (scripts_match and scripts_match.group(1)) else ''

    # Extract anything between <body> and <header> (e.g., search modal in home.html)
    pre_header_match = re.search(r'<body>\s*(.*?)\s*<header>', content, re.DOTALL)
    pre_header = pre_header_match.group(1) if pre_header_match else ''

    # Optional: home.html has absolute header. We will just use the sticky header from base for consistency.
    # So we don't need to save header CSS.

    new_content = f"""{{% extends 'account/base.html' %}}
{{% load static %}}

{{% block title %}}{title}{{% endblock %}}

{{% block extra_css %}}
{css.strip()}
{{% endblock %}}

{{% block content %}}
{pre_header.strip()}
{body_content.strip()}
{{% endblock %}}

{{% block extra_scripts %}}
{scripts.strip()}
{{% endblock %}}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'Processed {filename}')
