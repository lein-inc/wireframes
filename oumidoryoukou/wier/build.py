# -*- coding: utf-8 -*-
"""近江度量衡 Webリニューアル ワイヤーフレーム（wier）ジェネレータ
原稿シート（16lXY…）の「近江度量衡様 修正案」を最優先、無ければ「参考」を採用。
更新性/利便性はサイトマップ(ver3)を反映（CMS更新ページに更新マーク）。
"""
import os
OUT = os.path.dirname(os.path.abspath(__file__))

# 共有プレビュー用の認証（GitHub Pages公開時）※コメント機能は廃止
AUTH_HEAD = '<script src="_auth.js"></script>'

# ---------- 共通パーツ ----------
def ph(label, cls="", style=""):
    return f'<div class="ph {cls}" style="{style}"><span>{label}</span></div>'

def cms(text="CMS更新"):
    return f'<span class="cms-flag">◯ {text}</span>'

def todo(text="要確認/素材待ち"):
    return f'<span class="todo-flag">★ {text}</span>'

CORP_NAV = [
    ("製品・技術", "products.html"),
    ("サービス案内", "service.html"),
    ("納入実績", "delivery.html"),
    ("会社案内", "company.html"),
    ("126年ヒストリー", "history.html"),
    ("新着情報", "news.html"),
]
RECRUIT_NAV = [
    ("採用TOP", "recruit.html"),
    ("社員インタビュー", "recruit-interview.html"),
    ("採用ニュース", "recruit-news.html"),
    ("募集要項", "recruit-jobs.html"),
]

def _nav(items, active):
    out = ""
    for n, u in items:
        cls = ' class="active"' if u == active else ''
        out += f'<a href="{u}"{cls}>{n}</a>'
    return out

# ── d_3 グローバルナビ定義（TOPと同テイスト：メガメニュー＋ハンバーガー） ──
# key, ラベル, 直リンク, メガ種別('cards'|'links'|None), 子項目[(名称,URL)]
NAV_GROUPS = [
    ("products", "製品・技術", "products.html", "cards", [
        ("農産物用計量システム", "products-agricultural.html"),
        ("穀類用計量システム", "products-weighing.html"),
        ("工業用計量システム", "products-industry.html"),
        ("その他・特殊用途", "products-other.html"),
    ]),
    ("service", "サービス案内", "service.html", None, []),
    ("delivery", "納入実績", "delivery.html", None, []),
    ("company", "会社案内", "company.html", "links", [
        ("企業理念", "company.html#concept"), ("代表挨拶", "company.html#greeting"),
        ("サービス拠点", "company.html#servicebase"), ("品質・認証", "company.html#quality"),
        ("会社概要", "company.html#profile"),
    ]),
    ("history", "126年ヒストリー", "history.html", None, []),
    ("recruit", "採用情報", "recruit.html", "links", [
        ("社員インタビュー", "recruit-interview.html"), ("採用ニュース", "recruit-news.html"),
        ("募集要項", "recruit-jobs.html"), ("新卒採用", "recruit-jobs-graduate.html"),
        ("中途採用", "recruit-jobs-career.html"),
    ]),
]
NAV_EN = {"products":"Products","service":"Service","company":"Company","recruit":"Recruit"}

def _active_key(active):
    a = active or ""
    if a.startswith("products"): return "products"
    if a == "service.html": return "service"
    if a == "delivery.html": return "delivery"
    if a == "company.html": return "company"
    if a == "history.html": return "history"
    if a.startswith("recruit"): return "recruit"
    return ""

def header(active="", recruit=False, overlay=False):
    akey = _active_key(active)
    items_html = ""
    dr_html = ""
    for key, label, url, mega, children in NAV_GROUPS:
        is_active = " is-active" if key == akey else ""
        if not children:
            items_html += f'<div class="witem{is_active}"><a class="wlink" href="{url}">{label}</a></div>'
            dr_html += f'<a class="wdrawer__single" href="{url}">{label}</a>'
            continue
        en = NAV_EN.get(key, label)
        links = "".join(f'<a href="{cu}"><i class="ar">→</i>{cn}</a>' for cn, cu in children)
        items_html += (
            f'<div class="witem{is_active}">'
            f'<a class="wlink" href="{url}">{label}</a>'
            f'<div class="wmega"><div class="wmega__inner">'
            f'<div class="wmega__lead"><span class="men">{en}</span><span class="mjp">{label}</span>'
            f'<a class="wmega__more" href="{url}">詳しく見る →</a></div>'
            f'<div class="wmega__links">{links}</div>'
            f'</div></div></div>')
        sub = "".join(f'<a href="{cu}">{cn}</a>' for cn, cu in children)
        dr_html += (f'<div class="wdrawer__group"><button class="wdrawer__top">{label}</button>'
                    f'<div class="wdrawer__sub">{sub}</div></div>')
    return f'''<header class="wnav">
  <a class="wnav__logo" href="top.html"><span class="tlogo">近江度量衡株式会社</span></a>
  <nav class="wnav__menu">{items_html}</nav>
  <button class="wburger" aria-label="メニュー" aria-expanded="false"><span></span><span></span><span></span></button>
  <a class="wnav__cta" href="contact.html">お問い合わせ</a>
</header>
<div class="wdrawer" id="wdrawer" aria-hidden="true"><nav>{dr_html}<a class="wdrawer__single" href="contact.html">お問い合わせ</a></nav></div>
<div class="wrail"><span class="wrail__cap">News</span>
<div class="wrail__news">
<a class="wrail__item is-on" href="news-detail.html"><b>2026.07.01</b><span>夏季休業のお知らせ（8/13〜8/16）</span></a>
<a class="wrail__item" href="news-detail.html"><b>2026.06.20</b><span>フルオートドライヤー納入事例を公開しました</span></a>
<a class="wrail__item" href="news-detail.html"><b>2026.06.01</b><span>2027年度 採用情報を更新しました</span></a>
</div>
<span class="wrail__label">Kusatsu, Shiga</span></div>'''

def breadcrumb(items):
    parts = []
    for i,(label,url) in enumerate(items):
        if url and i < len(items)-1:
            parts.append(f'<a href="{url}">{label}</a>')
        else:
            parts.append(f'<span style="color:#333">{label}</span>')
    return '<nav class="breadcrumb"><div class="inner">' + '<span>›</span>'.join(parts) + '</div></nav>'

def footer(recruit=False):
    # index_8トーンのワイヤー共通フッター（ブランド/サイトマップ/CONTACT箱＋採用バナー）
    return '''
<footer class="wfoot">
  <div class="wfoot__grid">
    <div class="wfoot__brand">
      <p class="name">近江度量衡株式会社</p>
      <p>〒525-0054<br>滋賀県草津市東矢倉三丁目11番70号<br>TEL 077-562-7111 ／ FAX 077-562-7116<br><a href="company.html#servicebase">Google map</a></p>
    </div>
    <nav class="wfoot__nav">
      <div>
        <a href="top.html">トップページ</a>
        <a href="products.html">製品・技術</a>
        <a class="sub" href="products-agricultural.html">農産物用計量システム</a>
        <a class="sub" href="products-weighing.html">穀類用計量システム</a>
        <a class="sub" href="products-industry.html">工業用計量システム</a>
        <a class="sub" href="products-other.html">その他・特殊用途</a>
        <a href="service.html">サービス案内</a>
        <a href="delivery.html">納入実績</a>
      </div>
      <div>
        <a href="company.html">会社案内</a>
        <a href="history.html">126年ヒストリー</a>
        <a href="news.html">新着情報</a>
        <a href="recruit.html">採用情報</a>
        <a href="contact.html">お問い合わせ</a>
        <a href="privacy.html">プライバシーポリシー</a>
      </div>
    </nav>
    <div class="wfoot__contact">
      <span class="en">( Contact )</span>
      <h3>お問い合わせ・ご相談</h3>
      <p>お気軽にご相談ください。<br>お見積もり依頼も可能です。</p>
      <a class="cbtn" href="contact.html">Contact Form <i class="ar">→</i></a>
    </div>
  </div>
  <a class="wfoot__recruit" href="recruit.html">
    <span class="rtxt"><span class="en">Recruitment 2027</span><h3>「いきる」の単位とは、なんだろう。</h3></span>
    <span class="go">採用情報を見る →</span>
  </a>
  <div class="wfoot__bar"><span>OMISCALE CO.,LTD.</span><span>© 近江度量衡株式会社 ALL RIGHTS RESERVED.</span></div>
</footer>'''

def page(filename, title, body, active="", recruit=False, crumbs=None, overlay=False):
    bc = breadcrumb(crumbs) if crumbs else ""
    cls = ' class="theme-recruit"' if recruit else ""
    html = f'''<!DOCTYPE html>
<html lang="ja"{cls}>
<head>
{AUTH_HEAD}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
{header(active, recruit, overlay)}
<div class="wwrap">
{bc}
{body}
{footer(recruit)}
</div>
<script src="_nav.js"></script>
</body>
</html>'''
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    return filename

PAGES = []  # 後でindex生成に使う: (No, 名称, url, file, group, cms)

# ======================= A. TOP =======================
top_body = '''
<section class="fv fv--full fv--center">
  <div class="fv__bg">
    <div class="fv__ph"><span>FV：全画面動画エリア（枠のみ・動画は後で挿入）</span></div>
  </div>
  <div class="fv__content">
    <h1 class="fv__title"><span>「いきる」をはかり、</span><span>豊かな世界へ。</span></h1>
  </div>
  <div class="fv__scroll">SCROLL</div>
</section>

<!-- ② 採用テザー（FV直下バナー） -->
<div class="recruit-banner">
  <div class="recruit-banner__inner">
    <div class="recruit-banner__text"><h2>「いきる」の単位とは、なんだろう。</h2><p>RECRUITMENT 採用情報</p></div>
    <div class="recruit-banner__cta"><a class="btn btn--white" href="recruit.html">採用サイトへ ↗</a></div>
  </div>
</div>

<!-- ③ PRODUCTS -->
<section class="section">
  <div class="container">
    <p class="section-meta">Products &amp; Technology</p>
    <h2 class="section-title">製品・技術紹介</h2>
    <div class="grid-4" style="margin-top:32px;">
      <a class="card" href="products-agricultural.html"><div class="card__img">''' + ph('農産物 選果イメージ') + '''</div><div class="card__body"><div class="card__title">農産物用計量システム</div><p class="card__text">果物・野菜向けの計量・選別システム。品質管理・等級選別に対応。</p></div></a>
      <a class="card" href="products-weighing.html"><div class="card__img">''' + ph('穀類施設イメージ') + '''</div><div class="card__body"><div class="card__title">穀類用計量システム</div><p class="card__text">米・大豆などの穀類計量システム。全国約2,000施設への納入実績。</p></div></a>
      <a class="card" href="products-industry.html"><div class="card__img">''' + ph('工場ラインイメージ') + '''</div><div class="card__body"><div class="card__title">工業用計量システム</div><p class="card__text">ガラス・鉄鋼・肥料・化学など7カテゴリに対応する計量ソリューション。</p></div></a>
      <a class="card" href="products-other.html"><div class="card__img">''' + ph('特殊用途イメージ') + '''</div><div class="card__body"><div class="card__title">その他・特殊用途</div><p class="card__text">家畜・競走馬向け動物計量など、特殊用途の計量システム。</p></div></a>
    </div>
  </div>
</section>

<!-- ④ 納入実績テザー -->
<section class="section section--grey">
  <div class="container">
    <div class="grid-2" style="align-items:center;">
      <div>''' + ph('導入現場 写真（選果場／カントリーエレベーター／工場ライン）','','aspect-ratio:4/3') + '''</div>
      <div>
        <p class="section-meta">Delivery Record</p>
        <h2 class="section-title">導入事例・納入実績</h2>
        <p class="section-lead">農産物選果場・米麦カントリーエレベーター・工場ラインなど、多岐にわたる現場への納入実績をご紹介します。</p>
        <a class="btn btn--outline btn--sm" href="delivery.html" style="margin-top:24px;">納入実績を見る</a>
      </div>
    </div>
  </div>
</section>

<!-- ⑤ STATEMENT -->
<section class="section section--dark">
  <div class="container statement">
    <p class="statement__en">OUR STATEMENT</p>
    <h2 class="statement__main">「いきる」をはかり、豊かな世界へ。</h2>
    <p class="statement__body">1900年の創業以来、客観的に、正確に「はかる」ことを命題として歩んできた近江度量衡。農産物から工業製品まで——あらゆる現場で今も使われ続けている、現在進行形の技術力と誠実さ。「はかる」という仕事を通じて、日本と世界の社会を確かに支え続けること。それが、126年間変わらない私たちの使命です。</p>
    <div class="grid-3" style="margin-top:48px;text-align:left;">
      <div class="pillar"><div class="pillar__no">社是 01</div><div class="pillar__title">社会への貢献</div><p class="pillar__body">企業を通じた社会貢献と従業員の生活向上</p></div>
      <div class="pillar"><div class="pillar__no">社是 02</div><div class="pillar__title">技術の公用</div><p class="pillar__body">技術発展と優良品の製造</p></div>
      <div class="pillar"><div class="pillar__no">社是 03</div><div class="pillar__title">互助の精神</div><p class="pillar__body">職場の繁栄に向けた互助・協力</p></div>
    </div>
  </div>
</section>

<!-- ⑥ HISTORY ダイジェスト -->
<section class="section">
  <div class="container">
    <p class="section-meta">126 Years History</p>
    <h2 class="section-title">明治から令和へ。測り続けた126年。</h2>
    <p class="section-lead">1900年の創業から現在まで、時代とともに進化してきた近江度量衡の歩みをダイジェストでご紹介します。</p>
    <div class="timeline" style="margin-top:32px;">
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">明治33年</span><span class="timeline-year__num">1900</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>創業</h3><p>滋賀県にて計量器の製造・販売を開始。農産物の取引計量を支える地域の職人集団として出発。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">昭和中期</span><span class="timeline-year__num">1950s</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>選果機需要が急拡大</h3><p>高度経済成長期、農協向け選果・計量システムの供給体制を確立。全国への展開が始まる。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">平成12年</span><span class="timeline-year__num">2000</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>ISO 9001 認証取得</h3><p>品質保証体制を国際規格で整備。全数検査・精度管理の仕組みを標準化。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">平成期</span><span class="timeline-year__num">2010s</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>海外展開開始（上海・バンコク・韓国）</h3><p>アジアの農産物・食品産業の成長とともに海外3拠点を設立。技術と誇りを海外へ。</p></div></div>
      <div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">令和7年</span><span class="timeline-year__num">2025</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>創業126周年</h3><p>国内6拠点・海外3拠点・累計2,000施設への納入実績。次の126年へ向けたWebリニューアルプロジェクト進行中。</p></div></div>
    </div>
    <a class="btn btn--outline btn--sm" href="history.html" style="margin-top:32px;">126年ヒストリーを見る</a>
  </div>
</section>

<!-- ⑦ RECRUITMENT -->
<section class="section section--dark theme-recruit" style="background:#111315;">
  <div class="container">
    <p class="statement__en" style="color:#888;">RECRUITMENT</p>
    <h2 class="statement__main" style="text-align:left;color:#fff;">「いきる」の単位とは、なんだろう。</h2>
    <p class="section-lead" style="color:#bbb;">地に足のついた仕事のリアル・職場環境・社員の声——飾らず正直に。あなたの確かな仕事で、豊かな未来を担う力になる。</p>
    <div class="entry-split" style="margin-top:40px;">
      <div class="entry-card"><div class="entry-card__label">NEW GRADUATE 新卒採用</div><div class="entry-card__copy">「未来を、ここからはかる。」</div><p class="entry-card__desc">理系・工学系だけじゃない。着実にものをつくる誠実さに共感できる人を求めています。</p><a class="btn btn--red" href="recruit-jobs-graduate.html" style="background:#111315;color:#fff;">新卒採用を見る</a></div>
      <div class="entry-card"><div class="entry-card__label">MID-CAREER 中途採用</div><div class="entry-card__copy">「培った経験を、126年の精度に加えてください。」</div><p class="entry-card__desc">年齢・業界不問。あなたの経験が、次の100年の基盤になる。</p><a class="btn btn--red" href="recruit-jobs-career.html" style="background:#111315;color:#fff;">中途採用を見る</a></div>
    </div>
  </div>
</section>

<!-- ⑧ PEOPLE -->
<section class="section section--grey">
  <div class="container">
    <p class="section-meta">People</p>
    <h2 class="section-title">技術と誇りを持って働く、近江の現場のことば。</h2>
    <p class="section-lead">現場・設計・営業——それぞれの視点で語る、近江度量衡の仕事。''' + todo('実在する社員情報・コメントに差し替え') + '''</p>
    <div class="grid-3" style="margin-top:32px;">
      <div class="interview-card"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">製造部</div><div class="interview-card__name">山田 〇〇</div><p class="interview-card__quote">毎回違う課題に向き合うから、技術者として本当に成長できる。誇りを持てる仕事です。</p></div></div>
      <div class="interview-card"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">設計部</div><div class="interview-card__name">鈴木 〇〇</div><p class="interview-card__quote">図面通りにつくるのではなく、現場に合わせてつくる。グローバルな現場を支える実感があります。</p></div></div>
      <div class="interview-card"><div class="interview-card__img">''' + ph('社員写真') + '''</div><div class="interview-card__body"><div class="interview-card__dept">営業部</div><div class="interview-card__name">田中 〇〇</div><p class="interview-card__quote">お客様の現場を見て、何が必要か考える。「いきる」をはかるという仕事の意味がここにあります。</p></div></div>
    </div>
    <a class="btn btn--outline btn--sm" href="recruit-interview.html" style="margin-top:32px;">社員インタビューを見る</a>
  </div>
</section>

<!-- ⑨ NEWS -->
<section class="section">
  <div class="container">
    <p class="section-meta">News</p>
    <h2 class="section-title">新着情報 ''' + cms('クライアント更新') + '''</h2>
    <ul class="news-list" style="margin-top:24px;">
      <li class="news-item"><span class="news-item__date">2025.06.01</span><span class="news-item__cat">お知らせ</span><span class="news-item__title">北海道営業所を開設しました</span></li>
      <li class="news-item"><span class="news-item__date">2025.03.01</span><span class="news-item__cat">お知らせ</span><span class="news-item__title">会社設立126周年を達成しました</span></li>
      <li class="news-item"><span class="news-item__date">2025.04.01</span><span class="news-item__cat">採用</span><span class="news-item__title">2027年度採用エントリー受付開始のご案内</span></li>
    </ul>
    <div class="cms-note">★ 表示はサンプル。実際の記事はクライアントがWordPress管理画面から都度更新（月1〜2本）。</div>
    <a class="btn btn--outline btn--sm" href="news.html" style="margin-top:24px;">新着情報一覧へ</a>
  </div>
</section>
'''
# 【TOP は別管理】TOPページは d_3 デザインベースの専用HTML（モノトーン・ダミー、自己完結のCSS/JS）を
#   手管理しているため、build.py では top.html を生成・上書きしない。
#   （旧ワイヤーTOPの top_body は未使用。レイアウト参考として残置）
# page("top.html", "近江度量衡株式会社｜「いきる」をはかり、豊かな世界へ。", top_body, active="", overlay=True)
PAGES.append(("A","トップページ","/","top.html","corp",False))

# ======================= B. 製品・技術紹介 =======================
products_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">PRODUCTS &amp; TECHNOLOGY</p>
  <h1 class="page-header__title">製品・技術紹介</h1>
  <p class="page-header__lead">農産物・穀類・工業用など、あらゆる現場の計量ニーズに一品一様で応えます。</p>
</div></header>
<section class="section"><div class="container">
  <div class="grid-2">
    <a class="cat-card" href="products-agricultural.html"><div class="cat-card__img">''' + ph('AGRICULTURAL イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">AGRICULTURAL</div><div class="cat-card__title">農産物用計量システム</div><p class="cat-card__desc">果物・野菜向けの計量・選別システム。品質管理・等級選別に対応。</p><span class="cat-card__link">詳しく見る →</span></div></a>
    <a class="cat-card" href="products-weighing.html"><div class="cat-card__img">''' + ph('GRAIN イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">GRAIN</div><div class="cat-card__title">穀類用計量システム</div><p class="cat-card__desc">米・大豆などの穀類計量システム。全国約2,000施設への納入実績。</p><span class="cat-card__link">詳しく見る →</span></div></a>
    <a class="cat-card" href="products-industry.html"><div class="cat-card__img">''' + ph('INDUSTRIAL イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">INDUSTRIAL</div><div class="cat-card__title">工業用計量システム</div><p class="cat-card__desc">ガラス・鉄鋼・肥料・化学など7カテゴリに対応する計量ソリューション。</p><span class="cat-card__link">詳しく見る →</span></div></a>
    <a class="cat-card" href="products-other.html"><div class="cat-card__img">''' + ph('OTHERS イメージ') + '''</div><div class="cat-card__body"><div class="cat-card__slug">OTHERS</div><div class="cat-card__title">その他・特殊用途</div><p class="cat-card__desc">家畜・競走馬向け動物計量など、特殊用途の計量システム。</p><span class="cat-card__link">詳しく見る →</span></div></a>
  </div>
  <div class="cms-note">◯ 製品ページは投稿（カスタム投稿）で管理。新製品・新設備竣工時にクライアントが追加・更新（年1〜2件想定）。''' + cms('CMS更新') + '''</div>
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">製品・技術についてのお問い合わせ</h2><p>仕様・価格・納期・カスタマイズについてはご相談可能な体制を整備。</p></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products.html","製品・技術紹介｜近江度量衡株式会社", products_body, active="products.html",
     crumbs=[("TOP","top.html"),("製品・技術紹介",None)])
PAGES.append(("B","製品・技術紹介","/products/","products.html","corp",True))

# ---- 製品サブページ共通テンプレ ----
def product_detail(slug_en, name, desc, features, uses, assets_note=""):
    feat = "".join(f'<li>{f}</li>' for f in features)
    use = "".join(f'<div class="use-item"><span class="use-item__no">用途 0{i+1}</span>{u}</div>' for i,u in enumerate(uses))
    asset = ('<div class="cms-note">参考素材（Drive）：' + assets_note + '</div>') if assets_note else ''
    return '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">''' + slug_en + '''</p>
  <h1 class="page-header__title">''' + name + '''</h1>
</div></header>
<section class="section"><div class="container grid-2" style="align-items:start;">
  <div>''' + ph(name + ' 製品イメージ／図解','','aspect-ratio:4/3') + asset + '''</div>
  <div><p class="section-lead" style="margin-top:0;">''' + desc + '''</p>
  <div class="cms-note" style="background:#fff7ec;border-left-color:#e0a030;">注記：詳細仕様・写真は機密保持の都合により非掲載。別途資料をご請求ください。</div></div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Features</p><h2 class="section-title">主な特長</h2>
  <ul class="feature-list" style="margin-top:24px;max-width:760px;">''' + feat + '''</ul>
</div></section>
<section class="section"><div class="container">
  <p class="section-meta">Use Case</p><h2 class="section-title">主な用途・導入現場</h2>
  <div class="use-grid" style="margin-top:24px;">''' + use + '''</div>
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">''' + name + '''についてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''

def pdf_box(title, meta, href):
    return ('<div class="pdf-box"><div class="pdf-box__ic">PDF</div>'
      '<div class="pdf-box__body"><div class="pdf-box__title">'+title+'</div>'
      '<div class="pdf-box__meta">'+meta+'</div></div>'
      '<div class="pdf-box__btns"><a class="btn btn--dark btn--sm" href="'+href+'" target="_blank">PDFを開く</a>'
      '<a class="btn btn--outline btn--sm" href="'+href+'" download>ダウンロード</a></div></div>')

def machine(en, jp, target, bullets, imglabel):
    b = "".join('<li>'+x+'</li>' for x in bullets)
    return ('<div class="case" style="margin-top:24px;"><div class="case__img">'+ph(imglabel)+'</div>'
      '<div class="case__body"><div class="machine-meta">'+en+'</div>'
      '<div class="case__title" style="margin:0;">'+jp+'</div>'
      '<div class="machine-target">'+target+'</div>'
      '<ul class="feature-list" style="margin-top:4px;">'+b+'</ul></div></div>')

# ===== B1 農産物用：OMI STAR シリーズ（2021 STARパンフレット反映） =====
agri_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">AGRICULTURAL</p>
  <h1 class="page-header__title">農産物用計量システム</h1>
  <p class="page-header__lead">選別機の新星「OMI STAR シリーズ」が「はかる」技術をさらに加速。柑橘から小粒農産物・根菜類まで、農産物を選ばない 3ライン＋α でお応えします。</p>
</div></header>
<section class="section"><div class="container">
  <p class="section-meta">STAR Series</p>
  <h2 class="section-title">画期的な技術を結集した高精度の選果システム</h2>
  <p class="section-lead">農産物選果は新しい時代へ。重量・外観を高精度に「はかる」3つの選別機（Rollerstar／Millistar／Calistar）＋ 柑橘選果システム（＋α）で、産地・農協の現場に一品一様で対応します。''' + todo('製品写真：Calistar.jpg / Millister.jpg / Rollerster.jpg（Drive B_製品）') + '''</p>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">3 Lines</p><h2 class="section-title">STAR シリーズ 3機種</h2>
''' + machine("Rollerstar ／ ローラスター","柑橘・落葉果実・トマト などの農産物の選別に最適",
      "対応：柑橘・落葉果実・トマト",
      ["二個乗りを防ぐ独自の整列機構","1グラム単位で正確に重量を測定できる「はかる」技術","最大16個／秒／条を正確に選別仕分けできる高能力を実現"],
      "Rollerstar 製品写真") + machine("Millistar ／ ミリスター","ミニトマト・キンカン など小粒農産物を選別仕分け",
      "対応：ミニトマト・キンカン・小粒農作物",
      ["25個／秒／条で農産物を選別仕分けする能力","二個乗りを確実に防ぐ整列コンベアが選果能力をアシスト","1つのワークを8面画像認識し形状や色彩を見分ける Advanced Vision 搭載","低騒音で働く人にやさしい作業環境を実現"],
      "Millistar 製品写真") + machine("Calistar ／ キャリスター","根菜類・パプリカ・玉ねぎ・柑橘 など農産物を選ばないオールランダー",
      "対応：根菜類・パプリカ・玉ねぎ・柑橘 ほか",
      ["吊り下げ方式搬送体が更に高精度な重量測定を実現","小さなものから大きなものまで確実にホールドできるクリッパー","吊り下げ方式の搬送体だから実現できる低落差","根菜類など土モノの土砂の影響を受けない安心構造"],
      "Calistar 製品写真") + '''
  <div class="cms-note">＋α：高精度・高性能の「柑橘選果システム」もラインアップ。</div>
</div></section>
<section class="section"><div class="container">
  <p class="section-meta">Case Study</p><h2 class="section-title">導入事例</h2>
  <div class="grid-3" style="margin-top:24px;">
    <div class="card"><div class="card__img">''' + ph('JA熊本うき 宇城柑橘選果場') + '''</div><div class="card__body"><div class="card__title">JA熊本うき 宇城柑橘選果場様</div><p class="card__text">世界初、温州みかんを予冷から同一ラインで選果可能にした大型プラント。</p></div></div>
    <div class="card"><div class="card__img">''' + ph('奄美市 奄美大島選果場') + '''</div><div class="card__body"><div class="card__title">奄美市 奄美大島選果場様</div><p class="card__text">高精度の内部・外部品質管理を実現した、奄美タンカン選果ライン。</p></div></div>
    <div class="card"><div class="card__img">''' + ph('有限会社さもと農園') + '''</div><div class="card__body"><div class="card__title">三重県 有限会社さもと農園様</div><p class="card__text">機能を絞った小規模プラントにも対応。</p></div></div>
  </div>
  ''' + pdf_box("2021 STAR シリーズ パンフレット","農産物選別機 Rollerstar／Millistar／Calistar（PDF）","assets/star-series.pdf") + '''
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">農産物用計量システムについてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products-agricultural.html","農産物用計量システム｜近江度量衡株式会社", agri_body,
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("農産物用",None)])
PAGES.append(("B1","農産物用計量システム","/products/agricultural/","products-agricultural.html","corp",True))

# ===== B2 穀類用：フルオートドライヤーシステム（DRYER SYSTEM反映） =====
grain_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">GRAIN</p>
  <h1 class="page-header__title">穀類用計量システム</h1>
  <p class="page-header__lead">全国約2,000施設への納入実績。サンプル全自動自主検査「フルオートドライヤーシステム」で、穀類の自主検査工程を効率化します。</p>
</div></header>
<section class="section"><div class="container grid-2" style="align-items:start;">
  <div>''' + ph('フルオートドライヤーシステム 本体（CFD-120）','','aspect-ratio:4/3') + todo('製品写真：image_main / image_3D / image_panel（Drive B_製品 フルオートドライヤー）') + '''</div>
  <div>
    <p class="section-meta">OMI Total Full-Automatic Dryer System</p>
    <h2 class="section-title" style="font-size:24px;">フルオートドライヤーシステム</h2>
    <p class="section-lead" style="margin-top:12px;">業界初のサンプル全自動自主検査装置が、さらなる高効率化を実現してフルモデルチェンジ。200年以上の穀類フルオートドライヤー納入で培ったノウハウを結集し、現代のプラント設備に求められる性能を高い完成度で実現した新型システムです。<strong>米・麦・大豆の3品目兼用。</strong></p>
  </div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Feature</p><h2 class="section-title">特長</h2>
  <div class="feat-grid">
    <div class="feat-item"><div class="no">01</div><h4>省人化</h4><p>計量・乾燥・検査の全工程をオートメーション化。</p></div>
    <div class="feat-item"><div class="no">02</div><h4>省エネ</h4><p>乾燥精度をたもつ消費電力の抑え込み制御。</p></div>
    <div class="feat-item"><div class="no">03</div><h4>省スペース</h4><p>約64%削減したコンパクトなサイズ。</p></div>
    <div class="feat-item"><div class="no">04</div><h4>3品目兼用</h4><p>米・大豆・麦の3品目兼用が可能。</p></div>
    <div class="feat-item"><div class="no">05</div><h4>トータルコスト</h4><p>更新時の据置工程を統合しトータルコスト削減。</p></div>
  </div>
</div></section>
<section class="section"><div class="container">
  <p class="section-meta">Flow</p><h2 class="section-title">工程</h2>
  <div class="process" style="margin-top:24px;">
    <div class="process-step"><div class="process-step__num">01</div><div class="process-step__title">投入</div></div>
    <div class="process-step"><div class="process-step__num">02</div><div class="process-step__title">計量</div></div>
    <div class="process-step"><div class="process-step__num">03</div><div class="process-step__title">サンプル抽出</div></div>
    <div class="process-step"><div class="process-step__num">04</div><div class="process-step__title">乾燥</div></div>
    <div class="process-step"><div class="process-step__num">05</div><div class="process-step__title">検査</div></div>
  </div>
  <div class="grid-3" style="margin-top:32px;">
    <div class="value-item"><div class="value-item__title" style="font-size:15px;">搬送部</div><p class="value-item__body">搬送用ロボットアーム・昇降エレベーター・定量供給で、サンプルを確実に搬送。</p></div>
    <div class="value-item"><div class="value-item__title" style="font-size:15px;">サンプルボックス</div><p class="value-item__body">10ボックス×6段×2テーブル、計120サンプルを管理。</p></div>
    <div class="value-item"><div class="value-item__title" style="font-size:15px;">オートチェッカー</div><p class="value-item__body">抽出したサンプルを自動で検査し、自主検査工程を全自動化。</p></div>
  </div>
</div></section>
<section class="section section--grey" id="spec"><div class="container">
  <p class="section-meta">Spec &amp; Dimension</p><h2 class="section-title">仕様・寸法図（ドライヤー本体）</h2>
  <div class="spec-2col">
    <figure class="dim-figure"><img src="assets/dryer-dimension.png" alt="フルオートドライヤーシステム 寸法図"><figcaption>DIMENSION 寸法図（裏表紙より）</figcaption></figure>
    <table class="info-table" style="background:#fff;">
      <tr><th>型式</th><td>CFD-120</td></tr>
      <tr><th>対象物</th><td>穀類（米・麦・大豆）</td></tr>
      <tr><th>本体寸法（出荷時）</th><td>幅 2,020 × 高さ 1,800 × 奥行 700（mm）</td></tr>
      <tr><th>処理量</th><td>120サンプル（10ボックス×6段×2テーブル）</td></tr>
      <tr><th>操作部</th><td>7インチ型タッチパネル</td></tr>
      <tr><th>塗装色</th><td>マンセル 5Y7/1</td></tr>
      <tr><th>サンプルボックス最大投入量</th><td>約 800g（粉）</td></tr>
      <tr><th>機器重量</th><td>850kg</td></tr>
      <tr><th>消費電力</th><td>200V 約3.6kW 4.2KVA 18A</td></tr>
      <tr><th>消費エアー量</th><td>25L/min</td></tr>
      <tr><th>排風量</th><td>12㎥/min（50Hz）／14㎥/min（60Hz）</td></tr>
      <tr><th>備考</th><td>最大4台での連結可能／ヒーター自動温度制御／セーフティスイッチ／機内照明搭載</td></tr>
    </table>
  </div>
  ''' + pdf_box("フルオートドライヤーシステム 製品資料","OMI TOTAL FULL-AUTOMATIC DRYER SYSTEM（特長・工程・仕様・寸法図／PDF）","assets/dryer-system.pdf") + '''
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">穀類用計量システムについてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products-weighing.html","穀類用計量システム｜近江度量衡株式会社", grain_body,
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("穀類用",None)])
PAGES.append(("B2","穀類用計量システム","/products/weighing/","products-weighing.html","corp",True))

# ===== B3 工業用：工業分野（会社案内2025 工業ページ反映） =====
ind_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">INDUSTRY</p>
  <h1 class="page-header__title">工業用計量システム</h1>
  <p class="page-header__lead">あらゆる工業分野で品質を支える「はかる」技術。</p>
</div></header>
<section class="section"><div class="container grid-2" style="align-items:center;">
  <div>
    <p style="font-size:14px;color:#444;line-height:2;">工業用ゴム、樹脂、ガラス、金属、化学薬品など、近江度量衡には様々な工業製品の原料や薬品の計量配合プラントの納入実績があります。液体、粉体、ペレット、顆粒状など様々な形状の原料をはかるノウハウで、産業分野を超えてお客様のニーズに応えます。</p>
  </div>
  <div>''' + ph('計量配合プラント 全体イメージ','','aspect-ratio:16/10') + '''</div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Products</p>
  <h2 class="section-title">一台の計量機から製造ライン全体まで。</h2>
  <p class="section-lead">高精度、高生産性の装置でものづくり現場を支えます。</p>
  <div class="grid-2" style="margin-top:28px;">
    <div class="card" style="background:#fff;"><div class="card__img">''' + ph('粉体原料用ホッパースケール') + '''</div><div class="card__body"><div class="card__title">粉体原料計量システム</div><p class="card__text">ガラス製品の製造工程では、計量だけでなく、原料の貯蔵・自動調合・ミキシング・定量供給装置など、製造工程のほとんどのプロセスの装置とシステムを手掛けます。流動性に優れた構造で、硬質素材と摩耗対策により高い耐久性を備えた高能力のシステムを提供しています。</p></div></div>
    <div class="card" style="background:#fff;"><div class="card__img">''' + ph('ゴム混練設備計量機') + '''</div><div class="card__body"><div class="card__title">タイヤ・工業用ゴム計量システム</div><p class="card__text">プラント全体における上流工程の原料計量設備、下流工程の完成品計量設備、その間の各ライン設備を設計・製作。さらに完全自動化のための生産管理統合システムを提供し、安定した精度を保ち、生産性向上と品質の保証に大きく寄与しています。</p></div></div>
  </div>
</div></section>
<section class="section"><div class="container grid-2" style="align-items:center;">
  <div>
    <p class="section-meta">Total Engineering</p>
    <h2 class="section-title" style="font-size:24px;">ソフトウェアもハードウェアも自社製造で一括管理</h2>
    <p class="section-lead">高精度な計量を実現するためには、機械設備の設計・製作だけでなく、それらを制御するシステム開発が欠かせません。電気設備の設計・構築を専門とする技術電装部を抱え、機械設備の設計を行う設計部、製造を担当する製造部が連携したトータルエンジニアリングで、お客様に安心してお使いいただけるシステムをお届けしています。</p>
  </div>
  <div>''' + ph('電子部品の組立まで自社で実施','','aspect-ratio:4/3') + '''</div>
</div></section>
<section class="section section--grey"><div class="container">
  ''' + pdf_box("会社案内パンフレット 2025年版","工業分野ほか 事業・技術紹介（PDF）","assets/company-2025.pdf") + '''
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">工業用計量システムについてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("products-industry.html","工業用計量システム｜近江度量衡株式会社", ind_body,
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("工業用",None)])
PAGES.append(("B3","工業用計量システム","/products/industry/","products-industry.html","corp",True))

page("products-other.html","その他・特殊用途｜近江度量衡株式会社",
  product_detail("OTHERS","その他・特殊用途",
    "家畜・競走馬向け動物計量など、特殊用途の計量システム。一品一様で多様な計量ニーズに対応します。",
    ["家畜・競走馬向け動物計量システム","特殊形状・特殊環境への個別対応","用途に応じた一品一様の設計・製造"],
    ["畜産施設","競走馬育成・管理施設","研究機関","その他特殊計量現場"]),
  active="products.html", crumbs=[("TOP","top.html"),("製品・技術紹介","products.html"),("その他",None)])
PAGES.append(("B4","その他・特殊用途","/products/other/","products-other.html","corp",True))

# ======================= C. サービス案内 =======================
service_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">SERVICE</p>
  <h1 class="page-header__title">サービス案内</h1>
  <p class="page-header__lead">計量・測定のあらゆるニーズに対応するサービスを提供します。</p>
</div></header>
<section class="section"><div class="container">
  <div class="grid-2" style="gap:1px;background:var(--c-border);border:1px solid var(--c-border);">
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">01</div><div class="value-item__title">企画・エンジニアリング</div><p class="value-item__body">計量対象の特性や仕様条件について事前調査とヒアリングを実施。豊富な実績から類似事例を紹介し、現場に合った最適なシステムをご提案します。</p></div>
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">02</div><div class="value-item__title">設計・制御・開発</div><p class="value-item__body">ソフトウェアとハードウェアともすべて自社で設計・開発をして品質と精度を保証する高品質な設計を実現します。</p></div>
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">03</div><div class="value-item__title">製作・施工</div><p class="value-item__body">合理性を追求しニュープロダクト・システムを採用。コストパフォーマンスの高いシステムを製作・施工します。</p></div>
    <div class="value-item" style="border:none;background:#fff;"><div class="value-item__num">04</div><div class="value-item__title">メンテナンス・アフターサービス</div><p class="value-item__body">納入後も営業・技術サービス員が定期巡回。機器を最良の状態で維持するサポートを継続的に提供します。</p></div>
  </div>
</div></section>
<section class="section section--grey"><div class="container">
  <p class="section-meta">Flow</p><h2 class="section-title">ご依頼の流れ</h2>
  <div class="flow" style="margin-top:24px;max-width:760px;">
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>お問い合わせ</h4><p>Webフォーム・電話にてご連絡ください。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>現地調査・ヒアリング</h4><p>現場の状況を確認し、ご要望を詳しくお聞きします。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>提案・見積</h4><p>最適なシステム構成をご提案します。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>設計・製造</h4><p>一品一様で設計・製造します。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>納品・設置調整</h4><p>現地への納品・据付・調整を行います。</p></div></div>
    <div class="flow-step"><div class="flow-step__num"></div><div class="flow-step__body"><h4>保守・サポート</h4><p>全国ネットワークで継続サポートします。</p></div></div>
  </div>
</div></section>
<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">サービス・保守についてのお問い合わせ</h2></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("service.html","サービス案内｜近江度量衡株式会社", service_body, active="service.html",
     crumbs=[("TOP","top.html"),("サービス案内",None)])
PAGES.append(("C","サービス案内","/service/","service.html","corp",False))

# ======================= D. 納入実績 =======================
# 納入実績：CASE01-03 の導入先をロゴボックスで列挙（ダミー・PC3/SP2カラム）
DELIV_LOGO_STYLE = '''<style>
.logogrid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:20px;}
.logobox{position:relative;border:1px solid var(--c-border);aspect-ratio:3/2;display:flex;align-items:center;justify-content:center;text-align:center;padding:14px;
  background-color:#f7f7f7;background-image:repeating-linear-gradient(45deg,rgba(0,0,0,.04) 0 8px,transparent 8px 16px);}
.logobox span{position:relative;background:rgba(255,255,255,.92);padding:6px 10px;font-size:12px;color:#555;line-height:1.4;font-family:var(--font-ja);}
@media(max-width:600px){.logogrid{grid-template-columns:repeat(2,1fr);}}
</style>'''

_DELIV_CASES = [
 ("01","AGRICULTURAL","農産物用計量システム 導入先",
   ["〇〇農業協同組合","〇〇青果市場","〇〇中央卸売市場","〇〇選果場","〇〇柑橘出荷組合","〇〇りんご選果所","〇〇玉葱センター","〇〇園芸農業協同組合","〇〇ファーム","〇〇農産"]),
 ("02","GRAIN","穀類用計量システム 導入先",
   ["〇〇カントリーエレベーター","〇〇ライスセンター","〇〇農産","〇〇米穀","〇〇穀物倉庫","〇〇集出荷施設","〇〇農業協同組合 CE","〇〇精米工場","〇〇食糧","〇〇ホールディングス"]),
 ("03","INDUSTRIAL","工業用計量システム 導入先",
   ["〇〇ゴム工業","〇〇タイヤ","〇〇化学工業","〇〇ガラス","〇〇製鉄","〇〇肥料","〇〇食品工業","〇〇プラントエンジニアリング","〇〇マテリアル","〇〇セメント"]),
]
def _deliv_case_html():
    out = ""
    for i,(no,en,title,names) in enumerate(_DELIV_CASES):
        boxes = "".join(f'<div class="logobox"><span>{n}</span></div>' for n in names)
        mt = '40px' if i>0 else '28px'
        out += (f'<div style="margin-top:{mt};">'
                f'<div class="case__cat">CASE {no} / {en}</div>'
                f'<h3 class="section-title" style="font-size:22px;margin-top:6px;">{title}</h3>'
                f'<div class="logogrid">{boxes}</div></div>')
    return out
delivery_cases = _deliv_case_html()

delivery_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">DELIVERY RECORD</p>
  <h1 class="page-header__title">納入実績</h1>
  <p class="page-header__lead">農産物選果場・穀類施設・工業ラインなど、多岐にわたる現場への納入実績。</p>
</div></header>

<!-- ② 統計フィーチャー（アグリゲートのみ・個別特定なし） -->
<section class="section"><div class="container">
  <div class="numbers-grid" style="grid-template-columns:repeat(4,1fr);">
    <div class="number-card"><div class="number-card__num">2,000<span class="number-card__unit">+</span></div><div class="number-card__label">累計納入施設数</div></div>
    <div class="number-card"><div class="number-card__num">1,000<span class="number-card__unit">+</span></div><div class="number-card__label">穀類施設への納入</div></div>
    <div class="number-card"><div class="number-card__num">9<span class="number-card__unit">拠点</span></div><div class="number-card__label">国内外サービス網（国内6＋海外3）</div></div>
    <div class="number-card"><div class="number-card__num">3<span class="number-card__unit">分野</span></div><div class="number-card__label">農産物・穀類・工業</div></div>
  </div>
</div></section>

<!-- ③ 全国マップ -->
<section class="section section--grey"><div class="container">
  <p class="section-meta">Service Area</p><h2 class="section-title">主な納入エリア</h2>
  <div class="basemap" style="margin-top:24px;">
    <div>''' + ph('全国／海外 納入マップ（ピン表示）','','aspect-ratio:4/3') + '''</div>
    <div>
      <p class="section-lead" style="margin-top:0;font-size:14px;">国内は北海道から九州まで全国対応。海外は中国（上海）、タイ（バンコク）、韓国に拠点展開。</p>
      <p style="font-size:12px;color:#666;margin-top:12px;line-height:2;">【国内】北海道・東北・関東・北陸・東海・近畿・中国・四国・九州・沖縄<br>【海外】中国・バンコク・韓国・アメリカ・ハンガリー</p>
    </div>
  </div>
</div></section>

''' + DELIV_LOGO_STYLE + '''
<!-- ④ CASE01-03：導入先ロゴ列挙（各10社ダミー・PC3/SP2カラム） -->
<section class="section"><div class="container">
  <p class="section-meta">Field Record</p><h2 class="section-title">分野別の導入先</h2>
  <p class="section-lead">農産物・穀類・工業の各分野で、全国の企業・団体にご採用いただいています。''' + todo('掲載可能な社名・ロゴを確認（元請け経由はエンドユーザー非掲載）') + '''</p>
  ''' + delivery_cases + '''
</div></section>

<div class="recruit-banner" style="background:#222;"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2 style="font-size:24px;">掲載以外の実績についてお問い合わせください</h2><p>2,000施設以上の実績あり。分野・ご要望に近い実績をご案内します。</p></div>
  <div class="recruit-banner__cta"><a class="btn btn--white" href="contact.html">お問い合わせ</a></div>
</div></div>
'''
page("delivery.html","納入実績｜近江度量衡株式会社", delivery_body, active="delivery.html",
     crumbs=[("TOP","top.html"),("納入実績",None)])
PAGES.append(("D","納入実績","/deliveryrecord/","delivery.html","corp",False))

# ======================= E. 会社案内 =======================
# --- サービス拠点データ（住所は現行サイト omiscale.co.jp/company/servicebase/ より転記・要クライアント確認） ---
from urllib.parse import quote as _q

BASES_HQ = [
    ("本社／草津工場", "本社", "〒525-0054 滋賀県草津市東矢倉三丁目11番70号", "TEL 077-562-7111 ／ FAX 077-562-7116", "滋賀県草津市東矢倉3丁目11番70号", ""),
]
BASES_JP = [
    ("東京営業所", "営業所", "〒101-0023 東京都千代田区神田松永町23番地 NC島商ビル7F", "TEL 03-3257-9231 ／ FAX 03-3257-9233", "東京都千代田区神田松永町23番地", ""),
    ("札幌営業所", "営業所", "〒060-0807 北海道札幌市北区北7条西2丁目6番37 山京ビル1012号", "TEL 011-747-5321 ／ FAX 011-747-7146", "北海道札幌市北区北7条西2丁目6番37", "2026年8月移転予定 → 新住所へ差し替え"),
    ("北海道営業所（旭川）", "営業所", "〒078-8251 北海道旭川市東旭川北1条6-146-7", "TEL 0166-74-7391 ／ FAX 0166-74-7392", "北海道旭川市東旭川北1条6-146-7", ""),
    ("仙台出張所", "出張所", "〒981-1217 宮城県名取市美田園5丁目23-1 プランドール102号", "TEL 022-290-5671 ／ FAX 022-290-5672", "宮城県名取市美田園5丁目23-1", ""),
    ("新潟出張所", "出張所", "〒950-0982 新潟県新潟市中央区堀之内南1丁目15番6号 日南ビル3階-1号", "TEL 025-243-7721 ／ FAX 025-243-7728", "新潟県新潟市中央区堀之内南1丁目15番6号", ""),
    ("九州営業所（熊本）", "営業所", "〒860-0016 熊本県熊本市中央区山崎町66-7 熊本中央ビル2階", "TEL 096-356-1177 ／ FAX 096-356-1178", "熊本県熊本市中央区山崎町66-7", ""),
]
BASES_OV = [
    ("近江度量衡 設備(上海)有限公司", "海外現地法人", "上海市閔行区莘建東路58弄緑地科技島2号 1310室（〒201100）", "TEL 0086-21-64136483 ／ FAX 0086-21-64136485", "上海市閔行区莘建東路58弄 緑地科技島2号", ""),
    ("OMI WEIGHING MACHINE (THAILAND) CO.,LTD.", "海外現地法人", "90/43 16th Floor, Sathorn Thani Bldg 1, North Sathorn Road, Silom, Bangrak Bangkok 10500, Thailand", "TEL 0-2636-7702 ／ FAX 0-2636-7703", "Sathorn Thani Building 1, North Sathorn Road, Bangkok", ""),
    ("WON SANG CO., LTD.（韓国）", "海外現地法人", "830, 122 LS-ro, Dongan-gu, Anyang-si, Gyeonggi-do, 14118, Republic of Korea", "TEL 0082-31-346-3430 ／ FAX 0082-31-346-3433", "122 LS-ro, Dongan-gu, Anyang-si, Gyeonggi-do, Korea", ""),
]
BASES_GROUP = [
    ("株式会社テクノオーミ", "グループ会社", "〒525-0063 滋賀県草津市南山田町1081", "TEL 077-563-2011 ／ FAX 077-565-9777", "滋賀県草津市南山田町1081", "グループ会社として掲載するか要確認"),
]

def base_card(name, tag, addr, tel, mapq, note):
    note_html = todo(note) if note else ""
    ov = " base-card--ov" if tag == "海外現地法人" else ""
    return f'''<div class="base-card{ov}">
      <div class="base-card__info">
        <p class="base-card__tag">{tag}</p>
        <h3 class="base-card__name">{name}</h3>
        <p class="base-card__addr">{addr}</p>
        <p class="base-card__tel">{tel}</p>
        {note_html}
      </div>
      <div class="base-card__map"><iframe src="https://maps.google.com/maps?q={_q(mapq)}&z=15&hl=ja&output=embed" loading="lazy" title="{name} 地図"></iframe></div>
    </div>'''

def base_cards(bases):
    return '<div class="base-cards">' + "".join(base_card(*b) for b in bases) + '</div>'

company_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">COMPANY</p>
  <h1 class="page-header__title">会社案内</h1>
</div></header>
<nav class="page-nav"><div class="inner">
  <a href="#concept">企業理念</a><a href="#greeting">代表挨拶</a><a href="#servicebase">サービス拠点</a><a href="#quality">品質・認証</a><a href="#profile">会社概要</a>
</div></nav>

<!-- ② 企業理念 -->
<section class="section section--dark" id="concept">
  <div class="container statement">
    <p class="statement__en">OUR STATEMENT — We measure the future</p>
    <h2 class="statement__main">「いきる」をはかり、豊かな世界へ。</h2>
    <p class="statement__body">1900年（明治33年）の創業以来、私たちは一貫して「はかる」という技術を磨き続けてきました。はかることは、単に数値を知ることではありません。品質を見極め、価値を創り、未来への可能性を拓くこと。時代が移り変わり、社会や産業の姿が大きく変化する中でも、私たちは常に新しい技術への挑戦を続け、お客様とともに未来を創り続けてきました。</p>
    <div class="grid-3" style="margin-top:48px;text-align:left;">
      <div class="pillar"><div class="pillar__no">社是 01</div><div class="pillar__title">社会貢献</div></div>
      <div class="pillar"><div class="pillar__no">社是 02</div><div class="pillar__title">技術の公用</div></div>
      <div class="pillar"><div class="pillar__no">社是 03</div><div class="pillar__title">互助の精神</div></div>
    </div>
  </div>
</section>

<!-- ③ MISSION / VISION / VALUES -->
<section class="section"><div class="container">
  <div class="grid-3">
    <div class="value-item"><div class="value-item__title">MISSION</div><p class="value-item__body">私たちは、はかる。重さを。量を。長さを。そして時には、品質を、価値を、未来を。一世紀以上に亘り受け継がれてきた技術と挑戦の精神は、これからも新しい時代へと受け継がれていきます。</p></div>
    <div class="value-item"><div class="value-item__title">VISION</div><p class="value-item__body">働く人が誇りを持てる場所から、お客様の信頼は生まれる。社員が豊かであることで初めてお客様への最良のサービスが生まれる。</p></div>
    <div class="value-item"><div class="value-item__title">VALUES</div><p class="value-item__body">堅実であること。誇りをもつこと。126年間ぶれずに現場と向き合ってきた姿勢と、仕事の社会的意義から生まれる誇り。</p></div>
  </div>
</div></section>

<!-- ④ 代表挨拶 -->
<section class="section section--grey" id="greeting"><div class="container grid-2" style="align-items:start;">
  <div>''' + ph('代表者写真（スーツ姿・顔出し）','','aspect-ratio:3/4') + todo('原稿(約800字)・写真をクライアント提供') + '''</div>
  <div>
    <p class="section-meta">Message</p><h2 class="section-title">代表挨拶</h2>
    <p style="font-size:13px;color:#888;margin-top:8px;">代表取締役社長　小谷 俊彦</p>
    <p style="font-size:14px;color:#444;line-height:2;margin-top:20px;">We Measure the Future.<br>私たち近江度量衡は、1900年の創業以来、126年以上にわたり「はかる」という技術を通じて社会を支えてきました。重さをはかる。量をはかる。品質をはかる。それが私たちの原点です。しかし、私たちが本当に大切にしているのは、数字そのものではありません。その先にある、お客様の安心や喜び、そして未来です。……（約800字）<br><br>未来を測り、未来を創る。それが私たち近江度量衡の変わらぬ使命です。</p>
  </div>
</div></section>

<!-- ⑤ サービス拠点（第8回決定：各拠点に住所を明記し、横にGoogleマップを併設） -->
<section class="section" id="servicebase"><div class="container">
  <p class="section-meta">Service Base</p><h2 class="section-title">サービス拠点</h2>
  <p class="section-lead">本社（滋賀・草津）と国内6拠点＋海外3拠点のサービス網。各拠点の所在地はマップからご確認いただけます。</p>
  <div style="margin-top:24px;">''' + ph('グローバル拠点マップ（国内6＋海外3 全体図）','','aspect-ratio:21/9') + '''</div>
  <h3 class="base-group-title">本社</h3>
  ''' + base_cards(BASES_HQ) + '''
  <h3 class="base-group-title">国内拠点</h3>
  ''' + base_cards(BASES_JP) + '''
  <h3 class="base-group-title">海外拠点</h3>
  ''' + base_cards(BASES_OV) + '''
  <h3 class="base-group-title">グループ会社</h3>
  ''' + base_cards(BASES_GROUP) + '''
  <div class="cms-note" style="background:#fff7ec;border-left-color:#e0a030;">★ 各拠点の住所・TEL/FAXは現行サイトから転記。掲載内容（テクノオーミの掲載可否・札幌移転後の新住所を含む）はクライアント確認のうえ確定。''' + todo('拠点情報の最終確認') + '''</div>
</div></section>

<!-- ⑤b 品質・認証・取り組み（現行サイト「品質について／地域未来牽引企業／SDGs」を転記） -->
<section class="section" id="quality"><div class="container">
  <p class="section-meta">Quality &amp; Initiatives</p><h2 class="section-title">品質・認証・取り組み</h2>

  <div class="grid-2" style="margin-top:36px;align-items:center;gap:48px;">
    <div>
      <h3 style="font-size:20px;font-weight:700;margin-bottom:14px;">品質について — ISO9001</h3>
      <p style="font-size:14px;line-height:2.05;color:#333;">近江度量衡は2000年2月、ISO（国際標準化機構）が定めた国際的な品質保証規格「ISO9001」の認証を取得しました。ISO9001は、製品の受注・開発・設計・生産・保管出荷等の各過程の管理体制を評価する品質保証規格であり、ISOが定める厳正な審査をクリアした企業だけに与えられるものです。認証取得により当社の企業品質が国際的に認められ、長年にわたって培ってきた品質追求の姿勢が評価されたものと言えます。これを機に、さらに高い信頼をいただける企業を目指して努力を重ねてまいります。</p>
    </div>
    <div>''' + ph('ISO9001 マネジメントシステム登録証（JQA・現行サイトの画像を流用）','','aspect-ratio:16/10') + '''</div>
  </div>

  <div class="grid-2" style="margin-top:56px;align-items:center;gap:48px;">
    <div>''' + ph('地域未来牽引企業 ロゴ（現行サイトの画像を流用）','','aspect-ratio:16/10') + '''</div>
    <div>
      <h3 style="font-size:20px;font-weight:700;margin-bottom:14px;">地域未来牽引企業</h3>
      <p style="font-size:14px;line-height:2.05;color:#333;">「地域未来牽引企業」は、地域経済への影響力が大きく、成長性が見込まれるとともに、地域経済のバリューチェーンの要を担う、地域経済牽引事業の中心的な担い手候補である企業を経済産業省が選定するものです。この選定によって地域経済の活性化を後押しする中核企業として認知され、今後の成長についてさまざまな支援が期待できます。近江度量衡は、これからも地域経済の活性化や地域の特性・強みを活かす企業として、より一層邁進してまいります。</p>
    </div>
  </div>

  <div class="grid-2" style="margin-top:56px;align-items:center;gap:48px;">
    <div>
      <h3 style="font-size:20px;font-weight:700;margin-bottom:14px;">SDGsへの取り組み</h3>
      <p style="font-size:14px;line-height:2.05;color:#333;">SDGs（持続可能な開発目標）とは、2030年に向けて世界が合意した「持続可能な開発目標」です。近江度量衡株式会社は、高度技術サービスの提供を通じて、SDGs（持続可能な開発目標）に取り組んでいきます。</p>
    </div>
    <div>''' + ph('SUSTAINABLE DEVELOPMENT GOALS ロゴ','','aspect-ratio:16/10') + '''</div>
  </div>

  <div class="cms-note">◯ 現行サイト「品質について／地域未来牽引企業／SDGsへの取り組み」の文章を転記（表記のみ整え）。ISO登録証・各ロゴ画像は現行サイトから流用。</div>
</div></section>

<!-- ⑥ 会社概要 -->
<section class="section section--grey" id="profile"><div class="container">
  <p class="section-meta">Profile</p><h2 class="section-title">会社概要</h2>
  <table class="info-table" style="margin-top:24px;background:#fff;">
    <tr><th>会社名</th><td>近江度量衡株式会社（OMISCALE CO.,LTD.）</td></tr>
    <tr><th>設立</th><td>1900年（明治33年）</td></tr>
    <tr><th>資本金</th><td>200,000,000円</td></tr>
    <tr><th>代表者</th><td>代表取締役社長　小谷 俊彦 ''' + todo('確認') + '''</td></tr>
    <tr><th>従業員数</th><td>約150名 ''' + todo('最新の人数を確認') + '''</td></tr>
    <tr><th>事業内容</th><td>計量システムの設計・制御・製造・販売・保守</td></tr>
    <tr><th>ISO認証</th><td>ISO 9001</td></tr>
    <tr><th>拠点数</th><td>国内6拠点＋海外3拠点</td></tr>
    <tr><th>所在地（本社）</th><td>〒525-0054 滋賀県草津市東矢倉三丁目11番70号</td></tr>
    <tr><th>TEL</th><td>077-562-7111</td></tr>
  </table>
</div></section>
'''
page("company.html","会社案内｜近江度量衡株式会社", company_body, active="company.html",
     crumbs=[("TOP","top.html"),("会社案内",None)])
PAGES.append(("E","会社案内","/company/","company.html","corp",False))

# ======================= F. 126年ヒストリー =======================
# (era導入, [(年号era, 年number, 見出し, 本文, 素材ファイル名 or '')])
HISTORY = [
 ("明治・大正（1900-1925）", "明治33年の草津工房開設から、精度への執念と地域への誠実さが原点。", [
   ("明治33年","1900","創業 ― 草津に計量器工房を開設","初代が滋賀県草津にて計量器製造・販売を開始。農産物取引の公正計量を使命に、棒秤・台秤を供給。","image_1900_1.jpg / image_1900_2.jpg"),
   ("明治43年","1910","法人化 ― 近江度量衡株式会社を設立","事業拡大にともない法人格取得。職人工房から組織経営へ移行、従業員約15名。",""),
   ("大正9年","1920","近畿・東海エリアへ販路拡大","大阪・名古屋の穀物取引所向け高精度台秤を納入。産業発展に合わせ滋賀県外へ展開。",""),
 ]),
 ("昭和前期（1926-1944）", "農業計量で培った精度ノウハウを、工業用計量器へと展開しはじめた時代。", [
   ("昭和5年","1930","二代目に経営承継 ― 製品ラインナップ拡充","台秤に加え吊り秤・分銅・検定器具製造開始。中小工場・卸業者向け基盤を整備。",""),
   ("昭和10年","1935","工業用計量器の試作開始","鉄鋼・繊維産業向け大型計量器（トラックスケール前身）試作開始。農業計量の精度ノウハウの産業転用を開始。",""),
 ]),
 ("昭和中期（1945-1969）", "計量法制定と高度経済成長。選果機・計量ライン事業へ参入し全国展開の布石を打つ。", [
   ("昭和25年","1950","計量法制定 ― 国家検定対応機器の製造を開始","計量法施行で国家検定基準適合が必須化。検定合格基準をいち早く確立し、業界標準設定に関与。","image_1946.jpg"),
   ("昭和30年","1955","選果機・計量コンベア事業参入","高度経済成長期の農業機械化需要を捉え、選果・計量ラインシステムを開発。農協大型施設への初納入実現。","image_1959.jpg"),
   ("昭和35年","1960","東京・大阪に営業所開設","首都圏・関西圏の大型農産物市場・食品加工業者へアクセス強化。全国展開の布石。","image_1961_1.jpg"),
 ]),
 ("昭和後期（1970-1988）", "穀類カントリーエレベーター向けで業界トップシェアへ。マイコン制御の次世代機も製品化。", [
   ("昭和50年","1975","穀類カントリーエレベーター向け計量システムを本格展開","食糧庁管轄穀物備蓄施設へのシステム納入本格化。累計100施設突破。業界シェアトップクラスを確立。","image_1974.jpg"),
   ("昭和55年","1980","マイコン制御計量システムの製品化","マイクロプロセッサ搭載計量制御システムを開発・製品化。自動計量・データ記録・印字一体化した次世代機を普及。","image_1980.jpg"),
   ("昭和62年","1987","北海道・九州に営業所を開設","北海道（帯広）・九州（福岡）に営業所開設。産地密着サービス体制を全国展開。",""),
 ]),
 ("平成（1989-2018）", "創業100周年とISO取得。累計1,000施設突破からアジア展開へ。", [
   ("平成12年","2000","創業100周年 ― ISO 9001 認証取得","品質保証体制を国際規格で整備。全数検査・精度管理の仕組みを標準化。「検定合格率100%」誓約。","image_2000_1.jpg / image_2000_2.jpg"),
   ("平成19年","2007","カントリーエレベーター累計1,000施設突破","全国CEへのシステム納入が累計1,000施設突破。国内穀類計量分野でのトップシェア確立。","image_2007.jpg"),
   ("平成22年","2010","アジア展開開始 ― 上海拠点設立","中国・アジアの農産物産業急成長とともに海外進出。上海に現地法人設立。",""),
   ("平成27年","2015","タイ・バンコクに拠点設立 ― 海外3拠点体制が完成","上海・ソウル・バンコク3拠点体制でアジア全域をカバー。","image_2015.jpg"),
 ]),
 ("令和（2019-現在）", "リモート保守体制の整備、累計2,000施設突破、そして新ブランドビジョンへ。", [
   ("令和2年","2020","コロナ禍でのリモートメンテナンス体制を整備","遠隔診断・オンラインサポートシステムを急速整備。「動かし続ける」メンテナンスへの信頼を向上。",""),
   ("令和5年","2023","累計納入施設2,000突破","国内外合計納入施設数が2,000施設を突破。農産物・穀類・工業三分野での実績が積み重なった節目。","image_2024.jpg"),
   ("令和7年","2025","創業126周年 ― 北海道営業所を拡充移転","3月に創業126周年達成。6月には北海道営業所を拡充移転。Webリニューアルプロジェクト始動。",""),
   ("令和8年","2026","新ブランドビジョンを発表 ― Webサイトリニューアル","「いきる」をはかり、豊かな世界へ。新ブランドステートメントのもとWebサイトをリニューアル。次の100年に向けた採用・広報体制を強化。",""),
 ]),
]
def history_eras():
    out = ""
    for era, intro, rows in HISTORY:
        items = ""
        for e,n,h,b,asset in rows:
            assethtml = ph('当時の写真：'+asset,'timeline-ph') if asset else ''
            items += f'''<div class="timeline-item"><div class="timeline-year"><span class="timeline-year__era">{e}</span><span class="timeline-year__num">{n}</span></div><div class="timeline-dot"></div><div class="timeline-content"><h3>{h}</h3><p>{b}</p></div>{assethtml}</div>'''
        out += f'''<div style="margin-top:48px;"><p class="eyebrow">{era}</p><p class="section-lead" style="margin-top:0;margin-bottom:16px;">{intro}</p><div class="timeline">{items}</div></div>'''
    return out

# 126年ヒストリー：奥行きトンネル型の透視スクロール（遠い過去→手前へ迫る／時代を進むごとに通り抜ける）
_hc_panels = ""
_hc_photos = ""
_hc_years = []
_hc_n = 0
for _era, _intro, _rows in HISTORY:
    for _e, _n, _h, _b, _asset in _rows:
        _photo = ('<div class="hc-panel__photo">当時の写真：' + _asset + '</div>') if _asset else ''
        _hc_panels += ('<article class="hc-panel" data-year="' + _n + '" data-era="' + _era + '">'
            '<p class="hc-panel__era">' + _era + '</p>'
            '<h3 class="hc-panel__year"><small>' + _e + '</small>' + _n + '</h3>'
            '<p class="hc-panel__title">' + _h + '</p>'
            '<p class="hc-panel__desc">' + _b + '</p>' + _photo + '</article>')
        _lbl = ('背景写真：' + _asset) if _asset else ('背景イメージ：' + _era + '／' + _n + ' 年代の風景・資料写真')
        _hc_photos += '<div class="hc-photo"><span>' + _lbl + '</span></div>'
        _hc_years.append((_n, _era))
        _hc_n += 1

# 下部プログレスバーの年号目盛り（時代の切替は強調ティック）
_hc_ticks = ""
_prev_era = None
for _i, (_yr, _er) in enumerate(_hc_years):
    _pos = (_i / (len(_hc_years) - 1)) * 100 if len(_hc_years) > 1 else 0
    _cls = 'hc-tick' + (' --era' if _er != _prev_era else '')
    _hc_ticks += '<span class="' + _cls + '" style="left:' + ('%.2f' % _pos) + '%"><b>' + _yr + '</b></span>'
    _prev_era = _er

HC_STYLE = '''<style>
.hc-scene{position:relative;background:var(--c-black);color:#fff;}
.hc-pin{position:sticky;top:0;height:100vh;overflow:hidden;perspective:1200px;perspective-origin:64% 42%;}
.hc-bg{position:absolute;inset:0;pointer-events:none;background:
  radial-gradient(56% 52% at 66% 40%, rgba(255,255,255,.07), rgba(0,0,0,0) 70%),
  repeating-linear-gradient(0deg, rgba(255,255,255,.028) 0 1px, transparent 1px 3px);}
/* 背景写真（スライドごとにクロスフェード切替・ワイヤーではダミー枠） */
.hc-photos{position:absolute;inset:0;pointer-events:none;}
.hc-photo{position:absolute;inset:0;opacity:0;transform:scale(1.06);
  transition:opacity 1s ease,transform 1.6s ease;
  background:repeating-linear-gradient(45deg, rgba(255,255,255,.045) 0 2px, transparent 2px 14px);}
.hc-photo span{position:absolute;left:50%;top:12%;transform:translateX(-50%);white-space:nowrap;
  font-family:var(--font-en);font-size:10px;letter-spacing:.18em;color:rgba(255,255,255,.4);
  border:1px dashed rgba(255,255,255,.25);padding:6px 14px;}
.hc-photo.is-on{opacity:.5;transform:scale(1);}
.hc-photo::after{content:'';position:absolute;inset:0;background:radial-gradient(60% 60% at 50% 55%, rgba(0,0,0,0) 30%, rgba(17,19,21,.8) 100%);}
.hc-stage{position:absolute;inset:0;transform-style:preserve-3d;}
.hc-panel{position:absolute;left:50%;top:50%;width:min(880px,92vw);transform:translate(-50%,-50%);
  will-change:transform,opacity;text-align:center;padding:52px 56px 56px;
  border:1px solid rgba(255,255,255,.28);background:rgba(17,19,21,.66);}
.hc-panel.is-active{border-color:rgba(255,255,255,.85);}
.hc-panel__era{font-family:var(--font-en);font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--c-muted);}
.hc-panel__year{font-family:var(--font-mn);font-weight:600;font-size:clamp(20px,2.4vw,30px);line-height:1;letter-spacing:.06em;margin-top:12px;color:rgba(255,255,255,.85);}
.hc-panel__year small{display:inline;font-family:var(--font-en);font-weight:500;font-size:11px;letter-spacing:.22em;color:var(--c-muted);margin-right:12px;}
.hc-panel__title{font-family:var(--font-mn);font-weight:700;font-size:clamp(26px,3.4vw,46px);margin-top:20px;line-height:1.5;letter-spacing:.03em;}
.hc-panel__desc{font-family:var(--font-ja);font-size:14px;line-height:2.1;color:rgba(255,255,255,.8);margin:20px auto 0;max-width:680px;}
.hc-panel__photo{display:inline-block;margin-top:16px;font-family:var(--font-en);font-size:10px;letter-spacing:.14em;color:var(--c-muted);border:1px dashed rgba(255,255,255,.28);padding:7px 12px;}
.hc-hud{position:absolute;left:40px;top:96px;z-index:6;pointer-events:none;}
.hc-hud__era{font-family:var(--font-en);font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:rgba(255,255,255,.55);}
.hc-progress{position:absolute;left:40px;right:40px;bottom:64px;height:1px;background:rgba(255,255,255,.18);z-index:6;}
.hc-progress__fill{position:absolute;left:0;top:0;height:100%;width:0;background:#fff;}
/* 年号目盛り：全スライド分のティック＋年号ラベル、時代の頭は強調 */
.hc-tick{position:absolute;top:-3px;width:1px;height:7px;background:rgba(255,255,255,.3);transform:translateX(-.5px);}
.hc-tick.--era{top:-5px;height:11px;background:rgba(255,255,255,.55);}
.hc-tick b{position:absolute;top:11px;left:50%;transform:translateX(-50%);font:500 9px/1 var(--font-en);letter-spacing:.1em;color:rgba(255,255,255,.38);font-weight:500;white-space:nowrap;}
.hc-tick.--era b{color:rgba(255,255,255,.6);}
.hc-tick.is-on{background:#fff;top:-6px;height:13px;}
.hc-tick.is-on b{color:#fff;font-weight:700;top:13px;}
.hc-scroll{position:absolute;left:50%;bottom:96px;transform:translateX(-50%);z-index:6;font-family:var(--font-en);font-size:9px;letter-spacing:.3em;text-transform:uppercase;color:rgba(255,255,255,.5);}
/* ── SP：縦長ボックスで1枚を主役に ── */
@media(max-width:640px){
  .hc-hud{left:20px;top:76px;}
  .hc-progress{left:20px;right:20px;bottom:44px;}
  .hc-tick b{display:none;}
  .hc-tick.is-on b,.hc-tick.--era b{display:block;}
  .hc-tick.--era:not(.is-on) b{color:rgba(255,255,255,.3);}
  .hc-panel{width:86vw;min-height:64vh;padding:40px 24px;display:flex;flex-direction:column;justify-content:center;}
  .hc-panel__title{font-size:clamp(22px,6.6vw,30px);line-height:1.5;}
  .hc-panel__desc{font-size:12px;line-height:2;}
  .hc-panel__photo{margin-top:20px;}
}
/* reduced-motion フォールバック：通常の縦積み */
.hc--static .hc-pin{position:static;height:auto;overflow:visible;perspective:none;padding:60px 0;}
.hc--static .hc-stage{position:static;transform:none;}
.hc--static .hc-bg,.hc--static .hc-photos,.hc--static .hc-progress,.hc--static .hc-scroll,.hc--static .hc-hud{display:none;}
.hc--static .hc-panel{position:relative;left:auto;top:auto;transform:none!important;opacity:1!important;width:min(680px,90vw);margin:0 auto 18px;}
</style>'''

HC_SCRIPT = '''<script>
(function(){
  var scene=document.querySelector('.hc-scene'); if(!scene) return;
  var panels=[].slice.call(scene.querySelectorAll('.hc-panel'));
  var photos=[].slice.call(scene.querySelectorAll('.hc-photo'));
  var ticks=[].slice.call(scene.querySelectorAll('.hc-tick'));
  var fill=scene.querySelector('.hc-progress__fill');
  var eraHud=scene.querySelector('.hc-hud__era');
  var scroll=scene.querySelector('.hc-scroll');
  if(!panels.length) return;
  if(matchMedia('(prefers-reduced-motion:reduce)').matches){ scene.classList.add('hc--static'); return; }
  var N=panels.length, STEP=900, PMAX=900;
  function cl(v,a,b){a=(a==null?0:a);b=(b==null?1:b);return v<a?a:(v>b?b:v);}
  var ticking=false, lastActive=-1;
  function upd(){
    var vh=window.innerHeight, max=scene.offsetHeight-vh;
    var r=scene.getBoundingClientRect();
    var p= max>0 ? cl(-r.top,0,max)/max : 0;
    var pf=p*(N-1), active=Math.round(pf);
    for(var i=0;i<N;i++){
      var el=panels[i], d=i-pf, z=-d*STEP;
      if(z>PMAX) z=PMAX;
      var x = d*470;                                // 右奥→左手前の動線：未来=右、手前=左
      var y = -d*80;                                // 未来=奥(上)、手前=前(下)
      var op = d>=0 ? cl(1-d/0.95) : cl(1+d/0.7);   // アクティブ1枚だけを明瞭に（次スライドは読了後に現れる）
      el.style.transform='translate(-50%,-50%) translate('+x+'px,'+y+'px) translateZ('+z+'px)';
      el.style.opacity=String(op);
      el.style.zIndex=String(2000-Math.round(Math.abs(d)*12));
      var act=(i===active);
      if(act!==el._act){ el.classList.toggle('is-active',act); el._act=act; }
    }
    if(active!==lastActive){
      if(photos[lastActive]) photos[lastActive].classList.remove('is-on');
      if(photos[active]) photos[active].classList.add('is-on');
      if(ticks[lastActive]) ticks[lastActive].classList.remove('is-on');
      if(ticks[active]) ticks[active].classList.add('is-on');
      lastActive=active;
    }
    if(fill) fill.style.width=(p*100)+'%';
    if(eraHud){ var ap=panels[active]; if(ap) eraHud.textContent=ap.getAttribute('data-era'); }
    if(scroll) scroll.style.opacity=String(cl(1-p*6));
    ticking=false;
  }
  window.addEventListener('scroll',function(){ if(!ticking){requestAnimationFrame(upd);ticking=true;} },{passive:true});
  window.addEventListener('resize',upd);
  upd();
})();
</script>'''

history_body = ('''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">126 YEARS HISTORY</p>
  <h1 class="page-header__title">明治から令和へ。</h1>
  <p class="page-header__lead">1900年、草津の小さな工房から始まった物語。時代とともに移りゆく景色を、ひとつずつ辿ってください。</p>
</div></header>
''' + HC_STYLE + '''
<section class="hc-scene" style="height:calc(115vh * ''' + str(_hc_n) + ''' + 70vh);">
  <div class="hc-pin">
    <div class="hc-bg"></div>
    <div class="hc-photos">''' + _hc_photos + '''</div>
    <div class="hc-hud"><p class="hc-hud__era"></p></div>
    <div class="hc-stage">''' + _hc_panels + '''</div>
    <div class="hc-progress"><span class="hc-progress__fill"></span>''' + _hc_ticks + '''</div>
    <div class="hc-scroll">Scroll — 1900 → 2026</div>
  </div>
</section>
''' + HC_SCRIPT + '''
<!-- 証言ブロック -->
<section class="section"><div class="container">
  <div class="grid-2">
    <div class="value-item" style="background:var(--c-bg-light);"><p style="font-size:16px;font-weight:700;line-height:1.8;">「計量とは、人と人の信頼を結ぶ仕事だ。一グラムのずれも、嘘をつく。」</p><p style="font-size:12px;color:#888;margin-top:12px;">元社員・昭和40年代入社 ''' + todo('本番用原稿に差し替え') + '''</p></div>
    <div class="value-item" style="background:var(--c-bg-light);"><p style="font-size:16px;font-weight:700;line-height:1.8;">「一品一様というのは、ただ特注を作るということではない。お客様の現場を理解し、最適な精度で答えることだ。」</p><p style="font-size:12px;color:#888;margin-top:12px;">現役エンジニア ''' + todo('本番用原稿に差し替え') + '''</p></div>
  </div>
</div></section>
<div class="recruit-banner"><div class="recruit-banner__inner">
  <div class="recruit-banner__text"><h2>次の100年へ。ともに歩む人を募集中。</h2><p>126年の技術と誇りを受け継ぎ、更なる進化を担う仲間を求めています。</p></div>
  <div class="recruit-banner__cta"><a class="btn btn--red" href="recruit.html" style="background:#111315;color:#fff;">採用情報 ↗</a></div>
</div></div>
''')
page("history.html","126年ヒストリー｜近江度量衡株式会社", history_body, active="history.html",
     crumbs=[("TOP","top.html"),("126年ヒストリー",None)])
PAGES.append(("F","126年ヒストリー","/history/","history.html","corp",False))

# ======================= I. 新着情報 =======================
def news_list(cats, rows, detail="news-detail.html"):
    fil = "".join(f'<a class="page-nav-cat" style="padding:8px 16px;border:1px solid var(--c-border);font-size:12px;margin-right:8px;display:inline-block;">{c}</a>' for c in cats)
    items = ""
    for d,c,t in rows:
        items += f'<li class="news-item"><span class="news-item__date">{d}</span><span class="news-item__cat">{c}</span><a class="news-item__title" href="{detail}">{t}</a></li>'
    return fil, items

news_body_top = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">NEWS</p>
  <h1 class="page-header__title">新着情報</h1>
  <p class="page-header__lead">近江度量衡の最新ニュース・お知らせ・プレスリリース</p>
</div></header>
<section class="section"><div class="container">'''
import calendar as _cal
def _news_cal(year, month, marked):
    _cal.setfirstweekday(6)  # 日曜始まり
    head = "".join(f'<span class="news-cal__wd">{w}</span>' for w in ["日","月","火","水","木","金","土"])
    body = ""
    for week in _cal.monthcalendar(year, month):
        for day in week:
            if day == 0:
                body += '<span class="news-cal__day news-cal__day--empty">&nbsp;</span>'
            else:
                mk = ' news-cal__day--news' if day in marked else ''
                body += f'<span class="news-cal__day{mk}">{day}</span>'
    return head + body

NEWS_STYLE = '''<style>
.news-cal{border:1px solid var(--c-border);padding:16px;background:#fff;}
.news-cal__head{display:flex;justify-content:space-between;align-items:center;font-family:var(--font-en);font-weight:600;font-size:14px;margin-bottom:12px;}
.news-cal__grid{display:grid;grid-template-columns:repeat(7,1fr);gap:2px;text-align:center;}
.news-cal__wd{font-size:10px;color:var(--c-muted);padding:4px 0;}
.news-cal__day{font-size:12px;padding:6px 0;color:#333;border-radius:2px;}
.news-cal__day--empty{color:transparent;}
.news-cal__day--news{font-weight:700;background:var(--c-black);color:#fff;}
.news-archive{list-style:none;}
.news-archive li{border-bottom:1px solid var(--c-border);}
.news-archive a{display:block;padding:9px 4px;font-size:13px;color:#333;}
</style>'''

fil, items = news_list(["すべて","お知らせ","プレスリリース","製品情報","休業案内","採用"],
  [("2026.08.13","お知らせ","札幌営業所を移転しました"),
   ("2026.08.10","休業案内","夏季休業のお知らせ（8/13〜8/16）"),
   ("2026.07.15","プレスリリース","新型フルオートドライヤーシステムを発表しました"),
   ("2025.03.01","お知らせ","会社設立126周年を達成しました"),
   ("2025.04.01","採用","2027年度採用エントリー受付開始のご案内")])

news_body = news_body_top + NEWS_STYLE + '''
  <div style="margin-bottom:24px;">''' + fil + '''</div>
  <div class="basemap" style="grid-template-columns:1fr 300px;align-items:start;">
    <div>
      <ul class="news-list">''' + items + '''</ul>
      <div class="cms-note">◯ お知らせ・プレスリリース・季節の休業案内などを掲載。記事内の<b>動画埋め込み・画像ギャラリー</b>、および<b>カレンダーからの日付絞り込み</b>に対応（WordPressで自社更新）。''' + cms('CMS更新') + '''</div>
    </div>
    <aside>
      <div class="news-cal">
        <div class="news-cal__head"><span>2026年 8月</span><span style="color:#bbb;">‹ ›</span></div>
        <div class="news-cal__grid">''' + _news_cal(2026, 8, [10, 13]) + '''</div>
      </div>
      <p style="font-size:11px;color:#888;margin:8px 0 0;">■ の日付に記事あり（クリックで絞り込み）</p>
      <h3 style="font-size:11px;letter-spacing:.14em;color:var(--c-muted);margin:24px 0 6px;font-family:var(--font-en);">ARCHIVE</h3>
      <ul class="news-archive">
        <li><a href="#">2026年 8月（2）</a></li>
        <li><a href="#">2026年 7月（1）</a></li>
        <li><a href="#">2025年 3月（1）</a></li>
      </ul>
    </aside>
  </div>
</div></section>'''
page("news.html","新着情報｜近江度量衡株式会社", news_body, active="news.html",
     crumbs=[("TOP","top.html"),("新着情報",None)])
PAGES.append(("I","新着情報","/news/","news.html","corp",True))

# I1 記事詳細
news_detail_body = '''
<style>
/* ── 記事本文テンプレート（news-detail 専用） ── */
.art{font-size:15px;line-height:2;color:#333;}
.art>*+*{margin-top:20px;}
.el-tag{display:block;width:fit-content;font-family:var(--font-en);font-size:10px;letter-spacing:.16em;color:#999;border:1px dashed #bbb;padding:2px 10px;margin:44px 0 12px;}
.art .el-tag:first-child{margin-top:0;}
.art-h2{font-size:22px;font-weight:700;line-height:1.6;letter-spacing:.03em;border-left:4px solid #111315;padding-left:14px;margin-top:8px;}
.art-h3{font-size:17px;font-weight:700;line-height:1.6;border-bottom:1px solid var(--c-border);padding-bottom:8px;margin-top:8px;}
.art-toc{border:1px solid var(--c-border);background:#f6f6f6;padding:24px 28px;}
.art-toc__label{font-family:var(--font-en);font-size:11px;letter-spacing:.26em;color:#888;margin-bottom:10px;}
.art-toc ol{margin:0;padding-left:20px;}
.art-toc li{padding:3px 0;}
.art-toc a{color:#333;text-decoration:underline;text-underline-offset:3px;}
.art-ul{padding-left:2px;list-style:none;}
.art-ul li{padding:3px 0 3px 18px;position:relative;}
.art-ul li::before{content:'';position:absolute;left:0;top:14px;width:8px;height:1px;background:#111315;}
.art-ol{padding-left:22px;}
.art-ol li{padding:3px 0;}
.art-quote{border-left:3px solid #ccc;background:#f6f6f6;padding:20px 24px;color:#555;position:relative;}
.art-quote::before{content:'“';font-family:var(--font-en);font-size:34px;line-height:1;color:#bbb;display:block;margin-bottom:4px;}
.art-quote cite{display:block;font-style:normal;font-size:12px;color:#999;margin-top:8px;}
.art-box{border:1px solid #111315;padding:22px 26px;}
.art-box__title{font-weight:700;font-size:14px;letter-spacing:.06em;margin-bottom:6px;}
.art-fig{margin:0;}
.art-fig figcaption{font-size:12px;color:#888;margin-top:8px;}
.art-video{position:relative;}
.art-video::after{content:'▶';position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:20px;color:#fff;background:rgba(17,19,21,.28);pointer-events:none;}
.art-slider{position:relative;}
.art-slider__arrow{position:absolute;top:50%;transform:translateY(-50%);width:40px;height:40px;border:1px solid #111315;background:#fff;display:flex;align-items:center;justify-content:center;font-size:16px;z-index:2;}
.art-slider__arrow.--prev{left:-14px;}
.art-slider__arrow.--next{right:-14px;}
.art-slider__dots{display:flex;justify-content:center;gap:8px;margin-top:12px;}
.art-slider__dots i{width:8px;height:8px;border-radius:50%;background:#ccc;}
.art-slider__dots i.--on{background:#111315;}
</style>
<section class="section"><div class="container" style="max-width:760px;">
  <p style="font-size:12px;color:#888;letter-spacing:.06em;">2026.08.13　<span style="border:1px solid var(--c-border);padding:1px 8px;">お知らせ</span></p>
  <h1 style="font-size:30px;font-weight:700;line-height:1.5;margin:16px 0 8px;">札幌営業所を移転しました ''' + cms('CMS更新') + '''</h1>
  <div style="margin:24px 0;">''' + ph('記事メイン画像（任意）','','aspect-ratio:16/9') + '''</div>

  <div class="art">
    <p style="font-size:12px;color:#999;">※ 以下は記事本文で使える要素の一覧（テンプレート）です。CMSのリッチエディタから各スタイルを選んで組み合わせます。''' + todo('要素の過不足を確認') + '''</p>

    <span class="el-tag">目次（自動生成）</span>
    <div class="art-toc">
      <p class="art-toc__label">CONTENTS</p>
      <ol>
        <li><a href="#sec1">大見出しが入ります（H2）</a>
          <ol style="padding-left:18px;"><li><a href="#sec2-1">小見出しが入ります（H3）</a></li></ol>
        </li>
      </ol>
    </div>

    <span class="el-tag">大見出し H2</span>
    <h2 class="art-h2" id="sec1">大見出しが入ります。記事の章タイトルです</h2>

    <span class="el-tag">本文</span>
    <p>本文テキストが入ります。〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。太字は<strong>このように強調</strong>、リンクは<a href="#" style="color:#333;text-decoration:underline;text-underline-offset:3px;">テキストリンク</a>で表示されます。</p>

    <span class="el-tag">小見出し H3</span>
    <h3 class="art-h3" id="sec2-1">小見出しが入ります。章の中の節タイトルです</h3>
    <p>本文テキストが入ります。〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。</p>

    <span class="el-tag">リスト（箇条書き／番号付き）</span>
    <ul class="art-ul">
      <li>箇条書きリストの項目が入ります</li>
      <li>箇条書きリストの項目が入ります</li>
      <li>箇条書きリストの項目が入ります</li>
    </ul>
    <ol class="art-ol">
      <li>番号付きリストの項目が入ります</li>
      <li>番号付きリストの項目が入ります</li>
    </ol>

    <span class="el-tag">引用</span>
    <blockquote class="art-quote">
      引用文が入ります。〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。
      <cite>― 出典：〇〇〇〇（URL）</cite>
    </blockquote>

    <span class="el-tag">ボックス（囲み）</span>
    <div class="art-box">
      <p class="art-box__title">ポイント・補足タイトル</p>
      <p style="margin:0;">囲みボックスの本文が入ります。お知らせの中で特に伝えたい情報（営業時間・注意事項など）に使用します。</p>
    </div>

    <span class="el-tag">画像＋キャプション</span>
    <figure class="art-fig">
      ''' + ph('記事内画像','','aspect-ratio:16/9') + '''
      <figcaption>画像のキャプションが入ります（撮影場所・説明など）</figcaption>
    </figure>

    <span class="el-tag">YouTube動画</span>
    <div class="art-video">''' + ph('YouTube動画（URL貼付で自動埋込・16:9）','','aspect-ratio:16/9') + '''</div>

    <span class="el-tag">ギャラリースライド</span>
    <div class="art-slider">
      <div class="art-slider__arrow --prev">‹</div>
      <div class="art-slider__arrow --next">›</div>
      ''' + ph('ギャラリー画像 1/4（スライド切替）','','aspect-ratio:16/9') + '''
      <div class="art-slider__dots"><i class="--on"></i><i></i><i></i><i></i></div>
    </div>
  </div>
</div></section>
<section class="section section--grey"><div class="container">
  <h2 class="section-title" style="font-size:20px;">関連記事</h2>
  <ul class="news-list" style="margin-top:16px;">
    <li class="news-item"><span class="news-item__date">2025.03.01</span><a class="news-item__title" href="news-detail.html">会社設立126周年を達成しました</a></li>
    <li class="news-item"><span class="news-item__date">2025.04.01</span><a class="news-item__title" href="news-detail.html">2027年度採用エントリー受付開始のご案内</a></li>
  </ul>
  <a class="btn btn--outline btn--sm" href="news.html" style="margin-top:24px;">一覧へ戻る</a>
</div></section>
'''
page("news-detail.html","記事タイトル｜新着情報｜近江度量衡株式会社", news_detail_body, active="news.html",
     crumbs=[("TOP","top.html"),("新着情報","news.html"),("記事詳細",None)])
PAGES.append(("I1","記事詳細","/news/[slug]/","news-detail.html","corp",True))

# ======================= J. お問い合わせ =======================
contact_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">CONTACT</p>
  <h1 class="page-header__title">お問い合わせ</h1>
  <p class="page-header__lead">製品・サービス・採用に関するご相談・お問い合わせはこちらから。</p>
</div></header>
<section class="section"><div class="container grid-2" style="gap:48px;align-items:start;">
  <div>
    <div style="display:flex;gap:0;margin-bottom:24px;flex-wrap:wrap;">
      <span class="page-nav" style="display:inline-block;"></span>
      <a class="btn btn--dark btn--sm" style="border-radius:0;">製品・技術について</a>
      <a class="btn btn--outline btn--sm" style="border-radius:0;">サービス・保守</a>
      <a class="btn btn--outline btn--sm" style="border-radius:0;">採用について</a>
      <a class="btn btn--outline btn--sm" style="border-radius:0;">その他</a>
    </div>
    <div class="form-group"><label class="form-label">会社名</label><input class="form-input" placeholder="（任意）"></div>
    <div class="form-group"><label class="form-label">お名前<span class="req">必須</span></label><input class="form-input"></div>
    <div class="form-group"><label class="form-label">部署・役職</label><input class="form-input" placeholder="（任意）"></div>
    <div class="form-group"><label class="form-label">メールアドレス<span class="req">必須</span></label><input class="form-input"></div>
    <div class="form-group"><label class="form-label">電話番号</label><input class="form-input" placeholder="（任意）"></div>
    <div class="form-group"><label class="form-label">お問い合わせ内容<span class="req">必須</span></label><textarea class="form-textarea"></textarea></div>
    <div class="form-group"><label style="font-size:13px;"><input type="checkbox"> <a href="privacy.html" style="border-bottom:1px solid #333;">プライバシーポリシー</a>に同意する</label></div>
    <a class="btn btn--dark" style="width:100%;text-align:center;">送信する</a>
    <p style="font-size:12px;color:#888;margin-top:12px;">送信後に自動返信メールをお送りします。</p>
  </div>
  <div>
    <div style="border:1px solid var(--c-border);padding:28px;">
      <h3 style="font-size:16px;font-weight:700;margin-bottom:16px;">本社</h3>
      <p style="font-size:13px;line-height:2;color:#444;">〒525-0054<br>滋賀県草津市東矢倉三丁目11番70号<br>TEL 077-562-7111<br>受付時間：平日 9:00〜17:00</p>
      <p style="font-size:12px;color:#888;margin-top:16px;line-height:1.8;">北海道・東京・九州など全国6拠点が対応します。最寄りの拠点へ直接お問い合わせも可能です。</p>
    </div>
  </div>
</div></section>
'''
page("contact.html","お問い合わせ｜近江度量衡株式会社", contact_body, active="",
     crumbs=[("TOP","top.html"),("お問い合わせ",None)])
PAGES.append(("J","お問い合わせ","/contact/","contact.html","corp",False))

# ======================= K. プライバシーポリシー =======================
privacy_items = [
 ("個人情報の取得","個人情報を適法かつ公正な手段によって取得します。"),
 ("利用目的","お問い合わせへの対応・採用選考・製品・サービスのご案内のために利用します。"),
 ("第三者提供","法令に基づく場合を除き、ご本人の同意なく第三者に個人情報を提供しません。"),
 ("個人情報の管理","個人情報の漏洩・滅失・毀損の防止のため、適切なセキュリティ対策を講じます。"),
 ("開示・訂正・削除","ご本人から個人情報の開示・訂正・削除のご要請があった場合、合理的な範囲で対応します。"),
]
priv = "".join(f'<div style="margin-top:32px;"><h2 style="font-size:18px;font-weight:700;border-left:3px solid var(--c-omi-red);padding-left:12px;">{i+1}. {t}</h2><p style="font-size:14px;color:#444;line-height:2;margin-top:12px;">{b}</p></div>' for i,(t,b) in enumerate(privacy_items))
privacy_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">PRIVACY POLICY</p>
  <h1 class="page-header__title">プライバシーポリシー</h1>
</div></header>
<section class="section"><div class="container" style="max-width:800px;">''' + priv + '''
  <div style="margin-top:32px;"><h2 style="font-size:18px;font-weight:700;border-left:3px solid var(--c-omi-red);padding-left:12px;">6. お問い合わせ窓口</h2>
    <p style="font-size:14px;color:#444;line-height:2;margin-top:12px;">近江度量衡株式会社 個人情報管理責任者<br>〒525-0054 滋賀県草津市東矢倉三丁目11番70号<br>Mail：omi-info@omiscale.co.jp</p></div>
  <p style="font-size:12px;color:#888;margin-top:32px;">本ポリシーは2026年3月21日に制定し、必要に応じて改定します。</p>
</div></section>
'''
page("privacy.html","プライバシーポリシー｜近江度量衡株式会社", privacy_body, active="",
     crumbs=[("TOP","top.html"),("プライバシーポリシー",None)])
PAGES.append(("K","プライバシーポリシー","/privacy/","privacy.html","corp",False))

# ======================= G. 採用TOP =======================
RCT_STYLE = """<style>
/* ── 採用トップ：有機的レイアウト ── */
.rct-fv{padding:72px 5vw 0;overflow:hidden;}
.rct-fv__eyebrow{font-family:var(--font-en);font-size:12px;letter-spacing:.3em;color:var(--c-muted);}
.rct-fv__title{font-size:clamp(38px,6.4vw,86px);font-weight:900;line-height:1.4;letter-spacing:.04em;margin-top:18px;position:relative;z-index:2;}
.rct-fv__title span{display:block;}
.rct-fv__title .idnt{margin-left:1.4em;}
.rct-fv__grid{display:grid;grid-template-columns:5fr 7fr;gap:40px;align-items:start;margin-top:28px;}
.rct-fv__main{margin-top:-90px;}   /* タイトルに食い込ませる（有機的な重なり） */
.rct-fv__sub{padding-top:34px;display:flex;flex-direction:column;gap:28px;}
.rct-fv__sub p{font-size:14.5px;line-height:2.2;max-width:400px;}
.rct-fv__subphoto{width:72%;}
.rct-marq{overflow:hidden;border-top:1px solid var(--c-border);border-bottom:1px solid var(--c-border);padding:16px 0;margin-top:64px;background:#fff;}
.rct-marq__in{display:flex;gap:56px;white-space:nowrap;width:max-content;animation:rctmarq 28s linear infinite;}
.rct-marq__in span{font-family:var(--font-en);font-size:13px;font-weight:600;letter-spacing:.3em;text-transform:uppercase;color:var(--c-muted);}
@keyframes rctmarq{to{transform:translateX(-50%);}}
.rct-wm{font-family:var(--font-en);font-weight:700;font-size:clamp(58px,9vw,128px);line-height:1;letter-spacing:.02em;color:#f0f0f0;user-select:none;white-space:nowrap;}
.section--dark .rct-wm,.section--grey .rct-wm{color:rgba(255,255,255,.05);}
.section--grey .rct-wm{color:#e7e7e7;}
.rct-menu{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;}
.rct-menu a{display:flex;flex-direction:column;border:1px solid var(--c-border);background:#fff;transition:opacity .2s;}
.rct-menu a:hover{opacity:.75;}
.rct-menu a .ph{aspect-ratio:16/10;}
.rct-menu a:first-child{grid-row:span 2;}
.rct-menu a:first-child .ph{flex:1;aspect-ratio:auto;min-height:300px;}
.rct-menu__bar{display:flex;align-items:baseline;gap:14px;padding:18px 20px;}
.rct-menu__no{font-family:var(--font-en);font-size:11px;font-weight:600;letter-spacing:.18em;color:var(--c-muted);}
.rct-menu__ttl{font-size:15px;font-weight:700;}
.rct-menu__bar i{margin-left:auto;font-style:normal;}
.rct-vision{display:grid;grid-template-columns:6fr 5fr;gap:56px;align-items:start;}
.rct-vision__photos{display:flex;flex-direction:column;align-items:flex-end;}
.rct-vision__p1{width:100%;}
.rct-vision__p2{width:56%;margin-top:-18%;margin-right:58%;}  /* ずらして重ねる */
.rct-num{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.14);}
.rct-num__cell{background:var(--c-dark);padding:34px 26px;}
.rct-num__cell.--wide{grid-column:span 2;}
.rct-num__val{font-family:var(--font-en);font-weight:600;font-size:clamp(40px,4.6vw,72px);line-height:1;letter-spacing:.02em;}
.rct-num__cell.--wide .rct-num__val{font-size:clamp(64px,8vw,120px);}
.rct-num__val small{font-size:.38em;margin-left:6px;letter-spacing:.06em;}
.rct-num__label{font-size:12px;color:rgba(255,255,255,.6);margin-top:12px;}
.rct-people{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;align-items:start;}
.rct-people .interview-card:nth-child(2){margin-top:64px;}
.rct-people .interview-card:nth-child(3){margin-top:128px;}
.rct-welf{display:grid;grid-template-columns:5fr 7fr;gap:56px;align-items:start;}
.rct-welf__list{border-top:1px solid var(--c-border);}
.rct-welf__row{display:flex;align-items:baseline;gap:22px;padding:20px 4px;border-bottom:1px solid var(--c-border);}
.rct-welf__no{font-family:var(--font-en);font-size:11px;font-weight:600;letter-spacing:.16em;color:var(--c-muted);flex:0 0 34px;}
.rct-welf__ttl{font-size:15px;font-weight:700;flex:0 0 15em;}
.rct-welf__desc{font-size:12.5px;color:var(--c-mid);line-height:1.8;}
@media(max-width:760px){
  .rct-fv__grid{grid-template-columns:1fr;gap:24px;}
  .rct-fv__main{margin-top:0;order:-1;}
  .rct-fv__subphoto{width:60%;}
  .rct-menu{grid-template-columns:1fr 1fr;}
  .rct-menu a:first-child{grid-row:auto;grid-column:span 2;}
  .rct-menu a:first-child .ph{aspect-ratio:16/10;min-height:0;}
  .rct-vision{grid-template-columns:1fr;gap:32px;}
  .rct-num{grid-template-columns:1fr 1fr;}
  .rct-people{grid-template-columns:1fr;gap:24px;}
  .rct-people .interview-card:nth-child(2),.rct-people .interview-card:nth-child(3){margin-top:0;}
  .rct-welf{grid-template-columns:1fr;gap:28px;}
  .rct-welf__ttl{flex:0 0 auto;}
  .rct-welf__row{flex-wrap:wrap;}
}
</style>"""

_marq_items = "".join('<span>OMISCALE RECRUIT 2027</span><span>—</span><span>WE MEASURE THE VALUE OF LIVING</span><span>—</span>' for _ in range(4))

recruit_body = (RCT_STYLE + '''
<!-- ① FV：大タイポ×写真の重なり -->
<section class="rct-fv">
  <p class="rct-fv__eyebrow">OMISCALE RECRUIT 2027</p>
  <h1 class="rct-fv__title"><span>「いきる」の単位とは、</span><span class="idnt">なんだろう。</span></h1>
  <div class="rct-fv__grid">
    <div class="rct-fv__sub">
      <p>「働く人を大切にする」という理念のもと、あなたの確かな仕事で、豊かな未来を担う力になる。</p>
      <div class="fv__cta" style="position:static;"><a class="btn btn--red" href="recruit-jobs.html" style="background:#111315;color:#fff;">募集要項を見る</a><a class="btn btn--outline" href="recruit-interview.html">社員インタビュー</a></div>
      <div class="rct-fv__subphoto">''' + ph('サブ写真：作業の手元・道具','','aspect-ratio:4/5') + '''</div>
    </div>
    <div class="rct-fv__main">''' + ph('採用キービジュアル（現場・社員／動画可）','','aspect-ratio:4/3') + '''</div>
  </div>
  <div class="rct-marq"><div class="rct-marq__in">''' + _marq_items + '''</div></div>
</section>

<!-- ② コンテンツメニュー（写真モザイク） -->
<section class="section"><div class="container">
  <div class="rct-menu">
    <a href="recruit-interview.html"><span class="ph" style="min-height:300px;"><span>社員インタビュー 写真（大）</span></span><span class="rct-menu__bar"><span class="rct-menu__no">01</span><span class="rct-menu__ttl">社員インタビュー</span><i>→</i></span></a>
    <a href="#vision"><span class="ph"><span>ビジョン 写真</span></span><span class="rct-menu__bar"><span class="rct-menu__no">02</span><span class="rct-menu__ttl">ビジョン</span><i>→</i></span></a>
    <a href="#numbers"><span class="ph"><span>数字 写真</span></span><span class="rct-menu__bar"><span class="rct-menu__no">03</span><span class="rct-menu__ttl">数字で見る近江度量衡</span><i>→</i></span></a>
    <a href="#welfare"><span class="ph"><span>福利厚生 写真</span></span><span class="rct-menu__bar"><span class="rct-menu__no">04</span><span class="rct-menu__ttl">福利厚生・職場環境</span><i>→</i></span></a>
    <a href="recruit-jobs.html"><span class="ph"><span>募集要項 写真</span></span><span class="rct-menu__bar"><span class="rct-menu__no">05</span><span class="rct-menu__ttl">募集要項</span><i>→</i></span></a>
  </div>
</div></section>

<!-- ③ VISION：ウォーターマーク＋ずらし写真 -->
<section class="section" id="vision" style="overflow:hidden;"><div class="container">
  <p class="rct-wm">VISION</p>
  <div class="rct-vision" style="margin-top:-18px;">
    <div>
      <p class="statement__en">VISION &amp; VALUES</p>
      <h2 class="statement__main" style="text-align:left;font-size:clamp(24px,3vw,38px);">「いきる」をはかり、<br>豊かな世界へ。</h2>
      <p class="statement__body" style="text-align:left;margin-top:20px;">「技術」と「誇り」を礎に、日本から世界へ、計量という仕事で社会を豊かにし続けること。それが、近江度量衡の使命です。採用においても「働く人を大切にする」という理念を核に、長く誇りを持って働ける環境を目指しています。</p>
      <div class="grid-3" style="margin-top:32px;">
        <div class="pillar"><div class="pillar__title">技術</div></div>
        <div class="pillar"><div class="pillar__title">誇り</div></div>
        <div class="pillar"><div class="pillar__title">グローバル</div></div>
      </div>
      <p style="font-size:13px;margin-top:24px;"><a href="history.html" style="border-bottom:1px solid #999;">126年ヒストリーを見る →</a></p>
    </div>
    <div class="rct-vision__photos">
      <div class="rct-vision__p1">''' + ph('ビジョン写真①：現場・チーム','','aspect-ratio:4/3') + '''</div>
      <div class="rct-vision__p2">''' + ph('写真②：手元','','aspect-ratio:1') + '''</div>
    </div>
  </div>
</div></section>

<!-- ④ NUMBERS：巨大数字タイル -->
<section class="section section--dark" id="numbers" style="overflow:hidden;"><div class="container">
  <p class="rct-wm">NUMBERS</p>
  <p class="statement__en" style="margin-top:-10px;">数字で見る近江度量衡</p>
  <div class="rct-num" style="margin-top:28px;">
    <div class="rct-num__cell --wide"><div class="rct-num__val">126<small>年</small></div><div class="rct-num__label">創業からの歴史（1900年創業）</div></div>
    <div class="rct-num__cell"><div class="rct-num__val">2,000<small>+</small></div><div class="rct-num__label">累計納入施設数</div></div>
    <div class="rct-num__cell"><div class="rct-num__val">9<small>拠点</small></div><div class="rct-num__label">国内6＋海外3</div></div>
    <div class="rct-num__cell"><div class="rct-num__val">約150<small>名</small></div><div class="rct-num__label">従業員数 ''' + todo('要確認') + '''</div></div>
    <div class="rct-num__cell"><div class="rct-num__val">〇〇<small>%</small></div><div class="rct-num__label">新卒3年定着率 ''' + todo('数値提供待ち') + '''</div></div>
    <div class="rct-num__cell"><div class="rct-num__val">〇〇<small>歳</small></div><div class="rct-num__label">平均年齢 ''' + todo('数値提供待ち') + '''</div></div>
    <div class="rct-num__cell"><div class="rct-num__val">3<small>カ国</small></div><div class="rct-num__label">海外展開（中国・タイ・韓国）</div></div>
  </div>
</div></section>

<!-- ⑤ PEOPLE：互い違いの大きなカード -->
<section class="section" style="overflow:hidden;"><div class="container">
  <p class="rct-wm">PEOPLE</p>
  <div style="display:flex;flex-wrap:wrap;align-items:baseline;gap:18px;margin-top:-10px;">
    <h2 class="section-title">技術と誇りを持って働く、近江の現場のことば。</h2>
    <a class="btn btn--outline btn--sm" href="recruit-interview.html" style="margin-left:auto;">インタビュー一覧へ</a>
  </div>
  <p class="section-lead">現場・設計・営業——それぞれの視点で語る、近江度量衡の仕事。''' + todo('実在社員に差し替え') + '''</p>
  <div class="rct-people" style="margin-top:40px;">
    <a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">''' + ph('社員写真（縦）','','aspect-ratio:3/4') + '''</div><div class="interview-card__body"><div class="interview-card__dept">製造部 / 入社〇年目（20代）</div><div class="interview-card__name">山田 〇〇</div><p class="interview-card__quote">毎回違う課題に向き合うから、技術者として本当に成長できる。</p></div></a>
    <a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">''' + ph('社員写真（縦）','','aspect-ratio:3/4') + '''</div><div class="interview-card__body"><div class="interview-card__dept">設計部 / 入社〇年目（30代）</div><div class="interview-card__name">鈴木 〇〇</div><p class="interview-card__quote">図面通りにつくるのではなく、現場に合わせてつくる。</p></div></a>
    <a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">''' + ph('社員写真（縦）','','aspect-ratio:3/4') + '''</div><div class="interview-card__body"><div class="interview-card__dept">営業部 / 入社〇年目（30代）</div><div class="interview-card__name">田中 〇〇</div><p class="interview-card__quote">お客様の現場を見て、何が必要か考える。</p></div></a>
  </div>
</div></section>

<!-- ⑥ WELFARE：写真×リスト -->
<section class="section section--grey" id="welfare" style="overflow:hidden;"><div class="container">
  <p class="rct-wm">WELFARE</p>
  <div class="rct-welf" style="margin-top:-10px;">
    <div>
      <p class="section-meta">Welfare</p>
      <h2 class="section-title">福利厚生・職場環境</h2>
      <p class="section-lead" style="margin-top:14px;">「働く人を大切にする」という理念を体現する制度・環境を整えています。</p>
      <div style="margin-top:28px;">''' + ph('職場環境の写真：休憩・オフィス','','aspect-ratio:4/3') + '''</div>
    </div>
    <div class="rct-welf__list">
      <div class="rct-welf__row"><span class="rct-welf__no">01</span><span class="rct-welf__ttl">各種社会保険完備</span><span class="rct-welf__desc">健康保険・厚生年金・雇用保険・労災保険</span></div>
      <div class="rct-welf__row"><span class="rct-welf__no">02</span><span class="rct-welf__ttl">有給休暇・育児休暇</span><span class="rct-welf__desc">取得実績・取得率は掲載時に記載 ''' + todo('実績確認') + '''</span></div>
      <div class="rct-welf__row"><span class="rct-welf__no">03</span><span class="rct-welf__ttl">住宅手当・通勤手当</span><span class="rct-welf__desc">支給条件の詳細は募集要項に記載</span></div>
      <div class="rct-welf__row"><span class="rct-welf__no">04</span><span class="rct-welf__ttl">研修制度</span><span class="rct-welf__desc">入社時研修・OJT・資格取得支援</span></div>
      <div class="rct-welf__row"><span class="rct-welf__no">05</span><span class="rct-welf__ttl">フレックス・リモート対応</span><span class="rct-welf__desc">''' + todo('実施状況を確認') + '''</span></div>
      <div class="rct-welf__row"><span class="rct-welf__no">06</span><span class="rct-welf__ttl">社内施設・福利厚生</span><span class="rct-welf__desc">食堂・保養施設など ''' + todo('内容確認') + '''</span></div>
    </div>
  </div>
</div></section>

<!-- ⑦ CAREER PATH -->
<section class="section" id="career"><div class="container">
  <p class="section-meta">Career Path</p><h2 class="section-title">研修・キャリアパス</h2>
  <p class="section-lead">入社後の育成プログラム・OJT・キャリアパス事例を紹介。技術者として誇りを持って成長できる環境を、具体的なロードマップで。</p>
  <div class="process" style="margin-top:32px;">
    <div class="process-step"><div class="process-step__num">STEP 01</div><div class="process-step__title">入社〜3ヶ月</div><div class="process-step__desc">入社時研修・OJT開始</div></div>
    <div class="process-step"><div class="process-step__num">STEP 02</div><div class="process-step__title">〜1年</div><div class="process-step__desc">OJT・現場実務</div></div>
    <div class="process-step"><div class="process-step__num">STEP 03</div><div class="process-step__title">〜3年</div><div class="process-step__desc">独立担当・専門性強化</div></div>
    <div class="process-step"><div class="process-step__num">STEP 04</div><div class="process-step__title">5年〜</div><div class="process-step__desc">リーダー・専門職</div></div>
  </div>
  <div class="grid-3" style="margin-top:24px;">
    <div class="use-item">技術スペシャリスト</div><div class="use-item">プロジェクトマネジャー</div><div class="use-item">海外担当</div>
  </div>
</div></section>

<!-- ⑧ ENTRY -->
<section class="section section--dark theme-recruit" id="entry" style="background:#111315;"><div class="container">
  <div class="statement"><h2 class="statement__main" style="color:#fff;font-size:clamp(28px,3.6vw,46px);">あなたの「測る」を見つけてください。</h2>
  <p class="statement__body" style="color:#bbb;">新卒・中途、いずれも募集中です。126年の技術と誇りを、次の世代へ。</p></div>
  <div class="entry-split" style="margin-top:44px;">
    <div class="entry-card"><div class="entry-card__label">NEW GRADUATE 新卒採用</div><div class="entry-card__copy">「未来を測る第一歩を、ここから。」</div><a class="btn btn--white" href="recruit-jobs-graduate.html">新卒採用</a></div>
    <div class="entry-card"><div class="entry-card__label">MID-CAREER 中途採用</div><div class="entry-card__copy">「培った経験を、126年の精度に加えてください。」</div><a class="btn btn--white" href="recruit-jobs-career.html">中途採用</a></div>
  </div>
</div></section>
''')

page("recruit.html","採用情報｜近江度量衡 ― 「いきる」の単位とは、なんだろう。", recruit_body,
     active="recruit.html", recruit=True, crumbs=None)
PAGES.append(("G","採用TOP","/recruit/","recruit.html","recruit",False))

RC = [("TOP","top.html"),("採用情報","recruit.html")]

# ======================= G3. 社員インタビュー一覧 =======================
INTERVIEWEES = [
 ("製造部 / 入社〇年目（20代）","山田 〇〇","毎回違う課題に向き合うから、技術者として本当に成長できる。誇りを持てる仕事です。"),
 ("設計部 / 入社〇年目（30代）","鈴木 〇〇","図面通りにつくるのではなく、現場に合わせてつくる。グローバルな現場を支える実感があります。"),
 ("営業部 / 入社〇年目（30代）","田中 〇〇","お客様の現場を見て、何が必要か考える。"),
 ("技術開発部 / 入社〇年目（20代）","佐藤 〇〇","入社後、こんなに任せてもらえると思っていなかった。"),
 ("サービス部 / 入社〇年目（40代）","伊藤 〇〇","全国の現場を飛び回って、お客様に「ありがとう」と言われる瞬間が好き。"),
]
cards = "".join(f'<a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">'+ph('社員写真')+f'</div><div class="interview-card__body"><div class="interview-card__dept">{d}</div><div class="interview-card__name">{n}</div><p class="interview-card__quote">{q}</p><span class="interview-card__link">インタビューを読む →</span></div></a>' for d,n,q in INTERVIEWEES)
interview_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">PEOPLE</p>
  <h1 class="page-header__title">社員インタビュー</h1>
  <p class="page-header__lead">現場・設計・営業——それぞれの視点で語る、近江度量衡の仕事。</p>
</div></header>
<section class="section"><div class="container">
  <div class="grid-3">''' + cards + '''</div>
  <div class="cms-note">◯ 職種別3〜5名からスタートし段階的に増加。戦略的PR対象者（育休取得男性・働くお母さん等）も配置。インタビュー詳細は投稿テンプレートで自社更新（AI活用で持続可能な更新方式を検討）。''' + cms('CMS更新') + todo('実在社員・写真を提供') + '''</div>
</div></section>
'''
page("recruit-interview.html","社員インタビュー｜近江度量衡 採用", interview_body,
     active="recruit-interview.html", recruit=True, crumbs=RC+[("社員インタビュー",None)])
PAGES.append(("G3","社員インタビュー","/recruit/interview/","recruit-interview.html","recruit",True))

# G3-1 インタビュー詳細
QA = [
 ("近江度量衡を選んだ理由を教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("現在担当している業務内容を教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("仕事のやりがい・難しさを教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("今後の目標・キャリアの展望を教えてください。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
 ("就活生・転職希望者へのメッセージをお願いします。","〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇"),
]
qahtml = "".join(f'<div class="qa"><div class="qa__q">{q}</div><div class="qa__a">{a}</div></div>' for q,a in QA)
# インタビュー詳細：Q&A（写真枠を挟む）＋1日のスケジュール＋関連社員＋関連製品
def _qa(i):
    return f'<div class="qa"><div class="qa__q">{QA[i][0]}</div><div class="qa__a">{QA[i][1]}</div></div>'

ISCHED_STYLE = '''<style>
.ischedule{border-top:1px solid var(--c-border);}
.ischedule__row{display:flex;gap:22px;padding:15px 0;border-bottom:1px solid var(--c-border);}
.ischedule__time{flex:0 0 62px;font-family:var(--font-en);font-weight:600;font-size:15px;letter-spacing:.04em;color:var(--c-black);padding-top:2px;}
.ischedule__body b{display:block;font-family:var(--font-ja);font-size:14px;font-weight:700;}
.ischedule__body p{font-size:12.5px;color:var(--c-mid);line-height:1.7;margin-top:4px;}
</style>'''

_SCHED = [
 ("8:00","出社・朝礼","一日の作業予定と安全確認をチームで共有。"),
 ("8:30","段取り・設備点検","担当ラインを点検し、計量精度をチェックします。"),
 ("10:00","製造・組立作業","図面をもとに計量システムの組立・配線を進めます。"),
 ("12:00","昼休憩",""),
 ("13:00","打ち合わせ","設計・営業と仕様をすり合わせ。現場目線で意見を出します。"),
 ("15:00","検査・調整","完成した装置の計量精度を全数チェック・微調整。"),
 ("17:00","記録・翌日の準備","作業記録をまとめ、翌日の段取りを確認します。"),
 ("17:30","退社",""),
]
_sched_rows = "".join(
    f'<div class="ischedule__row"><span class="ischedule__time">{t}</span>'
    f'<div class="ischedule__body"><b>{h}</b>' + (f'<p>{b}</p>' if b else '') + '</div></div>'
    for t,h,b in _SCHED)

_related_members = "".join(
    f'<a class="interview-card" href="recruit-interview-detail.html"><div class="interview-card__img">'
    + ph('社員写真') +
    f'</div><div class="interview-card__body"><div class="interview-card__dept">{d}</div>'
    f'<div class="interview-card__name">{n}</div><p class="interview-card__quote">{q}</p>'
    f'<span class="interview-card__link">インタビューを読む →</span></div></a>'
    for d,n,q in [
        ("設計部 / 入社〇年目（30代）","鈴木 〇〇","図面通りにつくるのではなく、現場に合わせてつくる。"),
        ("営業部 / 入社〇年目（30代）","田中 〇〇","お客様の現場を見て、何が必要か考える。"),
        ("制御・技術電装部 / 入社〇年目（20代）","佐藤 〇〇","ソフトも自社。だから面白い。"),
    ])

IDV_STYLE = """<style>
/* ── インタビュー詳細（ベンチマーク: giken-kk voice 準拠） ── */
.gv-hero{display:grid;grid-template-columns:5fr 7fr;min-height:520px;background:var(--c-black);color:#fff;}
.gv-hero__txt{display:flex;flex-direction:column;justify-content:center;padding:72px 56px;}
.gv-hero__no{font-family:var(--font-en);font-size:12px;letter-spacing:.3em;color:var(--c-muted);}
.gv-hero__no b{display:block;font-size:64px;font-weight:600;line-height:1;margin-top:10px;color:rgba(255,255,255,.14);}
.gv-hero__role{font-size:clamp(24px,2.6vw,36px);font-weight:700;line-height:1.6;margin-top:16px;}
.gv-hero__meta{font-size:14px;color:rgba(255,255,255,.75);margin-top:14px;}
.gv-hero__meta b{font-family:var(--font-en);font-size:22px;color:#fff;margin-left:14px;letter-spacing:.1em;}
.gv-hero__photo .ph{height:100%;min-height:420px;}
.gv-status{background:#fff;border:1px solid var(--c-border);padding:36px 40px;display:grid;grid-template-columns:auto 1fr;gap:40px;align-items:center;}
.gv-status__avatar .ph{width:132px;height:132px;border-radius:50%;}
.gv-status__label{font-family:var(--font-en);font-size:11px;letter-spacing:.26em;color:var(--c-muted);}
.gv-status__grid{display:grid;grid-template-columns:repeat(4,auto);gap:8px 36px;margin-top:14px;width:fit-content;}
.gv-status__item small{display:block;font-size:10px;color:var(--c-muted);}
.gv-status__item b{font-size:13.5px;}
.gv-tags{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px;}
.gv-tags span{border:1px solid var(--c-black);border-radius:999px;padding:6px 16px;font-size:12px;font-weight:700;}
.gv-sec{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center;}
.gv-sec.--rev .gv-sec__txt{order:2;}
.gv-sec__en{font-family:var(--font-en);font-size:12px;font-weight:600;letter-spacing:.3em;color:var(--c-muted);}
.gv-sec__catch{font-size:clamp(22px,2.4vw,32px);font-weight:700;line-height:1.7;margin-top:12px;}
.gv-sec__body{font-size:14px;line-height:2.15;color:#333;margin-top:20px;}
.gv-qa{position:relative;}
.gv-qa__item{background:#fff;border:1px solid var(--c-border);padding:26px 30px;}
.gv-qa__item+.gv-qa__item{margin-top:14px;}
.gv-qa__q{font-size:15px;font-weight:700;}
.gv-qa__q::before{content:'Q.';font-family:var(--font-en);color:var(--c-muted);margin-right:10px;}
.gv-qa__a{font-size:13px;line-height:2;color:#444;margin-top:10px;padding-left:26px;}
.gv-sched__tabs{display:flex;gap:0;margin-bottom:24px;}
.gv-sched__tab{flex:1;text-align:center;padding:13px;font-family:var(--font-en);font-weight:700;letter-spacing:.2em;border:1px solid var(--c-black);font-size:13px;}
.gv-sched__tab.--on{background:var(--c-black);color:#fff;}
.gv-sched{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;}
.gv-msg{background:var(--c-black);color:#fff;}
.gv-msg__inner{display:grid;grid-template-columns:7fr 5fr;gap:56px;align-items:center;}
.gv-msg__label{font-family:var(--font-en);font-size:12px;letter-spacing:.3em;color:var(--c-muted);}
.gv-msg__catch{font-size:clamp(22px,2.6vw,34px);font-weight:700;line-height:1.8;margin-top:16px;}
.gv-msg__body{font-size:14px;line-height:2.15;color:rgba(255,255,255,.8);margin-top:18px;}
@media(max-width:760px){
  .gv-hero{grid-template-columns:1fr;}
  .gv-hero__txt{padding:48px 24px;}
  .gv-hero__photo .ph{min-height:0;height:auto;aspect-ratio:4/3;}
  .gv-status{grid-template-columns:1fr;gap:24px;padding:28px 22px;}
  .gv-status__grid{grid-template-columns:1fr 1fr;}
  .gv-sec{grid-template-columns:1fr;gap:24px;}
  .gv-sec.--rev .gv-sec__txt{order:0;}
  .gv-sched{grid-template-columns:1fr;gap:28px;}
  .gv-msg__inner{grid-template-columns:1fr;gap:28px;}
}
</style>"""

def _gv_sched(rows):
    out = '<div class="ischedule">'
    for t,h,b in rows:
        out += ('<div class="ischedule__row"><span class="ischedule__time">' + t + '</span>'
                '<div class="ischedule__body"><b>' + h + '</b>' + ('<p>' + b + '</p>' if b else '') + '</div></div>')
    return out + '</div>'

_SCHED_OFF = [
 ("8:00","起床",""),
 ("10:00","趣味・買い物",""),
 ("12:00","昼食",""),
 ("14:00","家族・友人と過ごす",""),
 ("18:00","夕食",""),
 ("23:00","就寝",""),
]

interview_detail_body = (IDV_STYLE + '''
<!-- HERO：職種／入社年・区分／イニシャル（ベンチマーク準拠のシンプル構成） -->
<section class="gv-hero">
  <div class="gv-hero__txt">
    <p class="gv-hero__no">INTERVIEW <b>01</b></p>
    <h1 class="gv-hero__role">製造・組立担当</h1>
    <p class="gv-hero__meta">中途／20〇〇年入社 <b>Y.S.</b></p>
    <p style="font-size:11px;color:rgba(255,255,255,.45);margin-top:18px;">※氏名はイニシャル・実名どちらも可（ご本人の希望に合わせます）''' + todo('ヒアリング【A】より') + '''</p>
  </div>
  <div class="gv-hero__photo">''' + ph('メイン写真：現場での上半身〜全身','','height:100%') + '''</div>
</section>
''' + ISCHED_STYLE + '''

<!-- MEMBER STATUS（アバター＋基本情報＋人柄タグ） -->
<section class="section" style="padding-bottom:0;"><div class="container" style="max-width:980px;">
  <div class="gv-status">
    <div class="gv-status__avatar">''' + ph('顔写真（丸抜き）','','width:132px;height:132px;border-radius:50%;') + '''</div>
    <div>
      <p class="gv-status__label">MEMBER STATUS</p>
      <div class="gv-status__grid">
        <div class="gv-status__item"><small>部門</small><b>製造部</b></div>
        <div class="gv-status__item"><small>職種</small><b>計量システムの組立・検査</b></div>
        <div class="gv-status__item"><small>入社</small><b>20〇〇年／中途</b></div>
        <div class="gv-status__item"><small>出身</small><b>滋賀県（任意）</b></div>
        <div class="gv-status__item"><small>好きな食べ物</small><b>〇〇〇〇</b></div>
        <div class="gv-status__item"><small>趣味</small><b>〇〇〇〇</b></div>
      </div>
      <div class="gv-tags"><span>コツコツ型</span><span>ものづくり好き</span><span>チームワーク</span><span>好奇心</span><span>慎重派</span>''' + todo('人柄タグ3〜5つ＝ヒアリング【A】より') + '''</div>
    </div>
  </div>
</div></section>

<!-- REASONS：入社理由 -->
<section class="section"><div class="container" style="max-width:1060px;">
  <div class="gv-sec">
    <div class="gv-sec__txt">
      <p class="gv-sec__en">REASONS <span style="letter-spacing:.1em;">― 入社理由</span></p>
      <h2 class="gv-sec__catch">「（回答から抜粋したキャッチコピー）」''' + cms('見出し=回答から制作側で抜粋') + '''</h2>
      <p class="gv-sec__body">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。''' + todo('ヒアリング【B】Q1 入社のきっかけ') + '''</p>
    </div>
    <div>''' + ph('写真：入社当時を語る表情（横）','','aspect-ratio:4/3') + '''</div>
  </div>
</div></section>

<!-- WORKS：仕事内容・やりがい -->
<section class="section section--grey"><div class="container" style="max-width:1060px;">
  <div class="gv-sec --rev">
    <div class="gv-sec__txt">
      <p class="gv-sec__en">WORKS <span style="letter-spacing:.1em;">― 仕事内容・やりがい</span></p>
      <h2 class="gv-sec__catch">「（回答から抜粋したキャッチコピー）」</h2>
      <p class="gv-sec__body">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。''' + todo('ヒアリング【B】Q2仕事内容＋Q3やりがい') + '''</p>
      <p class="gv-sec__body">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。''' + todo('ヒアリング【B】Q4 一品一様エピソード') + '''</p>
    </div>
    <div>''' + ph('写真：作業風景（横・大）','','aspect-ratio:4/3') + '''</div>
  </div>
  <div class="grid-2" style="margin-top:28px;gap:28px;">
    <div>''' + ph('写真：作業の手元','','aspect-ratio:16/9') + '''</div>
    <div>''' + ph('写真：チーム・職場','','aspect-ratio:16/9') + '''</div>
  </div>
</div></section>

<!-- FUTURE：今後の目標 -->
<section class="section"><div class="container" style="max-width:1060px;">
  <div class="gv-sec">
    <div class="gv-sec__txt">
      <p class="gv-sec__en">FUTURE <span style="letter-spacing:.1em;">― 今後の目標</span></p>
      <h2 class="gv-sec__catch">「（回答から抜粋したキャッチコピー）」</h2>
      <p class="gv-sec__body">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。''' + todo('ヒアリング【B】Q5 今後の目標') + '''</p>
    </div>
    <div>''' + ph('写真：ポートレート（縦）','','aspect-ratio:4/5;max-width:420px;margin-left:auto;') + '''</div>
  </div>
</div></section>

<!-- Q&A：一問一答 -->
<section class="section section--grey"><div class="container" style="max-width:860px;">
  <p class="section-meta">Q&amp;A</p>
  <h2 class="section-title">一問一答</h2>
  <div class="gv-qa" style="margin-top:28px;">
    <div class="gv-qa__item"><p class="gv-qa__q">仕事をする上で意識していることは？</p><p class="gv-qa__a">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。''' + todo('ヒアリング【C】') + '''</p></div>
    <div class="gv-qa__item"><p class="gv-qa__q">入社当時と比べ、仕事に対する姿勢はどのように変わりましたか？</p><p class="gv-qa__a">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。</p></div>
    <div class="gv-qa__item"><p class="gv-qa__q">入社前後で、働くイメージにギャップはありましたか？</p><p class="gv-qa__a">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。</p></div>
    <div class="gv-qa__item"><p class="gv-qa__q">入社後に成長できたと感じることは？</p><p class="gv-qa__a">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。</p></div>
    <div class="gv-qa__item"><p class="gv-qa__q">「働く人を大切にする」と感じる場面はありますか？</p><p class="gv-qa__a">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。（近江度量衡オリジナル質問）</p></div>
  </div>
</div></section>

<!-- SCHEDULE：ON / OFF -->
<section class="section"><div class="container" style="max-width:980px;">
  <p class="section-meta">Schedule</p>
  <h2 class="section-title">ある1日のスケジュール</h2>
  <div class="gv-sched__tabs" style="margin-top:28px;max-width:420px;">
    <div class="gv-sched__tab --on">ON ― 仕事の日</div>
    <div class="gv-sched__tab">OFF ― 休みの日</div>
  </div>
  <p style="font-size:11px;color:#999;margin:-12px 0 20px;">※実装はタブ切替（ワイヤーでは両方併記）''' + todo('ヒアリング【D】より') + '''</p>
  <div class="gv-sched">
    <div><p style="font-family:var(--font-en);font-weight:700;letter-spacing:.2em;font-size:12px;margin-bottom:12px;">ON</p>''' + _gv_sched(_SCHED) + '''</div>
    <div><p style="font-family:var(--font-en);font-weight:700;letter-spacing:.2em;font-size:12px;margin-bottom:12px;">OFF</p>''' + _gv_sched(_SCHED_OFF) + '''</div>
  </div>
</div></section>

<!-- MESSAGE：就活生・転職希望者へ -->
<section class="section gv-msg"><div class="container" style="max-width:1060px;">
  <div class="gv-msg__inner">
    <div>
      <p class="gv-msg__label">MESSAGE</p>
      <h2 class="gv-msg__catch">就活生・転職を考えている方へ</h2>
      <p class="gv-msg__body">〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇〇。''' + todo('ヒアリング【E】メッセージ') + '''</p>
    </div>
    <div>''' + ph('写真：笑顔のカット（横）','','aspect-ratio:4/3') + '''</div>
  </div>
</div></section>

<!-- 他の社員 -->
<section class="section section--grey"><div class="container">
  <p class="section-meta">Other Members</p>
  <h2 class="section-title">ほかの社員インタビュー</h2>
  <div class="grid-3" style="margin-top:24px;">''' + _related_members + '''</div>
  <div style="text-align:center;margin-top:36px;"><a class="btn btn--outline btn--sm" href="recruit-interview.html">インタビュー一覧へ戻る</a></div>
</div></section>

<section class="section"><div class="container">
  <div class="cms-note">◯ 構成ベンチマーク：岐建 採用サイト VOICE（HERO＝職種/入社年/イニシャル → MEMBER STATUS → REASONS → WORKS → FUTURE → 一問一答 → ON/OFFスケジュール → MESSAGE）。原稿はヒアリングシート（【A】ステータス／【B】Q1-5=REASONS・WORKS・FUTURE／【C】一問一答／【D】ON・OFFスケジュール／【E】メッセージ）から構成。''' + cms('CMS更新') + '''</div>
</div></section>
''')

page("recruit-interview-detail.html","社員インタビュー 詳細｜近江度量衡 採用", interview_detail_body,
     active="recruit-interview.html", recruit=True, crumbs=RC+[("社員インタビュー","recruit-interview.html"),("詳細",None)])
PAGES.append(("G3-1","インタビュー詳細","/recruit/interview/[slug]/","recruit-interview-detail.html","recruit",True))

# ======================= G8. 採用ニュース =======================
fil, items = news_list(["すべて","説明会","インターン","中途募集","お知らせ"],
  [("2026.04.10","説明会","2027年度新卒向け合同会社説明会のご案内（5月開催）"),
   ("2026.04.01","中途募集","機械設計エンジニア・営業職の中途採用募集を開始しました"),
   ("2026.03.01","お知らせ","2027年度新卒エントリー受付を開始しました"),
   ("2026.02.10","インターン","京都大学工学部との連携インターンシップ参加者募集"),
   ("2025.10.15","インターン","冬季インターンシップ参加者募集")], detail="recruit-news.html")
recruit_news_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">RECRUIT NEWS</p>
  <h1 class="page-header__title">採用ニュース</h1>
  <p class="page-header__lead">セミナー・説明会の開催情報、中途採用の募集情報など、採用に関するお知らせをタイムリーに発信します。</p>
</div></header>
<section class="section"><div class="container">
  <div style="margin-bottom:24px;">''' + fil + '''</div>
  <ul class="news-list">''' + items + '''</ul>
  <div class="cms-note">◯ コーポレートの新着情報（/news/）とは独立して運用。カスタム投稿でタイムリーに発信。''' + cms('CMS更新') + '''</div>
</div></section>
'''
page("recruit-news.html","採用ニュース｜近江度量衡 採用", recruit_news_body,
     active="recruit-news.html", recruit=True, crumbs=RC+[("採用ニュース",None)])
PAGES.append(("G8","採用ニュース","/recruit/news/","recruit-news.html","recruit",True))

# ======================= G6. 募集要項 =======================
jobs_body = '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">JOBS</p>
  <h1 class="page-header__title">募集要項</h1>
  <p class="page-header__lead">新卒・中途、いずれも積極採用中です。</p>
</div></header>
<section class="section"><div class="container grid-2">
  <a class="entry-card" href="recruit-jobs-graduate.html"><div class="entry-card__label">NEW GRADUATE 新卒採用</div><div class="entry-card__copy">「未来を測る第一歩を、ここから。」</div><p class="entry-card__desc">理系・工学系だけじゃない。ものをつくる誠実さに共感できる人を求めています。</p><span class="btn btn--white">新卒採用 募集要項 →</span></a>
  <a class="entry-card" href="recruit-jobs-career.html"><div class="entry-card__label">MID-CAREER 中途採用</div><div class="entry-card__copy">「培った経験を、126年の精度に加えてください。」</div><p class="entry-card__desc">年齢・業界不問。あなたの経験が次の100年の基盤になる。</p><span class="btn btn--white">中途採用 募集要項 →</span></a>
</div></section>
<div class="cms-note" style="max-width:1100px;margin:0 auto 56px;">◯ 募集要項はカスタム投稿で管理。選考フロー・FAQ・就活サイトリンクを設置。''' + cms('CMS更新') + todo('就活サイト連携要確認') + '''</div>
'''
page("recruit-jobs.html","募集要項｜近江度量衡 採用", jobs_body,
     active="recruit-jobs.html", recruit=True, crumbs=RC+[("募集要項",None)])
PAGES.append(("G6","募集要項","/recruit/jobs/","recruit-jobs.html","recruit",True))

# 募集要項詳細テンプレ
def job_detail(copy, desc, rows, flow):
    tr = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k,v in rows)
    steps = "".join(f'<div class="process-step"><div class="process-step__num">STEP 0{i+1}</div><div class="process-step__title">{s}</div></div>' for i,s in enumerate(flow))
    return '''
<header class="page-header"><div class="page-header__inner">
  <p class="page-header__meta">JOBS</p>
  <h1 class="page-header__title">''' + copy + '''</h1>
  <p class="page-header__lead">''' + desc + '''</p>
</div></header>
<section class="section"><div class="container" style="max-width:860px;">
  <h2 class="section-title" style="font-size:22px;">募集要項</h2>
  <table class="info-table" style="margin-top:20px;">''' + tr + '''</table>
  <h2 class="section-title" style="font-size:22px;margin-top:48px;">選考フロー</h2>
  <div class="process" style="margin-top:20px;">''' + steps + '''</div>
  <div style="margin-top:40px;text-align:center;"><a class="btn btn--red" href="recruit-entry-2027-graduate.html" style="background:#111315;color:#fff;">エントリーする</a></div>
</div></section>
'''
page("recruit-jobs-graduate.html","新卒採用 募集要項｜近江度量衡 採用2027",
  job_detail("未来を測る第一歩を、ここから。","理系・工学系だけじゃない。着実にものをつくる誠実さに共感できる人を求めています。",
   [("募集職種","技術系総合職（設計・製造・保守・営業） "+todo('最新の職種名を確認')),
    ("採用予定人数","〇〇名 "+todo('数値提供待ち')),
    ("応募資格","2027年3月卒業見込みの大学・大学院・短大・専門学校卒業予定の方（学部・学科不問）"),
    ("勤務地","本社（滋賀）および各拠点（転勤あり）"),
    ("給与（大卒）","〇〇万円 "+todo('数値提供待ち')),
    ("給与（院卒）","〇〇万円 "+todo('数値提供待ち')),
    ("諸手当","通勤手当・住宅手当・残業手当 等"),
    ("休日","土日祝・年末年始・有給休暇"),
    ("社会保険","健康保険・厚生年金・雇用保険・労災保険"),
    ("試用期間","3ヶ月（本採用と同条件）")],
   ["エントリー","書類選考","一次面接","適性検査","二次面接","内定"]),
  active="recruit-jobs.html", recruit=True, crumbs=RC+[("募集要項","recruit-jobs.html"),("新卒採用",None)])
PAGES.append(("G6-1","新卒採用","/recruit/jobs/graduate/","recruit-jobs-graduate.html","recruit",True))

page("recruit-jobs-career.html","中途採用 募集要項｜近江度量衡 採用2027",
  job_detail("培った経験を、126年の精度に加えてください。","年齢・業界不問。あなたの経験が、次の100年の基盤になる。",
   [("募集職種","技術系（設計・製造・保守）/ 営業 / 管理部門 "+todo('最新の募集職種を確認')),
    ("応募資格","業界・年齢不問。計量・機械・電気・ITに関連する経験者を歓迎。"),
    ("勤務地","本社（滋賀）または各拠点（相談可）"),
    ("給与","経験・能力を考慮のうえ、当社規定により決定 "+todo('給与レンジを確認')),
    ("諸手当","通勤手当・住宅手当・残業手当 等"),
    ("休日","土日祝・年末年始・有給休暇"),
    ("社会保険","健康保険・厚生年金・雇用保険・労災保険"),
    ("試用期間","3ヶ月（本採用と同条件）")],
   ["応募・書類選考","一次面接","適性検査","二次面接（場合により役員面接）","内定"]),
  active="recruit-jobs.html", recruit=True, crumbs=RC+[("募集要項","recruit-jobs.html"),("中途採用",None)])
PAGES.append(("G6-2","中途採用","/recruit/jobs/career/","recruit-jobs-career.html","recruit",True))

# ======================= G7. エントリーLP =======================
def entry_lp(copy, intro, stats, jobs, jobs_link):
    st = "".join(f'<div class="number-card"><div class="number-card__num">{v}</div><div class="number-card__label">{l}</div></div>' for l,v in stats)
    jr = "".join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k,v in jobs)
    return '''
<section class="fv"><div class="fv__bg">''' + ph('エントリーLP キービジュアル','','height:100%') + '''</div>
  <div class="fv__content"><p class="fv__eyebrow">OMISCALE RECRUIT 2027</p>
  <h1 class="fv__title" style="font-size:40px;">''' + copy + '''</h1>
  <p class="fv__sub">''' + intro + '''</p>
  <div class="fv__cta"><a class="btn btn--red" href="#entry" style="background:#111315;color:#fff;">エントリーする</a></div></div>
</section>
<section class="section"><div class="container">
  <p class="section-meta">About</p><h2 class="section-title">近江度量衡とは</h2>
  <p class="section-lead">創業1900年。農産物・穀類・工業製品向けの計量システムを一品一様で設計・製造。</p>
  <div class="numbers-grid numbers-grid--dark" style="grid-template-columns:repeat(4,1fr);margin-top:24px;">''' + st + '''</div>
</div></section>
<section class="section section--grey"><div class="container" style="max-width:820px;">
  <h2 class="section-title" style="font-size:22px;">募集要項（抜粋）</h2>
  <table class="info-table" style="margin-top:20px;background:#fff;">''' + jr + '''</table>
  <p style="font-size:13px;margin-top:16px;"><a href="''' + jobs_link + '''" style="border-bottom:1px solid #999;">詳しい募集要項を見る →</a></p>
</div></section>
<section class="section section--dark theme-recruit" id="entry" style="background:#111315;"><div class="container statement">
  <h2 class="statement__main" style="color:#fff;">''' + copy + '''</h2>
  <p class="statement__body" style="color:#bbb;">エントリーは専用フォームより受け付けています。</p>
  <div style="margin-top:24px;"><a class="btn btn--red" href="contact.html" style="background:#111315;color:#fff;">エントリーフォームへ</a></div>
</div></section>
'''
page("recruit-entry-2027-graduate.html","2027 新卒採用エントリー｜近江度量衡",
  entry_lp("この先を拓く挑戦を一緒に。",
    "農産物・穀類・工業製品の「計量」で社会を支える、近江度量衡。2027年度、新卒採用のエントリーを受け付けています。",
    [("創業","126年"),("納入施設","2,000+"),("国内外","9拠点"),("従業員","約150名")],
    [("募集職種","技術系総合職・営業職 "+todo('確認')),("応募資格","2027年3月卒業見込み（学部・学科不問）"),("給与","経験・能力を考慮の上、優遇します"),("勤務地","本社（滋賀）または各拠点")],
    "recruit-jobs-graduate.html"),
  active="", recruit=True, crumbs=RC+[("2027 新卒エントリー",None)])
PAGES.append(("G7-1","2027年度 新卒エントリーLP","/recruit/entry/2027/graduate/","recruit-entry-2027-graduate.html","recruit",False))

page("recruit-entry-2027-career.html","2027 中途採用エントリー｜近江度量衡",
  entry_lp("培った経験を、精度に。",
    "創業1900年の計量システム企業。農産物・工業製品向けのはかりを設計・製造し、「いきる」をはかり、豊かな世界へというコーポレートスローガンを掲げています。国内外9拠点で従業員約150名が勤務。",
    [("創業から","126年"),("納入実績","2,000+"),("国内外","9拠点"),("従業員","約150名")],
    [("募集職種","技術系総合職・営業職 "+todo('確認')),("応募資格","業界・年齢不問・経験者歓迎"),("給与","経験・能力を考慮した優遇制度あり"),("勤務地","本社（滋賀）または各拠点")],
    "recruit-jobs-career.html"),
  active="", recruit=True, crumbs=RC+[("2027 中途エントリー",None)])
PAGES.append(("G7-2","2027年度 中途エントリーLP","/recruit/entry/2027/career/","recruit-entry-2027-career.html","recruit",False))

# ======================= index（ワイヤー一覧ハブ） =======================
def index_rows(group):
    out = ""
    for no,name,url,fil,grp,is_cms in PAGES:
        if grp != group: continue
        depth = 0
        if "-" in no: depth = 2
        elif len(no) > 1 and no[1:].isdigit(): depth = 1
        pad = ["name-main","name-sub","name-sub3"][min(depth,2)]
        corpcls = (" "+group) if depth==0 else ""
        flag = ' <span style="background:#e8f4ea;color:#2f6b3d;border:1px solid #5a9e6a;font-size:9px;padding:0 5px;border-radius:2px;">CMS</span>' if is_cms else ""
        out += f'<tr><td class="no">{no}</td><td class="{pad}{corpcls}">{name}{flag}</td><td class="url">{url}</td><td><a class="wf-link" href="{fil}">{fil}</a></td></tr>'
    return out

index_html = '''<!DOCTYPE html>
<html lang="ja"><head><script src="_auth.js"></script><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ワイヤーフレーム一覧｜近江度量衡 Webリニューアル（wier）</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0;}
  body{padding:32px 40px;max-width:1040px;margin:0 auto;font-family:'Hiragino Sans','Yu Gothic',sans-serif;color:#222;}
  h1{font-size:16px;font-weight:700;margin-bottom:6px;padding-bottom:12px;border-bottom:2px solid #111;letter-spacing:.04em;}
  .badge{display:inline-block;background:#111315;color:#fff;font-size:10px;padding:1px 8px;letter-spacing:.06em;margin-right:8px;vertical-align:middle;}
  .meta{font-size:12px;color:#666;margin:10px 0 8px;line-height:1.9;}
  .legend{font-size:11px;color:#888;margin-bottom:20px;}
  .legend span{background:#e8f4ea;color:#2f6b3d;border:1px solid #5a9e6a;font-size:9px;padding:0 5px;border-radius:2px;}
  .section-label{font-size:11px;font-weight:700;letter-spacing:.14em;padding:8px 12px;margin:24px 0 8px;}
  .section-label--corp{background:#456489;color:#fff;}
  .section-label--recruit{background:#111315;color:#fff;}
  table{width:100%;border-collapse:collapse;font-size:12px;}
  th{background:#111;color:#fff;padding:7px 12px;text-align:left;font-weight:600;letter-spacing:.04em;white-space:nowrap;}
  td{padding:6px 12px;border-bottom:1px solid #ebebeb;vertical-align:middle;line-height:1.4;}
  tr:hover td{background:#fafafa;}
  td.no{color:#aaa;font-size:11px;width:52px;}
  td.url{font-family:monospace;font-size:11px;color:#777;}
  td.name-main{font-weight:700;font-size:12px;}
  td.name-main.corp{background:#eef3f8;}
  td.name-main.recruit{background:#fdf0f0;}
  td.name-sub{padding-left:22px;color:#444;}
  td.name-sub3{padding-left:40px;color:#666;font-size:11px;}
  a.wf-link{color:#111;text-decoration:underline;font-size:11px;font-family:monospace;}
  .table-scroll{overflow-x:auto;}
  .table-scroll table{min-width:560px;}
</style></head>
<body>
<h1><span class="badge">wier</span>近江度量衡 Webリニューアル　ワイヤーフレーム一覧</h1>
<p class="meta">ステートメント：<b>「いきる」をはかり、豊かな世界へ。</b>／採用コピー：<b>「いきる」の単位とは、なんだろう。</b><br>
最新原稿シート（修正案優先）＋サイトマップ ver3（更新性・利便性）を反映して改めて構成。採用（G）は /recruit/ 以下に独立UIで統合。</p>
<p class="legend"><span>CMS</span> ＝ クライアントがWordPress管理画面から更新するページ（投稿・カスタム投稿）。それ以外は固定ページ（更新頻度：低）。</p>

<div class="section-label section-label--corp">▼ CORPORATE SITE　コーポレートサイト</div>
<div class="table-scroll"><table><thead><tr><th>No.</th><th>ページ名</th><th>URL</th><th>WFファイル</th></tr></thead><tbody>''' + index_rows("corp") + '''</tbody></table></div>

<div class="section-label section-label--recruit">▼ RECRUITMENT SITE　採用サイト（同ドメイン / /recruit/ 以下・独立UI）</div>
<div class="table-scroll"><table><thead><tr><th>No.</th><th>ページ名</th><th>URL</th><th>WFファイル</th></tr></thead><tbody>''' + index_rows("recruit") + '''</tbody></table></div>
</body></html>'''
with open(os.path.join(OUT,"index.html"),"w",encoding="utf-8") as f:
    f.write(index_html)
print("TOTAL PAGES:", len(PAGES)+1, "(incl. index)")
