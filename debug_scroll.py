# Debug script to check scroll behavior
# Read index.html and find the main scroll container

with open('e:/epwinds/index.html','r',encoding='utf-8',errors='ignore') as f:
    html = f.read()

# Find pwb-body-wrap and its children
idx = html.find('id="pwb-body-wrap"')
print(f'pwb-body-wrap at: {idx}')

# Find the div right after pwb-body-wrap
start = html.find('>', idx) + 1
# Find next div
next_div = html.find('<div', start)
end_tag = html.find('>', next_div)
print(f'First child div: {html[next_div:end_tag+1]}')

# Find ijim
ijim = html.find('id="ijim"')
print(f'ijim at: {ijim}')
if ijim > 0:
    start = html.find('>', ijim) + 1
    next_div = html.find('<div', start)
    end_tag = html.find('>', next_div)
    print(f'ijim child: {html[next_div:end_tag+1]}')
