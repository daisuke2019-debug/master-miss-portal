# -*- coding: utf-8 -*-
import re

for filename in ['rebuild_full_portal.py', 'build_portal.py']:
    with open(filename, 'r', encoding='utf-8') as f:
        code = f.read()

    # Completely remove consecutiveWarningBanner div block
    banner_pattern = r'<!-- 🚨 Feature 2: 複数日 連続赤指摘店舗の重点警告アラート -->\s*<div id="consecutiveWarningBanner".*?</div>\s*</div>'
    code = re.sub(banner_pattern, '', code, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(code)

print('Completely removed consecutiveWarningBanner from both Python files!')
