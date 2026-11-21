#!/usr/bin/env python3
"""v3.1 TOP の絵（Statement〜NEWS を1枚でつなぐ線画の風景）を img/v31/a-terrain.svg に書き出す
  入力: _v3/m_a.json（measure.sh で PC1440 の各ブロック位置を測ったもの。land31 の左上が原点）
  山  : FV と同じ立体ワイヤー地形（奥の行から手前へ、高さぶん持ち上げた線を引き、行ごとに下側を白で塗って奥を隠す）
  街  : サン防災TOPのイラストのような、道路・街・海辺をアイソメの線画で（白地＋細いグレー線、要所に青）
        道路・川・海岸線・建物・木は「どの行の後に描くか」を決めて地形と一緒に描くので、手前の山に隠れる
  海  : Strengths の背景は入り江（淡い水色の面＋横線の波）。瀬戸大橋のような吊り橋が渡る
  ひとつ前（山だけのワイヤー版）は _v3/bk_v31a_wire/
"""
import json, os, math
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'img', 'v31')
M = json.load(open(os.path.join(HERE, 'm_a.json')))
W, H = M['W'], M['H']
rng = np.random.default_rng(1981)

DX, DY, K = 16, 18, 74       # 横の刻み / 行の間隔 / 高さ1あたりの持ち上げ(px)
# map  … 真上から見た等高線の地図（11/11 初版の平面トーン）に、アイソメの線画の街・道路を置く（いまの採用）
# wire … 山を立体ワイヤー地形で描く版（V31_MODE=wire python3 v31_art_a.py で書き出し可）
MODE = os.environ.get('V31_MODE', 'map')
KD = 0 if MODE == 'map' else K   # 地面の持ち上げ（地図では0）
GRAY, MID, BLUE = (150, 156, 162), (76, 136, 190), (1, 91, 158)
INK = '#5E6B78'              # 街の線
INK_B = '#015B9E'
WATER = '#F1F7FC'
FLAT = 0.06                  # 街・道路の地面の高さ


def noise(w, h, step, scales):
    z = np.zeros((h, w), np.float32)
    for s, a in scales:
        gw, gh = max(2, int(w * step / s) + 3), max(2, int(h * step / s) + 3)
        g = Image.fromarray(rng.standard_normal((gh, gw)).astype(np.float32), 'F')
        z += a * np.asarray(g.resize((w, h), Image.BICUBIC))
    return z


def sec(name):
    return next(b for b in M['b'] if b['s'] == 'section' and b['c'].split()[0] == name)


def one(sel):
    return next(b for b in M['b'] if b['s'] == sel)


def blocks():
    keep = ('.statement .wrap > *', '.service .sec-head', '.service .svc-flow', '.svc-card', '.service .center-pill',
            '.strengths .sec-head', '.str-grid', '.strengths .center-pill', '.founder-grid > *',
            '.rec-txt', '.rec-photo', '.news .sec-head', '.top-news')
    return [b for b in M['b'] if b['s'] in keep]


def pin_tips():
    return [(b['x'] + b['w'] / 2, b['y'] + 160) for b in M['b'] if b['s'] == '.mpin']


def f(v):
    return f'{v:.0f}' if abs(v - round(v)) < .05 else f'{v:.1f}'


def spline(pts, step=6):
    """Catmull-Rom で滑らかにして step px ごとの点列に"""
    P_ = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P_) - 2):
        p0, p1, p2, p3 = map(lambda q: np.array(q, float), P_[i - 1:i + 3])
        m = max(2, int(np.hypot(*(p2 - p1)) / step))
        for t in np.linspace(0, 1, m, endpoint=False):
            out.append(.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(np.array(pts[-1], float))
    return np.array(out)


# ================================================================ レイアウト（m_a.json 基準）
SEA_T0 = sec('strengths')['y'] - 110          # 入り江の上の岸
SEA_B0 = sec('strengths')['y'] + sec('strengths')['h'] - 40
def coast_top(u):
    return SEA_T0 + 34 * np.sin(u / 230 + .6) + 16 * np.sin(u / 97 + 2) + 60 * np.exp(-((u - 1250) / 160) ** 2)
def coast_bot(u):
    return SEA_B0 + 30 * np.sin(u / 260 + 2.4) + 14 * np.sin(u / 83) - 30 * np.exp(-((u - 260) / 180) ** 2)

y_svc = one('.service .sec-head')['y']
y_pill = one('.service .center-pill')['y'] + 62
fg = [b for b in M['b'] if b['s'] == '.founder-grid > *']
y_fd = min(b['y'] for b in fg); y_fd_end = max(b['y'] + b['h'] for b in fg)
ps = one('.people-strip')
rt, rp_ = one('.rec-txt'), one('.rec-photo')
y_rec_end = max(rt['y'] + rt['h'], rp_['y'] + rp_['h'])
y_news = one('.top-news')['y']; y_news_end = y_news + one('.top-news')['h']

ISLANDS = [(1120, SEA_T0 + 190, 170, 58, 1.0), (330, SEA_T0 + 165, 120, 44, .8), (1370, SEA_B0 - 250, 70, 40, .6)]  # 中心u,v, 半径u,v, 高さ

RIVER = [(1310, -20), (1250, 260), (1370, 520), (1330, 860), (1385, 1150), (1350, 1600), (1395, 2100), (1340, SEA_T0 + 60)]

ROADS = [
    # Statement の下：左端から街を抜け、川を渡って右へ
    [(-30, 960), (180, 1000), (420, 1090), (700, 1110), (960, 1060), (1180, 1120), (1470, 1160)],
    # 左の余白を下る峠道（Statement の下の街 → 港）
    [(170, 1000), (100, 1180), (60, 1450), (110, 1750), (66, 2050), (104, 2350), (70, 2560), (150, SEA_T0 - 70)],
    # 港の通り（入り江の上の岸ぞい）
    [(-30, SEA_T0 - 60), (300, SEA_T0 - 75), (640, SEA_T0 - 50), (980, SEA_T0 - 80), (1240, SEA_T0 - 40), (1470, SEA_T0 - 70)],
    # 入り江の下の岸ぞい
    [(-30, SEA_B0 + 110), (360, SEA_B0 + 90), (760, SEA_B0 + 120), (1120, SEA_B0 + 85), (1470, SEA_B0 + 105)],
    # 右の余白を下る道（下の岸 → 社員写真の帯）
    [(1300, SEA_B0 + 90), (1370, SEA_B0 + 300), (1340, y_fd + 200), (1390, y_fd_end), (1360, ps['y'] - 10)],
    # 採用の右 → 採用の下を横切る
    [(1360, ps['y'] + ps['h'] + 10), (1395, rt['y'] + 200), (1350, y_rec_end), (1200, y_rec_end + 120), (800, y_rec_end + 150), (400, y_rec_end + 110), (-30, y_rec_end + 140)],
    # 左の余白（採用の下 → ニュースの下）
    [(120, y_rec_end + 120), (70, y_news + 150), (110, y_news_end + 60), (260, y_news_end + 170)],
    # いちばん下の街の通り
    [(-30, H - 230), (260, H - 200), (620, H - 245), (980, H - 195), (1260, H - 240), (1470, H - 210)],
]

# 鉄道（入り江の下の街を横切る）
RAIL = [(-30, SEA_B0 + 250), (300, SEA_B0 + 230), (700, SEA_B0 + 265), (1100, SEA_B0 + 225), (1470, SEA_B0 + 250)]
STATION = (520, SEA_B0 + 250)

# 街（範囲 u0,u1,v0,v1 と建物の数）
TOWNS = [
    (190, 1290, y_svc - 330, y_svc - 50, 26),          # Statement の下
    (170, 1250, y_pill + 20, SEA_T0 - 20, 16),         # 港
    (160, 1280, SEA_B0 + 40, y_fd - 20, 22),           # 入り江の下〜Founder の上
    (180, 1260, y_rec_end + 20, y_news - 10, 12),      # 採用の下
    (160, 1300, y_news_end + 40, H - 30, 30),          # いちばん下
]


def mindist(uu, vv, line):
    d = np.full(uu.shape, 1e9, np.float32)
    for x, y in line[::2]:
        d = np.minimum(d, np.hypot(uu - x, vv - y))
    return d


# ================================================================ 高さ
n, rows = W // DX + 2, H // DY + 2
VV, UU = np.mgrid[0:rows, 0:n].astype(np.float32)
UU *= DX; VV *= DY
z = noise(n, rows, DX, ((700, .75), (300, .35), (120, .08)))


def bump(cx, cy, rx, ry, a):
    return a * np.exp(-(((UU - cx) / rx) ** 2 + ((VV - cy) / ry) ** 2))


calm = np.zeros_like(z)
for b in blocks():
    x0, y0, x1, y1 = b['x'] - 40, b['y'] - 30, b['x'] + b['w'] + 40, b['y'] + b['h'] + 150
    ddx = np.maximum(np.maximum(x0 - UU, UU - x1), 0); ddy = np.maximum(np.maximum(y0 - VV, VV - y1), 0)
    calm = np.maximum(calm, np.exp(-(np.hypot(ddx, ddy) / 60) ** 2))
z = z * (1 - .8 * calm)
for side in (0, 1):            # 両端の山：連続した尾根にせず、間をあけた山の塊に（等高線が縦に詰まらない）
    for v0 in np.arange(-150, H + 300, 520):
        cu = rng.uniform(10, 110) if side == 0 else W - rng.uniform(10, 110)
        z += bump(cu, v0 + rng.uniform(-140, 140), rng.uniform(260, 340), rng.uniform(220, 300), rng.uniform(.3, .55)) * (1 - .6 * calm)
for (px, py), a in zip(pin_tips(), (2.6, 2.1, 2.3, 1.8)):
    z += bump(px, py + a * KD, 150, 120, a)
for cx, cy, a in ((W * .5, y_fd_end + 60, 1.1), (W * .25, ps['y'] - 60, .9), (W * .8, y_rec_end + 40, .8)):
    z += bump(cx, cy, 380, 80, a)

# 道路・街は平らに（街の外へなだらかに）
road_pts = [spline(r) for r in ROADS]
river_pts = spline(RIVER, 8)
flat = np.zeros_like(z)
rail_pts = spline(RAIL)
for rp in road_pts + [rail_pts]:
    flat = np.maximum(flat, np.exp(-(mindist(UU, VV, rp) / 70) ** 2))
for u0, u1, v0, v1, _ in TOWNS:
    ddx = np.maximum(np.maximum(u0 - UU, UU - u1), 0); ddy = np.maximum(np.maximum(v0 - VV, VV - v1), 0)
    flat = np.maximum(flat, np.exp(-(np.hypot(ddx, ddy) / 80) ** 2))
z = z * (1 - flat) + FLAT * flat
# 川筋は谷
dr = mindist(UU, VV, river_pts)
z -= .9 * np.exp(-(dr / 60) ** 2) * (1 - .5 * flat)
z = np.maximum(z, -0.5)
# 入り江：岸の間は海面（ゆるい波）、岸の近くはなだらかに
ct, cb = coast_top(UU), coast_bot(UU)
water = (VV > ct) & (VV < cb)
isl = np.zeros_like(z)
for cu, cv, ru, rv_, a in ISLANDS:
    q = ((UU - cu) / ru) ** 2 + ((VV - cv) / rv_) ** 2
    water &= q > 1
    isl = np.maximum(isl, np.where(q < 1, a * (1 - q) ** 1.3 + .05, 0))
dsea = np.minimum(np.abs(VV - ct), np.abs(VV - cb))
shore = np.exp(-(dsea / 90) ** 2)
z = np.where(water, 0.04 * np.sin(UU / 60 + VV / 25), np.where(isl > 0, isl, z * (1 - shore) + FLAT * shore)).astype(np.float32)


def gz(u, v):
    r, c = np.clip(v / DY, 0, rows - 1.001), np.clip(u / DX, 0, n - 1.001)
    r0, c0 = int(r), int(c); fr, fc = r - r0, c - c0
    return ((z[r0, c0] * (1 - fc) + z[r0, c0 + 1] * fc) * (1 - fr) + (z[r0 + 1, c0] * (1 - fc) + z[r0 + 1, c0 + 1] * fc) * fr)


def P(u, v):
    return u, v - gz(u, v) * KD


def row_of(v):
    return int(min(rows - 1, max(0, math.ceil(v / DY))))


def is_water(u, v):
    return bool(water[row_of(v), int(min(n - 1, max(0, u / DX)))])


labels = []                    # 等高線の数字・図郭の座標など（文字は一番上に）
LAYER = {}                     # 行番号 → 描く SVG（地形の行のあとに描く）
def put(v, s, pri=1):
    LAYER.setdefault(row_of(v), []).append((pri, v, s))


# ================================================================ 地面に描く線（道路・川・海岸）
def ribbon(pts, half, fill, edge, ew=1.1, center=None, pri=0, curb=False):
    if MODE == 'map':
        d = 'M' + 'L'.join(f'{f(u)} {f(v)}' for u, v in pts)
        s = f'<path d="{d}" stroke="{edge}" stroke-width="{2 * half + 2 * ew}"/><path d="{d}" stroke="{fill}" stroke-width="{2 * half}"/>'
        if curb:      # 歩道の縁石
            s += f'<path d="{d}" stroke="#C3CBD3" stroke-width="{2 * half - 5}"/><path d="{d}" stroke="{fill}" stroke-width="{2 * half - 6.2}"/>'
        if center:
            s += f'<path d="{d}" stroke="{center}" stroke-width=".9" stroke-dasharray="9 7"/>'
        put(-1, s, pri)
        return
    for k in range(len(pts) - 1):
        (u0, v0), (u1, v1) = pts[k], pts[k + 1]
        du, dv = u1 - u0, v1 - v0; L = math.hypot(du, dv) or 1
        nu, nv = -dv / L * half, du / L * half
        a, b = P(u0 + nu, v0 + nv), P(u1 + nu, v1 + nv)
        c, d = P(u1 - nu, v1 - nv), P(u0 - nu, v0 - nv)
        s = (f'<path d="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}L{f(c[0])} {f(c[1])}L{f(d[0])} {f(d[1])}Z" fill="{fill}" stroke="{fill}" stroke-width=".6"/>'
             f'<path d="M{f(a[0])} {f(a[1])}L{f(b[0])} {f(b[1])}M{f(d[0])} {f(d[1])}L{f(c[0])} {f(c[1])}" stroke="{edge}" stroke-width="{ew}"/>')
        if center and k % 4 < 2:
            p, q = P(u0, v0), P(u1, v1)
            s += f'<path d="M{f(p[0])} {f(p[1])}L{f(q[0])} {f(q[1])}" stroke="{center}" stroke-width=".9"/>'
        put(max(v0, v1) + abs(nv), s, pri)


def ground_line(pts, color, w=1, op=1, dash=None, pri=0):
    da = f' stroke-dasharray="{dash}"' if dash else ''
    if MODE == 'map':
        put(-1, f'<path d="M{"L".join(f"{f(u)} {f(v)}" for u, v in pts)}" stroke="{color}" stroke-width="{w}" stroke-opacity="{op}"{da}/>', pri)
        return
    for k in range(len(pts) - 1):
        p, q = P(*pts[k]), P(*pts[k + 1])
        put(max(pts[k][1], pts[k + 1][1]), f'<path d="M{f(p[0])} {f(p[1])}L{f(q[0])} {f(q[1])}" stroke="{color}" stroke-width="{w}" stroke-opacity="{op}"{da}/>', pri)


# 川
rv = river_pts[river_pts[:, 1] < SEA_T0 + 70]
ribbon(rv, 12, '#EEF5FB', '#4C88BE', 1.1, pri=0)
ground_line(rv, '#4C88BE', .8, .45, '14 10', pri=0)
# 海岸（岸の線＋砂浜の点線）
us = np.arange(-10, W + 20, 10.0)
for fn, sgn in ((coast_top, -1), (coast_bot, 1)):
    ground_line(np.c_[us, fn(us)], '#4C88BE', 1.3, 1, pri=0)
    ground_line(np.c_[us, fn(us) + sgn * 12], INK, .8, .5, '2 6', pri=0)
for cu, cv, ru, rv_, a in ISLANDS:
    th = np.linspace(0, 2 * np.pi, 90)
    ground_line(np.c_[cu + ru * np.cos(th), cv + rv_ * np.sin(th)], '#4C88BE', 1.2, 1, pri=0)
    ground_line(np.c_[cu + (ru + 12) * np.cos(th), cv + (rv_ + 8) * np.sin(th)], '#4C88BE', .7, .35, '3 6', pri=0)
# 道路（街なかは歩道つき）
for k, rp in enumerate(road_pts):
    ribbon(rp, 12 if k in (1, 4, 6) else 15, '#fff', INK, 1.1, center='#9AA6B2', pri=0, curb=k not in (1, 4, 6))
# 鉄道（JRの白黒の帯）＋枕木
if MODE == 'map':
    d = 'M' + 'L'.join(f'{f(u)} {f(v)}' for u, v in rail_pts)
    put(-1, f'<path d="{d}" stroke="#fff" stroke-width="16"/><path d="{d}" stroke="{INK}" stroke-width="5.2"/>'
            f'<path d="{d}" stroke="#fff" stroke-width="3" stroke-dasharray="14 14" stroke-linecap="butt"/>', 0)



# ================================================================ アイソメの線画パーツ
RX, RY = .866, .5             # 右奥へ（x, -y）
def iso(px, py, a, b, h):
    """手前の角 (px,py) から右奥へ a、左奥へ b、上へ h"""
    return px + RX * a - RX * b, py - RY * a - RY * b - h


def pts_d(ps_, close=True):
    return 'M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in ps_) + ('Z' if close else '')


def hull(pts):
    pts = sorted(set((round(x, 1), round(y, 1)) for x, y in pts))
    def half(seq):
        h_ = []
        for q in seq:
            while len(h_) >= 2 and (h_[-1][0] - h_[-2][0]) * (q[1] - h_[-2][1]) - (h_[-1][1] - h_[-2][1]) * (q[0] - h_[-2][0]) <= 0:
                h_.pop()
            h_.append(q)
        return h_
    lo, up_ = half(pts), half(pts[::-1])
    return lo[:-1] + up_[:-1]


def building(u, v, a, b, h, roof='flat', win=True, accent=False):
    cx, cy = P(u, v)
    px, py = cx - (RX * a - RX * b) / 2, cy + (RY * a + RY * b) / 2      # 足もとの中心 → 手前の角
    A = (px, py); Ar = iso(px, py, a, 0, 0); Al = iso(px, py, 0, b, 0)
    T = iso(px, py, 0, 0, h); Tr = iso(px, py, a, 0, h); Tl = iso(px, py, 0, b, h); Tb = iso(px, py, a, b, h)
    lc = INK_B if accent else INK
    # 影（光は右奥から：左手前へ落ちる・ハッチング）
    sv = (-h * .62, h * .26)
    Bk = iso(px, py, a, b, 0)
    foot = [A, Ar, Bk, Al]
    put(v, f'<path d="{pts_d(hull(foot + [(x + sv[0], y + sv[1]) for x, y in foot]))}" fill="url(#hs)" stroke="none"/>', 1.5)
    s = [f'<g stroke="{lc}" stroke-width="1.05" stroke-linejoin="round">']
    s.append(f'<path d="{pts_d([A, Ar, Tr, T])}" fill="url(#hf)"/>')       # 右の面（ハッチングの陰）
    s.append(f'<path d="{pts_d([A, Al, Tl, T])}" fill="#fff"/>')           # 左の面
    if roof == 'flat' and h > 34:  # 各階の線（左の面）
        for t0 in np.arange(16, h - 6, 16):
            s.append(f'<path d="{pts_d([iso(px, py, 0, 0, t0), iso(px, py, 0, b, t0)], False)}" stroke-width=".6" stroke-opacity=".55"/>')
    if roof == 'flat':
        s.append(f'<path d="{pts_d([T, Tr, Tb, Tl])}" fill="#fff"/>')
        s.append(f'<path d="{pts_d([iso(px, py, 3, 3, h), iso(px, py, a - 3, 3, h), iso(px, py, a - 3, b - 3, h), iso(px, py, 3, b - 3, h)])}" stroke-opacity=".5"/>')
        if a > 30:                 # 屋上の設備
            ua, ub, uh = a * .3, b * .35, 6
            o = iso(px, py, a * .45, b * .3, h)
            s.append(f'<path d="{pts_d([o, iso(*o, ua, 0, 0), iso(*o, ua, 0, uh), iso(*o, 0, 0, uh)])}" fill="url(#hf)" stroke-width=".8"/>'
                     f'<path d="{pts_d([o, iso(*o, 0, ub, 0), iso(*o, 0, ub, uh), iso(*o, 0, 0, uh)])}" fill="#fff" stroke-width=".8"/>'
                     f'<path d="{pts_d([iso(*o, 0, 0, uh), iso(*o, ua, 0, uh), iso(*o, ua, ub, uh), iso(*o, 0, ub, uh)])}" fill="#fff" stroke-width=".8"/>')
    else:  # 切妻（棟は右奥方向）
        rh = min(a, b) * .45
        R0 = iso(px, py, 0, b / 2, h + rh); R1 = iso(px, py, a, b / 2, h + rh)
        rf = '#DCEAF5' if accent else '#EDF2F6'
        s.append(f'<path d="{pts_d([R0, R1, Tb, Tl])}" fill="{rf}"/>')
        s.append(f'<path d="{pts_d([T, Tl, R0])}" fill="#fff"/>')
        s.append(f'<path d="{pts_d([T, Tr, R1, R0])}" fill="{rf}"/>')
        for k in range(1, 5):      # 瓦の筋
            q0 = iso(*T, a * k / 5, 0, 0); q1 = iso(*R0, a * k / 5, 0, 0)
            s.append(f'<path d="{pts_d([q0, q1], False)}" stroke-width=".55" stroke-opacity=".5"/>')
    if win:
        nx = max(1, int(a // 13)); ny = max(1, int((h - 8) // 16))
        for i in range(nx):
            for j in range(ny):
                s0, t0 = (i + .5) * a / nx - 2.6, 6 + j * (h - 8) / ny
                q = [iso(px, py, s0, 0, t0), iso(px, py, s0 + 5.2, 0, t0), iso(px, py, s0 + 5.2, 0, t0 + 8), iso(px, py, s0, 0, t0 + 8)]
                s.append(f'<path d="{pts_d(q)}" fill="#fff" stroke-width=".8"/>')
        if h > 16:
            d0 = b * .45
            q = [iso(px, py, 0, d0, 0), iso(px, py, 0, d0 + 7, 0), iso(px, py, 0, d0 + 7, 13), iso(px, py, 0, d0, 13)]
            s.append(f'<path d="{pts_d(q)}" fill="#E3EEF7" stroke-width=".8"/>')
    s.append('</g>')
    put(v, ''.join(s), 2)


def tree(u, v, kind=0, sc=1.0):
    x, y = P(u, v)
    sh = f'<ellipse cx="{f(x - 7 * sc)}" cy="{f(y + 1)}" rx="{f(10 * sc)}" ry="{f(3.6 * sc)}" fill="url(#hs)"/>'
    if kind == 0:   # 広葉樹：もこもこの樹冠
        r = 9.5 * sc; cy = y - 9 * sc - r
        lob = 7; pts = [(x + r * math.cos(2 * math.pi * k / lob - 1.2), cy + r * math.sin(2 * math.pi * k / lob - 1.2)) for k in range(lob)]
        d = f'M{f(pts[0][0])} {f(pts[0][1])}' + ''.join(f'A{f(r * .48)} {f(r * .48)} 0 0 1 {f(pts[(k + 1) % lob][0])} {f(pts[(k + 1) % lob][1])}' for k in range(lob))
        s = (sh + f'<path d="M{f(x)} {f(y)}V{f(cy + r * .3)}M{f(x)} {f(cy + r * .55)}l{f(r * .3)} -{f(r * .3)}" stroke="{INK}" stroke-width="1"/>'
             f'<path d="{d}Z" fill="#EEF6F2" stroke="{INK}" stroke-width="1"/>'
             f'<path d="M{f(x + r * .1)} {f(cy + r * .55)}A{f(r * .55)} {f(r * .55)} 0 0 0 {f(x + r * .62)} {f(cy - r * .05)}" stroke="{INK}" stroke-width=".7" stroke-opacity=".55"/>')
    else:           # とがった木
        tp, bt = y - 34 * sc, y - 6 * sc
        s = (sh + f'<path d="M{f(x)} {f(y)}V{f(bt)}" stroke="{INK}" stroke-width="1"/>'
             f'<path d="M{f(x)} {f(tp)}L{f(x + 4.5 * sc)} {f(tp + 11 * sc)}L{f(x + 2.5 * sc)} {f(tp + 11 * sc)}L{f(x + 8 * sc)} {f(bt)}L{f(x - 8 * sc)} {f(bt)}L{f(x - 2.5 * sc)} {f(tp + 11 * sc)}L{f(x - 4.5 * sc)} {f(tp + 11 * sc)}Z" fill="#E6F1EC" stroke="{INK}" stroke-width="1"/>'
             f'<path d="M{f(x)} {f(tp + 4 * sc)}V{f(bt - 2)}" stroke="{INK}" stroke-width=".6" stroke-opacity=".5"/>')
    put(v, s, 3)


def turbine(u, v, hgt=86, ang=20):
    x, y = P(u, v); hx, hy = x, y - hgt
    s = [f'<path d="M{f(x - 2)} {f(y)}L{f(hx - .8)} {f(hy)}M{f(x + 2)} {f(y)}L{f(hx + .8)} {f(hy)}" stroke="{INK}" stroke-width="1"/>']
    for k in range(3):
        t = math.radians(ang + k * 120)
        ex, ey = hx + 34 * math.cos(t), hy + 34 * math.sin(t)
        nx, ny = -math.sin(t) * 3.2, math.cos(t) * 3.2
        s.append(f'<path d="M{f(hx)} {f(hy)}L{f(ex)} {f(ey)}L{f(hx + 10 * math.cos(t) + nx)} {f(hy + 10 * math.sin(t) + ny)}Z" fill="#fff" stroke="{INK}" stroke-width=".9"/>')
    s.append(f'<circle cx="{f(hx)}" cy="{f(hy)}" r="2.4" fill="#fff" stroke="{INK}"/>')
    put(v, ''.join(s), 3)


def surveyor(u, v, flip=1):
    """三脚の測量機と、のぞく人（ヘルメットは青）"""
    x, y = P(u, v)
    tx = x + 14 * flip
    s = (f'<g stroke="{INK}" stroke-width="1" fill="#fff">'
         f'<path d="M{f(tx)} {f(y - 18)}L{f(tx - 6)} {f(y)}M{f(tx)} {f(y - 18)}L{f(tx + 6)} {f(y)}M{f(tx)} {f(y - 18)}L{f(tx + 1)} {f(y + 2)}" fill="none"/>'
         f'<path d="M{f(tx - 4)} {f(y - 18)}h8v-8h-8Z" fill="#FFD84D"/>'
         f'<path d="M{f(x - 3)} {f(y)}L{f(x - 2)} {f(y - 12)}M{f(x + 3)} {f(y)}L{f(x + 2)} {f(y - 12)}" fill="none"/>'
         f'<path d="M{f(x - 5)} {f(y - 11)}L{f(x - 4)} {f(y - 24)}L{f(x + 4)} {f(y - 24)}L{f(x + 5)} {f(y - 11)}Z" fill="#E3EEF7"/>'
         f'<path d="M{f(x + 3 * flip)} {f(y - 21)}L{f(tx - 3 * flip)} {f(y - 22)}" fill="none"/>'
         f'<circle cx="{f(x)}" cy="{f(y - 29)}" r="4.2"/>'
         f'<path d="M{f(x - 5)} {f(y - 30)}a5 5 0 0 1 10 0Z" fill="{INK_B}" stroke="{INK_B}"/></g>')
    put(v, s, 4)


def person(u, v, c='#E3EEF7'):
    x, y = P(u, v)
    s = (f'<g stroke="{INK}" stroke-width="1" fill="#fff">'
         f'<path d="M{f(x - 3)} {f(y)}L{f(x - 1.5)} {f(y - 11)}M{f(x + 3)} {f(y)}L{f(x + 1.5)} {f(y - 11)}" fill="none"/>'
         f'<path d="M{f(x - 4.5)} {f(y - 10)}L{f(x - 3.5)} {f(y - 22)}L{f(x + 3.5)} {f(y - 22)}L{f(x + 4.5)} {f(y - 10)}Z" fill="{c}"/>'
         f'<circle cx="{f(x)}" cy="{f(y - 26.5)}" r="4"/></g>')
    put(v, s, 4)


def car(u, v, dirn=1, accent=False):
    x, y = P(u, v)
    a, b, h = 22, 11, 8
    px, py = x - (RX * a - RX * b) / 2 * dirn, y + 4
    def J(s_, t_, hh):
        X, Y = iso(0, 0, s_, t_, hh)
        return px + X * dirn, py + Y
    body = [J(0, 0, 0), J(a, 0, 0), J(a, 0, h), J(0, 0, h)]
    side = [J(0, 0, 0), J(0, b, 0), J(0, b, h), J(0, 0, h)]
    top = [J(0, 0, h), J(a, 0, h), J(a, b, h), J(0, b, h)]
    cab = [J(5, 0, h), J(15, 0, h), J(14, 0, h + 6), J(7, 0, h + 6)]
    cabt = [J(7, 0, h + 6), J(14, 0, h + 6), J(14, b, h + 6), J(7, b, h + 6)]
    fill = '#DCEAF5' if accent else '#fff'
    w1, w2 = J(5, 0, 0), J(17, 0, 0)
    s = (f'<g stroke="{INK}" stroke-width="1" stroke-linejoin="round">'
         f'<path d="{pts_d(top)}" fill="{fill}"/><path d="{pts_d(side)}" fill="#fff"/><path d="{pts_d(body)}" fill="{fill}"/>'
         f'<path d="{pts_d(cab)}" fill="#fff"/><path d="{pts_d(cabt)}" fill="{fill}"/>'
         f'<circle cx="{f(w1[0])}" cy="{f(w1[1])}" r="2.6" fill="#fff"/><circle cx="{f(w2[0])}" cy="{f(w2[1])}" r="2.6" fill="#fff"/></g>')
    put(v + 2, s, 4)


def boat(x, y, L=46, flip=1):
    s = (f'<g stroke="{INK}" stroke-width="1" stroke-linejoin="round" fill="#fff" transform="translate({f(x)} {f(y)}) scale({flip} 1)">'
         f'<path d="M{-L / 2} -8H{L / 2}L{L / 2 - 8} 2H{-L / 2 + 5}Z"/>'
         f'<path d="M{-L / 2 + 8} -8V-17H{-L / 2 + 22}V-8" fill="#E3EEF7"/>'
         f'<path d="M{-L / 2 - 14} 4H{-L / 2 - 2}M{L / 2 + 2} 5H{L / 2 + 22}" fill="none" stroke="#4C88BE" stroke-opacity=".6"/></g>')
    put(y + 1, s, 3)


def crane(u, v):
    x, y = P(u, v)
    s = (f'<g stroke="{INK_B}" stroke-width="1" fill="none" stroke-linejoin="round">'
         f'<path d="M{f(x - 8)} {f(y)}L{f(x - 4)} {f(y - 70)}M{f(x + 8)} {f(y)}L{f(x + 4)} {f(y - 70)}M{f(x - 7)} {f(y - 15)}L{f(x + 7)} {f(y - 15)}M{f(x - 6)} {f(y - 35)}L{f(x + 6)} {f(y - 35)}M{f(x - 5)} {f(y - 55)}L{f(x + 5)} {f(y - 55)}"/>'
         f'<path d="M{f(x - 12)} {f(y - 70)}H{f(x + 62)}M{f(x + 52)} {f(y - 70)}V{f(y - 40)}"/>'
         f'<path d="M{f(x + 47)} {f(y - 40)}h10v8h-10Z" fill="#fff"/></g>')
    put(v, s, 3)


def school(u, v):
    building(u, v, 110, 34, 40, 'flat', accent=True)
    x, y = P(u, v)
    put(v, f'<circle cx="{f(x - 6)}" cy="{f(y - 50)}" r="6" fill="#fff" stroke="{INK_B}"/><path d="M{f(x - 6)} {f(y - 50)}V{f(y - 54)}M{f(x - 6)} {f(y - 50)}H{f(x - 3)}" stroke="{INK_B}"/>', 3)


def lighthouse(u, v):
    x, y = P(u, v)
    s = (f'<g stroke="{INK_B}" stroke-width="1.1" fill="#fff" stroke-linejoin="round">'
         f'<path d="M{f(x - 8)} {f(y)}L{f(x - 5)} {f(y - 46)}H{f(x + 5)}L{f(x + 8)} {f(y)}Z"/>'
         f'<path d="M{f(x - 7)} {f(y - 16)}H{f(x + 7)}M{f(x - 6)} {f(y - 31)}H{f(x + 6)}" stroke-width=".8"/>'
         f'<path d="M{f(x - 7)} {f(y - 46)}H{f(x + 7)}V{f(y - 50)}H{f(x - 7)}Z"/>'
         f'<path d="M{f(x - 4)} {f(y - 50)}V{f(y - 58)}H{f(x + 4)}V{f(y - 50)}" fill="#FFF3C4"/>'
         f'<path d="M{f(x - 5)} {f(y - 58)}L{f(x)} {f(y - 63)}L{f(x + 5)} {f(y - 58)}Z" fill="#DCEAF5"/>'
         f'<path d="M{f(x - 10)} {f(y - 54)}H{f(x - 26)}M{f(x + 10)} {f(y - 54)}H{f(x + 26)}" stroke-dasharray="3 4" stroke-width=".8"/></g>')
    put(v, s, 4)


def bridge_seto(v_deck):
    """入り江の下寄りを横切る吊り橋（主塔2本＋ケーブル＋ハンガー）"""
    t1, t2, top = 250, 1190, 128
    y0 = P(W / 2, v_deck)[1]
    s = [f'<g stroke="{INK}" fill="none" stroke-linejoin="round">']
    s.append(f'<path d="M-10 {f(y0 + 7)}H{W + 10}V{f(y0)}H-10Z" fill="#fff" stroke-width="1.1"/>')
    for x in range(-10, W + 10, 14):
        s.append(f'<path d="M{x} {f(y0)}L{x + 7} {f(y0 + 7)}" stroke-width=".6" stroke-opacity=".6"/>')
    for tx in (t1, t2):
        s.append(f'<path d="M{tx - 7} {f(y0 + 26)}V{f(y0 - top)}M{tx + 7} {f(y0 + 26)}V{f(y0 - top)}M{tx - 7} {f(y0 - top + 4)}H{tx + 7}M{tx - 7} {f(y0 - top / 2)}H{tx + 7}" stroke="{INK_B}" stroke-width="1.3"/>')
        s.append(f'<path d="M{tx - 12} {f(y0 + 26)}H{tx + 12}" stroke-width="1"/>')
    def cable(xa, xb, ya, yb, sag):
        return [(xa + (xb - xa) * t, ya + (yb - ya) * t + sag * 4 * t * (1 - t)) for t in np.linspace(0, 1, 40)]
    for sp in (cable(-40, t1, y0 - 6, y0 - top, 22), cable(t1, t2, y0 - top, y0 - top, top - 12), cable(t2, W + 40, y0 - top, y0 - 6, 22)):
        s.append(f'<path d="{pts_d(sp, False)}" stroke="{INK_B}" stroke-width="1.2"/>')
        for x, y in sp[2:-2:2]:
            if 0 < x < W:
                s.append(f'<path d="M{f(x)} {f(y)}V{f(y0)}" stroke-width=".55" stroke-opacity=".7"/>')
    s.append('</g>')
    s.append(dim(t1, t2, y0 + 44, 'L = 940.0 m（中央径間）'))
    put(v_deck + 30, ''.join(s), 5)


def dim(x0, x1, y, label):
    """建築図面の寸法線（両端の引出し線＋斜めの止め＋数値）"""
    c = INK_B
    return (f'<g stroke="{c}" stroke-width=".8" fill="none"><path d="M{f(x0)} {f(y - 30)}V{f(y + 6)}M{f(x1)} {f(y - 30)}V{f(y + 6)}M{f(x0)} {f(y)}H{f(x1)}"/>'
            f'<path d="M{f(x0 - 4)} {f(y + 4)}l8 -8M{f(x1 - 4)} {f(y + 4)}l8 -8" stroke-width="1.3"/></g>'
            f'<text x="{f((x0 + x1) / 2)}" y="{f(y - 6)}" text-anchor="middle" font-size="11" letter-spacing="1.5" fill="{c}" stroke="#fff" stroke-width="4" paint-order="stroke">{label}</text>')


# ================================================================ 配置
blk = [(b['x'] - 30, b['y'] - 30, b['x'] + b['w'] + 30, b['y'] + b['h'] + 10) for b in blocks()]
blk += [(b['x'] - 10, b['y'] - 10, b['x'] + b['w'] + 10, b['y'] + 190) for b in M['b'] if b['s'] == '.mpin']
blk.append((0, ps['y'] - 20, W, ps['y'] + ps['h'] + 20))


def in_block(u, y, pad=0):
    return any(x0 - pad < u < x1 + pad and y0 - pad < y < y1 + pad for x0, y0, x1, y1 in blk)


def road_d(u, v):
    return min(np.min(np.hypot(rp[:, 0] - u, rp[:, 1] - v)) for rp in road_pts + [rail_pts])


def river_d(u, v):
    return abs(u - np.interp(v, river_pts[:, 1], river_pts[:, 0])) if v < SEA_T0 + 60 else 999


placed = []
def free(u, v, r):
    return all(math.hypot(u - a, v - b) > r + c for a, b, c in placed)


BTYPES = [  # (a, b, h, roof, 確率)
    ((30, 46), (24, 32), (20, 30), 'gable', .42),
    ((36, 52), (26, 34), (40, 66), 'flat', .26),
    ((26, 34), (26, 34), (80, 120), 'flat', .1),
    ((60, 84), (30, 38), (22, 30), 'flat', .14),
    ((30, 40), (22, 28), (16, 22), 'gable', .08),
]
def paddy(u, v, w, h, ang):
    """田（区画の線＋地図記号「॥」）"""
    ca, sa = math.cos(ang), math.sin(ang)
    def T(x, y):
        return u + x * ca - y * sa, v + x * sa + y * ca
    s = [f'<g stroke="{INK}" stroke-width=".7" fill="none">']
    s.append(f'<path d="{pts_d([T(-w / 2, -h / 2), T(w / 2, -h / 2), T(w / 2, h / 2), T(-w / 2, h / 2)])}" fill="#fff" stroke-width=".9"/>')
    nx, ny = 4, 2
    for i in range(1, nx):
        s.append(f'<path d="{pts_d([T(-w / 2 + w * i / nx, -h / 2), T(-w / 2 + w * i / nx, h / 2)], False)}" stroke-opacity=".6"/>')
    s.append(f'<path d="{pts_d([T(-w / 2, 0), T(w / 2, 0)], False)}" stroke-opacity=".6"/>')
    for i in range(nx):
        for j in range(ny):
            cx, cy = -w / 2 + w * (i + .5) / nx, -h / 2 + h * (j + .5) / ny
            for dx in (-2.2, 2.2):
                s.append(f'<path d="{pts_d([T(cx + dx, cy - 4), T(cx + dx, cy + 3)], False)}" stroke="#4C88BE" stroke-width=".9"/>')
    s.append('</g>')
    put(v, ''.join(s), 1)


def station(u, v):
    building(u, v, 120, 26, 22, 'flat', accent=True)
    x, y = P(u, v)
    put(v + 30, f'<path d="M{f(x - 140)} {f(y + 22)}H{f(x + 140)}M{f(x - 140)} {f(y + 30)}H{f(x + 140)}" stroke="{INK}" stroke-width=".9"/>'
                f'<text x="{f(x + 150)}" y="{f(y + 30)}" font-size="10" letter-spacing="1" fill="{INK}" stroke="#fff" stroke-width="3" paint-order="stroke">STATION</text>', 3)


station(*STATION); placed.append((STATION[0], STATION[1] - 30, 80))
pad_n = 0
for _ in range(3000):
    if pad_n >= 7:
        break
    ti = int(rng.integers(0, len(TOWNS))); u0, u1, v0, v1, _ = TOWNS[ti]
    u, v = rng.uniform(u0 + 60, u1 - 60), rng.uniform(v0 + 30, v1 - 20)
    w, h = rng.uniform(120, 170), rng.uniform(50, 70)
    if road_d(u, v) < 60 or is_water(u, v) or in_block(u, v, 60) or not free(u, v, w * .55) or river_d(u, v) < 90:
        continue
    if min(np.min(np.hypot(rail_pts[:, 0] - u, rail_pts[:, 1] - v)), 999) < 50:
        continue
    paddy(u, v, w, h, rng.uniform(-.25, .25)); placed.append((u, v, w * .55)); pad_n += 1

for ti, (u0, u1, v0, v1, cnt) in enumerate(TOWNS):
    if ti == 2:
        school(700, v0 + 150); placed.append((700, v0 + 150, 75))
    got, tries = 0, 0
    while got < cnt and tries < 4000:
        tries += 1
        u, v = rng.uniform(u0, u1), rng.uniform(v0, v1)
        k = rng.choice(len(BTYPES), p=[t[4] for t in BTYPES])
        (a0, a1), (b0, b1), (h0, h1), roof, _ = BTYPES[k]
        a, b, h = rng.uniform(a0, a1), rng.uniform(b0, b1), rng.uniform(h0, h1)
        r = (a + b) * .5
        if not (22 + b * .35 < road_d(u, v) < 140) or is_water(u, v) or is_water(u, v + 20):
            continue
        y = P(u, v)[1]
        if in_block(u, y + 10, 14) or in_block(u, y - h - 30, 14) or in_block(u - r, y - h / 2, 14) or in_block(u + r, y - h / 2, 14) or not free(u, v, r):
            continue
        if river_d(u, v) < r + 24:
            continue
        building(u, v, a, b, h, roof, accent=rng.random() < .22)
        placed.append((u, v, r)); got += 1
    got = 0
    for _ in range(3000):
        if got >= cnt * 2.2:
            break
        u, v = rng.uniform(u0 - 40, u1 + 40), rng.uniform(v0 - 10, v1 + 10)
        y = P(u, v)[1]
        if road_d(u, v) < 22 or is_water(u, v) or in_block(u, y - 20, 10) or in_block(u, y, 10) or not free(u, v, 10) or river_d(u, v) < 30:
            continue
        tree(u, v, int(rng.random() < .4), rng.uniform(.85, 1.15)); placed.append((u, v, 8)); got += 1

# 山の上の木（余白の尾根）
got = 0
for _ in range(9000):
    if got >= 150:
        break
    r_, c_ = int(rng.integers(2, rows - 2)), int(rng.integers(1, n - 1))
    u, v = c_ * DX + rng.uniform(-6, 6), r_ * DY
    y = v - z[r_, c_] * KD
    if not (.35 < z[r_, c_] < 2.2) or water[r_, c_] or in_block(u, y - 30, 10) or in_block(u, y, 10) or road_d(u, v) < 26 or not free(u, v, 12) or river_d(u, v) < 34:
        continue
    tree(u, v, int(rng.random() < .55), rng.uniform(.8, 1.1)); placed.append((u, v, 10)); got += 1

# 道を走る車・測量する人・風車
for ri, t, d, acc in ((0, .18, 1, False), (0, .62, -1, True), (2, .35, 1, False), (2, .8, -1, True), (3, .5, 1, False),
                      (5, .45, -1, True), (7, .3, 1, True), (7, .7, -1, False), (1, .45, 1, True)):
    rp = road_pts[ri]; u, v = rp[int(len(rp) * t)]
    car(u, v - 3, d, acc)
for ri, t in ((0, .4), (2, .12), (3, .3), (5, .7), (7, .5), (7, .9)):
    rp = road_pts[ri]; u, v = rp[int(len(rp) * t)]
    if not in_block(u, P(u, v)[1] + 20, 0):
        surveyor(u + 6, v + 24, 1 if t < .5 else -1)
        person(u + 44, v + 30)
for u, v in ((300, SEA_B0 + 230), (1080, H - 300), (1180, H - 330), (230, y_svc - 300)):
    if not in_block(u, P(u, v)[1] - 60, 10):
        turbine(u, v, ang=rng.uniform(0, 120))

# 港：クレーンと船・吊り橋
crane(330, SEA_T0 - 20); crane(960, SEA_T0 - 30)
for x, y, L, fl in ((140, SEA_T0 + 70, 50, 1), (1290, SEA_T0 + 210, 40, -1), (1340, SEA_B0 - 120, 54, -1), (90, SEA_B0 - 200, 36, 1)):
    boat(x, y, L, fl)
bridge_seto(SEA_B0 - 95)
lighthouse(ISLANDS[0][0] + 60, ISLANDS[0][1] + 10)
for cu, cv, ru, rv_, a in ISLANDS:
    for t in np.linspace(.2, 5.9, int(ru / 18)):
        tree(cu + ru * .62 * math.cos(t * 1.7), cv + rv_ * .55 * math.sin(t * 1.7), int(t * 10) % 2, .9)
# 川の橋（道路が川を渡るところに欄干）
for rp in road_pts:
    for u, v in rp[::2]:
        if v < SEA_T0 and abs(u - np.interp(v, river_pts[:, 1], river_pts[:, 0])) < 4:
            x, y = P(u, v)
            put(v + 14, f'<path d="M{f(x - 22)} {f(y - 15)}H{f(x + 22)}M{f(x - 22)} {f(y + 9)}H{f(x + 22)}" stroke="{INK_B}" stroke-width="1.2"/>'
                f'<path d="M{f(x - 22)} {f(y - 19)}H{f(x + 22)}M{f(x - 22)} {f(y + 5)}H{f(x + 22)}" stroke="{INK_B}" stroke-width=".8" stroke-dasharray="1 5"/>', 3)
            break


# ================================================================ 地形を描く（陰線処理つき）
def ridge():
    xs = np.arange(n) * DX
    out, prev = [], None
    bins, ops, sw, cols = (.9, 1.9), (.36, .5, .72), (.7, .8, 1.0), (GRAY, MID, BLUE)
    for i in range(rows):
        v = i * DY
        ys = v - z[i] * K
        pts = list(zip(xs, ys))
        out.append(f'<polygon points="{" ".join(f"{f(a)},{f(b)}" for a, b in pts)} {f(xs[-1])},{f(v + 2)} {f(xs[0])},{f(v + 2)}" fill="#fff"/>')
        wrow = water[i]
        if (VV[i, 0] > SEA_T0 - 120) and (VV[i, 0] < SEA_B0 + 120):   # 海：淡い面（海岸線の形で切り抜き）
            out.append(f'<rect x="0" y="{f(ys.min() - 2)}" width="{W}" height="{f(v + DY + 2 - ys.min() + 2)}" fill="{WATER}" clip-path="url(#sea)"/>')
        if prev is not None:  # 縦線（陸のみ）
            segs = {0: [], 1: [], 2: []}
            for j in range(0, n, 3):
                if wrow[j] or water[i - 1, j]:
                    continue
                zz = (z[i, j] + z[i - 1, j]) / 2
                b = 0 if zz < bins[0] else (1 if zz < bins[1] else 2)
                segs[b].append(f'M{f(xs[j])} {f(prev[j])}L{f(xs[j])} {f(ys[j])}')
            for b, s in segs.items():
                if s:
                    out.append(f'<path d="{"".join(s)}" stroke="rgb{cols[b]}" stroke-opacity="{ops[b]}" stroke-width="{sw[b]}"/>')
        # 横線：陸は高さで色分け、海は青い波線（1行おき）
        run, rb = [], None
        def flush():
            if len(run) > 1:
                pl = " ".join(f"{f(a)},{f(c)}" for a, c in run)
                if rb == 'w':
                    if i % 2 == 0:
                        out.append(f'<polyline points="{pl}" stroke="rgb{MID}" stroke-opacity=".32" stroke-width=".8"/>')
                else:
                    out.append(f'<polyline points="{pl}" stroke="rgb{cols[rb]}" stroke-opacity="{ops[rb]}" stroke-width="{sw[rb]}"/>')
        for j in range(n):
            b = 'w' if wrow[j] else (0 if z[i, j] < bins[0] else (1 if z[i, j] < bins[1] else 2))
            if b != rb:
                flush()
                run = run[-1:] if run else []
                rb = b
            run.append(pts[j])
        flush()
        for _, _, s in sorted(LAYER.get(i, []), key=lambda t: (t[0] > 1, t[1], t[0])):
            out.append(s)
        prev = ys
    return ''.join(out)


def contour_map():
    """等高線（4px 格子に上げて引く）＋入り江の等深線＋図郭線、その上に道路・街を手前順に"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    R = 4
    w4, h4 = W // R, H // R
    def up(a):
        return np.asarray(Image.fromarray(a.astype(np.float32), 'F').resize((w4, h4), Image.BICUBIC)) if a.dtype != bool else \
            np.asarray(Image.fromarray(a.astype(np.uint8) * 255).resize((w4, h4), Image.BILINEAR)) > 127
    zz, ww = up(z), up(water)
    out = []
    global labels
    grid = ''.join(f'<path d="M{x} 0V{H}"/>' for x in range(120, W, 240)) + ''.join(f'<path d="M0 {y}H{W}"/>' for y in range(120, H, 240))
    out.append(f'<g stroke="#015B9E" stroke-opacity=".045" stroke-width="1">{grid}</g>')
    cross = ''.join(f'<path d="M{x - 7} {y}h14M{x} {y - 7}v14"/>' for x in range(120, W, 240) for y in range(120, H, 240))
    out.append(f'<g stroke="#015B9E" stroke-opacity=".45" stroke-width=".8">{cross}</g>')
    lab = ''.join(f'<text x="8" y="{y - 5}">X {-148200 + y // 240 * 120:,}</text>' for y in range(360, H, 480)) + \
          ''.join(f'<text x="{x + 5}" y="{H - 90}" >Y {-61080 + x // 240 * 120:,}</text>' for x in range(120, W - 200, 480))
    labels.append(f'<g font-size="9" letter-spacing="1" fill="#015B9E" fill-opacity=".55">{lab}</g>')
    fig = plt.figure(); ax = fig.add_subplot()
    def paths(cs, want=False):
        for lv, path in zip(cs.levels, cs.get_paths()):
            d, vs = [], []
            for verts, code in path.iter_segments(simplify=False):
                d.append(('M' if code == 1 else 'L') + f(verts[0] * R) + ' ' + f(verts[1] * R))
                vs.append((verts[0] * R, verts[1] * R, code))
            if len(d) > 1:
                yield (lv, ''.join(d), vs) if want else (lv, ''.join(d))
    zl = np.where(ww, np.nan, zz)
    used = []
    for i, (lv, d, vs) in enumerate(paths(ax.contour(zl, levels=np.arange(-1.0, 5.0, 0.12)), True)):
        t = min(1, max(0, (lv - 0.5) / 2.4))
        c = tuple(int(a + (b - a) * t) for a, b in zip((138, 138, 138), (1, 91, 158)))
        idx = round(lv / .12) % 5 == 0
        out.append(f'<path d="{d}" stroke="rgb{c}" stroke-opacity="{min(1, (.55 + .4 * t) * (1.3 if idx else 1)):.2f}" stroke-width="{1.05 if idx else .6}"/>')
        if not idx or lv < .3:
            continue
        # 計曲線に標高（線に沿って回転・白フチで線を切る）
        acc = 0
        for k in range(1, len(vs) - 1):
            x0, y0, _ = vs[k - 1]; x1, y1, c1 = vs[k]
            if c1 == 1:
                acc = 0; continue
            acc += math.hypot(x1 - x0, y1 - y0)
            if acc < 260:
                continue
            if in_block(x1, y1, 30) or any(math.hypot(x1 - a, y1 - b) < 170 for a, b in used):
                continue
            x2, y2, _ = vs[k + 1]
            ang = math.degrees(math.atan2(y2 - y0, x2 - x0))
            if ang > 90: ang -= 180
            if ang < -90: ang += 180
            labels.append(f'<text transform="translate({f(x1)} {f(y1)}) rotate({ang:.0f})" y="3.4" text-anchor="middle" font-size="9.5" fill="rgb{c}" '
                          f'stroke="#fff" stroke-width="4" paint-order="stroke">{20 + round(lv / .12) * 2}</text>')
            used.append((x1, y1)); acc = 0
    # 入り江：淡い面＋等深線（点線）
    out.append(f'<rect width="{W}" height="{H}" fill="{WATER}" clip-path="url(#sea)"/>')
    dep = noise(w4, h4, R, ((500, .6), (200, .25)))
    sea_g = ''.join(f'<path d="{d}"/>' for _, d in paths(ax.contour(np.where(ww, dep, np.nan), levels=np.arange(-2, 2, .18))))
    out.append(f'<g clip-path="url(#sea)" stroke="#4C88BE" stroke-opacity=".38" stroke-width=".7" stroke-dasharray="5 4">{sea_g}</g>')
    for x, y, dd in ((70, SEA_T0 + 120, 3.2), (1390, SEA_T0 + 380, 6.8), (60, SEA_B0 - 330, 8.5), (1250, SEA_B0 - 170, 5.4), (620, SEA_T0 + 90, 2.6)):
        labels.append(f'<text x="{x}" y="{f(y)}" font-size="9.5" font-style="italic" fill="#4C88BE" stroke="{WATER}" stroke-width="3" paint-order="stroke">-{dd:.1f}</text>')
    plt.close(fig)
    items = [it for v in LAYER.values() for it in v]
    for _, _, s in sorted(items, key=lambda t: (t[0] > 1, t[1], t[0])):
        out.append(s)
    return ''.join(out)


def main():
    body = contour_map() if MODE == 'map' else ridge()
    zz = np.where(water | (flat > .3), -9, z).copy()
    for px, py in pin_tips():
        zz[max(0, int(py / DY) - 20):int(py / DY) + 30, max(0, int(px / DX) - 15):int(px / DX) + 15] = -9
    tri = []
    for _ in range(8):
        r, c = np.unravel_index(np.argmax(zz), zz.shape)
        if zz[r, c] < 1.0:
            break
        x, y = c * DX, r * DY - z[r, c] * KD
        if 60 < x < W - 80 and y > 40:
            tri.append(f'<g transform="translate({f(x)} {f(y)})"><path d="M0 -9 L8 5 L-8 5 Z" fill="#fff" stroke="#015B9E" stroke-width="1.3"/>'
                       f'<circle r="1.6" cy="0.5" fill="#015B9E"/><text x="12" y="4" font-size="10.5" fill="#015B9E">{20 + z[r, c] / .12 * 2:.1f}</text></g>')
        zz[max(0, r - 25):r + 25, max(0, c - 18):c + 18] = -9
    us_ = np.arange(-20, W + 30, 8.0)
    top = [P(u, coast_top(u)) for u in us_]; bot = [P(u, coast_bot(u)) for u in us_[::-1]]
    sea_d = pts_d(top + bot)
    for cu, cv, ru, rv_, a in ISLANDS:
        th = np.linspace(0, 2 * np.pi, 72, endpoint=False)
        sea_d += pts_d([P(cu + ru * math.cos(t), cv + rv_ * math.sin(t)) for t in th])
    holes = ''.join(f'<rect x="{b["x"] - 24}" y="{b["y"] - 24}" width="{b["w"] + 48}" height="{b["h"] + 48}" rx="40"/>' for b in blocks())
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="none" font-family="Inter,Arial,sans-serif">
<defs><pattern id="hs" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0 0V4" stroke="#5E6B78" stroke-opacity=".38" stroke-width=".7"/></pattern>
<pattern id="hf" width="3.6" height="3.6" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)"><rect width="3.6" height="3.6" fill="#F6F8FA"/><path d="M0 0V3.6" stroke="#5E6B78" stroke-opacity=".2" stroke-width=".6"/></pattern>
<clipPath id="sea"><path d="{sea_d}" clip-rule="evenodd"/></clipPath><filter id="f" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="30"/></filter>
<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>
<linearGradient id="g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>
<mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#fff"/><rect width="{W}" height="200" fill="url(#g)"/><rect y="{H - 70}" width="{W}" height="70" fill="url(#g2)"/><g fill="#555" filter="url(#f)">{holes}</g></mask></defs>
<g fill="none" stroke-linejoin="round" stroke-linecap="round" mask="url(#m)">{body}</g>
<g font-family="Inter,Arial,sans-serif" mask="url(#m)">{''.join(labels)}</g>
<g>{''.join(tri)}</g>
</svg>'''
    open(os.path.join(OUT, 'a-terrain.svg'), 'w').write(svg)
    print('a-terrain.svg', len(svg) // 1024, 'KB', W, H)


if __name__ == '__main__':
    main()
