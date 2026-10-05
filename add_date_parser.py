# -*- coding: utf-8 -*-
with open('build_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

date_func = """
        function extractDateFromFilename(fileName) {{
            if (!fileName) return '10/02';
            const m = fileName.match(/_result(\\d{{2}})(\\d{{2}})/i);
            if (m) {{
                return parseInt(m[1]) + '/' + m[2];
            }}
            const mYmd = fileName.match(/202\\d(\\d{{2}})(\\d{{2}})/);
            if (mYmd) {{
                return parseInt(mYmd[1]) + '/' + mYmd[2];
            }}
            return '10/02';
        }}
"""

target = "        function handleFileSelect(event) {"
replacement = date_func + "\n        function handleFileSelect(event) {"

code = code.replace(target, replacement, 1)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated build_portal.py successfully')
