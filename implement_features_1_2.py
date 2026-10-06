# -*- coding: utf-8 -*-
with open('rebuild_full_portal.py', 'r', encoding='utf-8') as f:
    code = f.read()

# JS logic additions for Feature 1 (Trend) and Feature 2 (Consecutive Miss Warning)
# Modify getFilteredData / renderPortal to calculate trend and consecutive miss shops

js_feature_logic = """
        function getFilteredData() {
            const dateSet = new Set();
            for (let s in currentStaffData) {
                for (let sh of currentStaffData[s].shops) {
                    if (sh.date) dateSet.add(sh.date);
                }
            }
            const dates = Array.from(dateSet).sort();

            const filteredStaffMap = {};
            const filteredColRanking = {};
            const consecutiveMissShops = []; // Feature 2: 複数日連続指摘店舗

            let totalShopsCount = 0;
            let totalARedCount = 0;
            let totalNonARedCount = 0;

            // 店舗ごとの日付別指摘履歴マップ作成 (Feature 2)
            const shopHistoryMap = {};
            for (let s in currentStaffData) {
                for (let sh of currentStaffData[s].shops) {
                    if (!shopHistoryMap[sh.name]) {
                        shopHistoryMap[sh.name] = { name: sh.name, staff: s, dates: {}, datesWithRed: [] };
                    }
                    const isRed = sh.is_a_red || (sh.non_a_count && sh.non_a_count > 0);
                    if (isRed) {
                        shopHistoryMap[sh.name].datesWithRed.push(sh.date);
                    }
                    shopHistoryMap[sh.name].dates[sh.date] = isRed;
                }
            }

            for (let shopName in shopHistoryMap) {
                const info = shopHistoryMap[shopName];
                if (info.datesWithRed.length >= 2) {
                    consecutiveMissShops.push(info);
                }
            }

            for (let s in currentStaffData) {
                const targetShops = currentStaffData[s].shops.filter(sh => {
                    if (activeDateFilter === 'all') return true;
                    return sh.date === activeDateFilter;
                });

                if (targetShops.length === 0) continue;

                let aCount = 0;
                let nonACount = 0;

                for (let sh of targetShops) {
                    if (sh.is_a_red) aCount += 1;
                    nonACount += sh.non_a_count;
                    for (let colItem of sh.non_a_items) {
                        filteredColRanking[colItem] = (filteredColRanking[colItem] || 0) + 1;
                    }
                }

                totalShopsCount += targetShops.length;
                totalARedCount += aCount;
                totalNonARedCount += nonACount;

                // Feature 1: トレンド計算 (直前日付 vs 最新日付)
                let trendVal = 0;
                let trendType = 'same'; // 'up' (悪化), 'down' (改善), 'same'
                if (dates.length >= 2) {
                    const latestDate = dates[dates.length - 1];
                    const prevDate = dates[dates.length - 2];

                    const latestShops = currentStaffData[s].shops.filter(sh => sh.date === latestDate);
                    const prevShops = currentStaffData[s].shops.filter(sh => sh.date === prevDate);

                    const latestMisses = latestShops.reduce((acc, sh) => acc + (sh.is_a_red ? 1 : 0) + sh.non_a_count, 0);
                    const prevMisses = prevShops.reduce((acc, sh) => acc + (sh.is_a_red ? 1 : 0) + sh.non_a_count, 0);

                    const diff = latestMisses - prevMisses;
                    if (diff > 0) {
                        trendType = 'up'; // 悪化
                        trendVal = diff;
                    } else if (diff < 0) {
                        trendType = 'down'; // 改善
                        trendVal = Math.abs(diff);
                    }
                }

                filteredStaffMap[s] = {
                    a_count: aCount,
                    non_a_red_total: nonACount,
                    shops: targetShops,
                    miss_rate: targetShops.length > 0 ? Math.round((aCount / targetShops.length) * 1000) / 10 : 0,
                    trendType: trendType,
                    trendVal: trendVal
                };
            }

            return {
                dates: dates,
                staffMap: filteredStaffMap,
                colRanking: filteredColRanking,
                totalShops: totalShopsCount,
                totalARed: totalARedCount,
                totalNonARed: totalNonARedCount,
                consecutiveMissShops: consecutiveMissShops
            };
        }
"""

# Replace getFilteredData function in rebuild_full_portal.py
import re
code = re.sub(r'function getFilteredData\(\)\s*\{.*?return\s*\{.*?\};\s*\}', js_feature_logic, code, flags=re.DOTALL)

# Add Consecutive Miss Banner HTML to main layout
consecutive_banner_html = """
        <!-- 🚨 Feature 2: 複数日連続赤指摘店舗の重点警告アラート -->
        <div id="consecutiveWarningBanner" class="p-4 sm:p-5 rounded-2xl bg-gradient-to-r from-red-500 to-rose-700 text-white shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-2 border-red-400">
            <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-2xl bg-white/20 backdrop-blur-md flex items-center justify-center text-2xl font-black shrink-0 border border-white/30">
                    🚨
                </div>
                <div>
                    <h3 class="text-base sm:text-lg font-black tracking-tight flex items-center gap-2">
                        <span>複数日 連続赤指摘店舗 (要重点指導)</span>
                        <span id="consecutiveCountBadge" class="bg-white text-red-700 text-xs px-2.5 py-0.5 rounded-full font-black shadow-sm">0店舗</span>
                    </h3>
                    <p class="text-xs sm:text-sm text-red-100 font-bold mt-0.5">複数日にわたって繰り返しマスタミス指摘が発生している店舗を自動検知中</p>
                </div>
            </div>
            <div id="consecutiveShopChips" class="flex flex-wrap items-center gap-1.5 w-full md:w-auto">
                <!-- JS描画 -->
            </div>
        </div>
"""

# Insert consecutive_banner_html right after Date Filter bar
code = code.replace('<!-- 📅 日付別切り替えタブバー (最重要・各日付独立保持＆ワンタップ切替) -->', consecutive_banner_html + '\n\n        <!-- 📅 日付別切り替えタブバー (最重要・各日付独立保持＆ワンタップ切替) -->')

# Update renderPortal to update Consecutive Banner and render Table Trend Badges
render_portal_updates = """
            // 7. 複数日連続指摘店舗バナーの更新 (Feature 2)
            const consecContainer = document.getElementById('consecutiveShopChips');
            const consecBadge = document.getElementById('consecutiveCountBadge');
            if (consecContainer && consecBadge) {
                const cShops = dataInfo.consecutiveMissShops;
                consecBadge.textContent = `${cShops.length}店舗`;
                if (cShops.length === 0) {
                    consecContainer.innerHTML = `<span class="text-xs font-bold text-red-100">連続指摘店舗はありません</span>`;
                } else {
                    let chipsHtml = '';
                    for (let cs of cShops.slice(0, 5)) {
                        chipsHtml += `<span class="text-xs bg-white/90 text-red-900 font-black px-3 py-1 rounded-xl shadow-sm border border-white/50">🚨 ${cs.name} (${cs.staff})</span>`;
                    }
                    if (cShops.length > 5) {
                        chipsHtml += `<span class="text-xs bg-red-900/60 text-white font-black px-2.5 py-1 rounded-xl">他 ${cShops.length - 5}店舗</span>`;
                    }
                    consecContainer.innerHTML = chipsHtml;
                }
            }
        }
"""

code = code.replace("// 6. ワーストランキング描画\n            renderColumnRanking(dataInfo.colRanking);\n        }", "// 6. ワーストランキング描画\n            renderColumnRanking(dataInfo.colRanking);\n" + render_portal_updates)

# Update renderTableAndCards to include Feature 1 Trend Badge
table_row_trend = """
                        <td class="py-4 px-6 font-black text-slate-900">
                            <div class="flex items-center gap-3">
                                <span class="w-7 h-7 rounded-lg ${rank <= 3 && info.a_count > 0 ? 'bg-red-600 text-white' : 'bg-slate-200 text-slate-700'} flex items-center justify-center text-xs font-black shrink-0">
                                    ${rank}
                                </span>
                                <div>
                                    <div class="text-base font-black flex items-center gap-2">
                                        <span>${s}</span>
                                        ${info.trendType === 'down' ? `<span class="text-xs bg-emerald-100 text-emerald-800 font-black px-2 py-0.5 rounded-full border border-emerald-300">🟢 ↓ ${info.trendVal} (改善)</span>` : (info.trendType === 'up' ? `<span class="text-xs bg-red-100 text-red-700 font-black px-2 py-0.5 rounded-full border border-red-300">🔴 ↑ +${info.trendVal} (要確認)</span>` : '')}
                                    </div>
                                    <div class="text-xs text-slate-500 font-bold">${totalShops}店舗巡回</div>
                                </div>
                            </div>
                        </td>
"""

old_tr_td = """                        <td class="py-4 px-6 font-black text-slate-900">
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

code = code.replace(old_tr_td, table_row_trend)

with open('rebuild_full_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('build_portal.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Successfully implemented Feature 1 (Trend) and Feature 2 (Consecutive Miss Warning)!')
