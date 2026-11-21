#!/usr/bin/env python3
"""11/11 v3 ページ別の修正（既存ページ）
  ・採用トップ：兄弟ページナビ化、職種・社員・FAQ を各詳細ページへの入口に
  ・社員紹介03（女性・入社5年目）は未撮影 → ダミー＋透かし
  ・施工管理の写真 S1200183（社用車ナンバーが写る）は使わない → S1200130
  ・施工管理ページに現場写真、ニュース一覧を記事詳細へリンク、お問い合わせの採用種別をエントリーページへ
"""
import re
from lib import read, write, photo, sub, pages, sibnav

# --- S1200183（ナンバー）を全ページから外す
for n in pages():
    h = read(n)
    if 'S1200183' in h:
        write(n, h.replace('img/photo/S1200183.jpg', photo('0130')))
        print('183→130', n)

# --- 採用トップ
h = read('recruit')
h = re.sub(r'<nav class="section-nav">.*?</nav>', sibnav('recruit'), h, count=1, flags=re.S)
h = sub(h, '<a href="design3-contact.html" class="pill yellow">エントリーする <span class="circ">→</span></a>\n          <a href="#faq" class="pill ghost">よくある質問 <span class="circ">→</span></a>',
        '<a href="design3-recruit-entry.html" class="pill yellow">エントリーする <span class="circ">→</span></a>\n          <a href="design3-recruit-job.html" class="pill ghost">職種紹介を見る <span class="circ">→</span></a>')
# 職種カード → 職種紹介の各項へ
for i in (1, 2, 3):
    h = re.sub(r'(<span class="no">0%d</span>.*?</ul>)' % i,
               lambda m: m.group(1) + f'\n        <a href="design3-recruit-job.html#job{i}" class="arw-link" style="margin-top:22px;">仕事内容を詳しく <span class="circ">→</span></a>',
               h, count=1, flags=re.S)
h = sub(h, '''    <div class="center-pill fade-target d-2">
      <a href="design3-contact.html" class="pill">エントリーフォームへ <span class="circ">→</span></a>
    </div>''', '''    <div class="center-pill fade-target d-2" style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap;">
      <a href="design3-recruit-requirements.html" class="pill">募集要項を見る <span class="circ">→</span></a>
      <a href="design3-recruit-entry.html" class="pill yellow">エントリーフォームへ <span class="circ">→</span></a>
    </div>''')
# 社員紹介 → インタビューへ（03 は未撮影＝ダミー）
h = sub(h, '<div class="ph-clip"><img src="img/photo/S1200662.jpg" alt="" loading="lazy">',
        '<div class="ph-clip is-dummy"><img src="img/dummy/26.jpg" alt="" loading="lazy">')
people = h[h.index('id="people"'):h.index('</section>', h.index('id="people"'))]
p2 = people
for i in (1, 2, 3):
    p2 = re.sub(r'(<span class="no">0%d</span>.*?</p>)' % i,
                lambda m: m.group(1) + f'\n        <a href="design3-recruit-interview.html#iv{i}" class="arw-link" style="color:#fff;">インタビューを読む <span class="circ" style="background:var(--aqua);">→</span></a>',
                p2, count=1, flags=re.S)
h = h.replace(people, p2)
# FAQ は3問だけ残して詳細ページへ
faq = h[h.index('<div class="qa fade-target">'):h.index('</section>', h.index('id="faq"'))]
items = re.findall(r'      <div class="qa-item">.*?</div></div>\n', faq)
assert len(items) == 6
faq2 = faq
for it in items[3:]:
    faq2 = faq2.replace(it, '')
faq2 = faq2.replace('    </div>\n  </div>\n', '    </div>\n    <div class="fade-target" style="margin-top:40px;"><a href="design3-recruit-faq.html" class="arw-link">よくある質問をすべて見る <span class="circ">→</span></a></div>\n  </div>\n', 1)
h = h.replace(faq, faq2)
write('recruit', h)
print('recruit ok')

# --- 施工管理：現場写真グリッド（イントロの3項目の後ろ）
h = read('service-management')
grid = f'''
    <div class="phgrid fade-target">
      <figure><img src="{photo('0131')}" alt="" loading="lazy"><figcaption>現場での打合せ・指示</figcaption></figure>
      <figure><img src="{photo('0258')}" alt="" loading="lazy"><figcaption>現場の状況確認</figcaption></figure>
      <figure><img src="{photo('0311')}" alt="" loading="lazy"><figcaption>測量による出来形の確認</figcaption></figure>
    </div>'''
i = h.index('<section', h.index('class="phero'))  # 最初の本文セクション
j = h.index('</section>', i)
body = h[i:j]
last_wrap_close = body.rindex('</div>')  # wrap の閉じ
body2 = body[:last_wrap_close] + grid + '\n  ' + body[last_wrap_close:]
h = h.replace(body, body2, 1)
write('service-management', h)
print('management ok')

# --- ニュース一覧：行を記事詳細へのリンクに
h = read('news')
h, n = re.subn(r'<div class="news-item">(.*?)</div></div>', r'<a class="news-item" href="design3-news-detail.html">\1</div></a>', h)
print('news rows', n)
write('news', h)

# --- お問い合わせ：種別カードに導線
h = read('contact')
print('contact types:', re.findall(r'<h3[^>]*>[^<]*</h3>', h)[:4])
write('contact', h)
