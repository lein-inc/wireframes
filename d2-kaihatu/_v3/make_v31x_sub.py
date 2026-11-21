#!/usr/bin/env python3
"""v3.1 B／C 案の下層ページを design3-*.html（v3 の下層）から生成（何度実行しても同じ）
  中身（文章・写真・構成）は v3 と同じ。見た目だけ各案のトンマナに寄せる
    B = css/v31b.css（TOP と共通：ヘッダー・CTA・フッター）＋ css/v31b-sub.css（下層の部品）
    C = css/v31c.css ＋ css/v31c-sub.css
  リンクは案の中で閉じる（design3-xxx.html → design31b-xxx.html）。TOP 側は make_v31x.py が同じ置換をする
  ※ v3 の下層（design3-*.html）を直したら、これを再実行すれば B/C にも反映される
"""
import os, re, glob
from lib import WF
from make_v31x import VARIANTS, FOOT_HD

NAME = {'b': 'kopetzki.law のトンマナ', 'c': 'sybiosme.com のトンマナ'}


def pages():
    out = []
    for p in sorted(glob.glob(os.path.join(WF, 'design3-*.html'))):
        slug = os.path.basename(p)[len('design3-'):-len('.html')]
        if slug != 'top':
            out.append(slug)
    return out


def build(v, slug):
    cfg = VARIANTS[v]
    h = open(os.path.join(WF, f'design3-{slug}.html')).read()
    h = h.replace('（デザイン案 v3）', f'（デザイン案 v3.1 {v.upper()}）')
    # バナー：「DESIGN v3 | 事業案内 | /service/（…）」→ 案名つきに
    def ban(m):
        t = m.group(2)
        t = re.sub(r'^DESIGN v3\s*\|', f'DESIGN v3.1 {v.upper()} ｜', t)
        t = re.sub(r'（v3[^）]*）', '', t)
        return m.group(1) + t + f'（{NAME[v]}・中身は v3 と同じ）</span>'
    h = re.sub(r'(<div class="wf-banner">\s*<span>)(.*?)</span>', ban, h, count=1)
    h = re.sub(r'(<link rel="stylesheet" href="css/v3\.css[^"]*">)',
               r'\1\n<link href="https://fonts.googleapis.com/css2?' + cfg['fonts'] + r'&display=swap" rel="stylesheet">'
               + f'\n<link rel="stylesheet" href="css/v31{v}.css?v=10">\n<link rel="stylesheet" href="css/v31{v}-sub.css?v=1">', h, count=1)
    h = h.replace('<body class="d2-sub">', f'<body class="d2-sub v31 v31{v}">', 1)
    h = h.replace('<footer class="site-footer">\n  <div class="wrap">', '<footer class="site-footer">\n' + FOOT_HD[v] + '  <div class="wrap">', 1)
    h = h.replace('design3-', f'design31{v}-')
    open(os.path.join(WF, f'design31{v}-{slug}.html'), 'w').write(h)


if __name__ == '__main__':
    ps = pages()
    for v in 'bc':
        for s in ps:
            build(v, s)
        print(f'ok v31{v}: {len(ps)} pages')
