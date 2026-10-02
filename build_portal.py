import json

with open('portal_json_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

staff_data = data['staff_data']
col_ranking = data['col_ranking']

ranking_html = ''
sorted_rank = sorted(col_ranking.items(), key=lambda x: x[1], reverse=True)
for rank, (col_name, count) in enumerate(sorted_rank, 1):
    ranking_html += f"""
    <div style="background: rgba(239, 68, 68, 0.08); border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="background: #ef4444; color: white; font-weight: bold; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px;">{rank}</span>
            <span style="font-weight: 600; color: #1e293b;">{col_name}</span>
        </div>
        <span style="background: #fee2e2; color: #991b1b; font-weight: bold; padding: 4px 10px; border-radius: 20px; font-size: 13px;">{count} 店舗</span>
    </div>
    """

js_staff_data = json.dumps(staff_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【公式】マスタミス自動カウントWebポータル</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans JP', 'Inter', sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
        }}
        .glass-header {{
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
        }}
        .card-shadow {{
            box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
        }}
        .badge-perfect {{
            background: #dcfce7;
            color: #166534;
            border: 1px solid #86efac;
        }}
        .badge-alert {{
            background: #fee2e2;
            color: #991b1b;
            border: 1px solid #fca5a5;
        }}
    </style>
</head>
<body class="min-h-screen pb-16">

    <!-- ヘッダー -->
    <header class="glass-header text-white py-6 px-8 sticky top-0 z-40 shadow-lg">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="bg-red-500 text-white text-xs font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">純赤色(#FFFF0000)厳密抽出</span>
                    <h1 class="text-2xl md:text-3xl font-extrabold tracking-tight">店舗マスタチェック指摘カウントWebポータル</h1>
                </div>
                <p class="text-slate-400 text-sm mt-1">毎朝提出マスタの純赤色マーカーのみを正確自動集計・どこでミスが多いかを可視化</p>
            </div>
            <div class="flex items-center gap-3 text-xs bg-slate-800/80 px-4 py-2 rounded-lg border border-slate-700">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>対象データ: 2026/10/01 提出分 (全40店舗・全157項目)</span>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 md:px-8 mt-8 space-y-8">

        <!-- 精密判定バナー -->
        <div class="bg-red-900/10 border-l-4 border-red-600 p-4 rounded-r-xl shadow-sm flex items-start gap-4">
            <div class="text-2xl">🎯</div>
            <div>
                <h3 class="font-bold text-red-950 text-base">【精密判定完了】純赤色セル（#FFFF0000）のみを厳密抽出カウント</h3>
                <p class="text-slate-700 text-sm mt-1">
                    黄色・緑色・ラベンダー色・グレー等の他背景色は誤検出を防ぐため自動除外済みです。<strong>A列（店舗名）の純赤マーカーのみを「マスタミス指摘数（計13回）」</strong>としてカウントし、<strong>A列以外の純赤マーカー箇所（計26箇所）を内訳項目</strong>として表示しております。
                </p>
            </div>
        </div>

        <!-- KPIカード -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-5">
            <div class="bg-white p-6 rounded-2xl border border-slate-100 card-shadow">
                <div class="text-slate-500 text-xs font-bold uppercase tracking-wider">全チェック店舗数</div>
                <div class="text-3xl font-black text-slate-900 mt-2">40 <span class="text-base font-normal text-slate-500">店舗</span></div>
                <div class="text-xs text-slate-400 mt-2">全店舗マスタ157項目スキャン完了</div>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-red-100 card-shadow bg-gradient-to-br from-white to-red-50/30">
                <div class="text-red-600 text-xs font-bold uppercase tracking-wider">A列赤指摘店舗数 (マスタミス回数)</div>
                <div class="text-3xl font-black text-red-600 mt-2">13 <span class="text-base font-normal text-slate-500">店舗</span></div>
                <div class="text-xs text-red-500 font-medium mt-2">全40店舗中 32.5% で店舗指摘あり</div>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-amber-100 card-shadow bg-gradient-to-br from-white to-amber-50/30">
                <div class="text-amber-700 text-xs font-bold uppercase tracking-wider">A列以外の赤指摘 項目総数</div>
                <div class="text-3xl font-black text-amber-600 mt-2">26 <span class="text-base font-normal text-slate-500">箇所</span></div>
                <div class="text-xs text-amber-600 mt-2">内訳項目（どの項目でミスが多いか）</div>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-emerald-100 card-shadow bg-gradient-to-br from-white to-emerald-50/30">
                <div class="text-emerald-700 text-xs font-bold uppercase tracking-wider">ミス0件の良好スタッフ</div>
                <div class="text-3xl font-black text-emerald-600 mt-2">6 <span class="text-base font-normal text-slate-500">名 / 全13名</span></div>
                <div class="text-xs text-emerald-600 font-medium mt-2">46.2% のスタッフがパーフェクト</div>
            </div>
        </div>

        <!-- ミス多発項目（A列以外の赤マーカー）ランキング -->
        <section class="bg-white rounded-2xl p-6 border border-slate-200 card-shadow">
            <div class="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                <div>
                    <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span>📌</span> A列以外の純赤マーカー多発項目ランキング（ミス箇所の特定）
                    </h2>
                    <p class="text-xs text-slate-500 mt-0.5">どの項目の記入ミス・更新漏れが多いかを一覧化（全26箇所）</p>
                </div>
                <span class="text-xs font-semibold bg-red-100 text-red-700 px-3 py-1 rounded-full">A列外の全指摘箇所</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
                {ranking_html}
            </div>
        </section>

        <!-- スタッフ別マスタミス指摘数 テーブル (全13名全員記載) -->
        <section class="bg-white rounded-2xl border border-slate-200 card-shadow overflow-hidden">
            <div class="p-6 border-b border-slate-100 flex flex-col md:flex-row justify-between md:items-center gap-4 bg-slate-50/50">
                <div>
                    <h2 class="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span>👔</span> 最終更新スタッフ別 マスタミス指摘数（全13名全員分）
                    </h2>
                    <p class="text-xs text-slate-500 mt-1">A列の純赤店舗マーカーのみを指摘数としてカウント（ミスがないスタッフも一目で評価可能）</p>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-100/70 text-slate-600 text-xs font-bold uppercase tracking-wider border-b border-slate-200">
                            <th class="py-4 px-6">最終更新スタッフ</th>
                            <th class="py-4 px-4 text-center">担当店舗数</th>
                            <th class="py-4 px-4 text-center">A列 赤指摘店舗数<br><span class="text-2xs font-normal text-slate-400">(マスタミス指摘回数)</span></th>
                            <th class="py-4 px-4 text-center">A列以外の赤指摘<br><span class="text-2xs font-normal text-slate-400">(内訳項目箇所数)</span></th>
                            <th class="py-4 px-6 text-center">評価ステータス</th>
                            <th class="py-4 px-6 text-right">アクション</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-100 text-sm font-medium">
                        <!-- JSで動的レンダリング -->
                    </tbody>
                </table>
            </div>
        </section>

    </main>

    <!-- モーダルダイアログ -->
    <div id="detailModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[85vh] flex flex-col overflow-hidden animate-fade-in">
            <div class="px-6 py-5 bg-slate-900 text-white flex justify-between items-center">
                <div>
                    <h3 id="modalStaffName" class="text-xl font-bold">スタッフ詳細</h3>
                    <p id="modalStaffMeta" class="text-xs text-slate-400 mt-1"></p>
                </div>
                <button onclick="closeModal()" class="text-slate-400 hover:text-white text-2xl font-bold p-1">&times;</button>
            </div>
            <div id="modalBody" class="p-6 overflow-y-auto space-y-4">
                <!-- 詳細コンテンツ -->
            </div>
            <div class="px-6 py-4 bg-slate-50 border-t border-slate-100 flex justify-end">
                <button onclick="closeModal()" class="bg-slate-800 hover:bg-slate-900 text-white px-5 py-2 rounded-xl text-sm font-bold transition-all">閉じる</button>
            </div>
        </div>
    </div>

    <script>
        const staffData = {js_staff_data};

        function renderTable() {{
            const tbody = document.querySelector('tbody');
            tbody.innerHTML = '';

            const entries = Object.entries(staffData).sort((a, b) => {{
                if (a[1].a_count !== b[1].a_count) return a[1].a_count - b[1].a_count;
                return b[1].shops.length - a[1].shops.length;
            }});

            entries.forEach(([staffName, info]) => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50/80 transition-colors';

                const shopCount = info.shops.length;
                const aCount = info.a_count;
                const nonACount = info.non_a_count;

                let statusBadge = '';
                if (aCount === 0) {{
                    statusBadge = '<span class="px-3 py-1 rounded-full text-xs font-bold badge-perfect flex items-center justify-center gap-1 w-28 mx-auto"><span>✨</span> ミスなし (0回)</span>';
                }} else {{
                    statusBadge = `<span class="px-3 py-1 rounded-full text-xs font-bold badge-alert flex items-center justify-center gap-1 w-28 mx-auto"><span>⚠️</span> 指摘 ${{aCount}}回</span>`;
                }}

                tr.innerHTML = `
                    <td class="py-4 px-6 font-bold text-slate-900 flex items-center gap-3">
                        <div class="w-9 h-9 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center font-bold text-slate-700 text-xs">
                            ${{staffName.charAt(0)}}
                        </div>
                        <div>
                            <div>${{staffName}}</div>
                            <div class="text-xs text-slate-400 font-normal">担当店舗数: ${{shopCount}}店</div>
                        </div>
                    </td>
                    <td class="py-4 px-4 text-center font-semibold text-slate-700">${{shopCount}} 店</td>
                    <td class="py-4 px-4 text-center">
                        <span class="text-base font-extrabold ${{aCount > 0 ? 'text-red-600' : 'text-emerald-600'}}">${{aCount}}</span> <span class="text-xs text-slate-400">回</span>
                    </td>
                    <td class="py-4 px-4 text-center font-bold ${{nonACount > 0 ? 'text-amber-600' : 'text-slate-400'}}">
                        ${{nonACount}} <span class="text-xs font-normal text-slate-400">箇所</span>
                    </td>
                    <td class="py-4 px-6 text-center">${{statusBadge}}</td>
                    <td class="py-4 px-6 text-right">
                        <button onclick="showDetail('${{staffName}}')" class="bg-slate-100 hover:bg-slate-200 text-slate-800 px-3.5 py-1.5 rounded-lg text-xs font-bold transition-all border border-slate-300">
                            詳細・内訳 ➔
                        </button>
                    </td>
                `;

                tbody.appendChild(tr);
            }});
        }}

        function showDetail(staffName) {{
            const info = staffData[staffName];
            if (!info) return;

            document.getElementById('modalStaffName').textContent = `${{staffName}} さんのチェック内訳`;
            document.getElementById('modalStaffMeta').textContent = `担当店舗数: ${{info.shops.length}}店舗 | A列赤指摘数: ${{info.a_count}}回 | A列以外の赤指摘: ${{info.non_a_count}}箇所`;

            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = '';

            info.shops.forEach(shop => {{
                const shopCard = document.createElement('div');
                shopCard.className = `p-4 rounded-xl border ${{shop.is_a_red ? 'border-red-200 bg-red-50/40' : 'border-slate-200 bg-white'}}`;

                let aStatus = shop.is_a_red 
                    ? '<span class="bg-red-600 text-white text-xs font-bold px-2.5 py-0.5 rounded-md">A列 赤マーカー指摘あり</span>'
                    : '<span class="bg-slate-100 text-slate-600 text-xs font-semibold px-2.5 py-0.5 rounded-md">A列 指摘なし</span>';

                let nonAItemsHtml = '';
                if (shop.non_a_items.length > 0) {{
                    nonAItemsHtml = `
                        <div class="mt-3 pt-2 border-t border-slate-200/60">
                            <div class="text-xs font-bold text-amber-800 mb-1.5 flex items-center gap-1">
                                <span>⚠️</span> A列以外の赤マーカー指摘項目 (${{shop.non_a_items.length}}箇所):
                            </div>
                            <div class="flex flex-wrap gap-1.5">
                                ${{shop.non_a_items.map(item => `<span class="bg-amber-100 text-amber-900 border border-amber-200 text-xs font-medium px-2 py-0.5 rounded">${{item}}</span>`).join('')}}
                            </div>
                        </div>
                    `;
                }} else {{
                    nonAItemsHtml = '<div class="text-xs text-slate-400 mt-2">A列以外の赤指摘項目はありません。</div>';
                }}

                shopCard.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div class="flex items-center gap-2">
                            <span class="font-bold text-slate-900 text-base">${{shop.name}} 店</span>
                            <span class="text-xs text-slate-500">(SV: ${{shop.sv}})</span>
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

        document.addEventListener('DOMContentLoaded', renderTable);
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as out:
    out.write(html_content)

print('Generated index.html successfully')
