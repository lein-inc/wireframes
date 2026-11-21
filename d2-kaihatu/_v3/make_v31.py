#!/usr/bin/env python3
"""v3.1 TOP（design3-top.html を元に生成。何度実行しても同じ）
  design31a-top.html … FV は v3 のまま（3Dワイヤー地形の動画＋タイプライター）。
    その下は「等高線の地図」に、サン防災TOPのようなアイソメ線画の街・道路・港・入り江・吊り橋が NEWS まで1枚で続く
    （img/v31/a-terrain.svg）。Strengths・Recruit の紺ベタは外して白地のまま風景の中に置く。撮影写真は「測点ピン」
    山を立体ワイヤーで描く版は _v3/bk_v31a_wire/（a-terrain-wire-town.svg / V31_MODE=wire）
  絵は _v3/v31_art_a.py が書き出す（位置は measure.sh で測った _v3/m_a.json）
  11/11 の初版（平面の等高線＋FVも地図）は _v3/bk_v31a_flat/、不採用の B 案は _v3/bk_v31b/
"""
import re, os
from lib import read, WF

TOP = read('top')

PINS = [  # (写真, 左%, 上px, 番号, 名前, リンク)  ※ Statement セクション内の位置
    ('0290', 70, 70, '01', '測量', 'design3-service-survey.html'),
    ('0389', 88, 210, '02', '調査・設計', 'design3-service-design.html'),
    ('0130', 73, 430, '03', '施工管理', 'design3-service-management.html'),
    ('0244', 90, 560, 'Tech', 'ドローン測量', 'design3-strengths.html'),
]


def pins():
    out = ['<div class="st-pins" aria-label="事業">']
    for n, x, y, no, name, href in PINS:
        out.append(f'  <a class="mpin" href="{href}" style="--x:{x}%; --y:{y}px;">'
                   f'<span class="mpin__ph"><img src="img/photo/S120{n}.jpg" alt=""></span>'
                   f'<span class="mpin__tag"><b>{no}</b>{name}</span></a>')
    out.append('</div>')
    return '\n'.join(out)


def build_a():
    h = TOP.replace('（デザイン案 v3）', '（デザイン案 v3.1）')
    h = re.sub(r'(<div class="wf-banner">\s*<span>).*?</span>',
               lambda m: m.group(1) + 'DESIGN v3.1 ｜ TOP：FVの3D地形がページの最後まで背景に残り、スクロールでカメラが各コンテンツの画角へ動く' + '</span>', h, count=1)
    h = re.sub(r'(<link rel="stylesheet" href="css/v3\.css[^"]*">)', r'\1\n<link rel="stylesheet" href="css/v31a.css?v=5">', h, count=1)
    h = h.replace('<body>', '<body class="v31 v31a">', 1)
    a = h.index('<!-- ============ STATEMENT')
    b = h.index('<!-- ============ CTA')
    body = h[a:b].replace('<section class="statement">', '<section class="statement">\n' + pins(), 1)
    # セクションごとのカメラ（js/v31a.js → terrain-infra-embed-v31.html）と、パネル化する箱
    for sel, shot in (('<section class="statement">', 'peaks'), ('<section class="service">', 'city'), ('<section class="strengths">', 'scan'),
                      ('<section class="founder">', 'bridge'), ('<section class="recruit" id="recruit">', 'road'), ('<section class="news">', 'wide')):
        assert body.count(sel) == 1, sel
        body = body.replace(sel, sel[:-1] + f' data-shot="{shot}">')
    body = re.sub(r'(<section class="(?:service|strengths|founder|news)" data-shot="\w+">\s*(?:<div class="bg-word"[^>]*>[^<]*</div>\s*)?<div class=")wrap', r'\1wrap p31', body)
    body = body.replace('<div class="rec-grid">', '<div class="rec-grid p31">', 1)
    h = h[:a] + '<div class="land31">\n' + body + '</div><!-- /land31 -->\n\n' + h[b:]
    h = h.replace('<div class="hero">', '<div class="hero" data-shot="fv">', 1)
    # v3 の「Our Promise を抜けたら固定背景を消す」をやめ、スクロール連動の js に差し替え
    a2 = h.index('<script>\n/* 固定背景は Our Promise を抜けたら非表示')
    b2 = h.index('</script>', a2) + len('</script>')
    h = h[:a2] + '<script src="js/v31a.js?v=1" defer></script>' + h[b2:]
    # FV は v3.1 用の動画（測量図らしい注記・点群スキャン・三角点つき）
    h = h.replace('src="terrain-infra-embed.html"', 'src="terrain-infra-embed-v31.html"', 1)
    # Service の写真に測点番号
    for i in (1, 2, 3):
        h = h.replace(f'<span class="no">0{i}</span>', f'<span class="no">0{i}</span><span class="pt">△ No.0{i}</span>', 1)
    open(os.path.join(WF, 'design31a-top.html'), 'w').write(h)
    print('ok design31a-top.html')


if __name__ == '__main__':
    build_a()
