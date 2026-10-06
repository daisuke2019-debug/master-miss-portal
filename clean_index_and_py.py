# -*- coding: utf-8 -*-
import re

banner_regex = r'<div id="consecutiveWarningBanner".*?</div>\s*</div>'

for fname in ['index.html', 'rebuild_full_portal.py', 'build_portal.py']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'consecutiveWarningBanner' in content:
        content = re.sub(banner_regex, '', content, flags=re.DOTALL)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Cleaned {fname}')

