import html
import re
import glob
import os

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find all <script>...</script> blocks that have content (not just src)
    pattern = re.compile(r'(<script[^>]*>)(.*?)(</script>)', re.DOTALL | re.IGNORECASE)
    
    def replace_script(match):
        open_tag = match.group(1)
        script_body = match.group(2)
        close_tag = match.group(3)
        
        # Skip scripts with src attribute (external scripts)
        if 'src=' in open_tag.lower():
            return match.group(0)
        
        # Decode HTML entities inside the script body
        decoded = html.unescape(script_body)
        return open_tag + decoded + close_tag
    
    new_content = pattern.sub(replace_script, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Fixed: {filepath}")

files = glob.glob('e:/epwinds/*.html') + glob.glob('e:/epwinds/*/*.html')
for f in files:
    fix_html_file(f)

print("Done fixing all HTML files.")
