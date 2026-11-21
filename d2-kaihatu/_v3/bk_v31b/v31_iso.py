"""アイソメ線画の小さな描画エンジン（v3.1-B 用）
  トーンは FV の3Dワイヤー地形を踏襲：線 #555/#8A8A8A、面は白〜#F2F2F2、差し色はブランドの青だけ
  座標: x=右下へ, y=左下へ, z=上。Scene.add() で奥行き(depth)付きで積み、svg() で奥から描く
"""
import math

LINE = '#4A5560'
FILL = '#FFFFFF'
FILL2 = '#F2F4F6'
FILL3 = '#E6EBF0'
BLUE = '#015B9E'
BLUE_L = '#4C88BE'
BLUE_P = '#EEF5FB'
YEL = '#FFD54F'
C30, S30 = math.cos(math.pi / 6), 0.5


def f(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


class Scene:
    def __init__(self, ox, oy, s, sw=1.1):
        self.ox, self.oy, self.s, self.sw = ox, oy, s, sw
        self.items = []   # (depth, svg)
        self.under = []   # 地面（常に先に描く）
        self.over = []    # 最前面（ピン・ラベル）

    # --- 投影
    def P(self, x, y, z=0):
        return (self.ox + (x - y) * self.s * C30, self.oy + (x + y) * self.s * S30 - z * self.s)

    def pts(self, ps):
        return ' '.join(f'{f(a)},{f(b)}' for a, b in (self.P(*p) for p in ps))

    def poly(self, ps, fill=FILL, stroke=LINE, sw=None, extra=''):
        return f'<polygon points="{self.pts(ps)}" fill="{fill}" stroke="{stroke}" stroke-width="{f(sw or self.sw)}" stroke-linejoin="round"{extra}/>'

    def line(self, ps, stroke=LINE, sw=None, extra=''):
        return f'<polyline points="{self.pts(ps)}" fill="none" stroke="{stroke}" stroke-width="{f(sw or self.sw)}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'

    def add(self, depth, svg):
        self.items.append((depth, svg))

    # --- 形
    def box(self, x, y, z, w, d, h, top=FILL, left=FILL2, right=FILL3, stroke=LINE, depth=None, win=None, sw=None):
        g = [self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], left, stroke, sw),
             self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], right, stroke, sw),
             self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], top, stroke, sw)]
        if win:  # 窓：(段数, 列数)
            rows, cols = win
            for r in range(rows):
                zz = z + h * (r + 0.35) / rows
                hh = h / rows * 0.38
                for c in range(cols):
                    a = x + w * (c + 0.25) / cols; b = a + w / cols * 0.5
                    g.append(self.poly([(a, y + d, zz), (b, y + d, zz), (b, y + d, zz + hh), (a, y + d, zz + hh)], '#fff', stroke, (sw or self.sw) * .7))
                for c in range(max(1, int(cols * d / w))):
                    n = max(1, int(cols * d / w))
                    a = y + d * (c + 0.25) / n; b = a + d / n * 0.5
                    g.append(self.poly([(x + w, a, zz), (x + w, b, zz), (x + w, b, zz + hh), (x + w, a, zz + hh)], '#fff', stroke, (sw or self.sw) * .7))
        self.add(depth if depth is not None else x + w + y + d, ''.join(g))

    def house(self, x, y, w, d, h, rh, roof=FILL, depth=None):
        z = h
        g = [self.poly([(x, y + d, 0), (x + w, y + d, 0), (x + w, y + d, h), (x, y + d, h)], FILL2),
             self.poly([(x + w, y, 0), (x + w, y + d, 0), (x + w, y + d, h), (x + w, y, h)], FILL3),
             self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d / 2, z + rh)], FILL),
             self.poly([(x, y + d / 2, z + rh), (x + w, y + d / 2, z + rh), (x + w, y + d, z), (x, y + d, z)], roof),
             ]
        # 窓とドア
        g.append(self.poly([(x + w * .2, y + d, 0), (x + w * .38, y + d, 0), (x + w * .38, y + d, h * .62), (x + w * .2, y + d, h * .62)], '#fff', LINE, self.sw * .7))
        g.append(self.poly([(x + w * .55, y + d, h * .35), (x + w * .8, y + d, h * .35), (x + w * .8, y + d, h * .7), (x + w * .55, y + d, h * .7)], '#fff', LINE, self.sw * .7))
        self.add(depth if depth is not None else x + w + y + d, ''.join(g))

    def tree(self, x, y, r=1.0, h=1.6, kind='round', fill=FILL):
        bx, by = self.P(x, y, 0)
        tx, ty = self.P(x, y, h)
        R = r * self.s
        if kind == 'round':
            g = (f'<line x1="{f(bx)}" y1="{f(by)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{LINE}" stroke-width="{f(self.sw)}"/>'
                 f'<circle cx="{f(tx)}" cy="{f(ty - R * .55)}" r="{f(R)}" fill="{fill}" stroke="{LINE}" stroke-width="{f(self.sw)}"/>'
                 f'<path d="M{f(tx - R * .45)} {f(ty - R * .5)} q{f(R * .2)} {f(-R * .5)} {f(R * .55)} {f(-R * .55)}" fill="none" stroke="{LINE}" stroke-width="{f(self.sw * .7)}" stroke-linecap="round"/>')
        else:
            g = (f'<line x1="{f(bx)}" y1="{f(by)}" x2="{f(tx)}" y2="{f(ty)}" stroke="{LINE}" stroke-width="{f(self.sw)}"/>'
                 f'<path d="M{f(tx)} {f(ty - R * 2.6)} L{f(tx + R * .8)} {f(ty + R * .2)} L{f(tx - R * .8)} {f(ty + R * .2)} Z" fill="{fill}" stroke="{LINE}" stroke-width="{f(self.sw)}" stroke-linejoin="round"/>')
        self.add(x + y + .01, g)

    def person(self, x, y, k=1.0, helmet=BLUE, vest=None, face=1, arm=None):
        """人：ヘルメット付きの作業員（スクリーン空間の小さなスプライト）"""
        bx, by = self.P(x, y, 0)
        u = self.s * 0.55 * k
        sw = self.sw * .9
        body = vest or FILL
        g = [f'<g transform="translate({f(bx)} {f(by)})" stroke="{LINE}" stroke-width="{f(sw)}" stroke-linejoin="round" stroke-linecap="round">',
             f'<ellipse cx="0" cy="0" rx="{f(u * .9)}" ry="{f(u * .38)}" fill="{FILL3}" stroke="none"/>',
             f'<path d="M{f(-u * .35)} 0 L{f(-u * .3)} {f(-u * 1.6)} M{f(u * .35)} 0 L{f(u * .3)} {f(-u * 1.6)}" fill="none"/>',
             f'<rect x="{f(-u * .62)}" y="{f(-u * 3.2)}" width="{f(u * 1.24)}" height="{f(u * 1.75)}" rx="{f(u * .35)}" fill="{body}"/>',
             f'<circle cx="0" cy="{f(-u * 3.75)}" r="{f(u * .5)}" fill="#fff"/>',
             f'<path d="M{f(-u * .62)} {f(-u * 3.8)} a{f(u * .62)} {f(u * .62)} 0 0 1 {f(u * 1.24)} 0 Z" fill="{helmet}"/>']
        if arm == 'point':
            g.append(f'<path d="M{f(u * .55)} {f(-u * 2.9)} L{f(u * 1.5)} {f(-u * 3.6)}" fill="none"/>')
        elif arm == 'hold':
            g.append(f'<path d="M{f(-u * .55)} {f(-u * 2.8)} L{f(-u * .9)} {f(-u * 2.1)} M{f(u * .55)} {f(-u * 2.8)} L{f(u * .9)} {f(-u * 2.1)}" fill="none"/>')
        g.append('</g>')
        self.add(x + y + .02, ''.join(g))

    def tripod(self, x, y, k=1.0, h=1.8):
        """トータルステーション（三脚＋本体は青）"""
        tx, ty = self.P(x, y, h * k)
        legs = [self.P(x - .55 * k, y - .1 * k), self.P(x + .45 * k, y - .45 * k), self.P(x + .15 * k, y + .6 * k)]
        u = self.s * .32 * k
        g = ''.join(f'<line x1="{f(tx)}" y1="{f(ty)}" x2="{f(a)}" y2="{f(b)}" stroke="{LINE}" stroke-width="{f(self.sw)}" stroke-linecap="round"/>' for a, b in legs)
        g += (f'<rect x="{f(tx - u * .9)}" y="{f(ty - u * 2.1)}" width="{f(u * 1.8)}" height="{f(u * 2.1)}" rx="{f(u * .25)}" fill="{BLUE}" stroke="{LINE}" stroke-width="{f(self.sw)}"/>'
              f'<circle cx="{f(tx)}" cy="{f(ty - u * 1.2)}" r="{f(u * .45)}" fill="#fff" stroke="{LINE}" stroke-width="{f(self.sw * .7)}"/>')
        self.add(x + y + .015, g)

    def prism(self, x, y, k=1.0, h=2.6):
        bx, by = self.P(x, y)
        tx, ty = self.P(x, y, h * k)
        n = 5
        g = ''
        for i in range(n):
            a = by + (ty - by) * i / n; b = by + (ty - by) * (i + 1) / n
            g += f'<line x1="{f(bx)}" y1="{f(a)}" x2="{f(bx)}" y2="{f(b)}" stroke="{BLUE if i % 2 else LINE}" stroke-width="{f(self.sw * 1.8)}"/>'
        g += f'<circle cx="{f(tx)}" cy="{f(ty)}" r="{f(self.s * .22 * k)}" fill="#fff" stroke="{LINE}" stroke-width="{f(self.sw)}"/>'
        self.add(x + y + .015, g)

    def drone(self, x, y, z, k=1.0, scan=True):
        cx, cy = self.P(x, y, z)
        u = self.s * .5 * k
        g = f'<g transform="translate({f(cx)} {f(cy)})" stroke="{LINE}" stroke-width="{f(self.sw)}" stroke-linecap="round">'
        if scan:  # 計測範囲（地面へ向かう点線）
            a = self.P(x - 2.2, y - 0.4); b = self.P(x + 0.4, y + 2.2)
            g += (f'<path d="M0 0 L{f(a[0] - cx)} {f(a[1] - cy)} M0 0 L{f(b[0] - cx)} {f(b[1] - cy)}" stroke="{BLUE_L}" stroke-dasharray="3 5" fill="none"/>')
        for dx, dy in ((-1.6, -.55), (1.6, -.55), (-1.1, .35), (1.1, .35)):
            g += f'<line x1="0" y1="0" x2="{f(dx * u)}" y2="{f(dy * u)}"/><ellipse cx="{f(dx * u)}" cy="{f(dy * u - u * .25)}" rx="{f(u * .75)}" ry="{f(u * .2)}" fill="#fff"/>'
        g += f'<rect x="{f(-u * .55)}" y="{f(-u * .4)}" width="{f(u * 1.1)}" height="{f(u * .75)}" rx="{f(u * .2)}" fill="{BLUE}"/></g>'
        self.over.append(g)

    def car(self, x, y, along='x', color=BLUE):
        if along == 'x':
            self.box(x, y, .15, 2.2, 1.1, .7, top=color, left=color, right=color, depth=x + y + 3.3)
            self.box(x + .5, y, .85, 1.2, 1.1, .5, top='#fff', left='#fff', right='#fff', depth=x + y + 3.31)
        else:
            self.box(x, y, .15, 1.1, 2.2, .7, top=color, left=color, right=color, depth=x + y + 3.3)
            self.box(x, y + .5, .85, 1.1, 1.2, .5, top='#fff', left='#fff', right='#fff', depth=x + y + 3.31)

    def excavator(self, x, y, k=1.0):
        s = k
        self.box(x, y, 0, 3.4 * s, 2.4 * s, .6 * s, top=FILL3, left=FILL2, right=FILL3, depth=x + y + 5.8 * s)
        self.box(x + .5 * s, y + .4 * s, .6 * s, 2.2 * s, 1.6 * s, .8 * s, depth=x + y + 5.9 * s)
        self.box(x + 1.6 * s, y + .5 * s, 1.4 * s, 1.0 * s, 1.0 * s, 1.1 * s, top=BLUE, left=BLUE, right=BLUE, depth=x + y + 6.0 * s)
        a = self.P(x + 2.6 * s, y + 1.9 * s, 1.3 * s); b = self.P(x + 4.3 * s, y + 1.9 * s, 3.1 * s); c = self.P(x + 5.6 * s, y + 1.9 * s, .9 * s)
        bk = [self.P(x + 5.4 * s, y + 1.5 * s, .9 * s), self.P(x + 6.0 * s, y + 1.5 * s, 0), self.P(x + 6.0 * s, y + 2.3 * s, 0), self.P(x + 5.4 * s, y + 2.3 * s, .9 * s)]
        w = self.sw * 4.5
        pl = f"{f(a[0])},{f(a[1])} {f(b[0])},{f(b[1])} {f(c[0])},{f(c[1])}"
        g = (f'<polyline points="{pl}" fill="none" stroke="{LINE}" stroke-width="{f(w + 2.2)}" stroke-linejoin="round" stroke-linecap="round"/>'
             f'<polyline points="{pl}" fill="none" stroke="#fff" stroke-width="{f(w)}" stroke-linejoin="round" stroke-linecap="round"/>'
             f'<polygon points="{" ".join(f"{f(p)},{f(q)}" for p, q in bk)}" fill="{FILL2}" stroke="{LINE}" stroke-width="{f(self.sw)}" stroke-linejoin="round"/>')
        self.add(x + y + 6.1 * s, g)

    def cone(self, x, y, k=1.0):
        bx, by = self.P(x, y); u = self.s * .3 * k
        g = (f'<path d="M{f(bx - u)} {f(by)} L{f(bx)} {f(by - u * 3)} L{f(bx + u)} {f(by)} Z" fill="#fff" stroke="{LINE}" stroke-width="{f(self.sw)}" stroke-linejoin="round"/>'
             f'<path d="M{f(bx - u * .6)} {f(by - u * 1.1)} H{f(bx + u * .6)}" stroke="{BLUE}" stroke-width="{f(self.sw * 2)}"/>')
        self.add(x + y + .01, g)

    def band(self, pts, w, fill, stroke, center=None, depth=None, sw=None):
        """地面上の帯（川・道路）。pts は (x,y) の中心線"""
        L, Rr = [], []
        for i, (x, y) in enumerate(pts):
            a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]; n = math.hypot(dx, dy) or 1
            nx, ny = -dy / n * w / 2, dx / n * w / 2
            L.append((x + nx, y + ny, 0)); Rr.append((x - nx, y - ny, 0))
        poly = L + Rr[::-1]
        g = f'<polygon points="{self.pts(poly)}" fill="{fill}" stroke="none"/>'
        g += self.line(L, stroke, sw) + self.line(Rr, stroke, sw)
        if center:
            g += self.line([(x, y, 0) for x, y in pts], center, (sw or self.sw) * .8, ' stroke-dasharray="8 7"')
        self.under.append(g)

    def pin(self, x, y, z, label, no):
        """ブランドの三角をいれたしずく型ピン＋塗り箱ラベル"""
        px, py = self.P(x, y, z)
        r = 15
        g = (f'<g transform="translate({f(px)} {f(py)})">'
             f'<path d="M0 0 C-6 -10 -{r} -16 -{r} -28 A{r} {r} 0 1 1 {r} -28 C{r} -16 6 -10 0 0 Z" fill="{BLUE}" stroke="#fff" stroke-width="2"/>'
             f'<path d="M0 -37 L8 -22 L-8 -22 Z" fill="#fff"/>'
             f'<g transform="translate(22 -40)"><rect width="{38 + 13.5 * len(label)}" height="24" fill="#013D6A"/>'
             f'<rect x="4" y="4" width="20" height="16" fill="{YEL}"/>'
             f'<text x="14" y="16.5" text-anchor="middle" font-size="10" font-weight="700" fill="#3A2B00" font-family="Inter,Arial,sans-serif">{no}</text>'
             f'<text x="30" y="17" font-size="13" font-weight="700" fill="#fff" letter-spacing="1">{label}</text></g></g>')
        self.over.append(g)

    def svg(self, w, h, extra_defs='', bg=''):
        body = ''.join(self.under) + ''.join(s for _, s in sorted(self.items, key=lambda t: t[0])) + ''.join(self.over)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="\'Noto Sans JP\',sans-serif">'
                f'{extra_defs}{bg}{body}</svg>')


def mesh(sc, x0, x1, y0, y1, hf, alpha=lambda X, Y: 1.0, step=1.0, base=.5, zmax=6):
    """FVと同じワイヤーメッシュの地面。hf(x,y)=高さ、alpha(画面X,Y)=0〜1 で薄める"""
    out = []
    def seg(p, q):
        a = sc.P(*p); b = sc.P(*q)
        al = min(alpha(*a), alpha(*b))
        if al <= 0.02 or al * (base + (.9 - base) * min(1, (p[2] + q[2]) / 2 / zmax)) < .03:
            return
        z = (p[2] + q[2]) / 2
        t = min(1, z / zmax)
        c = tuple(int(u + (v - u) * t) for u, v in zip((150, 156, 162), (1, 91, 158)))
        out.append(f'<line x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}" stroke="rgb{c}" stroke-opacity="{al * (base + (.9 - base) * t):.2f}"/>')
    n = int((x1 - x0) / step); m = int((y1 - y0) / step)
    for i in range(n + 1):
        x = x0 + i * step
        for j in range(m):
            y = y0 + j * step
            seg((x, y, hf(x, y)), (x, y + step, hf(x, y + step)))
    for j in range(m + 1):
        y = y0 + j * step
        for i in range(n):
            x = x0 + i * step
            seg((x, y, hf(x, y)), (x + step, y, hf(x + step, y)))
    sc.under.insert(0, f'<g stroke-width=".7" stroke-linecap="round">{"".join(out)}</g>')
