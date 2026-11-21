"""v3 編集用の共通ヘルパー（apply_*.py から import）"""
import os, re
from PIL import Image, ImageOps

WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(WF, '..', 'photos', '_original')


def path(name):
    return os.path.join(WF, f'design3-{name}.html')


def read(name):
    return open(path(name)).read()


def write(name, html):
    open(path(name), 'w').write(html)


def pages():
    return sorted(os.path.basename(p)[8:-5] for p in os.listdir(WF) if p.startswith('design3-') and p.endswith('.html'))


def photo(n):
    """撮影写真 S1200<n>.jpeg を長辺1800pxで img/photo/ に用意してパスを返す"""
    rel = f'img/photo/S120{n}.jpg'
    dst = os.path.join(WF, rel)
    if not os.path.exists(dst):
        im = ImageOps.exif_transpose(Image.open(os.path.join(ORIG, f'S120{n}.jpeg')))
        im.thumbnail((1800, 1800))
        im.convert('RGB').save(dst, quality=82, optimize=True, progressive=True)
    return rel


def sub(html, old, new, count=1):
    """完全一致置換（見つからなければ止める）"""
    assert old in html, f'not found: {old[:80]}'
    return html.replace(old, new, count)


def new_page(name, title, banner, body, tpl='news'):
    """既存ページ（ゲート・ヘッダー・CTA・フッター込み）を雛形に、phero〜cta直前を body に差し替えて新規ページを作る"""
    h = read(tpl)
    h = re.sub(r'<title>.*?</title>', f'<title>{title}（デザイン案 v3） | 株式会社第二開発技工</title>', h, 1)
    h = re.sub(r'<div class="wf-banner"><span>.*?</span>', f'<div class="wf-banner"><span>{banner}</span>', h, 1)
    a = h.index('<section class="phero')
    b = h.index('<section class="cta')
    h = h[:a] + body.strip() + '\n' + h[b:]
    write(name, h)


RECRUIT_NAV = [("recruit", "採用トップ"), ("recruit-interview", "社員インタビュー"), ("recruit-entry", "エントリー")]


def sibnav(cur, items=RECRUIT_NAV):
    li = ''.join(
        f'<li><a href="design3-{n}.html" class="{"cur" if n == cur else ""}{" entry" if n == "recruit-entry" else ""}">{t}</a></li>'
        for n, t in items)
    return f'<nav class="sibnav"><div class="wrap"><ul>{li}</ul></div></nav>'


def phero(crumbs, h1, en, ph=None, ph_en='', lead=''):
    """crumbs: [(href or None, label)]"""
    c = ' ／ '.join(f'<a href="{h}">{t}</a>' if h else t for h, t in [('design3-top.html', 'ホーム')] + crumbs)
    lead_html = f'<p class="phero__lead">{lead}</p>' if lead else ''
    img = f'<div class="phero__ph"><img src="{photo(ph)}" alt=""><span class="en">{ph_en}</span></div>' if ph else ''
    return (f'<section class="phero v3"><div class="wrap"><div class="pcrumb">{c}</div>'
            f'<div class="phero__bar"><h1>{h1}</h1><span class="phero__en">{en}</span></div>{lead_html}</div>{img}</section>')
