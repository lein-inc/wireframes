#!/usr/bin/env python3
"""v3.1 TOP の B／C／D 案を design3-top.html から生成（何度実行しても同じ）
  B = kopetzki.law のトンマナ（濃紺×白のスイス・グリッド、巨大な英字、細い罫線、ドット行列のアイコン、横縞）
  C = sybiosme.com のトンマナ（ダークグレーのモノトーン、網点のグラフィック、巨大で細いワードマーク、点線のタイムライン）
  D = wedding.s-tmro.com のトンマナ（生成りの紙面、細い英字＋筆記体、明朝の本文、写真のコラージュ、大きな曲線）
  3案とも FV は v3.1 の3Dライン映像（terrain-infra-embed-v31.html）を残し、#theme= で案の色に合わせる。角丸は使わない（角欠け）
  CSS: css/v31b.css / v31c.css / v31d.css　JS: js/v31x.js（出現・数字のカウント・工程の強調・視差・カード送り）
  文章・写真は v3 と同じ（DATA にまとめ、案ごとにレイアウトだけ変える）
  ※ 直前の TOYOX 版 B は _v3/bk_v31b_toyox_* に退避
"""
import re, os
from lib import read, WF

TOP = read('top')

# ---------------------------------------------------------------- 共通の中身（v3 と同じ）
SVC = [
    ('01', '測量', 'SURVEY', 'S1200290', 'design3-service-survey.html', '公共測量・工事測量・全国対応。TS・GNSS・ドローン・3Dスキャナーを駆使した、現場の“最初の一歩”。'),
    ('02', '調査・設計', 'DESIGN', 'S1200389', 'design3-service-design.html', '土木設計（道路・河川・造成）、地質調査、環境調査。測量と地続きで現場を読み解きます。'),
    ('03', '施工管理', 'MANAGEMENT', 'S1200130', 'design3-service-management.html', '測量会社ならではの現場支援。一般労働者派遣許可のもと、施工管理技術者を全国の現場へ派遣します。'),
]
TECH = [
    ('DRONE SURVEY', 'ドローン空撮測量', 'S1200213', '広域を短時間で。3次元空撮地形構造物処理システムを導入し、災害時の迅速な状況把握にも活用しています。'),
    ('3D SCANNER', '3Dレーザースキャナー', 'S1200130', '構造物・地形を高精度にデジタル化。BIM／CIMと連携し、設計から施工まで一気通貫でデータを活かします。'),
    ('GNSS', 'GNSS測位', 'S1200244', 'ネットワーク型RTK-GNSSで、現場の位置基準を素早く正確に。全国どこの現場でも同じ品質を約束します。'),
]
IV = [
    ('iv1', 'S1200516', '測量作業員', '「未経験から、ドローン操縦者に。」', '測量作業員／入社3年目', '前職：接客業', False),
    ('iv2', 'S1200605', '施工管理技術者', '「測量から、施工管理へシフト。」', '施工管理技術者／入社12年目', '測量作業員 → 施工管理技術者', False),
    ('iv3', 'S1200510', '測量作業員', '「女性でも、現場は変わりません。」', '測量作業員／入社5年目', '', True),
]
NEWS = [
    ('2027.01.XX', 'お知らせ', '', 'コーポレートサイトをリニューアルしました'),
    ('2023.11.14', 'お知らせ', '', '労働者派遣法に基づく情報公開'),
    ('2021.07.09', '技術', 'tech', '3次元空撮地形構造物処理システムを導入しました'),
    ('2015.01.XX', 'お知らせ', '', '代表者交代のご挨拶'),
]
ENTRY = [('新卒採用', 'New Graduate'), ('キャリア採用', 'Mid-career'), ('会社見学', 'Office Visit')]
FACTS = [('未経験', '歓迎'), ('1年', 'で基本習得'), ('資格', '取得支援'), ('全国', 'の現場')]
ST_LEAD = '「はかる」という仕事は、200年以上ずっと続いてきました。道具が変わっても、そこにある責任だけは、まったく同じです。私たちは、まちの形を正しく次の世代に手渡すために、今日も現場に立っています。'
ST_LINES = ['どこへでも行く。未来へも行く。', '1981年の創業から変わらないフットワークで、', '道路・橋・河川——日本の社会基盤を測り、つくり、', 'これからは、未来に残していく。']
SVC_LEAD = '「測量」「調査・設計」「施工管理」——専門の異なる3つの分野を、一つの会社で受け止めます。同じ会社の中で連携できるから、精度と工程の両面でお客様の負担を減らせます。'
TECH_LEAD = '伊能忠敬が歩いた一歩と、私たちの今日の一歩は、まっすぐつながっています。ドローン・3Dスキャナー・GNSS——道具は変わっても、まちの形を正しく測る責任は同じです。'
FD_Q = ['仕事があれば、一番に行こう。', '仕事があれば、どこへでも行こう。', '月へでも行くぞ。']
FD_BODY = '他者の真似をしない。人の後についていかない。創業のときに掲げたパイオニアスピリットは、ドローンや3Dスキャナーといった新しい技術へ真っ先に挑む、いまの私たちにそのまま受け継がれています。'
REC_H = '「測量って、何をする仕事？」<br>その問いから、始めていい。'
REC_LEAD = '学生時代の専攻も、それまでの職歴も関係ありません。約1年で基本業務を習得し、ドローン・3Dスキャナーなど先端技術に触れながら、施工管理技術者へキャリアアップできます。'
STEPS = [('01', '測る', 'Survey', 'TS・GNSS・ドローン・3Dスキャナーで、現場の形を正しく写し取る。'),
         ('02', '読み解く', 'Analyze', '測ったデータから、地形・地質・環境を読み解き、設計に落とし込む。'),
         ('03', 'つくる', 'Build', '施工管理技術者が現場に入り、工程と品質を守りながら形にする。'),
         ('04', '残す', 'Archive', '点群・図面・記録をデジタルで残し、次の世代の基盤にする。')]


def photo(i):
    return f'img/photo/{i}.jpg'


def wait_badge(cls):
    return f'<span class="{cls}">原稿・撮影待ち（写真は仮）</span>'


def news_rows(cls):
    return ''.join(f'<a href="design3-news-detail.html" class="{cls}"><span class="d">{d}</span><span class="c {c2}">{c}</span><span class="t">{t}</span><i>→</i></a>' for d, c, c2, t in NEWS)


# ================================================================ B：kopetzki.law のトンマナ
def body_b():
    dots = '<span class="k-dots" aria-hidden="true">' + '<i></i>' * 25 + '</span>'
    svc = ''.join(f'''<a href="{href}" class="k-card" data-rv>
        <span class="k-card__no">{no}</span><span class="k-card__plus" aria-hidden="true"></span>
        <h3>{t}</h3><span class="k-card__en">{en}</span><p>{txt}</p>
        <div class="k-card__ft">{dots}<span class="k-go">→</span></div></a>''' for no, t, en, ph, href, txt in SVC)
    steps = ''.join(f'<li data-step><b>{no}</b><span class="k-step__t">{t}</span><span class="k-step__en">{en}</span><span class="k-step__d">{d}</span></li>' for no, t, en, d in STEPS)
    tech = ''.join(f'<div class="k-tech" data-rv><span class="k-tech__en">{en}</span><h3>{t}</h3><p>{d}</p></div>' for en, t, ph, d in TECH)
    iv = ''.join(f'''<a href="design3-recruit-interview.html#{a}" class="k-iv" data-rv><span class="k-iv__no">0{k + 1}</span><span class="k-card__plus" aria-hidden="true"></span>
        <div class="k-iv__ph"><img src="{photo(ph)}" alt=""></div><h3>{q}</h3><p>{m}<br>{m2}{wait_badge("k-wait") if w else ""}</p></a>''' for k, (a, ph, dept, q, m, m2, w) in enumerate(IV))
    ent = ''.join(f'<a href="design3-recruit-entry.html" class="k-entry__card" data-rv><h3>{t}</h3><span>{en}</span><span class="k-go">→</span></a>' for t, en in ENTRY)
    return f'''<!-- ============ B（kopetzki トンマナ）：The Big Idea ============ -->
<section class="k-sec k-idea">
  <div class="k-grid">
    <p class="k-label" data-rv>The Big Idea</p>
    <div class="k-idea__main">
      <h2 class="k-xl" data-rv>測る技術で、<br><em>未来に残す。</em></h2>
      <div class="k-cols" data-rv>
        <p class="k-strong">{ST_LINES[0]}<br>{ST_LINES[1]}<br>{ST_LINES[2]}<br>{ST_LINES[3]}</p>
        <div><p class="k-txt">{ST_LEAD}</p><a href="statement-main.html" class="k-btn k-btn--dark">私たちのステートメント<span class="k-go">→</span></a></div>
      </div>
    </div>
  </div>
</section>

<!-- ============ B：Numbers ============ -->
<section class="k-sec k-num">
  <div class="k-grid">
    <p class="k-label" data-rv>Numbers</p>
    <div class="k-num__list">
      <div class="k-num__row" data-rv><b data-count="1981">1981</b><span>創業<small>倉敷で、最初の一歩を測った年。</small></span></div>
      <div class="k-num__row" data-rv><b data-count="3">3</b><span>事業分野<small>測量・調査設計・施工管理を一つの会社で。</small></span></div>
      <div class="k-num__row" data-rv><b><span data-count="200">200</span>+</b><span>年<small>「はかる」仕事が続いてきた時間。<em>その先を、測る。</em></small></span></div>
    </div>
  </div>
</section>

<!-- ============ B：How We Help（事業） ============ -->
<section class="k-sec k-help" id="service">
  <h2 class="k-mega" data-rv>How We Help</h2>
  <div class="k-grid">
    <p class="k-label" data-rv>Our Service</p>
    <div>
      <div class="k-help__head" data-rv><h3 class="k-l">測る、読み解く、<em>つくる。</em></h3><p class="k-txt">{SVC_LEAD}</p></div>
      <div class="k-cards">{svc}</div>
      <a href="design3-service.html" class="k-btn k-btn--dark" data-rv>事業案内を見る<span class="k-go">→</span></a>
    </div>
  </div>
</section>

<!-- ============ B：Approach（工程・強み） ============ -->
<section class="k-sec k-appr" id="strengths">
  <div class="k-appr__band"><h2 class="k-mega k-mega--w" data-rv>Approach</h2></div>
  <div class="k-grid">
    <p class="k-label" data-rv>Our Framework</p>
    <div class="k-appr__main">
      <div class="k-appr__ph" data-rv><img src="{photo('S1200244')}" alt="" data-par=".05"></div>
      <div>
        <h3 class="k-l" data-rv><b class="k-big">200</b>年前の一歩と、<br><em>今日の点群。</em></h3>
        <p class="k-txt" data-rv>{TECH_LEAD}</p>
        <div class="k-techs">{tech}</div>
        <a href="design3-strengths.html" class="k-btn" data-rv>強み・技術を知る<span class="k-go">→</span></a>
      </div>
    </div>
  </div>
  <ol class="k-steps">{steps}</ol>
</section>

<!-- ============ B：Meet Our Founder ============ -->
<section class="k-sec k-fd">
  <div class="k-fd__band"><h2 class="k-mega" data-rv>Meet Our Founder</h2></div>
  <div class="k-grid">
    <p class="k-label" data-rv>Founder's Spirit</p>
    <div class="k-fd__main">
      <div><p class="k-quote" data-rv>“{FD_Q[0]}<br>{FD_Q[1]}<br>{FD_Q[2]}”</p><p class="k-src">— 創業者の言葉（1981年 創業時）</p>
        <p class="k-txt" data-rv>{FD_BODY}</p><a href="design3-about.html#founder" class="k-btn k-btn--dark" data-rv>創業者の想い・ロゴの由来<span class="k-go">→</span></a></div>
      <div class="k-fd__ph" data-rv><img src="{photo('S1200373')}" alt=""><span class="k-cap">［第二開発技工 本社, 倉敷］</span></div>
    </div>
  </div>
</section>

<!-- ============ B：Pick Your Path（社員インタビュー） ============ -->
<section class="k-sec k-path" id="people">
  <div class="k-path__bg"><img src="{photo('S1200273')}" alt=""></div>
  <div class="k-grid">
    <p class="k-label k-label--w" data-rv>Our People</p>
    <div><h2 class="k-xl k-xl--w" data-rv>Pick Your Path</h2><div class="k-ivs">{iv}</div></div>
  </div>
</section>

<!-- ============ B：採用（黒＋巨大ワードマーク） ============ -->
<section class="k-sec k-rec" id="recruit">
  <div class="k-grid">
    <p class="k-label k-label--w" data-rv>Recruit</p>
    <div>
      <h2 class="k-l k-l--w" data-rv>{REC_H}</h2>
      <div class="k-cols" data-rv><p class="k-txt k-txt--w">{REC_LEAD}</p>
        <ul class="k-facts">{''.join(f'<li><b>{a}</b>{b}</li>' for a, b in FACTS)}</ul></div>
      <div class="k-entry">{ent}</div>
    </div>
  </div>
  <p class="k-word" aria-hidden="true">daini kaihatsu</p>
</section>

<!-- ============ B：ニュース ============ -->
<section class="k-sec k-news">
  <div class="k-grid">
    <p class="k-label" data-rv>News</p>
    <div><h2 class="k-xl" data-rv>News</h2><div class="k-nlist" data-rv>{news_rows('k-nrow')}</div>
      <a href="design3-news.html" class="k-btn" data-rv>ニュース一覧<span class="k-go">→</span></a></div>
  </div>
</section>

'''


# ================================================================ C：sybiosme.com のトンマナ
def body_c():
    ht = lambda cls: f'<span class="s-ht {cls}" aria-hidden="true"></span>'
    svc = ''.join(f'''<a href="{href}" class="s-card cut" data-rv><div class="s-card__ic">{ht('s-ht--' + str(k))}</div>
        <div class="s-card__tx"><span class="s-card__no">{no}</span><h3>{t}</h3><span class="s-card__en">{en}</span><p>{txt}</p></div>
        <div class="s-card__ph cut"><img src="{photo(ph)}" alt=""></div><span class="s-go">→</span></a>''' for k, (no, t, en, ph, href, txt) in enumerate(SVC))
    steps = ''.join(f'''<div class="s-step" data-step><div class="s-step__bars s-step__bars--{al}" aria-hidden="true">{''.join(f'<i style="--w:{w}%"></i>' for w in ws)}</div>
        <div class="s-step__tx"><span class="s-dot">Step {no}</span><h3>{t}<span>{en}</span></h3><p>{d}</p></div></div>'''
                    for (no, t, en, d), (al, ws) in zip(STEPS, (('l', [100, 82, 64, 46, 28, 14, 6]), ('c', [18, 72, 34, 100, 48, 86, 26]), ('c', [10, 24, 38, 52, 66, 82, 100]), ('r', [70, 70, 70, 70, 70, 70, 70]))))
    tech = ''.join(f'''<div class="s-tech cut" data-rv><div class="s-tech__ph"><img src="{photo(ph)}" alt=""></div><span class="s-dot">{en}</span><h3>{t}</h3><p>{d}</p></div>''' for en, t, ph, d in TECH)
    iv = ''.join(f'''<a href="design3-recruit-interview.html#{a}" class="s-iv cut"><div class="s-iv__ph"><img src="{photo(ph)}" alt=""></div>
        <div class="s-iv__tx"><span class="s-dot">{dept}</span><h3>{q}</h3><p>{m}{('<br>' + m2) if m2 else ''}</p>{wait_badge("s-wait") if w else ""}</div></a>''' for a, ph, dept, q, m, m2, w in IV)
    ent = ''.join(f'''<a href="design3-recruit-entry.html" class="s-plan cut{' s-plan--hi' if k == 0 else ''}" data-rv><span class="s-plan__en">{en}</span><h3>{t}</h3>
        <ul>{''.join(f'<li>{a}{b}</li>' for a, b in FACTS)}</ul><span class="s-plan__go"><i>→</i>エントリー</span></a>''' for k, (t, en) in enumerate(ENTRY))
    return f'''<!-- ============ C（sybiosme トンマナ）：ステートメント ============ -->
<section class="s-sec s-intro">
  <div class="s-wrap s-intro__grid">
    <figure class="s-gm" aria-hidden="true" data-rv>
      <canvas id="sTerrain"></canvas>
      <i class="s-gm__c s-gm__c--tl"></i><i class="s-gm__c s-gm__c--tr"></i><i class="s-gm__c s-gm__c--bl"></i><i class="s-gm__c s-gm__c--br"></i>
      <span class="s-gm__fig">Fig. 01 — Ground Model</span>
      <span class="s-gm__mode">Halftone / Point Cloud</span>
      <span class="s-gm__xy">N 34°35′<b id="sgN">12</b>″<br>E 133°45′<b id="sgE">48</b>″</span>
      <span class="s-gm__h">H.max <b id="sgH">0.0</b> m</span>
      <span class="s-gm__scale"><i></i>0　　50　　100 m</span>
      <span class="s-gm__az">AZ <b id="sgA">000</b>°</span>
    </figure>
    <div>
      <p class="s-dot" data-rv>Our Promise</p>
      <h2 class="s-l" data-rv>測る技術で、未来に残す。<span>どこへでも行く。未来へも行く。</span></h2>
      <p class="s-txt" data-rv>{ST_LINES[1]}{ST_LINES[2]}{ST_LINES[3]}</p>
      <p class="s-txt" data-rv>{ST_LEAD}</p>
      <a href="statement-main.html" class="s-btn" data-rv><i>→</i>私たちのステートメント</a>
    </div>
  </div>
</section>

<!-- ============ C：事業（ダークのカード＋網点のアイコン） ============ -->
<section class="s-sec s-svc" id="service">
  <div class="s-wrap">
    <p class="s-dot" data-rv>Service 01/03</p>
    <h2 class="s-l" data-rv>3つの事業。<span>一つの会社で。</span></h2>
    <p class="s-txt s-txt--w" data-rv>{SVC_LEAD}</p>
    <div class="s-cards">{svc}</div>
    <a href="design3-service.html" class="s-btn s-btn--w" data-rv><i>→</i>事業案内を見る</a>
  </div>
</section>

<!-- ============ C：工程（点線のタイムライン） ============ -->
<section class="s-sec s-flow">
  <div class="s-wrap">
    <p class="s-dot" data-rv>Process 02/03</p>
    <h2 class="s-l" data-rv>現場の4ステップ。<span>測るところから、残すところまで。</span></h2>
    <div class="s-steps">{steps}</div>
  </div>
</section>

<!-- ============ C：強み（明るいグレー） ============ -->
<section class="s-sec s-tech-sec" id="strengths">
  <div class="s-wrap">
    <p class="s-dot" data-rv>Technology 03/03</p>
    <h2 class="s-l s-l--dk" data-rv><b>200</b>年前の一歩と、<span>今日の点群。</span></h2>
    <p class="s-txt s-txt--dk" data-rv>{TECH_LEAD}</p>
    <div class="s-techs">{tech}</div>
    <a href="design3-strengths.html" class="s-btn s-btn--dk" data-rv><i>→</i>強み・技術を知る</a>
  </div>
</section>

<!-- ============ C：創業 ============ -->
<section class="s-sec s-fd">
  <div class="s-wrap s-fd__grid">
    <div class="s-fd__ph cut" data-rv><img src="{photo('S1200373')}" alt=""><span class="s-fd__yr">1981</span></div>
    <div><p class="s-dot" data-rv>Founder's Spirit</p>
      <p class="s-quote" data-rv>{FD_Q[0]}<br>{FD_Q[1]}<br><span>{FD_Q[2]}</span></p>
      <p class="s-txt" data-rv>{FD_BODY}</p><a href="design3-about.html#founder" class="s-btn" data-rv><i>→</i>創業者の想い・ロゴの由来</a></div>
  </div>
</section>

<!-- ============ C：社員（宙に浮くカード） ============ -->
<section class="s-sec s-people" id="people">
  <div class="s-wrap">
    <p class="s-dot s-dot--dk" data-rv>Interview</p>
    <h2 class="s-l s-l--dk s-c" data-rv>はたらく人。<span>現場の声を、そのまま。</span></h2>
  </div>
  <div class="s-float" id="sFloat">{iv}</div>
  <div class="s-float__nav"><button type="button" data-dir="-1" aria-label="前へ">←</button><button type="button" data-dir="1" aria-label="次へ">→</button></div>
</section>

<!-- ============ C：採用（プランのような入口カード） ============ -->
<section class="s-sec s-rec" id="recruit">
  <div class="s-wrap">
    <p class="s-dot s-dot--dk" data-rv>Recruit</p>
    <h2 class="s-l s-l--dk" data-rv>{REC_H}</h2>
    <p class="s-txt s-txt--dk" data-rv>{REC_LEAD}</p>
    <div class="s-plans">{ent}</div>
  </div>
</section>

<!-- ============ C：ニュース ============ -->
<section class="s-sec s-news">
  <div class="s-wrap s-news__grid">
    <div><p class="s-dot" data-rv>News</p><h2 class="s-l" data-rv>ニュース。<span>最近のこと。</span></h2>
      <a href="design3-news.html" class="s-btn" data-rv><i>→</i>ニュース一覧</a></div>
    <div class="s-nlist" data-rv>{news_rows('s-nrow')}</div>
  </div>
  <p class="s-word" aria-hidden="true">DAINI KAIHATSU</p>
</section>

'''


# ================================================================ D：wedding.s-tmro.com のトンマナ
def body_d():
    svc = ''.join(f'''<a href="{href}" class="w-svc w-svc--{k}" data-rv><div class="w-svc__ph"><img src="{photo(ph)}" alt="" data-par="{('.04', '-.03', '.05')[k]}"></div>
        <div class="w-svc__tx"><span class="w-no">{no}</span><h3><span class="w-script">{en.capitalize()}</span>{t}</h3><p>{txt}</p><span class="w-arw">詳しく見る ↘</span></div></a>''' for k, (no, t, en, ph, href, txt) in enumerate(SVC))
    tech = ''.join(f'<div class="w-row" data-rv><span class="w-row__k">{en.title()}<small>{t}</small></span><span class="w-row__v">{d}</span></div>' for en, t, ph, d in TECH)
    iv = ''.join(f'''<a href="design3-recruit-interview.html#{a}" class="w-iv w-iv--{k}" data-rv><div class="w-iv__ph"><img src="{photo(ph)}" alt=""></div>
        <p class="w-iv__dept">{dept}</p><h3>{q}</h3><p class="w-iv__m">{m}{('<br>' + m2) if m2 else ''}</p>{wait_badge("w-wait") if w else ""}</a>''' for k, (a, ph, dept, q, m, m2, w) in enumerate(IV))
    steps = ''.join(f'<a href="design3-recruit-entry.html" class="w-acc" style="--i:{k}" data-rv><span>0{k + 1} {en}</span><b>{t}</b><i>↘</i></a>' for k, (t, en) in enumerate(ENTRY))
    return f'''<!-- ============ D（wedding トンマナ）：Message ============ -->
<section class="w-sec w-msg">
  <div class="w-msg__grid">
    <div class="w-msg__ttl" data-rv><h2 class="w-thin">Message</h2><span class="w-script w-script--lg">for the future</span></div>
    <div class="w-msg__body">
      <p class="w-mincho-h" data-rv>測る技術で、未来に残す</p>
      <div class="w-mincho" data-rv>{''.join(f'<p>{l}</p>' for l in ST_LINES)}<p class="w-gap">{ST_LEAD}</p></div>
      <p class="w-en-body" data-rv>Surveying has continued for more than two hundred years. Our tools have changed, but the responsibility remains the same — to hand the shape of our towns to the next generation, accurately.</p>
      <a href="statement-main.html" class="w-tab" data-rv>Statement ↘</a>
    </div>
  </div>
</section>

<!-- ============ D：大きな曲線で切り抜いた写真 ============ -->
<section class="w-sec w-curve">
  <div class="w-curve__ph"><img src="{photo('S1200268')}" alt="" data-par=".06"></div>
  <div class="w-curve__cap" data-rv><h2 class="w-thin">Share<br>the <span class="w-script">Ground</span></h2><p>道路も、橋も、河川も。<br>つくる前には、必ず「測る」ことから。</p></div>
</section>

<!-- ============ D：事業（写真のコラージュ） ============ -->
<section class="w-sec w-svcs" id="service">
  <div class="w-wrap">
    <div class="w-head" data-rv><h2 class="w-thin">Service</h2><span class="w-ja">事業紹介</span></div>
    <p class="w-mincho w-lead" data-rv>{SVC_LEAD}</p>
    <div class="w-svc-grid">{svc}</div>
    <a href="design3-service.html" class="w-tab w-tab--dk" data-rv>事業案内 ↘</a>
  </div>
  <p class="w-mq" aria-hidden="true"><span>Surveying the ground&nbsp;&nbsp;Preserving the future&nbsp;&nbsp;Surveying the ground&nbsp;&nbsp;Preserving the future&nbsp;&nbsp;</span><span>Surveying the ground&nbsp;&nbsp;Preserving the future&nbsp;&nbsp;Surveying the ground&nbsp;&nbsp;Preserving the future&nbsp;&nbsp;</span></p>
</section>

<!-- ============ D：強み（チャコールの「Schedule」風の表） ============ -->
<section class="w-sec w-dark" id="strengths">
  <div class="w-wrap w-dark__grid">
    <div><h2 class="w-thin w-thin--w" data-rv>Technology</h2><span class="w-ja w-ja--w" data-rv>強み・技術</span>
      <p class="w-big" data-rv><b>200</b><span>年前の一歩と、今日の点群。</span></p>
      <p class="w-mincho w-mincho--w" data-rv>{TECH_LEAD}</p></div>
    <div><div class="w-rows">
      <div class="w-row" data-rv><span class="w-row__k">Since<small>創業</small></span><span class="w-row__v w-row__v--num">1981</span></div>
      {tech}
      <div class="w-row" data-rv><span class="w-row__k">Base<small>拠点</small></span><span class="w-row__v">岡山県倉敷市 ／ 全国の現場へ</span></div></div>
      <a href="design3-strengths.html" class="w-tab w-tab--w" data-rv>強み・技術 ↘</a></div>
  </div>
  <div class="w-dark__phs" aria-hidden="true"><img src="{photo('S1200213')}" alt=""><img src="{photo('S1200244')}" alt=""><img src="{photo('S1200130')}" alt=""></div>
</section>

<!-- ============ D：創業 ============ -->
<section class="w-sec w-fd">
  <div class="w-fd__grid">
    <div class="w-fd__ph" data-rv><img src="{photo('S1200373')}" alt=""></div>
    <div class="w-fd__tx">
      <div class="w-head" data-rv><h2 class="w-thin">Founder</h2><span class="w-script">Spirit</span></div>
      <div class="w-quote" data-rv>{''.join(f'<p>{q}</p>' for q in FD_Q)}</div>
      <p class="w-src">— 創業者の言葉（1981年 創業時）</p>
      <p class="w-mincho" data-rv>{FD_BODY}</p>
      <a href="design3-about.html#founder" class="w-tab" data-rv>Our Story ↘</a>
    </div>
  </div>
</section>

<!-- ============ D：社員（プロフィールのコラージュ） ============ -->
<section class="w-sec w-ivs" id="people">
  <div class="w-wrap">
    <div class="w-head" data-rv><h2 class="w-thin">Our <span class="w-script">People</span></h2><span class="w-ja">社員インタビュー</span></div>
    <div class="w-iv-grid">{iv}</div>
  </div>
</section>

<!-- ============ D：採用（曲線の写真＋重なる番号の行） ============ -->
<section class="w-sec w-rec" id="recruit">
  <div class="w-rec__ph"><img src="{photo('S1200273')}" alt="" data-par=".05"></div>
  <div class="w-wrap w-rec__grid">
    <div class="w-head" data-rv><h2 class="w-thin">Your <span class="w-script">Reply</span></h2><span class="w-ja">採用情報</span></div>
    <div><p class="w-mincho-h w-mincho-h--s" data-rv>{REC_H}</p><p class="w-mincho" data-rv>{REC_LEAD}</p>
      <ul class="w-facts" data-rv>{''.join(f'<li><b>{a}</b>{b}</li>' for a, b in FACTS)}</ul>
      <div class="w-accs">{steps}</div></div>
  </div>
</section>

<!-- ============ D：ニュース ============ -->
<section class="w-sec w-news">
  <div class="w-wrap w-news__grid">
    <div class="w-head" data-rv><h2 class="w-thin">News</h2><span class="w-ja">お知らせ</span></div>
    <div><div class="w-nlist" data-rv>{news_rows('w-nrow')}</div><a href="design3-news.html" class="w-tab" data-rv>All News ↘</a></div>
  </div>
</section>

'''


VARIANTS = {
    'b': dict(theme='navy', banner='DESIGN v3.1 B ｜ TOP：kopetzki.law のトンマナ（濃紺×白のスイス・グリッド・巨大な英字・細い罫線）／FVは3Dライン映像（濃紺）', body=body_b,
              fonts='family=Inter+Tight:wght@300;400;500;600'),
    'c': dict(theme='dark', banner='DESIGN v3.1 C ｜ TOP：sybiosme.com のトンマナ（ダークグレーのモノトーン・網点・巨大で細いワードマーク）／FVは3Dライン映像（ダーク）', body=body_c,
              fonts='family=Inter+Tight:wght@200;300;400;500'),
    'd': dict(theme='paper', banner='DESIGN v3.1 D ｜ TOP：wedding.s-tmro.com のトンマナ（生成りの紙面・細い英字＋筆記体・明朝・写真のコラージュ）／FVは3Dライン映像（紙）', body=body_d,
              fonts='family=Montserrat:wght@200;300;400&family=Pinyon+Script&family=Shippori+Mincho:wght@400;500;600'),
}

HERO_WORD = {'c': '<p class="s-hero-word" aria-hidden="true">DAINI KAIHATSU</p>\n',
             'b': '',
             'd': '<div class="w-hero-tabs" aria-hidden="true"><span>Message ↘</span><span>Information ↘</span><span class="on">Entry ↘</span></div>\n'}


# フッターの頭（案のトンマナに合わせた大きな一言）
FOOT_HD = {'b': '''  <div class="k-foot-hd">
    <p class="k-label">Daini Kaihatsu Giko</p>
    <p class="k-foot-big">Surveying the ground.<br><em>Preserving</em> the future.</p>
  </div>
''',
           'c': '''  <div class="s-foot-hd">
    <p class="s-dot">Get in touch</p>
    <p class="s-foot-big">Surveying the ground. <span>Preserving the future.</span></p>
    <a href="#" class="s-foot-top cut" aria-label="ページの先頭へ">↑</a>
  </div>
'''}


def build(v):
    cfg = VARIANTS[v]
    h = TOP.replace('（デザイン案 v3）', f'（デザイン案 v3.1 {v.upper()}）')
    h = re.sub(r'(<div class="wf-banner">\s*<span>).*?</span>', lambda m: m.group(1) + cfg['banner'] + '</span>', h, count=1)
    h = re.sub(r'(<link rel="stylesheet" href="css/v3\.css[^"]*">)',
               r'\1\n<link href="https://fonts.googleapis.com/css2?' + cfg['fonts'] + r'&display=swap" rel="stylesheet">'
               + f'\n<link rel="stylesheet" href="css/v31{v}.css?v=10">', h, count=1)
    h = h.replace('<body>', f'<body class="v31 v31{v}">', 1)
    h = h.replace('src="terrain-infra-embed.html"', f'src="terrain-infra-embed-v31.html#theme={cfg["theme"]}"', 1)
    i = h.index('<div class="scroll-cue">')
    h = h[:i] + HERO_WORD[v] + h[i:]
    a = h.index('<!-- ============ STATEMENT')
    b = h.index('<!-- ============ CTA')
    h = h[:a] + cfg['body']() + h[b:]
    # 固定の3D（FV）は FV を抜けたら隠す（以降のセクションは自前の背景）
    h = h.replace("st=document.querySelector('.statement')", "st=document.querySelector('.hero')", 1)
    h = h.replace('<footer class="site-footer">\n  <div class="wrap">', '<footer class="site-footer">\n' + FOOT_HD[v] + '  <div class="wrap">', 1)
    h = h.replace('</body>', '<script src="js/v31x.js?v=2" defer></script>\n</body>', 1)
    h = h.replace('design3-', f'design31{v}-')  # 11/18 下層も B/C 版へ（make_v31x_sub.py）
    open(os.path.join(WF, f'design31{v}-top.html'), 'w').write(h)
    print(f'ok design31{v}-top.html')


if __name__ == '__main__':
    for v in 'bc':  # D（wedding）は 11/12 不採用。生成部分は残す・出力は _v3/bk_v31d_wedding/
        build(v)
