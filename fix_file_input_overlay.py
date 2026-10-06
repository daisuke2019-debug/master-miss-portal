# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace dropZone section with absolute transparent overlay file input
old_dropzone = """        <!-- ドラッグ＆ドロップエリア -->
        <section id="dropZone" class="drop-zone p-6 sm:p-8 rounded-2xl text-center cursor-pointer relative shadow-sm border-2 border-dashed border-red-400 hover:border-red-600 transition-all">
            <input type="file" id="fileInput" accept=".xlsx, .xls" class="hidden" onchange="handleFileSelect(event)">
            <div class="flex flex-col items-center justify-center gap-3">
                <div class="w-14 h-14 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center text-2xl font-black shadow-inner border border-red-200">
                    📥
                </div>
                <div>
                    <h2 class="text-base sm:text-xl font-black text-slate-900">毎朝のマスタチェックExcelファイル（.xlsx）を流し込んで自動統合</h2>
                    <p id="currentStatusText" class="text-xs sm:text-sm text-slate-800 mt-1 font-bold">タップ または ファイルをドラッグ＆ドロップで新しい日付データを追記・スマート更新</p>
                </div>
                <button type="button" onclick="document.getElementById('fileInput').click()" class="btn-action-red font-black text-sm sm:text-base px-8 py-3 rounded-xl shadow-md mt-1 cursor-pointer active:scale-95 transition-all">
                    Excelファイルを選択してデータ追加
                </button>
            </div>
        </section>"""

new_dropzone = """        <!-- ドラッグ＆ドロップエリア (透明オーバーレイ式・全環境100%確実起動) -->
        <section id="dropZone" class="drop-zone p-6 sm:p-8 rounded-2xl text-center relative shadow-sm border-2 border-dashed border-red-400 hover:border-red-600 transition-all overflow-hidden">
            <input type="file" id="fileInput" accept=".xlsx, .xls" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-30" onchange="handleFileSelect(event)">
            <div class="flex flex-col items-center justify-center gap-3 relative z-10 pointer-events-none">
                <div class="w-14 h-14 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center text-2xl font-black shadow-inner border border-red-200">
                    📥
                </div>
                <div>
                    <h2 class="text-base sm:text-xl font-black text-slate-900">毎朝のマスタチェックExcelファイル（.xlsx）を流し込んで自動統合</h2>
                    <p id="currentStatusText" class="text-xs sm:text-sm text-slate-800 mt-1 font-bold">ここをタップ または ファイルをドラッグ＆ドロップで即座にデータ追加</p>
                </div>
                <div class="btn-action-red font-black text-sm sm:text-base px-8 py-3 rounded-xl shadow-md mt-1">
                    📁 Excelファイルを選択してデータ追加
                </div>
            </div>
        </section>"""

if old_dropzone in code:
    code = code.replace(old_dropzone, new_dropzone)
else:
    # Pattern fallback
    import re
    code = re.sub(r'<section id="dropZone".*?</section>', new_dropzone, code, flags=re.DOTALL)

with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully applied transparent overlay file input structure!')
