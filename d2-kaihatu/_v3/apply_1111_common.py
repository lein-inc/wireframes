#!/usr/bin/env python3
"""11/11 v3 共通ブラッシュアップ（既存11ページ）
  ・css/v3.css を読込／タイトルの「v2」表記を v3 に
  ・下層ヒーローに写真（右へ抜ける・左上斜めカット）
  ・ページ末尾のCTAを「業務のご相談／採用エントリー」2面の写真パネルに統一
  ・フッター：採用情報の列を新設（職種紹介・社員インタビュー・募集要項・FAQ・エントリー）、プライバシーポリシーをページ化
  ・ダミー写真（img/dummy）に「ダミー画像」透かし
  ・ニュースのホバー画像を撮影写真に（js/d3-news-hover.js）
  再実行すると assert で止まる（バックアップ _v3/bk_20261111a/）
"""
import re
from lib import read, write, photo, sub, pages

HERO = {  # ページ → (写真番号, 写真右下の英字)
    'service': ('0213', 'Our Business'),
    'service-survey': ('0303', 'Surveying'),
    'service-design': ('0390', 'Research & Design'),
    'service-management': ('0121', 'Construction Management'),
    'strengths': ('0244', 'Technology'),
    'social': ('0252', 'Social Activities'),
    'about': ('0374', 'Head Office / Kurashiki'),
    'recruit': ('0240', 'Join Our Team'),
    'news': ('0399', 'News'),
    'contact': ('0372', 'Contact'),
}

CTA3 = f'''<section class="cta3">
  <div class="pair">
    <a href="design3-contact.html" class="panel biz">
      <img src="{photo('0313')}" alt="" loading="lazy">
      <span class="en">Contact</span>
      <h3>測量・調査設計・施工管理のご相談</h3>
      <p>公共測量から民間の工事測量、施工管理技術者の派遣まで。まずはお気軽にご相談ください。</p>
      <div class="go"><span class="tel">086-423-1899<small>平日 9:00〜17:00</small></span><span class="circ">→</span></div>
    </a>
    <a href="design3-recruit-entry.html" class="panel rec">
      <img src="{photo('0268')}" alt="" loading="lazy">
      <span class="en">Entry</span>
      <h3>採用エントリー</h3>
      <p>未経験から、測量のプロへ。会社見学だけのご応募も歓迎しています。</p>
      <div class="go"><span class="circ">→</span></div>
    </a>
  </div>
</section>
'''

FOOT_OLD = '''    <div><h4>会社案内</h4><ul>
      <li><a href="design3-about.html#greeting">代表あいさつ</a></li>
      <li><a href="design3-about.html#company">会社概要</a></li>
      <li><a href="design3-about.html#history">沿革</a></li>
      <li><a href="design3-about.html#clients">主要取引先</a></li>
      <li><a href="design3-about.html#access">アクセス</a></li>
    </ul></div>
    <div><h4>採用・その他</h4><ul>
      <li><a href="design3-top.html">ホーム</a></li>
      <li><a href="design3-recruit.html">採用情報</a></li>
      <li><a href="design3-news.html">ニュース</a></li>
      <li><a href="design3-contact.html">お問い合わせ</a></li>
      <li><a href="#">プライバシーポリシー</a></li>
    </ul></div>'''
FOOT_NEW = '''    <div><h4>会社案内</h4><ul>
      <li><a href="design3-about.html#greeting">代表あいさつ</a></li>
      <li><a href="design3-about.html#company">会社概要</a></li>
      <li><a href="design3-about.html#history">沿革</a></li>
      <li><a href="design3-about.html#clients">主要取引先</a></li>
      <li><a href="design3-about.html#access">アクセス</a></li>
      <li><a href="design3-news.html">ニュース</a></li>
      <li><a href="design3-contact.html">お問い合わせ</a></li>
      <li><a href="design3-privacy.html">プライバシーポリシー</a></li>
    </ul></div>
    <div><h4>採用情報</h4><ul>
      <li><a href="design3-recruit.html">採用トップ</a></li>
      <li><a href="design3-recruit-job.html">職種紹介</a></li>
      <li><a href="design3-recruit-interview.html">社員インタビュー</a></li>
      <li><a href="design3-recruit-requirements.html">募集要項</a></li>
      <li><a href="design3-recruit-faq.html">よくある質問</a></li>
      <li><a href="design3-recruit-entry.html">エントリー</a></li>
    </ul></div>'''


def hero(html, name):
    n, en = HERO[name]
    m = re.search(r'<section class="phero"><div class="wrap">(.*?)</div></section>', html)
    assert m, name
    new = (f'<section class="phero v3"><div class="wrap">{m.group(1)}</div>'
           f'<div class="phero__ph"><img src="{photo(n)}" alt=""><span class="en">{en}</span></div></section>')
    return html.replace(m.group(0), new, 1)


def cta(html, name):
    f = html.index('<footer class="site-footer">')
    head, tail = html[:f], html[f:]
    # 末尾の既存CTA（section.cta か cta-box を含む section）を外す
    m = list(re.finditer(r'<section class="cta">.*?</section>\n?|<section style="background:#F2F8FC;"><div class="wrap"><div class="cta-box.*?</section>\n?', head, re.S))
    if m:
        last = m[-1]
        assert head[last.end():].strip() == '', name
        head = head[:last.start()]
    if name != 'contact':
        head = head.rstrip('\n') + '\n' + CTA3 + '\n'
    return head + tail


def dummy(html):
    return re.sub(r'<div class="([^"]*)">(\s*)<img src="img/dummy/',
                  lambda m: f'<div class="{m.group(1)} is-dummy">{m.group(2)}<img src="img/dummy/', html)


for name in pages():
    h = read(name)
    assert 'css/v3.css' not in h, f'{name}: 適用済み'
    h = re.sub(r'(<link rel="stylesheet" href="css/design3\.css[^"]*">)', r'\1\n<link rel="stylesheet" href="css/v3.css?v=1">', h, 1)
    h = h.replace('（デザイン案 v2）', '（デザイン案 v3）')
    h = h.replace('js/d2-news-hover.js', 'js/d3-news-hover.js')
    if FOOT_OLD in h:
        h = h.replace(FOOT_OLD, FOOT_NEW)
    else:
        print('footer pattern not found:', name)
    h = h.replace('<a href="design3-recruit.html#jobs" class="c-entry">', '<a href="design3-recruit-entry.html" class="c-entry">')
    if name in HERO:
        h = hero(h, name)
    h = cta(h, name)
    h = dummy(h)
    write(name, h)
    print('ok', name)

# ニュースのホバー画像（v2 の d2-news-hover.js は触らない）
js = open('../js/d2-news-hover.js').read()
DUMMY = re.search(r"var DUMMY = \[.*?\];", js).group(0)
PH = ['0224', '0389', '0273', '0157', '0647', '0089', '0372', '0350', '0682']
js = js.replace(DUMMY, 'var DUMMY = [' + ','.join(f"'{photo(n)}'" for n in PH) + '];')
js = js.replace('design2 共通', 'design3 共通・撮影写真版')
open('../js/d3-news-hover.js', 'w').write(js)
print('js ok')
