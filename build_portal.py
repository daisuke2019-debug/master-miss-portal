import json

with open('portal_json_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

staff_data = data['staff_data']
all_issue_counts = data['all_issue_counts']

# 多発エラー項目のランキング作成 (TOP 6)
sorted_issues = sorted(all_issue_counts.items(), key=lambda x: x[1], reverse=True)[:6]
ranking_html = ''
for rank, (issue_name, count) in enumerate(sorted_issues, 1):
    ranking_html += f"""
    <div class="flex items-center justify-between p-3.5 bg-slate-50 hover:bg-slate-100/80 rounded-xl transition-all border border-slate-200/60">
        <div class="flex items-center gap-3">
            <span class="w-6 h-6 rounded-full bg-slate-800 text-white font-bold text-xs flex items-center justify-center">{rank}</span>
            <span class="font-bold text-slate-800 text-sm">{issue_name}</span>
        </div>
        <span class="text-xs font-black bg-red-100 text-red-700 px-3 py-1 rounded-full border border-red-200">{count} 店舗</span>
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
            background-color: #0f172a;
            color: #f8fafc;
        }}
        .board-header {{
            background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .main-card {{
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }}
        .row-hover:hover {{
            background-color: rgba(255, 255, 255, 0.03);
        }}
        .badge-danger {{
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.4);
        }}
        .badge-success {{
            background: rgba(16, 185, 129, 0.2);
            color: #6ee7b7;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }}
    </style>
</head>
<body class="min-h-screen pb-20">

    <!-- 👑 BOARD Executive Header -->
    <header class="board-header py-8 px-6 md:px-12 sticky top-0 z-40">
        <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="bg-indigo-600 text-white font-extrabold text-xs px-3 py-1 rounded-full uppercase tracking-wider shadow-sm">BOARD8 統括ダッシュボード</span>
                    <span class="text-xs text-slate-400">Dai CEO 直轄ポータル</span>
                </div>
                <h1 class="text-2xl md:text-3xl font-black text-white mt-1 tracking-tight">店舗マスタチェック 指摘カウントポータル</h1>
            </div>
            <div class="flex items-center gap-4 text-xs font-semibold bg-slate-800/90 text-slate-300 px-4 py-2.5 rounded-xl border border-slate-700">
                <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>2026/10/01 提出マスタ全40店舗集計完了</span>
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 md:px-8 mt-8 space-y-8">

        <!-- 📊 トップKPIサマリー (一目でわかる極上シンプル指標) -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="main-card p-6 rounded-2xl">
                <div class="text-slate-400 text-xs font-bold uppercase tracking-wider">全チェック店舗数</div>
                <div class="text-4xl font-black text-white mt-2">40 <span class="text-sm font-normal text-slate-400">店舗</span></div>
                <div class="text-xs text-slate-400 mt-2">13名の最終更新スタッフ対象</div>
            </div>

            <div class="main-card p-6 rounded-2xl bg-gradient-to-br from-slate-800 to-red-950/40 border-red-500/30">
                <div class="text-red-400 text-xs font-bold uppercase tracking-wider">A列マスタミス指摘数 (総計)</div>
                <div class="text-4xl font-black text-red-400 mt-2">13 <span class="text-sm font-normal text-slate-400">回</span></div>
                <div class="text-xs text-red-300/80 font-bold mt-2">最多指摘: 櫻井 蓮 (4回)</div>
            </div>

            <div class="main-card p-6 rounded-2xl bg-gradient-to-br from-slate-800 to-emerald-950/40 border-emerald-500/30">
                <div class="text-emerald-400 text-xs font-bold uppercase tracking-wider">A列ノーミス評価スタッフ</div>
                <div class="text-4xl font-black text-emerald-400 mt-2">6 <span class="text-sm font-normal text-slate-400">名 / 全13名</span></div>
                <div class="text-xs text-emerald-300/80 font-bold mt-2">46.2% がパーフェクト</div>
            </div>
        </div>

        <!-- 👔 メインテーブル: スタッフ別マスタミス指摘数 (最優先表示) -->
        <section class="main-card rounded-2xl overflow-hidden">
            <div class="p-6 border-b border-slate-700/60 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-800/40">
                <div>
                    <h2 class="text-xl font-extrabold text-white flex items-center gap-2">
                        <span>👔</span> 最終更新スタッフ別 指摘数一覧 (指摘が多い順)
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">A列の赤店舗マーカーをカウント。クリックで具体店舗・内訳を表示</p>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-800/80 text-slate-400 text-xs font-bold uppercase tracking-wider border-b border-slate-700">
                            <th class="py-4 px-6">最終更新スタッフ</th>
                            <th class="py-4 px-4 text-center">担当店舗数</th>
                            <th class="py-4 px-4 text-center">A列 指摘数<br><span class="text-2xs font-normal text-red-400">(マスタミス回数)</span></th>
                            <th class="py-4 px-4 text-center">全列指摘累計<br><span class="text-2xs font-normal text-amber-400">(内訳箇所数)</span></th>
                            <th class="py-4 px-6 text-center">評価ステータス</th>
                            <th class="py-4 px-6 text-right">アクション</th>
                        </tr>
                    </thead>
                    <tbody id="staffTableBody" class="divide-y divide-slate-800 text-sm font-medium">
                        <!-- JSでレンダリング -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- 📌 ミス多発項目内訳 (どこでミスが多いか一目でわかる) -->
        <section class="main-card p-6 rounded-2xl">
            <div class="mb-4 pb-3 border-b border-slate-700/60 flex justify-between items-center">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center gap-2">
                        <span>📌</span> ミス多発項目 内訳ランキング (全40店舗)
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">どの項目で記入漏れ・エラーが多いかを可視化</p>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {ranking_html}
            </div>
        </section>

    </main>

    <!-- モーダルダイアログ (シンプル＆見やすいデザイン) -->
    <div id="detailModal" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
        <div class="main-card rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden border border-slate-700">
            <div class="px-6 py-5 bg-slate-900 text-white flex justify-between items-center border-b border-slate-800">
                <div>
                    <h3 id="modalStaffName" class="text-xl font-extrabold text-white">スタッフ詳細</h3>
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

        function renderTable() {{
            const tbody = document.getElementById('staffTableBody');
            tbody.innerHTML = '';

            // ★指摘数が最上位の櫻井蓮(4回)が一番上にズバッと来るように降順ソート
            const entries = Object.entries(staffData).sort((a, b) => {{
                if (b[1].a_count !== a[1].a_count) return b[1].a_count - a[1].a_count;
                return b[1].total_red_items - a[1].total_red_items;
            }});

            entries.forEach(([staffName, info]) => {{
                const tr = document.createElement('tr');
                tr.className = 'row-hover transition-colors';

                const shopCount = info.shops.length;
                const aCount = info.a_count;
                const totalRedItems = info.total_red_items;

                let statusBadge = '';
                if (aCount === 0) {{
                    statusBadge = '<span class="px-3 py-1 rounded-full text-xs font-bold badge-success inline-flex items-center gap-1">✨ A列ミス0回</span>';
                }} else {{
                    statusBadge = `<span class="px-3 py-1 rounded-full text-xs font-bold badge-danger inline-flex items-center gap-1">⚠️ A列指摘 ${{aCount}}回</span>`;
                }}

                tr.innerHTML = `
                    <td class="py-4 px-6 font-bold text-white flex items-center gap-3">
                        <div class="w-9 h-9 rounded-full bg-slate-800 text-indigo-400 border border-slate-700 flex items-center justify-center font-bold text-xs">
                            ${{staffName.charAt(0)}}
                        </div>
                        <div>
                            <div class="text-base font-extrabold text-white">${{staffName}}</div>
                            <div class="text-xs text-slate-400 font-normal">担当: ${{shopCount}}店舗</div>
                        </div>
                    </td>
                    <td class="py-4 px-4 text-center font-semibold text-slate-300">${{shopCount}} 店</td>
                    <td class="py-4 px-4 text-center">
                        <span class="text-xl font-black ${{aCount > 0 ? 'text-red-400' : 'text-emerald-400'}}">${{aCount}}</span> <span class="text-xs text-slate-500">回</span>
                    </td>
                    <td class="py-4 px-4 text-center font-bold text-amber-400">
                        ${{totalRedItems}} <span class="text-xs font-normal text-slate-500">箇所</span>
                    </td>
                    <td class="py-4 px-6 text-center">${{statusBadge}}</td>
                    <td class="py-4 px-6 text-right">
                        <button onclick="showDetail('${{staffName}}')" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-md">
                            内訳を見る ➔
                        </button>
                    </td>
                `;

                tbody.appendChild(tr);
            }});
        }}

        function showDetail(staffName) {{
            const info = staffData[staffName];
            if (!info) return;

            document.getElementById('modalStaffName').textContent = `${{staffName}} さんの店舗チェック内訳`;
            document.getElementById('modalStaffMeta').textContent = `担当: ${{info.shops.length}}店舗 | A列指摘: ${{info.a_count}}回 | 全列指摘累計: ${{info.total_red_items}}箇所`;

            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = '';

            info.shops.forEach(shop => {{
                const shopCard = document.createElement('div');
                shopCard.className = `p-4 rounded-xl border ${{shop.is_a_red ? 'border-red-500/40 bg-red-950/20' : 'border-slate-800 bg-slate-800/40'}}`;

                let aStatus = shop.is_a_red 
                    ? '<span class="bg-red-500 text-white text-xs font-bold px-2.5 py-1 rounded-md">A列 赤指摘あり</span>'
                    : '<span class="bg-slate-800 text-slate-400 text-xs font-semibold px-2.5 py-1 rounded-md">A列 指摘なし</span>';

                shopCard.innerHTML = `
                    <div class="flex justify-between items-center mb-2">
                        <div class="flex items-center gap-2">
                            <span class="font-extrabold text-white text-base">${{shop.name}} 店</span>
                            <span class="text-xs text-slate-400">(SV: ${{shop.sv}})</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-bold px-2 py-0.5 rounded">指摘箇所: ${{shop.red_count}}箇所</span>
                            ${{aStatus}}
                        </div>
                    </div>
                    <div class="mt-2 text-xs text-slate-300 bg-slate-900/80 p-3 rounded-lg border border-slate-800 font-mono leading-relaxed">
                        <span class="text-slate-500 font-bold">【内訳詳細】</span><br>${{shop.items_detail}}
                    </div>
                `;

                modalBody.appendChild(shopCard);
            }});

            document.getElementById('detailModal').classList.remove('hidden');
        }}

        function closeModal() {{
            document.getElementById('detailModal').classList.add('hidden');
        }}

        document.addEventListener('DOMContentLoaded', renderTable);
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(html_content)

print('Rebuilt index.html with ultra-clean modern BOARD layout successfully')
