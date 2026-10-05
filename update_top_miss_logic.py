# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = """            // 4. KPI
            document.getElementById('statTotalShops').innerHTML = `${dataInfo.totalShops} <span class="text-sm font-bold text-slate-700">店舗</span>`;
            document.getElementById('statARedCount').innerHTML = `${dataInfo.totalARed} <span class="text-sm font-bold text-slate-800">店舗</span>`;
            document.getElementById('statNonARedCount').innerHTML = `${dataInfo.totalNonARed} <span class="text-sm font-bold text-slate-800">箇所</span>`;

            let maxStaff = '--';
            let maxVal = 0;
            let perfectCount = 0;
            const staffList = Object.keys(staffMap);
            for (let s of staffList) {
                if (staffMap[s].a_count > maxVal) {
                    maxVal = staffMap[s].a_count;
                    maxStaff = s;
                }
                if (staffMap[s].a_count === 0) {
                    perfectCount++;
                }
            }
            document.getElementById('statTopMissStaff').textContent = maxVal > 0 ? `最多: ${maxStaff} (${maxVal}店舗)` : 'ミス者なし';"""

replacement = """            // 4. KPI
            document.getElementById('statTotalShops').innerHTML = `${dataInfo.totalShops} <span class="text-sm font-bold text-slate-700">店舗</span>`;
            document.getElementById('statARedCount').innerHTML = `${dataInfo.totalARed} <span class="text-sm font-bold text-slate-800">店舗</span>`;
            document.getElementById('statNonARedCount').innerHTML = `${dataInfo.totalNonARed} <span class="text-sm font-bold text-slate-800">箇所</span>`;

            let maxStaff = '--';
            let maxVal = 0;
            let perfectCount = 0;
            const staffList = Object.keys(staffMap);

            if (activeDateFilter === 'all') {
                // 【全期間 累計時】: A列外の赤セル累積箇所数が最も多いスタッフを探す
                for (let s of staffList) {
                    if (staffMap[s].non_a_red_total > maxVal) {
                        maxVal = staffMap[s].non_a_red_total;
                        maxStaff = s;
                    }
                    if (staffMap[s].a_count === 0 && staffMap[s].non_a_red_total === 0) {
                        perfectCount++;
                    }
                }
                document.getElementById('statTopMissStaff').textContent = maxVal > 0 ? `最多(A外赤): ${maxStaff} (${maxVal}箇所)` : '指摘なし';
            } else {
                // 【日別時】: A列赤指摘店舗が最も多いスタッフ
                for (let s of staffList) {
                    if (staffMap[s].a_count > maxVal) {
                        maxVal = staffMap[s].a_count;
                        maxStaff = s;
                    }
                    if (staffMap[s].a_count === 0) {
                        perfectCount++;
                    }
                }
                document.getElementById('statTopMissStaff').textContent = maxVal > 0 ? `最多: ${maxStaff} (${maxVal}店舗)` : 'ミス者なし';
            }"""

if target in code:
    code = code.replace(target, replacement)
    with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
        f.write(code)
    with open('build_portal.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Updated top miss calculation logic successfully!')
else:
    print('Target code block not found in rebuild_full_portal.py')
