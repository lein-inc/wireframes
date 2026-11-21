#!/usr/bin/env python3
"""11/19 関指示（共通の体裁調整）
  1. 見出しの下につく ( 英語 ) を全ページで削除（.sec-h .en / .sec-head .en-label の括弧つき表記）
  2. アウトライン文字（背景の巨大英字・カードの番号）は字形の重なり部分の線が見えていた
     → 重なりのない書体 Archivo 800 に置き換え（Inter は可変フォントで輪郭が重なったまま）
  3. 下層ヘッダー右の ( 英語 ) と写真上の英字ラベルを削除
  4. 下層ヘッダーを「左に見出しエリア／右に写真」の2カラムでコンパクトに（CSS は v3.css 末尾）
  5. ページ下部CTAの採用パネル：採用TOP以外ではエントリー直ではなく採用TOPへ（表記も「採用情報」）
  HTMLの書き換えは 1（英字の span 削除）・3・5 とフォント読み込み。何度実行しても同じ結果
"""
import os, re, glob
WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(WF, n)
FONT_OLD = 'family=Inter:wght@400;500;700;800&'
FONT_NEW = 'family=Inter:wght@400;500;700;800&family=Archivo:wght@800&'
REC_OLD = re.compile(r'<a href="design3-recruit-entry\.html" class="panel rec">(\s*<img[^>]*>\s*)<span class="en">Entry</span>(\s*)<h3>採用エントリー</h3>')
n = {}
for f in sorted(glob.glob(P('design3-*.html'))) + [P('design31a-top.html')]:
    h = open(f).read(); o = h
    b = os.path.basename(f)
    if FONT_NEW not in h:
        h = h.replace(FONT_OLD, FONT_NEW)
    if b.startswith('design3-'):
        # 1. 見出し下の英字
        h = re.sub(r'(</h2>)<span class="en">[^<]*</span>', r'\1', h)          # .sec-h
        h = re.sub(r'(</h2>)<span class="en-label">[^<]*</span>', r'\1', h)    # .sec-head（下層）
        # 3. 下層ヘッダーの英字（右の括弧つき・写真上）
        h = re.sub(r'<span class="phero__en">[^<]*</span>', '', h)
        h = re.sub(r'(<div class="phero__ph"><img [^>]*>)<span class="en">[^<]*</span>', r'\1', h)
        # 統合した事業案内の区切り見出し右の英字
        h = re.sub(r'(<div class="svc-div__head[^"]*">.*?</h2>)<span class="en">[^<]*</span>', r'\1', h)
    # 5. 採用パネル（採用TOP以外）
    if b != 'design3-recruit.html':
        h = REC_OLD.sub(r'<a href="design3-recruit.html" class="panel rec">\1<span class="en">Recruit</span>\2<h3>採用情報</h3>', h)
    if h != o:
        open(f, 'w').write(h); n[b] = 1
print('changed', len(n), sorted(n))
