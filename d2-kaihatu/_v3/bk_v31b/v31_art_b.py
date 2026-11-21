#!/usr/bin/env python3
"""v3.1-B の絵（アイソメ線画のまち）を img/v31/ に書き出す
  b-town.svg … FV（1440×820）。ワイヤーメッシュの地面＋川・橋・道路・まち・測量班・ドローン・工事現場
  b-ground.svg … FV下〜NEWS の背景（メッシュの丘と小物がページの両脇・つなぎ目に続く）。_v3/m_b.json の位置を使う
  b-vig-*.svg … 事業カードの上にのせる小景 / b-sky.svg … Founder（月へでも行くぞ）の空
"""
import json, math, os
from v31_iso import Scene, mesh, BLUE, BLUE_L, BLUE_P, FILL, FILL2, FILL3, LINE, YEL

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'img', 'v31')


def write(name, svg):
    open(os.path.join(OUT, name), 'w').write(svg)
    print(name, len(svg) // 1024, 'KB')


def smooth(pts, n=6):
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                   + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(pts[-1])
    return out


def gauss(x, y, cx, cy, r, h):
    return h * math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (r * r))


# ------------------------------------------------------------------ FV
def town():
    W, H = 1440, 820
    sc = Scene(880, -96, 14.5)

    def hf(x, y):
        return (gauss(x, y, 2, 6, 8, 6) + gauss(x, y, 14, -4, 8, 5) + gauss(x, y, -8, 20, 9, 7.5)
                + gauss(x, y, -10, 40, 8, 6) + gauss(x, y, -6, 52, 6, 4) + gauss(x, y, 64, 4, 9, 5) + gauss(x, y, 70, 26, 8, 3.5))

    def alpha(X, Y):
        # 左下（コピーの場所）と下端は地面を消す
        a = 1.0
        d = math.hypot(max(0, 760 - X) / 1.25, max(0, Y - 210))
        a *= max(0, min(1, 1 - (d - 40) / 200)) if X < 760 and Y > 210 else 1
        a *= max(0, min(1, (H - 10 - Y) / 120))
        return a

    mesh(sc, -14, 72, -14, 72, hf, alpha)

    # 川（左奥→右手前）
    river = smooth([(-14, 30), (0, 31), (12, 33), (24, 29), (34, 33), (44, 40), (54, 43), (64, 47), (76, 50)])
    sc.band(river, 4.2, BLUE_P, BLUE_L, sw=1.2)
    sc.under.append(sc.line([(x, y + .3, 0) for x, y in river[2:-2]], BLUE_L, .7, ' stroke-dasharray="10 12" stroke-opacity=".6"'))
    # 道路（右奥→橋→左へ抜ける）
    road = smooth([(22, -14), (22, 0), (22, 14), (22, 28), (20, 36), (12, 40), (0, 40), (-16, 40)])
    sc.band(road, 2.6, '#F2F2F2', '#6B7480', center='#8A8A8A', sw=1)
    road2 = smooth([(22, 18), (32, 18), (44, 18), (58, 18), (74, 18)])
    sc.band(road2, 2.2, '#F2F2F2', '#6B7480', center='#8A8A8A', sw=1)

    # 橋（道路×川）
    bx, by = 20.7, 29.2
    for py in (27.9, 30.6):
        sc.box(bx + .2, py, 0, .6, .5, 1.0, depth=bx + py + 1)
    sc.box(bx - .1, 26.6, 1.0, 2.8, 5.2, .35, top='#F2F2F2', depth=bx + 26.6 + 7.5)
    sc.add(bx + 26.6 + 7.6, sc.line([(bx - .1, 26.6, 1.7), (bx - .1, 31.8, 1.7)], LINE, 1) + sc.line([(bx + 2.7, 26.6, 1.7), (bx + 2.7, 31.8, 1.7)], LINE, 1)
           + ''.join(sc.line([(bx + 2.7, yy, 1.35), (bx + 2.7, yy, 1.7)], LINE, .8) for yy in [26.6 + i * .65 for i in range(9)]))

    # 敷地（白い面でメッシュを消す）
    for (x, y, w, d) in [(24, 4, 14, 12), (24, 20, 9, 6), (36, 20, 12, 10)]:
        sc.under.append(sc.poly([(x, y, 0), (x + w, y, 0), (x + w, y + d, 0), (x, y + d, 0)], '#fff', '#C9D0D8', .8))

    # 本社（ロゴの三角）＋まち
    sc.box(30, 6, 0, 5, 4, 9, win=(4, 3))
    sc.add(30 + 5 + 6 + 4 + .02, sc.poly([(30.5, 10, 7.7), (33.5, 10, 7.7), (33.5, 10, 8.8), (30.5, 10, 8.8)], '#fff', LINE, .8)
           + sc.poly([(30.8, 10, 7.85), (31.8, 10, 7.85), (31.3, 10, 8.65)], BLUE, BLUE, .6))
    sc.box(25, 5, 0, 4, 3.4, 3.2, win=(2, 2))
    sc.box(25, 10, 0, 3.4, 4.6, 4.6, win=(3, 2))
    sc.house(36, 6, 3.2, 3, 2.4, 1.4, roof=BLUE_P)
    sc.house(36, 11, 3, 3, 2.2, 1.3)
    sc.box(25, 21, 0, 3.2, 3.6, 2.6, win=(2, 2))
    sc.house(29, 21.5, 3, 3, 2.2, 1.3, roof=BLUE_P)
    sc.box(38, 21, 0, 7, 3.4, 3.8, win=(2, 4))       # 倉庫
    sc.box(40, 26, 0, 3, 2.6, 2.0)
    for (x, y) in [(23.6, 3), (28, 15.4), (35, 15.4), (39.4, 15.2), (46.5, 21.5), (46, 25), (24, 17.4)]:
        sc.tree(x, y, .9, 1.4)
    sc.car(26, 17.3, 'x'); sc.car(48, 17.4, 'x', '#fff'); sc.car(22.6, 6, 'y')

    # 川沿いの木
    for (x, y, k) in [(6, 27, 'cone'), (8, 27.6, 'cone'), (28, 36, 'round'), (31, 37.6, 'cone'),
                      (50, 37.5, 'round'), (52, 38.2, 'cone'), (60, 51, 'round'), (16, 25.5, 'round')]:
        sc.tree(x, y, .95, 1.5, k)

    # 測量班（川の手前の河川敷）
    sc.tripod(36, 42, 1.3)
    sc.person(36.9, 42.6, 1.2, BLUE, arm='hold')
    sc.prism(43, 47, 1.2)
    sc.person(43.8, 47.3, 1.2, '#fff', vest=YEL)
    sc.add(36 + 42 + .5, sc.line([(36, 42, 2.3), (43, 47, 3.1)], BLUE_L, .9, ' stroke-dasharray="2 5"'))

    # 工事現場（対岸の手前）
    sc.under.append(sc.poly([(52, 50, 0), (66, 50, 0), (66, 60, 0), (52, 60, 0)], '#fff', '#C9D0D8', .8))
    sc.excavator(54, 51.5, 1.35)
    sc.box(61, 56, 0, 2.6, 2.6, 1.2, top='#F2F2F2')  # 土砂
    for (x, y) in [(52.5, 50.5), (55, 50.5), (57.5, 50.5), (60, 50.5), (62.5, 50.5), (65.5, 51), (65.5, 54)]:
        sc.cone(x, y, 1.1)
    sc.person(60, 54.5, 1.2, BLUE, arm='point')
    sc.person(58.5, 57.5, 1.2, '#fff', vest=YEL)

    # ドローン
    sc.drone(46, 33, 9, 1.5)
    sc.drone(12, 14, 14, 1.0, scan=False)

    # ピン
    sc.pin(39, 44, 6, '測量', '01')
    sc.pin(36.5, 9, 5.5, '調査・設計', '02')
    sc.pin(59, 55, 7, '施工管理', '03')

    write('b-town.svg', sc.svg(W, H))


# ------------------------------------------------------------------ 事業カードの小景
def vig_base(sc, n=7, hills=()):
    def hf(x, y):
        return sum(gauss(x, y, *h) for h in hills)
    def alpha(X, Y):
        return max(0, min(1, 1 - (math.hypot((X - 180) / 1.7, (Y - 150)) - 70) / 60))
    mesh(sc, 0, n, 0, n, hf, alpha, .5)


def vig_survey():
    sc = Scene(180, 72, 16)
    vig_base(sc, 9, ((1, 1, 2.5, 2.5),))
    sc.tripod(3.6, 3.6, 1.4)
    sc.person(4.5, 4.4, 1.25, BLUE, arm='hold')
    sc.prism(7.2, 6.2, 1.25)
    sc.person(7.9, 6.6, 1.25, '#fff', vest=YEL)
    sc.add(13, sc.line([(3.6, 3.6, 2.5), (7.2, 6.2, 3.2)], BLUE_L, 1, ' stroke-dasharray="2 5"'))
    sc.tree(6.5, 1.5, .9, 1.4, 'cone'); sc.tree(1.2, 6.6, .9, 1.4)
    sc.drone(2.2, 6.8, 6, 1.2, scan=False)
    write('b-vig-survey.svg', sc.svg(360, 230))


def vig_design():
    sc = Scene(180, 66, 16)
    vig_base(sc, 9)
    sc.box(2.4, 2.6, 0, 4.4, 2.2, 1.6, top='#fff', depth=9.3)                      # 机
    sc.box(3.0, 2.8, 1.6, .25, 1.6, 1.3, top='#fff', right=BLUE_P, depth=6.5)     # モニター
    sc.add(6.6, sc.line([(3.26, 3.0, 1.9), (3.26, 4.2, 2.3), (3.26, 4.2, 2.6)], BLUE_L, 1))
    sc.box(4.6, 3.0, 1.6, 1.8, 1.2, .05, top='#fff', depth=9.4)                    # 図面
    sc.add(9.5, ''.join(sc.line([(4.8 + i * .35, 3.15, 1.66), (4.8 + i * .35, 4.05, 1.66)], BLUE_L, .7) for i in range(5)))
    sc.person(4.4, 6.0, 1.3, '#fff', arm='point')
    sc.person(6.6, 6.2, 1.3, BLUE, arm='hold')
    sc.tree(7.6, 1.6, .8, 1.4)
    write('b-vig-design.svg', sc.svg(360, 230))


def vig_management():
    sc = Scene(150, 70, 15)
    vig_base(sc, 10)
    sc.excavator(2, 2.2, 1.1)
    for (x, y) in [(1, 6.8), (3.4, 7.4), (5.8, 7.8), (8.4, 7.4)]:
        sc.cone(x, y, 1.2)
    sc.person(7.6, 5.2, 1.25, BLUE, arm='point')
    sc.person(8.8, 3.6, 1.25, '#fff', vest=YEL)
    write('b-vig-management.svg', sc.svg(360, 230))


# ------------------------------------------------------------------ Founder の空（月へでも行くぞ）
def sky(w=1440, h=760):
    # 月は右の円形写真に重ねる（写真＝月）。軌道と雲・ドローンだけ線で描く
    cx, cy, r = 1084, 250, 196
    craters = ''.join(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{rr}" fill="none" stroke="#8A9099" stroke-opacity=".5"/>'
                      for dx, dy, rr in [(-150, -90, 14), (160, 60, 10), (120, -150, 8)])
    orbit = (f'<ellipse cx="{cx}" cy="{cy}" rx="330" ry="96" transform="rotate(-14 {cx} {cy})" fill="none" stroke="{BLUE_L}" stroke-opacity=".55" stroke-dasharray="3 7"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 26}" fill="none" stroke="#8A9099" stroke-opacity=".45"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{r + 60}" fill="none" stroke="#8A9099" stroke-opacity=".22"/>')
    def cloud(x, y, k):
        return (f'<path transform="translate({x} {y}) scale({k})" d="M0 30 h150 a22 22 0 0 0 -12 -40 a30 30 0 0 0 -52 -18 a34 34 0 0 0 -60 14 a24 24 0 0 0 -26 44 Z" '
                f'fill="#fff" stroke="{LINE}" stroke-width="{1.1 / k:.2f}" stroke-linejoin="round"/>')
    stars = ''.join(f'<path d="M{x} {y - 5} V{y + 5} M{x - 5} {y} H{x + 5}" stroke="{BLUE_L}" stroke-opacity=".6" stroke-linecap="round"/>'
                    for x, y in [(760, 90), (1350, 120), (1300, 470), (820, 520), (60, 120), (640, 40)])
    sc = Scene(0, 0, 16)
    sc.drone(0, 0, 0, 1.4, scan=False)
    drone = f'<g transform="translate(830 330)">{"".join(sc.over)}</g>'
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{orbit}{craters}{stars}'
           f'{cloud(1250, 560, 1.1)}{cloud(1340, 600, .7)}{cloud(-40, 640, 1.3)}{drone}</svg>')
    write('b-sky.svg', svg)


# ------------------------------------------------------------------ Strengths（夜の地形）
def night(w=1440, h=440):
    """FVのワイヤー地形を紺地に反転。上端に山並み（尾根が高いほど明るい）"""
    sc = Scene(720, 84, 18)
    def hf(x, y):
        return (gauss(x, y, 6, 14, 5, 11) + gauss(x, y, 14, 7, 4, 14) + gauss(x, y, 22, 1, 5, 9)
                + gauss(x, y, 0, 21, 4, 8) + gauss(x, y, -7, 27, 5, 12) + gauss(x, y, 30, -6, 4, 10)
                + gauss(x, y, -15, 34, 4, 7) + gauss(x, y, 38, -12, 4, 6) + gauss(x, y, -22, 40, 4, 5))
    def alpha(X, Y):
        return max(0, min(1, (h - Y) / 160))
    mesh(sc, -40, 56, -40, 56, hf, alpha, 1.0, base=.06, zmax=9)
    g = sc.under[0].replace('stroke="rgb(', 'data-c="(').replace('<line ', '<line stroke="#86DCCD" ')
    write('b-night.svg', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMin slice">{g}</svg>')


# ------------------------------------------------------------------ 下層の地面（FV 下〜NEWS）
def ground():
    M = json.load(open(os.path.join(HERE, 'm_b.json')))
    W, H = M['W'], M['H']
    sec = {b['c'].split()[0]: b for b in M['b'] if b['s'] == 'section'}
    parts = []

    def patch(cx, cy, n, hills, fade, props, s=14.5):
        sc = Scene(cx, cy - n * s * .5, s)
        def hf(x, y):
            return sum(gauss(x, y, *hh) for hh in hills)
        def alpha(X, Y):
            return max(0, min(1, 1 - (math.hypot((X - cx) / fade[0], (Y - cy) / fade[1]) - .55) / .45))
        mesh(sc, 0, n, 0, n, hf, alpha)
        props(sc)
        parts.append(''.join(sc.under) + ''.join(t for _, t in sorted(sc.items, key=lambda t: t[0])) + ''.join(sc.over))

    st = sec['statement']; sv = sec['service']; nw = sec['news']; hh = sec['h31b']
    # ① Statement の右：FVの地面が続き、丘の上で測量
    def p1(sc):
        sc.tripod(16, 13, 1.3); sc.person(16.9, 13.6, 1.2, BLUE, arm='hold')
        sc.prism(21, 18, 1.2); sc.person(21.7, 18.4, 1.2, '#fff', vest=YEL)
        sc.add(40, sc.line([(16, 13, 2.3), (21, 18, 3.1)], BLUE_L, .9, ' stroke-dasharray="2 5"'))
        for (x, y, k) in [(10, 22, 'cone'), (11.5, 23, 'cone'), (24, 10, 'round'), (25, 12, 'cone'), (13, 9, 'round')]:
            sc.tree(x, y, .95, 1.5, k)
        sc.drone(12, 16, 9, 1.3)
    patch(1180, st['y'] + st['h'] * .52, 34, ((6, 6, 7, 5), (30, 4, 6, 3.5), (4, 28, 6, 3)), (420, 470), p1)
    # ② Service の左右の余白：木と三角コーン
    def p2(sc):
        for (x, y, k) in [(6, 10, 'cone'), (7.4, 11, 'cone'), (12, 15, 'round'), (9, 18, 'round')]:
            sc.tree(x, y, .95, 1.5, k)
        sc.house(13, 9, 2.6, 2.4, 1.8, 1.1)
    patch(80, sv['y'] - 30, 22, ((4, 4, 6, 4),), (200, 260), p2)
    def p3(sc):
        for (x, y) in [(10, 12), (12.5, 12.5), (15, 13)]:
            sc.cone(x, y, 1.2)
        sc.person(13, 16, 1.2, BLUE, arm='point')
        sc.tree(18, 9, .95, 1.5, 'cone'); sc.tree(8, 18, .95, 1.5)
    patch(1340, sv['y'] + sv['h'] - 220, 24, ((20, 4, 6, 4),), (240, 300), p3)
    # ③ NEWS の下：まちに戻って締める
    def p4(sc):
        sc.box(8, 8, 0, 3, 2.6, 3.4, win=(2, 2)); sc.house(12.5, 9, 2.6, 2.4, 1.8, 1.1, roof=BLUE_P)
        sc.house(8, 12.5, 2.6, 2.4, 1.8, 1.1); sc.box(12.5, 13, 0, 3.2, 2.4, 2.2, win=(1, 2))
        for (x, y, k) in [(6, 15, 'round'), (17, 8, 'cone'), (17.6, 12, 'round'), (10, 17, 'cone')]:
            sc.tree(x, y, .95, 1.5, k)
    patch(260, nw['y'] + nw['h'] - 130, 24, ((2, 2, 6, 4),), (300, 260), p4)

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none">{"".join(parts)}</svg>')
    write('b-ground.svg', svg)


if __name__ == '__main__':
    import sys
    a = sys.argv[1:] or ['town', 'vig', 'sky', 'night', 'ground']
    if 'town' in a: town()
    if 'vig' in a: vig_survey(); vig_design(); vig_management()
    if 'sky' in a: sky()
    if 'night' in a: night()
    if 'ground' in a and os.path.exists(os.path.join(HERE, 'm_b.json')): ground()
