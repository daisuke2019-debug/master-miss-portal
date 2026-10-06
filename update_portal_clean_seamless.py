# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove Consecutive Warning Banner HTML
import re
code = re.sub(r'<!-- 🚨 Feature 2: 複数日 連続赤指摘店舗の重点警告アラート -->.*?</div>\s*</div>', '', code, flags=re.DOTALL)

# 2. Update renderTableAndCards to remove Trend Badges (Keep clean staff name)
clean_tr_td = """                        <td class="py-4 px-6 font-black text-slate-900">
                            <div class="flex items-center gap-3">
                                <span class="w-7 h-7 rounded-lg ${rank <= 3 && info.a_count > 0 ? 'bg-red-600 text-white' : 'bg-slate-200 text-slate-700'} flex items-center justify-center text-xs font-black shrink-0">
                                    ${rank}
                                </span>
                                <div>
                                    <div class="text-base font-black">${s}</div>
                                    <div class="text-xs text-slate-500 font-bold">${totalShops}店舗巡回</div>
                                </div>
                            </div>
                        </td>"""

code = re.sub(r'<td class="py-4 px-6 font-black text-slate-900">\s*<div class="flex items-center gap-3">.*?<div class="text-xs text-slate-500 font-bold">\$\{totalShops\}店舗巡回</div>\s*</div>\s*</div>\s*</td>', clean_tr_td, code, flags=re.DOTALL)

# 3. Update dateFilterButtons and Dropdown HTML / JS for seamless switching
seamless_date_js = """
            // 1. 日付フィルターUIのシームレス描画 (直近タブ + 連動ドロップダウン)
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

                // 📅 シームレス日付ドロップダウンセレクト
                btnsHtml += `
                    <div class="relative inline-block">
                        <select id="mainDateSelectDropdown" onchange="setDateFilter(this.value)" class="px-3.5 py-2 rounded-xl text-xs sm:text-sm font-black text-slate-900 border-2 border-slate-400 focus:outline-none focus:ring-2 focus:ring-red-600 shadow-sm cursor-pointer ${activeDateFilter !== 'all' ? 'bg-red-50 border-red-500 text-red-950 font-black' : 'bg-white'}">
                            <option value="all" ${activeDateFilter === 'all' ? 'selected' : ''}>🌐 全期間 (累計) 表示</option>
                            ${dates.map(d => {
                                const cnt = Object.values(currentStaffData).reduce((acc, st) => acc + st.shops.filter(s => s.date === d).length, 0);
                                return `<option value="${d}" ${activeDateFilter === d ? 'selected' : ''}>📅 ${d}分データ (${cnt}店舗)</option>`;
                            }).join('')}
                        </select>
                    </div>
                `;

                dateBtnContainer.innerHTML = btnsHtml;
            }
"""

code = re.sub(r'// 1\. 日付フィルターUIのスマート描画.*?dateBtnContainer\.innerHTML = btnsHtml;\s*\}', seamless_date_js, code, flags=re.DOTALL)

with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully removed unwanted banners/badges and implemented seamless dropdown date filter!')
