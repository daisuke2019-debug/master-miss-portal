# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update handleFileSelect to save to localStorage
old_save_code = "currentStaffData = updatedStaffData;"
new_save_code = """currentStaffData = updatedStaffData;
                    try {
                        localStorage.setItem('master_miss_portal_staff_data', JSON.stringify(currentStaffData));
                    } catch(e) { console.error('LocalStorage save error:', e); }"""

code = code.replace(old_save_code, new_save_code)

# 2. Update DOMContentLoaded to load from localStorage if present
old_load_code = "document.addEventListener('DOMContentLoaded', () => {\n            renderPortal();\n        });"
new_load_code = """document.addEventListener('DOMContentLoaded', () => {
            try {
                const savedData = localStorage.getItem('master_miss_portal_staff_data');
                if (savedData) {
                    currentStaffData = JSON.parse(savedData);
                }
            } catch(e) { console.error('LocalStorage load error:', e); }
            
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
        });"""

code = code.replace(old_load_code, new_load_code)

with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully added localStorage persistence to rebuild_full_portal.py!')
