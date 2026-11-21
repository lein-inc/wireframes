#!/usr/bin/env python3
"""11/19 関指示「原稿シートを最新として、ほかもすべて」
  原稿確認シート（10I6oiU5…）でOK・修正済みの文面と、v3/v3.1A の文面が食い違っているところをシートの文面に戻す。
  - 要修正でコメントの中身が不明なもの（ホーム17・45〜48・51、会社案内28・35）は触らない
  - 社会活動の加盟団体はホーム34の指摘（（一社）追記・倉敷測量設計業協会（任意団体））を反映済みの文面を優先
  - シートにない v3 の追加要素（職種の詳細表、FAQ追加分など）は残す（確認リスト行き）
  一度きりの適用。バックアップ _v3/bk_20261119_sheet_sync/
"""
import os, shutil
WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(WF, n)
BK = os.path.join(WF, '_v3', 'bk_20261119_sheet_sync')
assert not os.path.exists(BK), '適用済み'
os.makedirs(BK)

TOP_SOCIAL = '''<!-- ============ SOCIAL（原稿シート ホーム30〜37） ============ -->
<section class="news social31" data-shot="peaks">
  <div class="wrap p31">
    <div class="news-flex">
      <div class="sec-head fade-target" style="margin-bottom:0;">
        <span class="en-label">Social Activities</span>
        <h2>社会活動</h2>
      </div>
      <div class="top-social fade-target d-1">
        <div class="ts-fig has-hfig"><figure class="hfig" data-model="disaster" data-fig="Fig. D — Disaster Response" data-mode="Drone / Slope Change" data-metric="H.max|m|186" data-n="34°35′" data-e="133°45′"></figure></div>
        <h3>災害の前と、災害の後に立つ。</h3>
        <p>（一社）岡山県測量設計業協会、倉敷測量設計業協会（任意団体）に加盟し、有事のときにすぐ動ける体制を維持しています。3次元空撮地形構造物処理システムを活用したドローン測量で、被災地の状況を短時間で把握します。</p>
        <p>地域の技術を次世代へ手渡す活動にも取り組んでいます。</p>
        <div class="btns">
          <a href="design3-social.html" class="arw-link">社会活動 <span class="circ">→</span></a>
          <a href="design3-about.html" class="arw-link">会社案内 <span class="circ">→</span></a>
        </div>
      </div>
    </div>
  </div>
</section>
<style>
  .social31 .top-social { max-width: 640px; }
  .social31 .ts-fig { position: relative; height: 240px; margin-bottom: 30px; }
  .social31 .top-social h3 { font-size: clamp(20px, 2vw, 26px); font-weight: 900; letter-spacing: .04em; margin-bottom: 16px; }
  .social31 .top-social p { color: var(--txt-2); font-size: 15.5px; line-height: 2; margin-top: 10px; }
  .social31 .btns { display: flex; gap: 28px; flex-wrap: wrap; margin-top: 26px; }
</style>

'''

R = {
    'design31a-top.html': [
        # ステートメント（サブコピー）：シート ホーム2
        ('''      <span class="fade-target d-2">1981年の創業から変わらないフットワークで、</span>
      <span class="fade-target d-3">道路・橋・河川——日本の社会基盤を測り、つくり、</span>
      <span class="fade-target d-4">これからは、未来に残していく。</span>''',
         '''      <span class="fade-target d-2">公共測量・工事測量から3Dスキャナー・ドローンによる先端計測まで。</span>
      <span class="fade-target d-3">岡山・倉敷から全国の現場を支える、</span>
      <span class="fade-target d-4">測量・調査・施工管理のプロフェッショナル集団。</span>'''),
        # 技術・強み：シート ホーム18・22・25・28・29
        ('<h2><span class="big">200</span>年前の一歩と、今日の点群。</h2>', '<h2>技術・強み</h2>'),
        ('<p>広域を短時間で。3次元空撮地形構造物処理システムを導入し、災害時の迅速な状況把握にも活用しています。</p>',
         '<p>広域を短時間で。3次元空撮地形構造物処理システム導入済み。</p>'),
        ('<h3>3Dレーザースキャナー</h3>\n        <p>構造物・地形を高精度にデジタル化。BIM／CIMと連携し、設計から施工まで一気通貫でデータを活かします。</p>',
         '<h3>3Dスキャナー</h3>\n        <p>構造物・地形を高精度にデジタル化。BIM／CIMとの連携。</p>'),
        ('<p>ネットワーク型RTK-GNSSで、現場の位置基準を素早く正確に。全国どこの現場でも同じ品質を約束します。</p>',
         '<p>ネットワーク型RTK-GNSSで、現場の位置基準を素早く。</p>'),
        ('<a href="design3-strengths.html" class="pill ghost">強み・技術を知る <span class="circ">→</span></a>',
         '<a href="design3-strengths.html" class="pill ghost">技術・強みを見る <span class="circ">→</span></a>'),
        # 社会活動ブロック（TOPに無かった）：シート ホーム30〜37 → 採用の前に追加
        ('<!-- ============ 社員写真マーキー ============ -->', TOP_SOCIAL + '<!-- ============ 社員写真マーキー ============ -->'),
        # 採用：ボタンに FAQ（シート ホーム53）
        ('<a href="design3-recruit-entry.html" class="pill ghost">エントリー <span class="circ">→</span></a>\n      </div>\n    </div>\n    <div class="rec-photo">',
         '<a href="design3-recruit.html#faq" class="pill ghost">FAQ <span class="circ">→</span></a>\n      </div>\n    </div>\n    <div class="rec-photo">'),
        # ニュース（ダミー）日付：シート ホーム40
        ('<span class="d">2027.01.XX</span>', '<span class="d">2026.07.XX</span>'),
        # CTA：シート ホーム55
        ('<h3>測量・調査設計・施工管理のご相談</h3>\n      <p>公共測量から民間の工事測量、施工管理技術者の派遣まで。まずはお気軽にご相談ください。</p>',
         '<h3>測量・調査・施工管理のご相談</h3>\n      <p>お気軽にお問い合わせください。</p>'),
    ],
    'design3-service.html': [
        ('<div class="f"><div class="v">3<small>種</small></div><div class="l">測量業／派遣／補償コンサル登録</div></div>',
         '<div class="f"><div class="v">3<small>種類</small></div><div class="l">許可・登録（測量業／派遣／補償コンサル）</div></div>'),
    ],
    'design3-service-survey.html': [
        ('担当者の異動先まで追いかけていただけるほどの信頼関係を', '顧客担当者の異動先でも業務依頼をいただける信頼関係を'),
    ],
    'design3-strengths.html': [
        ('<h3>それでも、大切にしているのは「現場に立つこと」。</h3>', '<h3>それでも、私たちが大切にしているのは、「現場に立つこと」です。</h3>'),
    ],
    'design3-recruit.html': [
        ('<a href="design3-recruit.html#jobs" class="pill ghost">職種紹介を見る <span class="circ">→</span></a>',
         '<a href="#faq" class="pill ghost">よくある質問 <span class="circ">→</span></a>'),
        ('<div class="facts-row fade-target d-1" style="margin-top:80px;">\n      <div class="f"><div class="v">未経験</div>',
         '<h3 class="welcome-h fade-target d-1" style="margin-top:80px; font-size:20px; font-weight:900; letter-spacing:.04em;">こんな方を歓迎しています</h3>\n'
         '    <div class="facts-row fade-target d-1" style="margin-top:22px;">\n      <div class="f"><div class="v">未経験</div>'),
        ('<p>測量現場のサポート業務からスタート。器械の設置、記帳、後方整理などを通じて、測量の基本を学びます。先輩と同じ現場に入り、「何を・なぜ測るのか」を一つずつ覚えていく、いちばん最初の入口です。</p>',
         '<p>測量現場のサポート業務からスタート。器械の設置、記帳、後方整理などを通じて、測量の基本を学びます。</p>'),
        ('<p>測量業務全般を担当。TS・GNSS・ドローン・3Dレーザースキャナーなどの機材操作を含む、現場の主軸を担う仕事です。観測したデータは会社に持ち帰り、CADや点群処理で成果品にまとめます。</p>',
         '<p>測量業務全般を担当。TS・GNSS・ドローン等の機材操作を含む、現場の主軸を担う仕事です。</p>'),
        ('<p>官公庁・ゼネコンの工事現場に派遣され、施工管理業務を担当します。測量の現場感覚を活かし、「実際に施工できる計画」と精度の高い出来形管理で現場を支えます。</p>',
         '<p>工事現場に派遣され、施工管理業務を担当。測量経験を活かして、精度の高い管理をおこないます。</p>'),
    ],
}
# ページ下部CTA（左パネルの見出し）：シートの各タブ末尾
CTA = {'design3-service-survey.html': '測量のご相談はお気軽に。', 'design3-service-design.html': '調査・設計のご相談はお気軽に。',
       'design3-service-management.html': '施工管理・技術者派遣のご相談', 'design3-strengths.html': '技術のご相談はお気軽に。',
       'design3-social.html': '災害時の緊急対応・地域活動のご相談', 'design3-about.html': 'お問い合わせはこちらから',
       'design3-recruit.html': 'エントリー・お問い合わせはこちら'}
for f, h3 in CTA.items():
    R.setdefault(f, []).append(('<h3>測量・調査設計・施工管理のご相談</h3>', f'<h3>{h3}</h3>'))

for f, rs in R.items():
    shutil.copy2(P(f), BK)
    h = open(P(f)).read()
    for a, b in rs:
        assert h.count(a) == 1, (f, a[:60], h.count(a))
        h = h.replace(a, b)
    open(P(f), 'w').write(h)
print('ok', len(R), 'files')
