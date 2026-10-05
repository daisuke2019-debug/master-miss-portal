# -*- coding: utf-8 -*-
with open('build_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

js_code = """
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

        function handleFileSelect(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const detectedDate = extractDateFromFilename(file.name);
            const statusEl = document.getElementById('currentStatusText');
            if (statusEl) statusEl.textContent = `⏳ ${{file.name}} (${{detectedDate}}分) 解析中...`;

            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, {{ type: 'array', cellStyles: true }});

                    let targetSheetName = workbook.SheetNames.includes('店舗マスタ') ? '店舗マスタ' : workbook.SheetNames[0];
                    const sheet = workbook.Sheets[targetSheetName];
                    if (!sheet || !sheet['!ref']) throw new Error('データシートが見つかりません');

                    const range = XLSX.utils.decode_range(sheet['!ref']);
                    const headers = [];
                    for (let C = range.s.c; C <= range.e.c; ++C) {{
                        const cell = sheet[XLSX.utils.encode_cell({{ r: 0, c: C }})];
                        headers.push(cell && cell.v ? String(cell.v).trim() : `Column_${{C+1}}`);
                    }}

                    const parsedShops = [];

                    for (let R = 1; R <= range.e.r; ++R) {{
                        const shopCell = sheet[XLSX.utils.encode_cell({{ r: R, c: 0 }})];
                        const staffCell = sheet[XLSX.utils.encode_cell({{ r: R, c: 3 }})];
                        const svCell = sheet[XLSX.utils.encode_cell({{ r: R, c: 4 }})];

                        if (!shopCell || !shopCell.v) continue;
                        const shopName = String(shopCell.v).trim();
                        if (shopName === '店舗' || shopName === '店舗名' || shopName.includes('合計')) continue;

                        const staffName = staffCell && staffCell.v ? String(staffCell.v).trim() : '未設定';
                        const svName = svCell && svCell.v ? String(svCell.v).trim() : '';

                        let isARed = false;
                        const nonARedItems = [];

                        for (let C = 0; C <= range.e.c; ++C) {{
                            const cell = sheet[XLSX.utils.encode_cell({{ r: R, c: C }})];
                            let isRed = false;

                            if (cell && cell.s && cell.s.fill) {{
                                const fill = cell.s.fill;
                                const fg = fill.fgColor || fill.bgColor;
                                if (fg) {{
                                    const rgb = String(fg.rgb || '').toUpperCase();
                                    if (rgb === 'FFFF0000' || rgb === 'FF0000' || rgb === 'RED' || rgb.endsWith('FF0000')) {{
                                        isRed = true;
                                    }}
                                }}
                            }}

                            if (isRed) {{
                                const colName = headers[C] || `Col${{C+1}}`;
                                if (C === 0) {{
                                    isARed = true;
                                }} else {{
                                    nonARedItems.push(colName);
                                }}
                            }}
                        }}

                        parsedShops.push({{
                            name: shopName,
                            staff: staffName,
                            sv: svName,
                            date: detectedDate,
                            is_a_red: isARed,
                            non_a_count: nonARedItems.length,
                            non_a_items: nonARedItems
                        }});
                    }}

                    if (parsedShops.length === 0) {{
                        throw new Error('有効な店舗データが見つかりませんでした');
                    }}

                    const updatedStaffData = {{}};

                    // 1. 保有データのうち対象日付(detectedDate)以外の既存データを維持
                    for (let s in currentStaffData) {{
                        const existingShops = currentStaffData[s].shops.filter(sh => sh.date !== detectedDate);
                        updatedStaffData[s] = {{
                            a_count: 0,
                            non_a_red_total: 0,
                            shops: existingShops
                        }};
                    }}

                    // 2. パースした新データを追加マージ
                    for (let item of parsedShops) {{
                        const s = item.staff;
                        if (!updatedStaffData[s]) {{
                            updatedStaffData[s] = {{ a_count: 0, non_a_red_total: 0, shops: [] }};
                        }}
                        updatedStaffData[s].shops.push({{
                            name: item.name,
                            sv: item.sv,
                            date: item.date,
                            is_a_red: item.is_a_red,
                            non_a_count: item.non_a_count,
                            non_a_items: item.non_a_items
                        }});
                    }}

                    // 3. 全期間＆各日付再計算
                    const updatedColRanking = {{}};
                    for (let s in updatedStaffData) {{
                        let aTot = 0;
                        let nonATot = 0;
                        for (let sh of updatedStaffData[s].shops) {{
                            if (sh.is_a_red) aTot += 1;
                            nonATot += sh.non_a_count;
                            for (let colItem of sh.non_a_items) {{
                                updatedColRanking[colItem] = (updatedColRanking[colItem] || 0) + 1;
                            }}
                        }}
                        const totalCount = updatedStaffData[s].shops.length;
                        updatedStaffData[s].a_count = aTot;
                        updatedStaffData[s].non_a_red_total = nonATot;
                        updatedStaffData[s].miss_rate = totalCount > 0 ? Math.round((aTot / totalCount) * 1000) / 10 : 0;
                    }}

                    currentStaffData = updatedStaffData;
                    currentColRanking = updatedColRanking;

                    if (statusEl) statusEl.textContent = `✅ ${{file.name}} (${{detectedDate}}分) スマート統合完了`;
                    renderPortal();

                }} catch (err) {{
                    console.error('File Read Error:', err);
                    if (statusEl) statusEl.textContent = `⚠️ 解析エラー: ${{err.message || '読み込み失敗'}}`;
                    alert(`【エラー】\n${{err.message || 'ファイルの読み込みに失敗しました'}}`);
                }}
            }};
            reader.readAsArrayBuffer(file);
        }}
"""

idx_start = code.find('function extractDateFromFilename')
if idx_start != -1:
    idx_end = code.find('function renderPortal()', idx_start)
    if idx_end != -1:
        code = code[:idx_start] + js_code + '\n\n        ' + code[idx_end:]

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully embedded Smart Merge JS into build_portal.py!')
