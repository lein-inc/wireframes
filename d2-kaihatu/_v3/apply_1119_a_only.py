#!/usr/bin/env python3
"""11/19 関指示：TOP は A案のみ（B・C は不採用）。C案の網点の図（Fig.01 Ground Model）を A案側で
   写真が無い・ダミーの箇所／写真より図のほうが伝わる箇所に使う。グローバルナビのリンク先も整理
  - js/hfig.js ＋ css/hfig.css（網点の図の部品）を作成済み。ここでは差し込みとリンク整理だけ
  - 一度きりの適用。バックアップ _v3/bk_20261119_a_only/
"""
import os, re, glob, shutil
WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(WF, n)
BK = os.path.join(WF, '_v3', 'bk_20261119_a_only')
assert not os.path.exists(BK), '適用済み'
os.makedirs(BK)
FILES = [f for f in sorted(glob.glob(P('design3-*.html'))) if not f.endswith('design3-top.html')] + [P('design31a-top.html')]
for f in FILES:
    shutil.copy2(f, BK)

TOP = 'design31a-top.html'


def fig(model, title, mode, metric, n='34°35′', e='133°45′'):
    return (f'<figure class="hfig" data-model="{model}" data-fig="{title}" data-mode="{mode}" '
            f'data-metric="{metric}" data-n="{n}" data-e="{e}"></figure>')


# ダミー画像 → 網点の図（ページ, ダミー画像, 図）
SWAP = [
    ('design3-service-design.html', 'img/dummy/39.jpg', fig('strata', 'Fig. 01 — Boring Log', 'Soil Strata / Section', 'Depth|m|1')),
    ('design3-service-design.html', 'img/dummy/40.jpg', fig('eco', 'Fig. 02 — Habitat Survey', 'Observation Points', 'Points|pt|240')),
    ('design3-service-design.html', 'img/dummy/41.jpg', fig('air', 'Fig. 03 — Monitoring', 'Water / Air', 'Δ|ppm|40')),
    ('design3-service-design.html', 'img/dummy/42.jpg', fig('ripple', 'Fig. 04 — Vibration', 'Noise / Vibration', 'L.max|dB|420')),
    ('design3-service-survey.html', 'img/dummy/38.jpg', fig('river', 'Fig. 01 — Bathymetry', 'Sonar / Cross Section', 'D.max|m|24', '34°31′', '133°46′')),
    ('design3-social.html', 'img/dummy/43.jpg', fig('disaster', 'Fig. 01 — Before / After', 'Slope Change Detection', 'H.max|m|186')),
    ('design3-strengths.html', 'img/dummy/36.jpg', fig('route', 'Fig. 1800 — Survey Route', 'Ino Tadataka / 40,000 km', 'Walk|km|400', '35°41′', '139°46′')),
    ('design3-strengths.html', 'img/dummy/03.jpg', fig('scan', 'Fig. 02 — Workflow', 'Scan → Point Cloud → CAD', 'H.max|m|186')),
]

HEAD = '<link rel="stylesheet" href="css/hfig.css?v=1">'
JS = '<script src="js/hfig.js?v=1" defer></script>'


def add_assets(h):
    if 'css/hfig.css' not in h:
        h = h.replace('</head>', HEAD + '\n</head>', 1)
        h = h.replace('</body>', JS + '\n</body>', 1)
    return h


for page, img, f in SWAP:
    h = open(P(page)).read()
    # img-ph：<div class="img-ph … is-dummy"><img src=…></div>
    m = re.search(r'<div class="(img-ph[^"]*?) is-dummy"><img src="' + re.escape(img) + r'"[^>]*></div>', h)
    if m:
        h = h.replace(m.group(0), f'<div class="{m.group(1)} has-hfig">{f}</div>', 1)
    else:  # ph-clip：英字ラベル・veil は外す（図に注記があるので）
        m = re.search(r'<div class="(ph-clip[^"]*?) hov is-dummy"><img src="' + re.escape(img) + r'"[^>]*>.*?</div>', h)
        assert m, (page, img)
        h = h.replace(m.group(0), f'<div class="{m.group(1)} has-hfig">{f}</div>', 1)
    open(P(page), 'w').write(add_assets(h))

# A案 TOP：強み（ドローン／3Dスキャナー／GNSS）は文字だけだったので、各項目に図
h = open(P(TOP)).read()
for icon, f in (('DRONE SURVEY', fig('drone', 'Fig. A — Drone Survey', 'Flight Lines / Ortho', 'Alt|m|120')),
                ('3D SCANNER', fig('structure', 'Fig. B — 3D Laser Scan', 'Bridge / Point Cloud', 'H|m|40')),
                ('GNSS', fig('gnss', 'Fig. C — GNSS', 'Network RTK', 'σ|mm|30'))):
    old = f'<div class="str-item">\n        <span class="icon">{icon}</span>'
    assert old in h, icon
    h = h.replace(old, f'<div class="str-item has-fig">\n        <div class="str-fig has-hfig">{f}</div>\n        <span class="icon">{icon}</span>', 1)
h = add_assets(h)
open(P(TOP), 'w').write(h)

# ---- グローバルナビ・リンク整理 ----
#  TOP は A案（design31a-top.html）。ロゴ・パンくず・フッターの「ホーム」をすべて A案へ
#  グローバルナビは A案 TOP と同じ並び（ホームはロゴで戻る）：事業案内／強み・技術／社会活動／会社案内／ニュース／お問い合わせ＋右上「採用情報」
#  「私たちのステートメント」は旧WF（グレーの statement-main.html）に飛んでいたので会社案内の代表あいさつへ
for f in FILES:
    h = open(f).read(); o = h
    h = re.sub(r'(<nav class="gnav"><ul>)<li><a href="design3-top.html">ホーム</a></li>', r'\1', h)
    h = h.replace('href="design3-top.html"', f'href="{TOP}"')
    h = h.replace('href="statement-main.html"', 'href="design3-about.html#greeting"')
    if h != o:
        open(f, 'w').write(h)
print('ok')
