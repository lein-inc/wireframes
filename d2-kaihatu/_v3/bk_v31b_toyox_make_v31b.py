#!/usr/bin/env python3
"""v3.1 TOP（B案）design31b-top.html を design3-top.html から生成（何度実行しても同じ）
  参考：TOYOX 採用サイト（recruit.toyox.co.jp）のレイアウト
    ＝浮いたヘッダー／セクションをまたいで流れる青いリボン／波の縁の青いセクション／シェイプで切り抜いた写真／
      大きな見出し＋英字ラベル／縦書きの見出し／社員カードの横並び／ENTRY の大文字マーキー
  ただし角丸は使わず「角欠け」。FV は v3 の3Dワイヤー地形の動画（v3.1 の embed）を残す
  CSS: css/v31b.css　JS: js/v31b.js（リボンを描く・写真のゆっくりした視差・社員カードの左右送り）
  ※ 11/11 昼の B 案（アイソメのまち）は不採用で _v3/bk_v31b/ に退避済み。これは別物の新 B 案
"""
import re, os
from lib import read, WF

TOP = read('top')


def ribbon(cls, d1, d2, vb='0 0 1440 600'):
    """セクションをまたいで流れる2本のリボン（太い青＋細い水色）"""
    return (f'<svg class="rb {cls}" viewBox="{vb}" preserveAspectRatio="none" aria-hidden="true">'
            f'<path class="rb__a" d="{d1}"/><path class="rb__b" d="{d2}"/></svg>')


WAVE_TOP = '<svg class="wave wave--top" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 90V52C180 8 360 0 560 30S920 92 1120 60 1360 10 1440 22V90Z"/></svg>'
WAVE_BOT = '<svg class="wave wave--bot" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0V40C200 86 420 92 640 58S1020 0 1220 22 1400 70 1440 64V0Z"/></svg>'

BODY = f'''<!-- ============ B：イントロ（写真を角欠けで重ね、右にステートメント） ============ -->
<section class="b-intro" id="promise">
  {ribbon('rb--intro', 'M-40 200C220 120 420 60 640 120S1000 250 1180 150 1400 40 1500 60', 'M-40 236C230 156 440 96 660 156S1020 286 1200 186 1420 76 1500 96', '0 0 1440 260')}
  <div class="b-wrap b-intro__grid">
    <div class="b-intro__ph">
      <div class="b-ph b-ph--a cut-l fade-target"><img src="img/photo/S1200290.jpg" alt="" data-par=".06"></div>
      <div class="b-ph b-ph--b cut-r fade-target d-2"><img src="img/photo/S1200313.jpg" alt="" data-par="-.05"></div>
      <span class="b-tag fade-target d-3">SURVEY ／ KURASHIKI</span>
    </div>
    <div class="b-intro__txt">
      <span class="b-en fade-target">Our Promise</span>
      <h2 class="b-h fade-target d-1">測る技術で、<br>未来に残す。</h2>
      <div class="b-lines fade-target d-2">
        <p>どこへでも行く。未来へも行く。</p>
        <p>1981年の創業から変わらないフットワークで、<br>道路・橋・河川——日本の社会基盤を測り、つくり、<br>これからは、未来に残していく。</p>
        <p>「はかる」という仕事は、200年以上ずっと続いてきました。<br>道具が変わっても、そこにある責任だけは、まったく同じです。</p>
      </div>
      <a href="statement-main.html" class="b-btn fade-target d-3">私たちのステートメント <span class="b-btn__ar">→</span></a>
    </div>
  </div>
</section>

<!-- ============ B：ワイド写真＋波（会社の役割をひとことで） ============ -->
<section class="b-band">
  {WAVE_TOP}
  <div class="b-band__ph"><img src="img/photo/S1200268.jpg" alt="" data-par=".08"></div>
  <div class="b-band__txt">
    <h2 class="fade-target">まちの「最初の一歩」を<br>測る仕事。</h2>
    <p class="fade-target d-1">道路も、橋も、河川も、つくる前には必ず「測る」ことから始まります。<br>私たちは、岡山・倉敷から全国の現場へ。社会基盤づくりの最初と最後を支えています。</p>
  </div>
  <div class="b-band__sub cut-l fade-target d-2"><img src="img/photo/S1200244.jpg" alt=""></div>
  {WAVE_BOT}
</section>

<!-- ============ B：事業を知る（青のセクション＋白い角欠けカード） ============ -->
<section class="b-biz" id="service">
  {ribbon('rb--biz', 'M-40 140C260 60 420 260 700 220S1120 20 1500 90', 'M-40 180C270 100 440 300 720 262S1140 64 1500 132')}
  <div class="b-wrap">
    <div class="b-head b-head--w">
      <div class="b-head__ph cut-l fade-target"><img src="img/photo/S1200389.jpg" alt=""></div>
      <div>
        <h2 class="b-ttl fade-target d-1">事業を知る</h2>
        <span class="b-ttl__en fade-target d-1">BUSINESS</span>
        <p class="b-head__lead fade-target d-2">「測量」「調査・設計」「施工管理」。専門の異なる3つの分野を、一つの会社で受け止めます。<br>同じ会社の中で連携できるから、精度と工程の両面でお客様の負担を減らせます。</p>
      </div>
    </div>
    <div class="b-cards">
      <a href="design3-service-survey.html" class="b-card cut-l fade-target">
        <span class="b-no">#01</span>
        <div class="b-card__ph cut-r"><img src="img/photo/S1200290.jpg" alt=""></div>
        <h3>測量</h3><span class="b-card__en">SURVEY</span>
        <p>公共測量・工事測量・全国対応。TS・GNSS・ドローン・3Dスキャナーを駆使した、現場の“最初の一歩”。</p>
        <span class="b-card__go">→</span>
      </a>
      <a href="design3-service-design.html" class="b-card cut-l fade-target d-1">
        <span class="b-no">#02</span>
        <div class="b-card__ph cut-r"><img src="img/photo/S1200389.jpg" alt=""></div>
        <h3>調査・設計</h3><span class="b-card__en">DESIGN</span>
        <p>土木設計（道路・河川・造成）、地質調査、環境調査。測量と地続きで現場を読み解きます。</p>
        <span class="b-card__go">→</span>
      </a>
      <a href="design3-service-management.html" class="b-card cut-l fade-target d-2">
        <span class="b-no">#03</span>
        <div class="b-card__ph cut-r"><img src="img/photo/S1200130.jpg" alt=""></div>
        <h3>施工管理</h3><span class="b-card__en">MANAGEMENT</span>
        <p>測量会社ならではの現場支援。一般労働者派遣許可のもと、施工管理技術者を全国の現場へ派遣します。</p>
        <span class="b-card__go">→</span>
      </a>
    </div>
    <div class="b-center fade-target"><a href="design3-service.html" class="b-btn b-btn--w">事業案内を見る <span class="b-btn__ar">→</span></a></div>
  </div>
</section>

<!-- ============ B：強みを知る（縦書きの見出し＋縦長の写真カード） ============ -->
<section class="b-tech" id="strengths">
  {WAVE_TOP.replace('wave--top', 'wave--top wave--w')}
  <div class="b-wrap b-tech__grid">
    <div class="b-vt fade-target"><span class="b-vt__en">TECHNOLOGY</span><h2>強みを知る</h2></div>
    <div>
      <div class="b-tech__head">
        <p class="b-tech__big fade-target"><b>200</b>年前の一歩と、<br>今日の点群。</p>
        <p class="b-tech__lead fade-target d-1">伊能忠敬が歩いた一歩と、私たちの今日の一歩は、まっすぐつながっています。ドローン・3Dスキャナー・GNSS——道具は変わっても、まちの形を正しく測る責任は同じです。</p>
      </div>
      <div class="b-tcards">
        <div class="b-tcard fade-target"><div class="b-tcard__ph cut-l"><img src="img/photo/S1200213.jpg" alt=""></div><span class="b-chip">DRONE SURVEY</span><h3>ドローン空撮測量</h3><p>広域を短時間で。3次元空撮地形構造物処理システムを導入し、災害時の迅速な状況把握にも活用しています。</p></div>
        <div class="b-tcard b-tcard--low fade-target d-1"><div class="b-tcard__ph cut-l"><img src="img/photo/S1200130.jpg" alt=""></div><span class="b-chip">3D SCANNER</span><h3>3Dレーザースキャナー</h3><p>構造物・地形を高精度にデジタル化。BIM／CIMと連携し、設計から施工まで一気通貫でデータを活かします。</p></div>
        <div class="b-tcard fade-target d-2"><div class="b-tcard__ph cut-l"><img src="img/photo/S1200244.jpg" alt=""></div><span class="b-chip">GNSS</span><h3>GNSS測位</h3><p>ネットワーク型RTK-GNSSで、現場の位置基準を素早く正確に。全国どこの現場でも同じ品質を約束します。</p></div>
      </div>
      <p class="b-note fade-target">※ i-Construction／BIM・CIMにも対応済み。</p>
      <div class="fade-target"><a href="design3-strengths.html" class="b-btn">強み・技術を知る <span class="b-btn__ar">→</span></a></div>
    </div>
  </div>
</section>

<!-- ============ B：創業の想い ============ -->
<section class="b-founder">
  {ribbon('rb--fd', 'M-40 60C300 10 520 170 820 130S1240 0 1500 40', 'M-40 96C310 46 540 206 840 166S1260 36 1500 76', '0 0 1440 220')}
  <div class="b-wrap b-founder__grid">
    <div>
      <span class="b-en fade-target">Founder's Spirit</span>
      <p class="b-quote fade-target d-1">仕事があれば、一番に行こう。<br>仕事があれば、どこへでも行こう。<br>月へでも行くぞ。</p>
      <p class="b-src fade-target d-1">— 創業者の言葉（1981年 創業時）</p>
      <p class="b-body fade-target d-2">他者の真似をしない。人の後についていかない。創業のときに掲げたパイオニアスピリットは、ドローンや3Dスキャナーといった新しい技術へ真っ先に挑む、いまの私たちにそのまま受け継がれています。</p>
      <a href="design3-about.html#founder" class="b-btn fade-target d-3">創業者の想い・ロゴの由来 <span class="b-btn__ar">→</span></a>
    </div>
    <div class="b-founder__ph cut-r fade-target d-1"><img src="img/photo/S1200373.jpg" alt="" data-par=".05"><span class="b-founder__cap">1981 —</span></div>
  </div>
</section>

<!-- ============ B：働く人を知る（社員インタビュー：縦書き＋カードの横送り） ============ -->
<section class="b-people" id="people">
  <div class="b-people__grid">
    <div class="b-vt b-vt--b fade-target"><span class="b-vt__en">INTERVIEW</span><h2>社員インタビュー</h2></div>
    <div class="b-people__rail">
      <div class="b-people__track" id="bTrack">
        <a href="design3-recruit-interview.html#iv1" class="b-pcard fade-target"><div class="b-pcard__ph cut-l"><img src="img/photo/S1200516.jpg" alt=""><span class="b-pcard__dept">測量作業員</span></div><h3>「未経験から、<br>ドローン操縦者に。」</h3><p>測量作業員／入社3年目<br>前職：接客業</p><span class="b-card__go">→</span></a>
        <a href="design3-recruit-interview.html#iv2" class="b-pcard b-pcard--low fade-target d-1"><div class="b-pcard__ph cut-l"><img src="img/photo/S1200605.jpg" alt=""><span class="b-pcard__dept">施工管理技術者</span></div><h3>「測量から、<br>施工管理へシフト。」</h3><p>施工管理技術者／入社12年目<br>測量作業員 → 施工管理技術者</p><span class="b-card__go">→</span></a>
        <a href="design3-recruit-interview.html#iv3" class="b-pcard fade-target d-2"><div class="b-pcard__ph cut-l"><img src="img/photo/S1200510.jpg" alt=""><span class="b-pcard__dept">測量作業員</span></div><h3>「女性でも、<br>現場は変わりません。」</h3><p>測量作業員／入社5年目<br><span class="b-wait">原稿・撮影待ち（写真は仮）</span></p><span class="b-card__go">→</span></a>
        <a href="design3-recruit-job.html" class="b-pcard b-pcard--more b-pcard--low fade-target d-3"><div class="b-pcard__more cut-l"><span>JOB</span>職種紹介を見る<i>→</i></div></a>
      </div>
      <div class="b-people__nav"><button type="button" data-dir="-1" aria-label="前へ">←</button><button type="button" data-dir="1" aria-label="次へ">→</button></div>
    </div>
  </div>
  <div class="b-strip" aria-hidden="true"><div class="b-strip__track">
    <img src="img/photo/S1200553.jpg" alt=""><img src="img/photo/S1200635.jpg" alt=""><img src="img/photo/S1200213.jpg" alt=""><img src="img/photo/S1200401.jpg" alt=""><img src="img/photo/S1200137.jpg" alt=""><img src="img/photo/S1200662.jpg" alt=""><img src="img/photo/S1200350.jpg" alt=""><img src="img/photo/S1200157.jpg" alt="">
    <img src="img/photo/S1200553.jpg" alt=""><img src="img/photo/S1200635.jpg" alt=""><img src="img/photo/S1200213.jpg" alt=""><img src="img/photo/S1200401.jpg" alt=""><img src="img/photo/S1200137.jpg" alt=""><img src="img/photo/S1200662.jpg" alt=""><img src="img/photo/S1200350.jpg" alt=""><img src="img/photo/S1200157.jpg" alt="">
  </div></div>
</section>

<!-- ============ B：採用（青＋波＋入口カード＋ENTRY の大文字マーキー） ============ -->
<section class="b-entry" id="recruit">
  {WAVE_TOP}
  {ribbon('rb--entry', 'M-40 300C240 220 420 420 720 380S1160 160 1500 240', 'M-40 340C250 260 440 460 740 420S1180 200 1500 282')}
  <div class="b-wrap">
    <h2 class="b-entry__h fade-target">「測量って、何をする仕事？」<br>その問いから、始めていい。</h2>
    <p class="b-entry__lead fade-target d-1">学生時代の専攻も、それまでの職歴も関係ありません。約1年で基本業務を習得し、ドローン・3Dスキャナーなど先端技術に触れながら、施工管理技術者へキャリアアップできます。</p>
    <ul class="b-facts fade-target d-1"><li><b>未経験</b>歓迎</li><li><b>1年</b>で基本習得</li><li><b>資格</b>取得支援</li><li><b>全国</b>の現場</li></ul>
    <div class="b-center fade-target d-2"><a href="design3-recruit-requirements.html" class="b-btn b-btn--line">募集要項・よくある質問 <span class="b-btn__ar">→</span></a></div>
    <div class="b-ecards">
      <a href="design3-recruit-entry.html" class="b-ecard cut-l fade-target"><h3>新卒採用</h3><span>New Graduate</span><i class="b-card__go">→</i></a>
      <a href="design3-recruit-entry.html" class="b-ecard cut-l fade-target d-1"><h3>キャリア採用</h3><span>Mid-career</span><i class="b-card__go">→</i></a>
      <a href="design3-recruit-entry.html" class="b-ecard cut-l fade-target d-2"><h3>会社見学</h3><span>Office Visit</span><i class="b-card__go">→</i></a>
    </div>
  </div>
  <div class="b-mq" aria-hidden="true"><div class="b-mq__track"><span>ENTRY</span><span>ENTRY</span><span>ENTRY</span><span>ENTRY</span><span>ENTRY</span><span>ENTRY</span><span>ENTRY</span><span>ENTRY</span></div></div>
  {WAVE_BOT.replace('wave--bot', 'wave--bot wave--w')}
</section>

<!-- ============ B：ニュース ============ -->
<section class="b-news">
  <div class="b-wrap b-news__grid">
    <div><h2 class="b-ttl b-ttl--b fade-target">ニュース</h2><span class="b-ttl__en b-ttl__en--b fade-target">NEWS</span>
      <a href="design3-news.html" class="b-btn fade-target d-1" style="margin-top:28px;">ニュース一覧 <span class="b-btn__ar">→</span></a></div>
    <div class="b-nlist fade-target d-1">
      <a href="design3-news-detail.html"><span class="d">2027.01.XX</span><span class="c">お知らせ</span><span class="t">コーポレートサイトをリニューアルしました</span><i>→</i></a>
      <a href="design3-news-detail.html"><span class="d">2023.11.14</span><span class="c">お知らせ</span><span class="t">労働者派遣法に基づく情報公開</span><i>→</i></a>
      <a href="design3-news-detail.html"><span class="d">2021.07.09</span><span class="c tech">技術</span><span class="t">3次元空撮地形構造物処理システムを導入しました</span><i>→</i></a>
      <a href="design3-news-detail.html"><span class="d">2015.01.XX</span><span class="c">お知らせ</span><span class="t">代表者交代のご挨拶</span><i>→</i></a>
    </div>
  </div>
</section>

'''

HERO_EXTRA = f'''  <a href="design3-news-detail.html" class="b-ticker cut-l"><b>News</b><span class="d">2027.01.XX</span><span class="t">コーポレートサイトをリニューアルしました</span><i>→</i></a>
  {ribbon('rb--hero', 'M-40 520C260 600 520 470 760 520S1200 640 1500 420', 'M-40 560C270 640 540 510 780 560S1220 680 1500 462')}
'''


def build_b():
    h = TOP.replace('（デザイン案 v3）', '（デザイン案 v3.1 B）')
    h = re.sub(r'(<div class="wf-banner">\s*<span>).*?</span>',
               lambda m: m.group(1) + 'DESIGN v3.1 B ｜ TOP：TOYOX採用サイトのレイアウトを踏襲（角丸→角欠け）／FVは3Dライン映像のまま' + '</span>', h, count=1)
    h = re.sub(r'(<link rel="stylesheet" href="css/v3\.css[^"]*">)', r'\1\n<link rel="stylesheet" href="css/v31b.css?v=3">', h, count=1)
    h = h.replace('<body>', '<body class="v31 v31b">', 1)
    h = h.replace('src="terrain-infra-embed.html"', 'src="terrain-infra-embed-v31.html"', 1)
    # HERO：下にニュースのティッカーとリボン
    i = h.index('<div class="scroll-cue">')
    h = h[:i] + HERO_EXTRA + h[i:]
    a = h.index('<!-- ============ STATEMENT')
    b = h.index('<!-- ============ CTA')
    h = h[:a] + BODY + h[b:]
    # 固定背景（3D）は B ではイントロに入ったら隠す（以降のセクションは自前の背景）
    h = h.replace("st=document.querySelector('.statement')", "st=document.querySelector('.b-intro')", 1)
    h = h.replace('st.getBoundingClientRect().bottom < 0', 'st.getBoundingClientRect().top < 0', 1)
    h = h.replace('</body>', '<script src="js/v31b.js?v=1" defer></script>\n</body>', 1)
    open(os.path.join(WF, 'design31b-top.html'), 'w').write(h)
    print('ok design31b-top.html')


if __name__ == '__main__':
    build_b()
