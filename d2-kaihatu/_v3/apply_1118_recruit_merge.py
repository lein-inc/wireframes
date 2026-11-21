#!/usr/bin/env python3
"""11/18 関指示：採用ページを「インタビュー・エントリー以外は採用TOPにまとめる」＋グローバルナビから採用情報を外す
  - design3-recruit.html に 職種紹介／キャリアステップ／募集要項（タブ）／選考の流れ／よくある質問（全件）を統合
  - 採用TOPの sibnav はページ内メニュー（アンカー＋スクロール位置で現在地表示）。右端のエントリーは別ページのまま
  - design3-recruit-job / -requirements / -faq.html は _v3/bk_20261118_recruit/ へ退避して削除
  - 全 design3-*.html と design31a-top.html のリンクを付け替え（job→#jobs, requirements→#requirements, faq→#faq）
  - グローバルナビ（.gnav）の「採用情報」を削除（右上の header-cta が採用情報への入口）
  一度きりの適用（再実行すると recruit-job 等が無いので止まる）
"""
import os, re, glob, shutil
WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(WF, n)
BK = os.path.join(WF, '_v3', 'bk_20261118_recruit')
RD = lambda n: open(P(n)).read()

assert os.path.exists(P('design3-recruit-job.html')), '適用済み'
os.makedirs(BK, exist_ok=True)
for f in glob.glob(P('design3-*.html')) + [P('design31a-top.html')]:
    shutil.copy2(f, BK)

job, req, faq, top = RD('design3-recruit-job.html'), RD('design3-recruit-requirements.html'), RD('design3-recruit-faq.html'), RD('design3-recruit.html')


def sections(h):
    """sibnav の後〜cta3 の前の <section>…</section> を順に返す"""
    body = h[h.index('</nav>', h.index('class="sibnav"')) + 6: h.index('<section class="cta3">')]
    return re.findall(r'<section[^>]*>.*?</section>', body, re.S)


def one(pat, h):
    m = re.search(pat, h, re.S)
    assert m, pat
    return m


job_s, car_s = sections(job)
req_s, flow_s = sections(req)
faq_ss = sections(faq)

# --- 職種紹介（詳細版）: 見出しは TOP の「3つの募集職種」＋リード文 -------------
top_jobs = one(r'<section class="has-bgword" id="jobs">.*?</section>', top).group(0)
head = one(r'<div class="sec-head fade-target">.*?</div>', top_jobs).group(0)
job_s = re.sub(r'<div class="sec-head fade-target">.*?</div>', head, job_s, count=1, flags=re.S)
job_s = job_s.replace('<section class="has-bgword ">', '<section class="has-bgword" id="jobs">', 1)
job_s = job_s.replace('href="design3-recruit-requirements.html" class="pill ghost">募集要項',
                      'href="#requirements" class="pill ghost">募集要項')
car_s = car_s.replace('<section class="has-bgword tone">', '<section class="has-bgword tone" id="career">', 1)
car_s = car_s.replace('href="design3-recruit.html#first-step"', 'href="#first-step"')
top = top.replace(top_jobs, job_s + '\n' + car_s, 1)

# キャリア（tone）の後の「未経験からの1年」も tone なので白に
top = top.replace('<section class="tone has-bgword" id="first-step">', '<section class="has-bgword" id="first-step">', 1)
top = top.replace('<section class="has-bgword" id="support">', '<section class="tone has-bgword" id="support">', 1)

# ある日のスケジュールに id
top = re.sub(r'<section class="has-bgword">(\s*<div class="bg-word" aria-hidden="true">[^<]*</div>\s*<div class="wrap">\s*<div class="sec-head fade-target">\s*<h2><span class="hbox">ある日)',
             r'<section class="has-bgword" id="day">\1', top, count=1)

# --- 募集要項・選考の流れ・よくある質問（全件）で TOP の FAQ を置き換え ---------------
req_s = req_s.replace('<section class="has-bgword ">', '<section class="tone has-bgword" id="requirements">', 1)
flow_s = flow_s.replace('<section class="has-bgword tone">', '<section class="has-bgword" id="flow">', 1)
flow_s = flow_s.replace('<a href="design3-recruit-faq.html" class="pill ghost">よくある質問 <span class="circ">→</span></a>',
                        '<a href="#faq" class="pill ghost">よくある質問 <span class="circ">→</span></a>')
groups = []
for s in faq_ss:
    t = one(r'<span class="hbox">(.*?)</span>', s).group(1)
    en = one(r'<span class="en-label">(.*?)</span>', s).group(1)
    qa = one(r'(<div class="qa fade-target">.*)</div>\s*</section>', s).group(1).rstrip()  # 最後の </div>（wrap の閉じ）は含めない
    groups.append(f'    <h3 class="qa-cat fade-target"><span class="en">{en}</span>{t}</h3>\n    {qa}')
faq_new = ('<section class="tone has-bgword" id="faq">\n  <div class="bg-word" aria-hidden="true">FAQ</div>\n  <div class="wrap">\n'
           '    <div class="sec-head fade-target">\n      <h2><span class="hbox">よくある質問</span></h2><span class="en-label">FAQ</span>\n    </div>\n'
           + '\n'.join(groups) + '\n  </div>\n</section>')
top_faq = one(r'<section class="tone has-bgword" id="faq">.*?</section>', top).group(0)
top = top.replace(top_faq, req_s + '\n' + flow_s + '\n' + faq_new, 1)

# --- ページ内メニュー -----------------------------------------------------------
PNAV = [('jobs', '職種紹介'), ('career', 'キャリアステップ'), ('first-step', '未経験からの1年'), ('support', '資格取得支援'),
        ('people', '社員紹介'), ('day', '1日の流れ'), ('requirements', '募集要項'), ('flow', '選考の流れ'), ('faq', 'よくある質問')]
for a, _ in PNAV:
    assert f'id="{a}"' in top, a
li = ''.join(f'<li><a href="#{a}">{t}</a></li>' for a, t in PNAV)
li += '<li><a href="design3-recruit-entry.html" class=" entry">エントリー</a></li>'
top = re.sub(r'<nav class="sibnav">.*?</nav>', f'<nav class="sibnav pnav" aria-label="ページ内メニュー"><div class="wrap"><ul>{li}</ul></div></nav>', top, count=1, flags=re.S)
SPY = ('<script>/* ページ内メニュー：スクロール位置の見出しを現在地に */(function(){var as=[].slice.call(document.querySelectorAll(".pnav a[href^=\'#\']"));'
       'var ss=as.map(function(a){return document.getElementById(a.getAttribute("href").slice(1));});'
       'function f(){var y=innerHeight*.35,c=-1;ss.forEach(function(s,i){if(s&&s.getBoundingClientRect().top<y)c=i;});'
       'as.forEach(function(a,i){a.classList.toggle("cur",i===c);});if(c>=0){var a=as[c],u=a.parentNode.parentNode;u.scrollLeft+=a.getBoundingClientRect().left-u.getBoundingClientRect().left-40;}}'
       'addEventListener("scroll",f,{passive:true});f();})();</script>\n')
top = top.replace('<section class="cta3">', SPY + '<section class="cta3">', 1)
open(P('design3-recruit.html'), 'w').write(top)

# --- 退避・削除 -----------------------------------------------------------------
for n in ('design3-recruit-job.html', 'design3-recruit-requirements.html', 'design3-recruit-faq.html'):
    os.remove(P(n))
for v in 'bc':
    for n in ('job', 'requirements', 'faq'):
        f = P(f'design31{v}-recruit-{n}.html')
        if os.path.exists(f):
            shutil.move(f, BK)

# --- リンク付け替え・gnav から採用情報を削除・他ページの sibnav ------------------
SIB = ('<nav class="sibnav"><div class="wrap"><ul><li><a href="design3-recruit.html" class="">採用トップ</a></li>'
       '<li><a href="design3-recruit-interview.html" class="{iv}">社員インタビュー</a></li>'
       '<li><a href="design3-recruit-entry.html" class="{en} entry">エントリー</a></li></ul></div></nav>')
for f in sorted(glob.glob(P('design3-*.html'))) + [P('design31a-top.html')]:
    h = open(f).read(); o = h
    h = re.sub(r'design3-recruit-job\.html#(job\d)', r'design3-recruit.html#\1', h)
    h = h.replace('design3-recruit-job.html', 'design3-recruit.html#jobs')
    h = h.replace('design3-recruit-requirements.html', 'design3-recruit.html#requirements')
    h = h.replace('design3-recruit-faq.html', 'design3-recruit.html#faq')
    h = h.replace('<li><a href="design3-recruit.html">採用情報</a></li>', '')
    b = os.path.basename(f)
    if b in ('design3-recruit-interview.html', 'design3-recruit-entry.html'):
        cur = 'iv' if 'interview' in b else 'en'
        h = re.sub(r'<nav class="sibnav">.*?</nav>', SIB.format(iv='cur' if cur == 'iv' else '', en='cur' if cur == 'en' else ''), h, count=1, flags=re.S)
    if h != o:
        open(f, 'w').write(h)
print('ok')
