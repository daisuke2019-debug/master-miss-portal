# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add direct onclick to file button inside dropZone
old_button_html = '<button type="button" class="btn-action-red font-black text-sm sm:text-base px-8 py-3 rounded-xl shadow-md mt-1 cursor-pointer active:scale-95 transition-all">'
new_button_html = '<button type="button" onclick="document.getElementById(\'fileInput\').click()" class="btn-action-red font-black text-sm sm:text-base px-8 py-3 rounded-xl shadow-md mt-1 cursor-pointer active:scale-95 transition-all">'

code = code.replace(old_button_html, new_button_html)

# 2. Add dropZone event listeners back into script
dropzone_events = """
        // DropZone Event Listeners
        document.addEventListener('DOMContentLoaded', () => {
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('fileInput');

            if (dropZone && fileInput) {
                dropZone.addEventListener('click', (e) => {
                    if (e.target.tagName !== 'BUTTON' && e.target !== fileInput) {
                        fileInput.click();
                    }
                });

                dropZone.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    dropZone.classList.add('dragover');
                });

                dropZone.addEventListener('dragleave', () => {
                    dropZone.classList.remove('dragover');
                });

                dropZone.addEventListener('drop', (e) => {
                    e.preventDefault();
                    dropZone.classList.remove('dragover');
                    if (e.dataTransfer && e.dataTransfer.files.length > 0) {
                        fileInput.files = e.dataTransfer.files;
                        handleFileSelect({ target: fileInput });
                    }
                });
            }
            renderPortal();
        });
"""

code = code.replace("document.addEventListener('DOMContentLoaded', () => {\n            renderPortal();\n        });", dropzone_events)

with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('DropZone event listeners and file button click event successfully restored!')
