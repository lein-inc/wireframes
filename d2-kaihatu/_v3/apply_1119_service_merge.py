#!/usr/bin/env python3
"""11/18打ち合わせ決定（木村さん）：予算の都合で事業内容は1ページにまとめ、ページ内リンクで移動
  - design3-service.html に 測量／調査・設計／施工管理 の中身（各下層の phero〜cta3 の間のセクション）を統合
  - 各事業の頭に区切り見出し（No・名称・写真）、事業ごとの終わりに原稿シートの CTA 文言で問い合わせリンク
  - phero の直後にページ内メニュー（sibnav pnav：採用TOPと同じ部品）＋スクロール位置で現在地表示
  - design3-service-survey / -design / -management.html は _v3/bk_20261119_service/ へ退避して削除（B/C の同名も）
  - 全ページのリンクを付け替え（survey→#survey, design→#design, management→#management）
  一度きりの適用
"""
import os, re, glob, shutil
WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(WF, n)
BK = os.path.join(WF, '_v3', 'bk_20261119_service')
assert os.path.exists(P('design3-service-survey.html')), '適用済み'
os.makedirs(BK, exist_ok=True)
for f in glob.glob(P('design3-*.html')) + [P('design31a-top.html')]:
    shutil.copy2(f, BK)

SUBS = [  # slug, id, No, 名称, 英字, CTA文言（原稿シート各タブ末尾）
    ('survey', 'survey', '01', '測量', 'SURVEY', '測量のご相談はお気軽に。'),
    ('design', 'design', '02', '調査・設計', 'SURVEY & DESIGN', '調査・設計のご相談はお気軽に。'),
    ('management', 'management', '03', '施工管理', 'CONSTRUCTION MANAGEMENT', '施工管理・技術者派遣のご相談'),
]
top = open(P('design3-service.html')).read()
blocks = []
for slug, aid, no, name, en, cta in SUBS:
    h = open(P(f'design3-service-{slug}.html')).read()
    ph = re.search(r'<div class="phero__ph"><img src="([^"]+)"', h).group(1)
    a = h.index('</section>', h.index('<section class="phero v3">')) + len('</section>')
    b = h.index('<section class="cta3">')
    body = h[a:b].strip()
    head = (f'<section class="svc-div" id="{aid}">\n  <div class="wrap">\n'
            f'    <div class="svc-div__head fade-target"><span class="no">{no}</span><h2>{name}</h2><span class="en">{en}</span></div>\n'
            f'    <div class="svc-div__ph fade-target d-1"><img src="{ph}" alt="" loading="lazy"></div>\n  </div>\n</section>')
    tail = (f'<section class="svc-div__end">\n  <div class="wrap"><a href="design3-contact.html" class="pill ghost">{cta} <span class="circ">→</span></a>'
            f'<a href="#svc-top" class="svc-div__back">3つの事業へ戻る ↑</a></div>\n</section>')
    blocks.append(f'<!-- ============ {no} {name}（旧 design3-service-{slug}.html） ============ -->\n{head}\n{body}\n{tail}')

# 3つの事業：カードのリンクをページ内へ
for slug, aid, *_ in SUBS:
    top = top.replace(f'href="design3-service-{slug}.html" class="dcard', f'href="#{aid}" class="dcard')
top = top.replace('<section class="has-bgword tone">\n  <div class="bg-word" aria-hidden="true">FIELDS</div>',
                  '<section class="has-bgword tone" id="svc-top">\n  <div class="bg-word" aria-hidden="true">FIELDS</div>', 1)
assert 'id="svc-top"' in top
top = top.replace('それぞれの専門分野が異なるため、独立して深掘りできる構成にしています。', 'それぞれの専門分野を、このページの中で順にご紹介します。')

# 「一社完結」（dark-band）の前に3事業を差し込む
i = top.index('<section class="dark-band dark has-bgword">')
top = top[:i] + '\n\n'.join(blocks) + '\n\n' + top[i:]

# ページ内メニュー
PNAV = [('svc-top', '3つの事業'), ('survey', '測量'), ('design', '調査・設計'), ('management', '施工管理')]
li = ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in PNAV) + '<li><a href="design3-contact.html" class=" entry">お問い合わせ</a></li>'
i = top.index('</section>', top.index('<section class="phero v3">')) + len('</section>')
top = top[:i] + f'\n<nav class="sibnav pnav" aria-label="ページ内メニュー"><div class="wrap"><ul>{li}</ul></div></nav>' + top[i:]
SPY = ('<script>/* ページ内メニュー：スクロール位置の見出しを現在地に */(function(){var as=[].slice.call(document.querySelectorAll(".pnav a[href^=\'#\']"));'
       'var ss=as.map(function(a){return document.getElementById(a.getAttribute("href").slice(1));});'
       'function f(){var y=innerHeight*.35,c=-1;ss.forEach(function(s,i){if(s&&s.getBoundingClientRect().top<y)c=i;});'
       'as.forEach(function(a,i){a.classList.toggle("cur",i===c);});if(c>=0){var a=as[c],u=a.parentNode.parentNode;u.scrollLeft+=a.getBoundingClientRect().left-u.getBoundingClientRect().left-40;}}'
       'addEventListener("scroll",f,{passive:true});f();})();</script>\n')
top = top.replace('<section class="cta3">', SPY + '<section class="cta3">', 1)
# 網点の図（調査・設計のダミー差し替え分）を読む
if 'css/hfig.css' not in top:
    top = top.replace('</head>', '<link rel="stylesheet" href="css/hfig.css?v=4">\n</head>', 1)
    top = top.replace('</body>', '<script src="js/hfig.js?v=4" defer></script>\n</body>', 1)
open(P('design3-service.html'), 'w').write(top)

# 退避・削除
for slug, *_ in SUBS:
    os.remove(P(f'design3-service-{slug}.html'))
    for v in 'bc':
        f = P(f'design31{v}-service-{slug}.html')
        if os.path.exists(f):
            shutil.move(f, os.path.join(BK, os.path.basename(f)))

# リンク付け替え（全ページ）
for f in sorted(glob.glob(P('design3*.html'))):
    h = open(f).read(); o = h
    for slug, aid, *_ in SUBS:
        h = re.sub(rf'design3-service-{slug}\.html(#[\w-]+)?', f'design3-service.html#{aid}', h)
    if h != o:
        open(f, 'w').write(h)
print('ok')
