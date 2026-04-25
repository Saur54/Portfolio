import os

file_path = 'portfolio/templates/portfolio/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define regex patterns or boundaries to extract sections
import re

def extract_section(section_id, text):
    pattern = r'(<!-- ' + section_id.upper() + r' -->\s*<section id="' + section_id + r'".*?</section>)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    # try without comment if needed
    pattern2 = r'(<section id="' + section_id + r'".*?</section>)'
    match = re.search(pattern2, text, re.DOTALL | re.IGNORECASE)
    return match.group(1) if match else ''

home = extract_section('home', content)
about = extract_section('about', content)
education = extract_section('education', content)
experience = extract_section('experience', content)
skills = extract_section('skills', content)
services = extract_section('services', content)
projects = extract_section('projects', content)
contact = extract_section('contact', content)

# Header (everything before home)
header_match = re.search(r'(.*?)(<!-- HERO -->|<section id="home">)', content, re.DOTALL)
header = header_match.group(1) if header_match else ''

# Footer (everything after contact)
footer_match = re.search(r'</section>\s*(<!-- Modal.*)', content, re.DOTALL)
footer = '\n\n' + footer_match.group(1) if footer_match else ''
if not footer_match:
    # Fallback for footer part
    parts = content.split('</section>')
    footer = '\n\n' + '</section>'.join(parts[8:])

# Combine in new order
new_content = header + \
              "<!-- HERO -->\n" + home + "\n\n" + \
              "<!-- ABOUT -->\n" + about + "\n\n" + \
              "<!-- EDUCATION -->\n" + education + "\n\n" + \
              "<!-- EXPERIENCE -->\n" + experience + "\n\n" + \
              "<!-- SKILLS -->\n" + skills + "\n\n" + \
              "<!-- SERVICES -->\n" + services + "\n\n" + \
              "<!-- PROJECTS -->\n" + projects + "\n\n" + \
              "<!-- CONTACT -->\n" + contact + \
              footer

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Reordering complete.")
