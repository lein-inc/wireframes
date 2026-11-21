#!/usr/bin/env python3
"""v3.1-A の絵（等高線の線画）を img/v31/ に書き出す
  入力: _v3/m_a.json（measure.sh で PC1440 の各ブロック位置を測ったもの）
  出力: a-terrain.svg（FV〜NEWS の背景1枚）/ a-sea.svg（Strengths の等深線）/ a-coast-top.svg・a-coast-bottom.svg
  線のトーンは FV の3Dワイヤー地形を踏襲：グレーの細線、高いところほど青
"""
import json, os, math
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'img', 'v31')
M = json.load(open(os.path.join(HERE, 'm_a.json')))
W, H = M['W'], M['H']
R = 4  # 格子の解像度(px)
rng = np.random.default_rng(1981)


def noise(w, h, scales=((900, 1.0), (420, .5), (190, .25), (90, .1))):
    z = np.zeros((h, w), np.float32)
    for s, a in scales:
        gw, gh = max(2, int(w * R / s) + 3), max(2, int(h * R / s) + 3)
        g = Image.fromarray(rng.standard_normal((gh, gw)).astype(np.float32), 'F')
        z += a * np.asarray(g.resize((w, h), Image.BICUBIC))
    return z


def sec(name):
    return next(b for b in M['b'] if b['s'] == 'section' and b['c'].split()[0] == name)


def blocks():
    keep = ('.h31a__copy', '.statement .wrap > *', '.service .sec-head', '.service .svc-flow', '.svc-card',
            '.service .center-pill', '.founder-grid > *', '.news .sec-head', '.top-news')
    return [b for b in M['b'] if b['s'] in keep]


def p(v):
    return f'{v:.0f}'


def path_d(path):
    d = []
    for verts, code in path.iter_segments(simplify=False):
        x, y = verts[0] * R, verts[1] * R
        d.append(('M' if code == 1 else 'L') + p(x) + ' ' + p(y))
        if code == 79:
            d[-1] = 'Z'
    return ''.join(d)


def smooth(pts, n=10):
    """Catmull-Rom で点列をなめらかに"""
    out = []
    P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                   + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(pts[-1])
    return out


def poly_d(pts):
    return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)


# ---------------------------------------------------------------- terrain
def terrain():
    w, h = W // R, H // R
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) * R
    z = noise(w, h) * 1.15
    # 山：FV右上に大きな山塊、ページ両端に尾根が続く
    def bump(cx, cy, rx, ry, a):
        return a * np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2))
    z += bump(1180, 120, 420, 330, 2.6) + bump(860, -60, 300, 220, 1.6) + bump(1420, 560, 260, 300, 1.4)
    edge = np.minimum(xx, W - xx)
    z += 1.25 * np.exp(-(edge / 170) ** 2) * (0.6 + 0.4 * np.sin(yy / 420 + 1.3))
    # セクションのつなぎ目に地形を横断させる（文字の無い帯）
    for name in ('statement', 'service', 'founder', 'news'):
        s = sec(name)
        z += bump(W * (0.15 if name in ('service', 'news') else 0.85), s['y'] + 40, 520, 120, 0.9)
    fig = plt.figure()
    ax = fig.add_subplot()
    levels = np.arange(-3.0, 6.0, 0.13)
    cs = ax.contour(z, levels=levels)
    lines = []
    for i, (lv, path) in enumerate(zip(cs.levels, cs.get_paths())):
        if len(path.vertices) < 2:
            continue
        t = min(1, max(0, (lv - 0.6) / 2.8))
        # グレー(#8A8A8A)→青(#015B9E)
        c = tuple(int(a + (b - a) * t) for a, b in zip((138, 138, 138), (1, 91, 158)))
        idx = (i % 5 == 0)
        op = (0.5 + 0.4 * t) * (1.3 if idx else 1)
        sw = 1.1 if idx else 0.6
        lines.append(f'<path d="{path_d(path)}" stroke="rgb{c}" stroke-opacity="{min(op, 1):.2f}" stroke-width="{sw}"/>')
    plt.close(fig)

    # 三角点（局所最大）
    peaks = []
    zz = z.copy()
    for _ in range(9):
        iy, ix = np.unravel_index(np.argmax(zz), zz.shape)
        if zz[iy, ix] < 1.2:
            break
        if 70 < ix * R < W - 90 and iy * R > 40:
            peaks.append((ix * R, iy * R, zz[iy, ix]))
        zz[max(0, iy - 70):iy + 70, max(0, ix - 70):ix + 70] = -9
    tri = ''.join(
        f'<g transform="translate({x:.0f} {y:.0f})"><path d="M0 -9 L8 5 L-8 5 Z" fill="#fff" stroke="#015B9E" stroke-width="1.3"/>'
        f'<circle r="1.6" cy="0.5" fill="#015B9E"/><text x="12" y="4" font-size="10.5" fill="#015B9E">{40 + v * 38:.1f}</text></g>'
        for x, y, v in peaks)

    # 川：FV右上 → 蛇行して左へ → 右の余白を下って海（Strengths）へ
    st = sec('strengths')
    river = smooth([(1500, 60), (1290, 250), (1080, 330), (820, 470), (700, 640), (860, 760), (1240, 850),
                    (1380, 1050), (1370, 1500), (1395, 2000), (1365, 2500), (1390, 2900), (1330, st['y'] + 30)], 14)
    rd = poly_d(river)
    # 道路：FV上部を横断し川を橋で渡る
    road = smooth([(-40, 300), (260, 230), (560, 250), (820, 330), (1080, 300), (1300, 380), (1480, 470)], 14)
    od = poly_d(road)
    # 橋の位置（川と道路の交点の近く）
    bi = min(((i, j) for i in range(0, len(road), 2) for j in range(0, len(river), 2)),
             key=lambda ij: math.dist(road[ij[0]], river[ij[1]]))
    bx, by = road[bi[0]]
    a = math.degrees(math.atan2(road[bi[0] + 1][1] - road[bi[0] - 1][1], road[bi[0] + 1][0] - road[bi[0] - 1][0]))
    # 街区（道路沿いの平地）
    city = []
    for k, (cx, cy) in enumerate([(330, 120), (420, 96), (520, 130), (610, 104), (700, 150), (400, 180), (560, 196), (650, 214)]):
        ww, hh = 52 + (k * 17) % 40, 34 + (k * 23) % 26
        city.append(f'<rect x="{cx}" y="{cy}" width="{ww}" height="{hh}" fill="#F7F7F7" stroke="#666" stroke-opacity=".7" stroke-width=".8"/>')
    # 方眼（図郭線）
    grid = ''.join(f'<path d="M{x} 0 V{H}"/>' for x in range(120, W, 240)) + ''.join(f'<path d="M0 {y} H{W}"/>' for y in range(120, H, 240))

    holes = ''.join(f'<rect x="{b["x"]-30}" y="{b["y"]-30}" width="{b["w"]+60}" height="{b["h"]+60}" rx="60"/>' for b in blocks())
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none" font-family="Inter,Arial,sans-serif">
<defs><filter id="f" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="34"/></filter>
<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/><g fill="#333" filter="url(#f)">{holes}</g></mask></defs>
<g stroke="#015B9E" stroke-opacity=".06" stroke-width="1" fill="none">{grid}</g>
<g fill="none" stroke-linejoin="round" stroke-linecap="round" mask="url(#m)">{''.join(lines)}</g>
<g fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path d="{rd}" stroke="#4C88BE" stroke-width="34"/><path d="{rd}" stroke="#EEF5FB" stroke-width="32"/>
  <path d="{rd}" stroke="#4C88BE" stroke-opacity=".45" stroke-width=".8" stroke-dasharray="14 10"/>
  <path d="{od}" stroke="#555" stroke-width="20"/><path d="{od}" stroke="#F2F2F2" stroke-width="18"/>
  <path d="{od}" stroke="#555" stroke-opacity=".5" stroke-width=".8" stroke-dasharray="10 8"/>
</g>
<g transform="translate({bx:.0f} {by:.0f}) rotate({a:.1f})" fill="#F2F2F2" stroke="#555" stroke-width="1">
  <rect x="-46" y="-13" width="92" height="26"/><path d="M-46 -8 H46 M-46 8 H46" fill="none" stroke-opacity=".6"/>
</g>
<g>{''.join(city)}</g>
<g>{tri}</g>
</svg>'''
    open(os.path.join(OUT, 'a-terrain.svg'), 'w').write(svg)
    print('a-terrain.svg', len(svg) // 1024, 'KB', W, H)


# ---------------------------------------------------------------- sea
def sea():
    st = sec('strengths')
    w, h = W // R, st['h'] // R
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32) * R
    z = noise(w, h, ((700, 1.0), (300, .4), (120, .12))) * .5 + (yy / (st['h'])) * 1.6 + 0.6 * np.exp(-((xx - 1150) / 300) ** 2 - ((yy - 200) / 200) ** 2)
    fig = plt.figure(); ax = fig.add_subplot()
    cs = ax.contour(z, levels=np.arange(-1.5, 3.5, 0.16))
    lines = []
    for i, path in enumerate(cs.get_paths()):
        if len(path.vertices) < 2:
            continue
        idx = i % 5 == 0
        lines.append(f'<path d="{path_d(path)}" stroke-opacity="{.32 if idx else .16}" stroke-width="{1 if idx else .6}"/>')
    plt.close(fig)
    labels = ''.join(f'<text x="{x}" y="{y}">-{d:.1f}</text>' for x, y, d in
                     [(1250, 120, 2.4), (1330, 300, 4.8), (90, 640, 7.5), (1180, 780, 9.6), (60, 160, 3.0)])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {st['h']}" preserveAspectRatio="xMidYMid slice">
<g fill="none" stroke="#86DCCD" stroke-linejoin="round">{''.join(lines)}</g>
<g fill="#86DCCD" fill-opacity=".55" font-family="Inter,Arial,sans-serif" font-size="11" letter-spacing="1">{labels}</g>
</svg>'''
    open(os.path.join(OUT, 'a-sea.svg'), 'w').write(svg)
    print('a-sea.svg', len(svg) // 1024, 'KB')


def coast():
    xs = np.linspace(0, W, 120)
    def wave(ph, amp, base):
        return [(x, base + amp * (math.sin(x / 210 + ph) * .7 + math.sin(x / 83 + ph * 2) * .3)) for x in xs]
    for name, flip in (('top', False), ('bottom', True)):
        main = wave(0.4 if not flip else 2.1, 22, 50)
        l1 = wave(0.4 if not flip else 2.1, 22, 30)
        l2 = wave(0.6 if not flip else 2.4, 18, 12)
        fill = poly_d(main) + f' L{W} 92 L0 92 Z'
        g = (f'<path d="{fill}" fill="#013D6A"/>'
             f'<path d="{poly_d(main)}" fill="none" stroke="#4C88BE" stroke-width="1.2"/>'
             f'<path d="{poly_d(l1)}" fill="none" stroke="#4C88BE" stroke-opacity=".45" stroke-width=".8"/>'
             f'<path d="{poly_d(l2)}" fill="none" stroke="#8A8A8A" stroke-opacity=".35" stroke-width=".7"/>')
        if flip:
            g = f'<g transform="translate(0 90) scale(1 -1)">{g}</g>'
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 90" preserveAspectRatio="none">{g}</svg>'
        open(os.path.join(OUT, f'a-coast-{name}.svg'), 'w').write(svg)
    print('coast ok')


if __name__ == '__main__':
    terrain(); sea(); coast()
