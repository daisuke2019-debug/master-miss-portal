import json

with open('portal_json_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

staff_data = data['staff_data']
col_ranking = data['col_ranking']

sorted_rank = sorted(col_ranking.items(), key=lambda x: x[1], reverse=True)
ranking_html = ''
for rank, (col_name, count) in enumerate(sorted_rank, 1):
    ranking_html += f"""
    <div class="flex items-center justify-between p-3.5 bg-slate-800/60 hover:bg-slate-800 rounded-xl transition-all border border-slate-700/60">
        <div class="flex items-center gap-3">
            <span class="w-6 h-6 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center">{rank}</span>
            <span class="font-bold text-white text-sm">{col_name}</span>
        </div>
        <span class="text-xs font-black bg-red-950/80 text-red-300 px-3 py-1 rounded-full border border-red-800/60">{count} 店舗</span>
    </div>
    """

js_staff_data = json.dumps(staff_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【AI Company】マスタミス自動カウントポータル</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&family=Noto+Sans+JP:wght@500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans JP', 'Plus Jakarta Sans', sans-serif;
            background-color: #0b0f19;
            color: #f8fafc;
        }}
        .board-header {{
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .main-card {{
            background: #151c2c;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }}
        .row-hover:hover {{
            background-color: rgba(255, 255, 255, 0.03);
        }}
        .progress-bar-bg {{
            background: rgba(255, 255, 255, 0.1);
        }}
    </style>
</head>
<body class="min-h-screen pb-20">

    <!-- 👑 BOARD Executive Header -->
    <header class="board-header py-7 px-6 md:px-12 sticky top-0 z-40 shadow-2xl">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="bg-red-600 text-white font-extrabold text-xs px-3 py-1 rounded-full uppercase tracking-wider shadow-sm">ミス最多順ソート ＆ 個別・日別最優先</span>
                    <span class="text-xs text-slate-400">Dai CEO 直轄管理ポータル</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-black text-white mt-1 tracking-tight">店舗マスタミス 個別・日別状況 ＆ 指摘ランキング</h1>
            </div>

            <!-- 📅 日別フィルター / 確認エリア -->
            <div class="flex items-center gap-3 bg-slate-900/90 p-2 rounded-xl border border-slate-700">
                <span class="text-xs text-slate-400 pl-2 font-bold">対象提出日:</span>
                <select class="bg-slate-800 text-white text-xs font-bold px-3 py-1.5 rounded-lg border border-slate-600 focus:outline-none">
                    <option value="1001">2026/10/01 (提出分: 40店舗)</option>
                </select>
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse mr-1"></span>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 md:px-8 mt-8 space-y-8">

        <!-- 📊 日別 ＆ ミス率 概況サマリー -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-5">
            <div class="main-card p-5 rounded-2xl">
                <div class="text-slate-400 text-xs font-bold uppercase tracking-wider">10/01 チェック総店舗数</div>
                <div class="text-3xl font-black text-white mt-1">40 <span class="text-sm font-normal text-slate-400">店舗</span></div>
                <div class="text-xs text-slate-400 mt-2">13名の最終更新スタッフ対象</div>
            </div>

            <div class="main-card p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-red-950/50 border-red-500/40">
                <div class="text-red-400 text-xs font-bold uppercase tracking-wider">10/01 A列指摘店舗数</div>
                <div class="text-3xl font-black text-red-400 mt-1">13 <span class="text-sm font-normal text-slate-400">店舗 (32.5%)</span></div>
                <div class="text-xs text-red-300/90 font-bold mt-2">最多ミス: 櫻井 蓮 (4回 / 100%)</div>
            </div>

            <div class="main-card p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-amber-950/50 border-amber-500/40">
                <div class="text-amber-400 text-xs font-bold uppercase tracking-wider">10/01 A列外赤セル内訳</div>
                <div class="text-3xl font-black text-amber-400 mt-1">26 <span class="text-sm font-normal text-slate-400">箇所</span></div>
                <div class="text-xs text-amber-300/90 font-bold mt-2">具体ミス項目数 (櫻井: 9箇所)</div>
            </div>

            <div class="main-card p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-emerald-950/50 border-emerald-500/40">
                <div class="text-emerald-400 text-xs font-bold uppercase tracking-wider">ノーミス率 (A列)</div>
                <div class="text-3xl font-black text-emerald-400 mt-1">46.2 <span class="text-sm font-normal text-slate-400">%</span></div>
                <div class="text-xs text-emerald-300/90 font-bold mt-2">6名 / 13名 がA列ミス0件</div>
            </div>
        </div>

        <!-- 🚨 最優先表示: ミスが多い人順 一覧テーブル (ミス発生率・個別のミス内訳直感表示) -->
        <section class="main-card rounded-2xl overflow-hidden border border-red-500/30">
            <div class="p-6 border-b border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-red-950/20">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="bg-red-600 text-white text-xs font-black px-2.5 py-0.5 rounded">最重要</span>
                        <h2 class="text-xl font-black text-white">
                            最終更新スタッフ別 ミスが多い順ランキング ＆ 個別ミス発生率
                        </h2>
                    </div>
                    <p class="text-xs text-slate-300 mt-1">ミス回数・発生割合が高い順に並んでおります。「個別ミス詳細」で該当店舗のミス項目を即座に確認できます</p>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-900 text-slate-400 text-xs font-bold uppercase tracking-wider border-b border-slate-800">
                            <th class="py-4 px-6">順位 / スタッフ名</th>
                            <th class="py-4 px-4 text-center">担当店舗数</th>
                            <th class="py-4 px-4 text-center">A列 指摘数<br><span class="text-2xs font-normal text-red-400">(ミス回数)</span></th>
                            <th class="py-4 px-6 text-center">ミス発生割合 (%)<br><span class="text-2xs font-normal text-slate-400">(担当店舗に対するミス率)</span></th>
                            <th class="py-4 px-4 text-center">A列外赤セル<br><span class="text-2xs font-normal text-amber-400">(内訳箇所数)</span></th>
                            <th class="py-4 px-6 text-right">個別のミス確認</th>
                        </tr>
                    </thead>
                    <tbody id="staffTableBody" class="divide-y divide-slate-800 text-sm font-medium">
                        <!-- JSで動的レンダリング -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- 🔍 個別店舗のミス一覧 (最優先閲覧セクション) -->
        <section class="main-card p-6 rounded-2xl">
            <div class="mb-4 pb-3 border-b border-slate-800 flex justify-between items-center">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <span>🚨</span> 10/01 提出分 個別店舗の指摘・ミス発生ログ (全13店舗)
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">A列指摘およびA列以外の赤背景セルが発生している店舗の個別具体内訳</p>
                </div>
                <span class="text-xs font-bold bg-red-900/60 text-red-300 border border-red-700/60 px-3 py-1 rounded-full">13店舗で指摘あり</span>
            </div>

            <div id="individualMissContainer" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- JSでレンダリング -->
            </div>
        </section>

        <!-- 📌 A列以外 赤セル多発項目内訳 -->
        <section class="main-card p-6 rounded-2xl">
            <div class="mb-4 pb-3 border-b border-slate-800 flex justify-between items-center">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <span>📌</span> ミス多発項目 ランキング (全40店舗中)
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">具体的にどの項目で入力漏れ・赤セル指摘が多いか</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {ranking_html}
            </div>
        </section>

    </main>

    <!-- モーダルダイアログ -->
    <div id="detailModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="main-card rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden border border-slate-700">
            <div class="px-6 py-5 bg-slate-900 text-white flex justify-between items-center border-b border-slate-800">
                <div>
                    <h3 id="modalStaffName" class="text-xl font-extrabold text-white">スタッフ個別詳細</h3>
                    <p id="modalStaffMeta" class="text-xs text-slate-400 mt-1"></p>
                </div>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white text-2xl font-bold p-1">&times;</button>
            </div>
            <div id="modalBody" class="p-6 overflow-y-auto space-y-4 text-slate-200">
                <!-- 詳細コンテンツ -->
            </div>
            <div class="px-6 py-4 bg-slate-900/80 border-t border-slate-800 flex justify-end">
                <button onclick="closeModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-xl text-sm font-bold transition-all shadow-md">閉じる</button>
            </div>
        </div>
    </div>

    <script>
        const staffData = {js_staff_data};

        function renderPortal() {{
            const tbody = document.getElementById('staffTableBody');
            tbody.innerHTML = '';

            // ★ミスが多い人順（ミス数降順 ➔ ミス率降順）にソート！
            const entries = Object.entries(staffData).sort((a, b) => {{
                if (b[1].a_count !== a[1].a_count) return b[1].a_count - a[1].a_count;
                if (b[1].miss_rate !== a[1].miss_rate) return b[1].miss_rate - a[1].miss_rate;
                return b[1].non_a_red_total - a[1].non_a_red_total;
            }});

            const missShopsList = [];

            entries.forEach(([staffName, info], index) => {{
                const tr = document.createElement('tr');
                tr.className = 'row-hover transition-colors';

                const shopCount = info.shops.length;
                const aCount = info.a_count;
                const missRate = info.miss_rate;
                const nonARedTotal = info.non_a_red_total;
                const rankNum = index + 1;

                // プログレスバーのカラー判定
                let barColor = 'bg-emerald-500';
                let textColor = 'text-emerald-400';
                if (missRate > 70) {{
                    barColor = 'bg-red-500';
                    textColor = 'text-red-400';
                }} else if (missRate > 0) {{
                    barColor = 'bg-amber-500';
                    textColor = 'text-amber-400';
                }}

                tr.innerHTML = `
                    <td class="py-4 px-6 font-bold text-white flex items-center gap-3">
                        <span class="w-6 h-6 rounded-full ${{aCount > 0 ? 'bg-red-600 text-white' : 'bg-slate-700 text-slate-300'}} text-xs font-black flex items-center justify-center">${{rankNum}}</span>
                        <div>
                            <div class="text-base font-extrabold text-white">${{staffName}}</div>
                        </div>
                    </td>
                    <td class="py-4 px-4 text-center font-semibold text-slate-300">${{shopCount}} 店</td>
                    <td class="py-4 px-4 text-center">
                        <span class="text-xl font-black ${{aCount > 0 ? 'text-red-400' : 'text-emerald-400'}}">${{aCount}}</span> <span class="text-xs text-slate-500">回</span>
                    </td>
                    <td class="py-4 px-6 text-center">
                        <div class="flex items-center justify-center gap-2">
                            <span class="font-extrabold ${{textColor}} text-base">${{missRate}}%</span>
                        </div>
                        <div class="w-24 h-2 progress-bar-bg rounded-full mx-auto mt-1 overflow-hidden">
                            <div class="${{barColor}} h-full rounded-full" style="width: ${{missRate}}%"></div>
                        </div>
                    </td>
                    <td class="py-4 px-4 text-center font-bold text-amber-400">
                        ${{nonARedTotal}} <span class="text-xs font-normal text-slate-500">箇所</span>
                    </td>
                    <td class="py-4 px-6 text-right">
                        <button onclick="showDetail('${{staffName}}')" class="bg-red-600 hover:bg-red-500 text-white px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-md">
                            個別のミス確認 ➔
                        </button>
                    </td>
                `;

                tbody.appendChild(tr);

                // 個別ミス店舗の抽出
                info.shops.forEach(shop => {{
                    if (shop.is_a_red || shop.non_a_count > 0) {{
                        missShopsList.push({{
                            staff: staffName,
                            shopName: shop.name,
                            sv: shop.sv,
                            isA: shop.is_a_red,
                            nonACount: shop.non_a_count,
                            items: shop.non_a_items
                        }});
                    }}
                }});
            }});

            // 個別ミス店舗の表示
            const indContainer = document.getElementById('individualMissContainer');
            indContainer.innerHTML = '';

            missShopsList.forEach(item => {{
                const card = document.createElement('div');
                card.className = `p-4 rounded-xl border ${{item.isA ? 'border-red-500/50 bg-red-950/30' : 'border-amber-500/30 bg-slate-800/40'}}`;

                let tag = item.isA 
                    ? '<span class="bg-red-600 text-white text-xs font-bold px-2.5 py-0.5 rounded">A列ミスあり</span>' 
                    : '<span class="bg-amber-900/60 text-amber-300 text-xs font-bold px-2.5 py-0.5 rounded border border-amber-700/60">A列外赤セルあり</span>';

                let itemsHtml = '';
                if (item.items.length > 0) {{
                    itemsHtml = `
                        <div class="mt-2.5 pt-2 border-t border-slate-700/60">
                            <div class="text-xs text-amber-300 font-bold mb-1">A列以外の赤背景セル項目 (${{item.items.length}}箇所):</div>
                            <div class="flex flex-wrap gap-1.5">
                                ${{item.items.map(it => `<span class="bg-amber-900/40 text-amber-200 border border-amber-500/30 text-xs font-medium px-2 py-0.5 rounded">${{it}}</span>`).join('')}}
                            </div>
                        </div>
                    `;
                }}

                card.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div>
                            <span class="text-xs text-slate-400">最終更新: ${{item.staff}} (SV: ${{item.sv}})</span>
                            <h3 class="font-extrabold text-white text-base mt-0.5">${{item.shopName}} 店</h3>
                        </div>
                        ${{tag}}
                    </div>
                    ${{itemsHtml}}
                `;

                indContainer.appendChild(card);
            }});
        }}

        function showDetail(staffName) {{
            const info = staffData[staffName];
            if (!info) return;

            document.getElementById('modalStaffName').textContent = `${{staffName}} さんの個別のミス詳細`;
            document.getElementById('modalStaffMeta').textContent = `担当: ${{info.shops.length}}店舗 | A列ミス数: ${{info.a_count}}回 | ミス率: ${{info.miss_rate}}% | A列外赤セル: ${{info.non_a_red_total}}箇所`;

            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = '';

            info.shops.forEach(shop => {{
                const shopCard = document.createElement('div');
                shopCard.className = `p-4 rounded-xl border ${{shop.is_a_red ? 'border-red-500/50 bg-red-950/30' : 'border-slate-800 bg-slate-800/40'}}`;

                let aStatus = shop.is_a_red 
                    ? '<span class="bg-red-600 text-white text-xs font-bold px-2.5 py-1 rounded-md">A列 赤指摘あり</span>'
                    : '<span class="bg-slate-800 text-slate-400 text-xs font-semibold px-2.5 py-1 rounded-md">A列 指摘なし</span>';

                let nonAItemsHtml = '';
                if (shop.non_a_items.length > 0) {{
                    nonAItemsHtml = `
                        <div class="mt-3 pt-2 border-t border-slate-700/60">
                            <div class="text-xs font-bold text-amber-300 mb-1.5">A列以外の赤背景セル項目 (${{shop.non_a_items.length}}箇所):</div>
                            <div class="flex flex-wrap gap-1.5">
                                ${{shop.non_a_items.map(item => `<span class="bg-amber-900/40 text-amber-200 border border-amber-500/40 text-xs font-medium px-2 py-0.5 rounded">${{item}}</span>`).join('')}}
                            </div>
                        </div>
                    `;
                }}

                shopCard.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex items-center gap-2">
                            <span class="font-extrabold text-white text-base">${{shop.name}} 店</span>
                            <span class="text-xs text-slate-400">(SV: ${{shop.sv}})</span>
                        </div>
                        ${{aStatus}}
                    </div>
                    ${{nonAItemsHtml}}
                `;

                modalBody.appendChild(shopCard);
            }});

            document.getElementById('detailModal').classList.remove('hidden');
        }}

        function closeModal() {{
            document.getElementById('detailModal').classList.add('hidden');
        }}

        document.addEventListener('DOMContentLoaded', renderPortal);
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(html_content)

print('Generated new index.html with individual miss priority and miss rates successfully')
