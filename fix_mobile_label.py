# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '<div class="text-slate-500">担当</div>'
replacement = '<div class="text-slate-500">巡回</div>'

code = code.replace(target, replacement)

with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Mobile card replaced successfully!')
