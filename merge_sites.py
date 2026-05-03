import re

# Read both files
with open('e:/epwinds/ball-site/index.html','r',encoding='utf-8',errors='ignore') as f:
    ball = f.read()
with open('e:/epwinds/index.html','r',encoding='utf-8',errors='ignore') as f:
    epi = f.read()

# Extract Ball Site body content (inside pwb-body-wrap, excluding pwb-body-wrap itself)
body_start = ball.find('<div id="pwb-body-wrap">')
body_end = ball.find('<div id="pwb-loading-wrap">')

if body_start < 0 or body_end < 0:
    print('ERROR: Could not find markers in Ball Site')
    exit(1)

# Find the closing </div> of pwb-body-wrap before pwb-loading-wrap
# Count divs to find the right closing tag
depth = 0
wrap_close = -1
for i in range(body_start, body_end):
    if ball[i:i+4] == '<div':
        depth += 1
    elif ball[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            wrap_close = i
            break

print(f'pwb-body-wrap closes at: {wrap_close}')

# The inner content is between '<div id="pwb-body-wrap">' and its closing </div>
inner_start = ball.find('>', body_start) + 1
inner_end = wrap_close
ball_inner = ball[inner_start:inner_end].strip()

print(f'Ball inner content length: {len(ball_inner)}')
print(f'First 200 chars: {ball_inner[:200]}')

# Extract Ball Site <head> preloads that are unique
head_end = ball.find('</head>')
ball_head = ball[:head_end]

# Find preloads and scene state in Ball Site head
ball_preloads = []
for m in re.finditer(r'<link[^>]*rel="preload"[^>]*>', ball_head):
    ball_preloads.append(m.group(0))
for m in re.finditer(r'<meta name="pw:has-visual-script"[^>]*>', ball_head):
    ball_preloads.append(m.group(0))

print(f'Ball preloads found: {len(ball_preloads)}')
for p in ball_preloads[:5]:
    print(f'  {p[:100]}')

# Find EpiMinds </head> position
epi_head_end = epi.find('</head>')
print(f'EpiMinds head end at: {epi_head_end}')

# Insert Ball Site preloads before </head> in EpiMinds
epi_with_preloads = epi[:epi_head_end] + '\n    <!-- Ball Site preloads -->\n    ' + '\n    '.join(ball_preloads) + '\n' + epi[epi_head_end:]

# Now insert Ball Site body content into EpiMinds pwb-body-wrap
# Find the closing </div> of EpiMinds pwb-body-wrap (before pwb-loading-wrap)
epi_bodywrap_start = epi_with_preloads.find('<div id="pwb-body-wrap">')
epi_loading_start = epi_with_preloads.find('<div id="pwb-loading-wrap">')

epi_depth = 0
epi_wrap_close = -1
for i in range(epi_bodywrap_start, epi_loading_start):
    if epi_with_preloads[i:i+4] == '<div':
        epi_depth += 1
    elif epi_with_preloads[i:i+6] == '</div>':
        epi_depth -= 1
        if epi_depth == 0:
            epi_wrap_close = i
            break

print(f'EpiMinds pwb-body-wrap closes at: {epi_wrap_close}')

# Insert Ball Site content before the closing </div> of EpiMinds pwb-body-wrap
# Also add a transition marker div
ball_content_with_marker = f'''
      <!-- BALL SITE CONTENT START -->
      <div id="ballsite-transition-anchor" class="pw-anchor-style pwb-anchor"></div>
      {ball_inner}
      <!-- BALL SITE CONTENT END -->
'''

final_html = epi_with_preloads[:epi_wrap_close] + ball_content_with_marker + epi_with_preloads[epi_wrap_close:]

# Remove the old iframe overlay and animation script (if they exist)
# Remove ballsite-overlay div
overlay_start = final_html.find('<div id="ballsite-overlay"')
if overlay_start >= 0:
    overlay_end = final_html.find('</div>', overlay_start) + 6
    final_html = final_html[:overlay_start] + final_html[overlay_end:]
    print('Removed old overlay div')

# Remove ballsite-iframe
iframe_start = final_html.find('<iframe id="ballsite-iframe"')
if iframe_start >= 0:
    iframe_end = final_html.find('</iframe>', iframe_start) + 9
    final_html = final_html[:iframe_start] + final_html[iframe_end:]
    print('Removed old iframe')

# Remove the old transition-wrapper
wrapper_start = final_html.find('<div id="transition-wrapper"')
if wrapper_start >= 0:
    wrapper_end = final_html.find('</div>', wrapper_start) + 6
    final_html = final_html[:wrapper_start] + final_html[wrapper_end:]
    print('Removed old transition wrapper')

# Remove old ballsite animation script
script_start = final_html.find("(function() {\n        const video = document.getElementById('i43s51u');")
if script_start >= 0:
    # Find the enclosing <script> tag
    tag_start = final_html.rfind('<script>', 0, script_start)
    tag_end = final_html.find('</script>', script_start) + 9
    final_html = final_html[:tag_start] + final_html[tag_end:]
    print('Removed old animation script')

# Write output
with open('e:/epwinds/index.html','w',encoding='utf-8') as f:
    f.write(final_html)

print(f'Done! Final file size: {len(final_html)} bytes')
