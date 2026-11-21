#!/usr/bin/env python3
"""v3.1 TOP デザインパターン（design3-top.html を元に2案を生成。何度実行しても同じ）
  A: design31a-top.html … 地形図（等高線の線画）がFVからTOP全体に流れる。撮影写真は地図上の測点ピン
  B: design31b-top.html … アイソメ線画のまち。FVのワイヤーメッシュの地面が下まで続き、各セクションがその上に乗る
  イラストのトーンは v1〜v3 のFV（3Dワイヤー地形）の線画を踏襲：白地＋細いグレー/青の線、面はほぼ白
  絵は _v3/v31_art_a.py / v31_art_b.py が img/v31/ に SVG を書き出す
"""
import re, sys
from lib import read, WF
import os

TOP = read('top')


def strip_hero(h):
    a = h.index('<!-- ============ HERO')
    b = h.index('<!-- ============ STATEMENT')
    return h[:a], h[b:]


def common(h, tag, banner):
    h = h.replace('（デザイン案 v3）', f'（デザイン案 v3.1-{tag}）')
    h = re.sub(r'(<div class="wf-banner">\s*<span>).*?</span>', lambda m: m.group(1) + banner + '</span>', h, count=1)
    h = re.sub(r'(<link rel="stylesheet" href="css/v3\.css[^"]*">)',
               rf'\1\n<link rel="stylesheet" href="css/v31{tag.lower()}.css?v=1">', h, count=1)
    h = h.replace('<body>', f'<body class="v31 v31{tag.lower()}">', 1)
    return h


PINS_A = [  # (写真, 左%, 上%, 番号, 名前, リンク)
    ('0290', 63, 13, '01', '測量', 'design3-service-survey.html'),
    ('0389', 84, 31, '02', '調査・設計', 'design3-service-design.html'),
    ('0130', 70, 55, '03', '施工管理', 'design3-service-management.html'),
    ('0244', 89, 69, 'Tech', 'ドローン測量', 'design3-strengths.html'),
]

HERO_A = '''<!-- ============ HERO（v3.1-A 地形図） ============ -->
<section class="h31a">
  <div class="wrap h31a__in">
    <div class="h31a__copy">
      <span class="h31a__coord">SURVEY MAP ／ 34°35′N 133°46′E ／ KURASHIKI, OKAYAMA</span>
      <h1>測る技術で、<br>未来に残す。</h1>
      <p class="h31a__en">Surveying the ground. Preserving the future.</p>
      <p class="h31a__sub">測量・調査設計・施工管理。岡山・倉敷から、全国の社会基盤づくりを支える。</p>
      <div class="h31a__btns">
        <a href="design3-recruit.html" class="pill yellow">採用情報を見る <span class="circ">→</span></a>
        <a href="design3-contact.html" class="pill ghost">お問い合わせ <span class="circ">→</span></a>
      </div>
    </div>
  </div>
{pins}
  <div class="h31a__legend" aria-hidden="true">
    <span class="north"><i></i>N</span>
    <span class="scale"><i></i><i></i><i></i><i></i><em>0　　　500m</em></span>
  </div>
</section>

'''


def pins_a():
    out = []
    for n, x, y, no, name, href in PINS_A:
        out.append(f'  <a class="mpin" href="{href}" style="--x:{x}%; --y:{y}%;">'
                   f'<span class="mpin__ph"><img src="img/photo/S120{n}.jpg" alt=""></span>'
                   f'<span class="mpin__tag"><b>{no}</b>{name}</span></a>')
    return '\n'.join(out)


def build_a():
    h = common(TOP, 'A', 'DESIGN v3.1-A ｜ TOP：地形図（等高線の線画がFVからTOP全体に流れる）')
    head, rest = strip_hero(h)
    # 地形の背景（FV〜NEWS）を1枚のSVGでつなぐ
    cta = rest.index('<!-- ============ CTA')
    body = (HERO_A.replace('{pins}', pins_a()) + rest[:cta])
    land = ('<div class="land31">\n<img class="land31__bg" src="img/v31/a-terrain.svg" alt="" aria-hidden="true">\n'
            + body + '</div><!-- /land31 -->\n\n')
    h = head + land + rest[cta:]
    # Service の写真に測点番号
    h = h.replace('<span class="no">01</span>', '<span class="no">01</span><span class="pt">△ No.01</span>', 1)
    h = h.replace('<span class="no">02</span>', '<span class="no">02</span><span class="pt">△ No.02</span>', 1)
    h = h.replace('<span class="no">03</span>', '<span class="no">03</span><span class="pt">△ No.03</span>', 1)
    open(os.path.join(WF, 'design31a-top.html'), 'w').write(h)
    print('ok design31a-top.html')


HERO_B = '''<!-- ============ HERO（v3.1-B アイソメ線画のまち） ============ -->
<section class="h31b">
  <img class="h31b__town" src="img/v31/b-town.svg" alt="" aria-hidden="true">
  <div class="wrap h31b__in">
    <div class="h31b__copy">
      <p class="h31b__en">SURVEYING<br>THE GROUND.</p>
      <h1>測る技術で、未来に残す。</h1>
      <p class="h31b__sub">測量・調査設計・施工管理。<br>岡山・倉敷から、全国の社会基盤づくりを支える。</p>
      <div class="h31b__btns">
        <a href="design3-recruit.html" class="pill yellow">採用情報を見る <span class="circ">→</span></a>
        <a href="design3-contact.html" class="pill ghost">お問い合わせ <span class="circ">→</span></a>
      </div>
    </div>
  </div>
</section>

'''


def build_b():
    h = common(TOP, 'B', 'DESIGN v3.1-B ｜ TOP：アイソメ線画のまち（FVのワイヤー地形とまちがTOP全体に広がる）')
    head, rest = strip_hero(h)
    cta = rest.index('<!-- ============ CTA')
    body = HERO_B + rest[:cta]
    land = ('<div class="land31">\n<img class="land31__bg" src="img/v31/b-ground.svg" alt="" aria-hidden="true">\n'
            + body + '</div><!-- /land31 -->\n\n')
    h = head + land + rest[cta:]
    # Service カード：写真の上にアイソメの小景をのせる
    for i, key in ((1, 'survey'), (2, 'design'), (3, 'management')):
        h = h.replace(f'<span class="no">0{i}</span>',
                      f'<span class="no">0{i}</span><img class="vig" src="img/v31/b-vig-{key}.svg" alt="" aria-hidden="true">', 1)
    # Founder：「月へでも行くぞ」に月と空
    h = h.replace('<section class="founder">', '<section class="founder"><img class="sky31" src="img/v31/b-sky.svg" alt="" aria-hidden="true">', 1)
    open(os.path.join(WF, 'design31b-top.html'), 'w').write(h)
    print('ok design31b-top.html')


if __name__ == '__main__':
    which = sys.argv[1:] or ['a', 'b']
    if 'a' in which: build_a()
    if 'b' in which: build_b()
