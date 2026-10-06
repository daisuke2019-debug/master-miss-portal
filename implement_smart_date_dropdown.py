# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace renderPortal date filter buttons logic with Smart Quick Tabs + Dropdown Select
smart_date_ui_js = """
            // 1. 日付フィルターUIのスマート描画 (直近3日クイックタブ + ドロップダウンセレクト)
            const dateBtnContainer = document.getElementById('dateFilterButtons');
            if (dateBtnContainer) {
                let btnsHtml = '';

                // 🌐 全期間 (累計) ボタン
                const isAllActive = activeDateFilter === 'all';
                btnsHtml += `
                    <button onclick="setDateFilter('all')" class="px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black transition-all shadow-sm flex items-center gap-1.5 ${isAllActive ? 'bg-slate-900 text-white border-2 border-slate-900 shadow-md ring-2 ring-slate-900' : 'bg-slate-100 hover:bg-slate-200 text-slate-800 border-2 border-slate-300'}">
                        <span>🌐</span>
                        <span>全期間 (累計)</span>
                    </button>
                `;

                if (dates.length > 0) {
                    const latestDate = dates[dates.length - 1];
                    const isLatestActive = activeDateFilter === latestDate;
                    const latestCount = Object.values(currentStaffData).reduce((acc, st) => acc + st.shops.filter(s => s.date === latestDate).length, 0);

                    // ⚡ 最新日ボタン
                    btnsHtml += `
                        <button onclick="setDateFilter('${latestDate}')" class="px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black transition-all shadow-sm flex items-center gap-1.5 ${isLatestActive ? 'bg-red-600 text-white border-2 border-red-600 shadow-md ring-2 ring-red-600' : 'bg-red-50 hover:bg-red-100 text-red-700 border-2 border-red-300'}">
                            <span>⚡</span>
                            <span>最新 ${latestDate}分 (${latestCount}店舗)</span>
                        </button>
                    `;

                    // 📅 前回日ボタン (2日以上ある場合)
                    if (dates.length >= 2) {
                        const prevDate = dates[dates.length - 2];
                        const isPrevActive = activeDateFilter === prevDate;
                        const prevCount = Object.values(currentStaffData).reduce((acc, st) => acc + st.shops.filter(s => s.date === prevDate).length, 0);

                        btnsHtml += `
                            <button onclick="setDateFilter('${prevDate}')" class="px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black transition-all shadow-sm flex items-center gap-1.5 ${isPrevActive ? 'bg-red-600 text-white border-2 border-red-600 shadow-md ring-2 ring-red-600' : 'bg-slate-100 hover:bg-slate-200 text-slate-800 border-2 border-slate-300'}">
                                <span>📅</span>
                                <span>前回 ${prevDate}分 (${prevCount}店舗)</span>
                            </button>
                        `;
                    }
                }

                // 📅 過去日付ドロップダウンセレクト (全1ヶ月分対応)
                const isCustomSelected = dates.includes(activeDateFilter) && activeDateFilter !== dates[dates.length - 1] && activeDateFilter !== dates[dates.length - 2];

                btnsHtml += `
                    <div class="relative inline-block">
                        <select onchange="setDateFilter(this.value)" class="px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black bg-white text-slate-900 border-2 border-slate-400 focus:outline-none focus:ring-2 focus:ring-red-600 shadow-sm cursor-pointer ${isCustomSelected ? 'bg-amber-100 border-amber-500 text-amber-950 font-black' : ''}">
                            <option value="" disabled ${!isCustomSelected && activeDateFilter !== 'all' && activeDateFilter !== dates[dates.length - 1] && activeDateFilter !== dates[dates.length - 2] ? '' : ''}>📅 他の日付を選択 (${dates.length}日分)...</option>
                            ${dates.map(d => {
                                const cnt = Object.values(currentStaffData).reduce((acc, st) => acc + st.shops.filter(s => s.date === d).length, 0);
                                return `<option value="${d}" ${activeDateFilter === d ? 'selected' : ''}>📅 ${d}分 (${cnt}店舗)</option>`;
                            }).join('')}
                        </select>
                    </div>
                `;

                dateBtnContainer.innerHTML = btnsHtml;
            }
"""

# Replace rendering of dateFilterButtons inside renderPortal
import re
target_pattern = r'// 1\. 日付フィルターボタン群の動的描画.*?dateBtnContainer\.innerHTML = btnsHtml;\s*\}'
code = re.sub(target_pattern, smart_date_ui_js, code, flags=re.DOTALL)

with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully implemented Smart Quick Tabs + Dropdown Select Date Filter!')
