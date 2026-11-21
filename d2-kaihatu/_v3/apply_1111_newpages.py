#!/usr/bin/env python3
"""11/11 v3 新規ページ（採用まわり＋ニュース詳細＋プライバシーポリシー）
  原稿がまだ無いところは .chk バッジ（原稿待ち／要確認／仮文言）で明示する
  ・recruit-job          職種紹介（3職種の詳細）
  ・recruit-interview    社員インタビュー（3名：A=入社3年目／B=入社12年目／C=入社5年目・女性＝未撮影でダミー）
  ・recruit-requirements 募集要項（新卒／中途 タブ）＋選考の流れ
  ・recruit-faq          よくある質問（採用トップから分離）
  ・recruit-entry        エントリーフォーム
  ・news-detail          ニュース記事詳細（サンプル）
  ・privacy              プライバシーポリシー
  何度実行しても同じ結果（新規ページを丸ごと作り直す）
"""
import re
from lib import new_page, read, write, photo, sibnav, phero

CHK = lambda t='原稿待ち': f'<span class="chk">{t}</span>'
BANNER = lambda ja, url: f'DESIGN v3 | {ja} | {url}（v3で新規追加／原稿待ちの箇所はバッジ表示）'
REC = [('design3-recruit.html', '採用情報')]


def sec(inner, en, word=None, cls='', id_=''):
    w = word or en.upper()
    i = f' id="{id_}"' if id_ else ''
    return f'''<section class="has-bgword {cls}"{i}>
  <div class="bg-word" aria-hidden="true">{w}</div>
  <div class="wrap">
{inner}
  </div>
</section>
'''


def head(ja, en, sub=''):
    s = f'\n      <p class="sub">{sub}</p>' if sub else ''
    return f'''    <div class="sec-head fade-target">
      <h2><span class="hbox">{ja}</span></h2><span class="en-label">{en}</span>{s}
    </div>'''


# ============================================================ 職種紹介
JOBS = [
    ('job1', '01', '測量助手', 'Survey Assistant', '0336', '0094',
     '測量現場のサポート業務からスタート。器械の設置、記帳、後方整理などを通じて、測量の基本を学びます。先輩と同じ現場に入り、「何を・なぜ測るのか」を一つずつ覚えていく、いちばん最初の入口です。',
     [('おもな仕事', '器械（TS・レベル）の据付補助、標尺・プリズム持ち、記帳、杭打ち、機材の準備・片付け'),
      ('応募条件', '未経験可・35歳以下（長期キャリア形成のため）'),
      ('必要な資格', '不要（普通自動車免許 AT限定可）'),
      ('入社後', '約1年で測量作業員へ。測量士補の取得を会社が支援')]),
    ('job2', '02', '測量作業員', 'Surveyor', '0290', '0157',
     '測量業務全般を担当。TS・GNSS・ドローン・3Dレーザースキャナーなどの機材操作を含む、現場の主軸を担う仕事です。観測したデータは会社に持ち帰り、CADや点群処理で成果品にまとめます。',
     [('おもな仕事', '基準点・水準・地形・路線測量、工事測量（丁張り・出来形）、ドローン空撮、データ整理'),
      ('応募条件', '測量士補以上、または同等の実務経験'),
      ('必要な資格', '普通自動車免許（AT限定可）'),
      ('入社後', '測量士の取得を支援。3〜5年で施工管理技術者へのキャリアシフトも')]),
    ('job3', '03', '施工管理技術者', 'Construction Manager', '0130', '0311',
     '官公庁・ゼネコンの工事現場に派遣され、施工管理業務を担当します。測量の現場感覚を活かし、「実際に施工できる計画」と精度の高い出来形管理で現場を支えます。',
     [('おもな仕事', '工程・品質・出来形・安全の管理、測量（丁張り・出来形）、写真管理・書類作成'),
      ('応募条件', '土木施工管理技士、または同等の実務経験'),
      ('必要な資格', '普通自動車免許（AT限定可）'),
      ('入社後', '1級土木施工管理技士などの資格取得を支援')]),
]


def job_html(j, rev):
    id_, no, ja, en, ph, ph2, txt, dl = j
    dls = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in dl)
    return f'''    <div class="job{' rev' if rev else ''} fade-target" id="{id_}">
      <div>
        <div class="ph"><img src="{photo(ph)}" alt="" loading="lazy"></div>
        <div class="ph" style="width:56%; margin:16px 0 0 auto; aspect-ratio:3/2;"><img src="{photo(ph2)}" alt="" loading="lazy"></div>
      </div>
      <div>
        <div class="no">{no}</div>
        <h3>{ja}</h3><div class="sub">{en}</div>
        <p>{txt}</p>
        <dl>{dls}</dl>
        <div class="btns">
          <a href="design3-recruit-requirements.html" class="pill ghost">募集要項 <span class="circ">→</span></a>
          <a href="design3-recruit-entry.html?job={id_}" class="pill yellow">この職種にエントリー <span class="circ">→</span></a>
        </div>
      </div>
    </div>'''


career = '''    <div class="steps" style="grid-template-columns:repeat(3,1fr);">
      <div class="step fade-target"><div class="term">STEP 01</div><h4>測量助手</h4><p>入社〜1年。器械の据付・記帳・後方整理で基本を覚える。</p></div>
      <div class="step fade-target"><div class="term">STEP 02</div><h4>測量作業員</h4><p>1年〜。現場を任され、ドローン・3Dスキャナーも担当。測量士補・測量士へ。</p></div>
      <div class="step fade-target"><div class="term">STEP 03</div><h4>施工管理技術者</h4><p>3〜5年〜。測量の経験を活かして施工管理へ。土木施工管理技士へ。</p></div>
    </div>'''

body = (phero(REC + [(None, '職種紹介')], '職種紹介', 'JOBS', '0350', 'Three Ways to Start',
              '測量助手・測量作業員・施工管理技術者。未経験からのスタートも、経験を活かした転職も、入口はひとつではありません。')
        + sibnav('recruit-job')
        + sec(head('<span class="big">3</span>つの職種', 'Jobs') + '\n' + '\n'.join(job_html(j, i % 2) for i, j in enumerate(JOBS)), 'Jobs')
        + sec(head('キャリアステップ', 'Career Path', '多くの社員が「測量助手 → 測量作業員 → 施工管理技術者」と段階を踏んで成長しています。') + '\n' + career
              + '\n    <div class="fade-target" style="margin-top:44px;"><a href="design3-recruit.html#first-step" class="arw-link">未経験からの1年を見る <span class="circ">→</span></a></div>',
              'Career Path', 'CAREER', cls='tone'))
new_page('recruit-job', '職種紹介', BANNER('職種紹介', '/recruit/job/'), body)

# ============================================================ 社員インタビュー
IV = [
    ('iv1', 'INTERVIEW 01', '「未経験から<br>ドローン操縦者に」', '測量作業員', '入社3年目', '前職：接客業',
     '0516', ['0466', '0546'], False,
     [('入社のきっかけは？', '前職は接客業。まったく違う世界に飛び込みましたが、先輩がゼロから教えてくれたので不安はありませんでした。'),
      ('いまの仕事内容を教えてください。', None),
      ('仕事のやりがい・おもしろさは？', None),
      ('入社前と入社後で、イメージは変わりましたか？', None)],
     '「測量って何？」から始めて大丈夫です。'),
    ('iv2', 'INTERVIEW 02', '「測量から<br>施工管理へシフト」', '施工管理技術者', '入社12年目', '測量作業員 → 施工管理技術者',
     '0605', ['0585', '0633'], False,
     [('施工管理にキャリアを移したきっかけは？', '測量の現場感覚があるからこそ、施工管理で“実際に施工可能な計画”が立てられる。この会社のキャリアパスの強みです。'),
      ('いまの仕事内容を教えてください。', None),
      ('測量の経験が生きている場面は？', None),
      ('後輩の育成で大切にしていることは？', None)],
     '現場を知っている人が、いちばん強い。'),
    ('iv3', 'INTERVIEW 03', '「女性でも、<br>現場は変わりません」', '測量作業員', '入社5年目', '',
     None, [], True,
     [('入社のきっかけは？', None),
      ('女性が現場で働くことについて、どう感じていますか？', '最初は「女性でも大丈夫？」と聞かれることが多かったけど、機材が軽くなり、現場も進化しています。'),
      ('仕事のやりがいは？', None),
      ('働きやすさの工夫はありますか？', None)],
     None),
]


def iv_html(v):
    id_, no, q, job, year, prev, ph, ph2, dmy, qa, msg = v
    img = (f'<div class="ph is-dummy"><img src="img/dummy/26.jpg" alt=""></div>' if dmy
           else f'<div class="ph"><img src="{photo(ph)}" alt=""></div>')
    prof = f'<b>{job}</b>{year}' + (f'<br>{prev}' if prev else '') + ('<br>※ インタビュー・撮影は未実施（写真はダミー）' if dmy else '')
    body = ''
    for i, (qq, a) in enumerate(qa):
        body += f'<h4>{qq}</h4>\n'
        body += (f'<p>{a}</p>\n' if a else f'<p style="color:var(--muted);">ここに回答が入ります。{CHK("インタビュー原稿待ち")}</p>\n')
        if i == 1 and ph2:
            body += '<div class="ph2">' + ''.join(f'<img src="{photo(p)}" alt="" loading="lazy">' for p in ph2) + '</div>\n'
    m = f'<div class="msg"><b>MESSAGE</b>{msg or "応募を考えている方へのメッセージ"}{CHK("原稿待ち")}</div>'
    return f'''<section class="iv" id="{id_}">
  <div class="iv-head fade-target">
    {img}
    <div class="txt"><span class="no">{no}</span><div class="q">{q}</div><div class="prof">{prof}</div></div>
  </div>
  <div class="iv-body">
{body}{m}
  </div>
</section>
'''


idx = '<div class="iv-index fade-target">' + ''.join(
    f'''<a href="#{v[0]}"><div class="ph{' is-dummy' if v[8] else ''}"><img src="{'img/dummy/26.jpg' if v[8] else photo(v[6])}" alt="" loading="lazy"></div>
      <div class="meta">{v[3]}／{v[4]}</div><h3>{v[2].replace('<br>', '')}</h3></a>''' for v in IV) + '</div>'
body = (phero(REC + [(None, '社員インタビュー')], '社員インタビュー', 'INTERVIEW', '0510', 'Our People',
              'どんなきっかけで入社し、いまどんな仕事をしているのか。第二開発技工ではたらく社員に聞きました。')
        + sibnav('recruit-interview')
        + sec(head('社員インタビュー', 'People', '人数・人選は撮影素材にあわせて調整します。' + CHK('要確認')) + '\n' + idx, 'People')
        + ''.join(iv_html(v) for v in IV)
        + '<section style="padding-top:0;"><div class="wrap" style="text-align:center;"><a href="design3-recruit-entry.html" class="pill yellow">エントリーする <span class="circ">→</span></a></div></section>\n')
new_page('recruit-interview', '社員インタビュー', BANNER('社員インタビュー', '/recruit/interview/'), body)

# ============================================================ 募集要項
def req_table(rows):
    return '<table class="req-table">' + ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in rows) + '</table>'


W = CHK()
COMMON = [
    ('勤務地', '本社（岡山県倉敷市西富井446-2）／現場は岡山県内を中心に全国'),
    ('勤務時間', f'— {W}'),
    ('休日・休暇', f'— {W}'),
    ('給与', f'— {W}'),
    ('諸手当', f'— {W}'),
    ('福利厚生', f'社会保険完備／資格取得支援（受験料・登録料を会社負担）{CHK("要確認")}'),
]
NEWG = [('募集職種', '測量助手（未経験可）'), ('応募資格', f'高校・専門学校・大学卒業見込みの方（学部・学科不問）{CHK("要確認")}'),
        ('必要な資格', '普通自動車免許（AT限定可）※入社までの取得で可' + CHK('要確認'))] + COMMON
MID = [('募集職種', '測量助手／測量作業員／施工管理技術者'),
       ('応募資格', '測量助手：未経験可・35歳以下（長期キャリア形成のため）<br>測量作業員：測量士補以上、または同等の実務経験<br>施工管理技術者：土木施工管理技士、または同等の実務経験'),
       ('必要な資格', '普通自動車免許（AT限定可）')] + COMMON
flow = '''    <div class="steps">
      <div class="step fade-target"><div class="term">STEP 01</div><h4>エントリー</h4><p>フォームまたはお電話でご応募ください。</p></div>
      <div class="step fade-target"><div class="term">STEP 02</div><h4>会社見学・説明</h4><p>社屋や機材、仕事の様子をご案内します。</p></div>
      <div class="step fade-target"><div class="term">STEP 03</div><h4>面接</h4><p>面接は1〜2回を予定しています。</p></div>
      <div class="step fade-target"><div class="term">STEP 04</div><h4>内定</h4><p>入社日はご相談のうえ決定します。</p></div>
    </div>
    <p class="fade-target" style="margin-top:20px; font-size:14px; color:var(--muted);">※ 選考の流れ・回数は仮です。''' + CHK('要確認') + '</p>'
tabs = f'''    <div class="tabs" role="tablist"><button class="on" data-tab="t-mid">中途採用</button><button data-tab="t-new">新卒採用</button></div>
    <div class="tabpane on" id="t-mid">{req_table(MID)}</div>
    <div class="tabpane" id="t-new">{req_table(NEWG)}</div>
    <script>document.querySelectorAll('.tabs button').forEach(function(b){{b.addEventListener('click',function(){{document.querySelectorAll('.tabs button').forEach(function(x){{x.classList.toggle('on',x===b);}});document.querySelectorAll('.tabpane').forEach(function(p){{p.classList.toggle('on',p.id===b.dataset.tab);}});}});}});</script>'''
body = (phero(REC + [(None, '募集要項')], '募集要項', 'REQUIREMENTS', '0647', 'Requirements')
        + sibnav('recruit-requirements')
        + sec(head('募集要項', 'Requirements', '給与・勤務時間・休日などの条件は、原稿をいただき次第反映します。') + '\n' + tabs, 'Requirements')
        + sec(head('選考の流れ', 'Selection Flow') + '\n' + flow
              + '\n    <div class="fade-target" style="margin-top:44px; display:flex; gap:14px; flex-wrap:wrap;"><a href="design3-recruit-entry.html" class="pill yellow">エントリーする <span class="circ">→</span></a><a href="design3-recruit-faq.html" class="pill ghost">よくある質問 <span class="circ">→</span></a></div>',
              'Selection Flow', 'FLOW', cls='tone'))
new_page('recruit-requirements', '募集要項', BANNER('募集要項', '/recruit/requirements/'), body)

# ============================================================ よくある質問（採用）
import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bk_20261111a', 'design3-recruit.html')).read()  # FAQ 6問の原本
qa_all = re.findall(r'<div class="qa-item">.*?</div></div>', src)
assert len(qa_all) == 6
G1 = qa_all[0:2] + [qa_all[4]]          # 応募・資格
G2 = [qa_all[2], qa_all[5], qa_all[3]]  # 働き方
G3 = [f'<div class="qa-item"><div class="q">会社見学だけでも申し込めますか？</div><div class="a">はい、歓迎しています。エントリーフォームの「会社見学を希望する」にチェックを入れてお送りください。{CHK("要確認")}</div></div>',
      f'<div class="qa-item"><div class="q">現場までの移動はどうしていますか？</div><div class="a">社用車で先輩と一緒に移動します。{CHK("仮文言")}</div></div>',
      f'<div class="qa-item"><div class="q">作業服や道具は支給されますか？</div><div class="a">作業服・ヘルメット・安全帯などは会社で用意します。{CHK("仮文言")}</div></div>']


def qa(ja, en, items, cls=''):
    return sec(head(ja, en) + '\n    <div class="qa fade-target">\n      ' + '\n      '.join(items) + '\n    </div>', en, 'FAQ', cls=cls)


body = (phero(REC + [(None, 'よくある質問')], 'よくある質問', 'FAQ', '0656', 'FAQ')
        + sibnav('recruit-faq')
        + qa('応募・資格について', 'Application', G1)
        + qa('働き方について', 'Work Style', G2, 'tone')
        + qa('入社・見学について', 'Joining', G3))
new_page('recruit-faq', 'よくある質問', BANNER('よくある質問（採用）', '/recruit/faq/'), body)

# ============================================================ エントリー
form = f'''    <ol class="formsteps fade-target"><li class="on">1. 入力</li><li>2. 確認</li><li>3. 完了</li></ol>
    <form class="fade-target">
      <div class="form-row"><label>応募区分<span class="req">必須</span></label><div class="radios"><label><input type="radio" name="kubun" checked> 中途採用</label><label><input type="radio" name="kubun"> 新卒採用</label><label><input type="radio" name="kubun"> 会社見学のみ</label></div></div>
      <div class="form-row"><label>希望職種<span class="req">必須</span></label><div class="radios"><label><input type="radio" name="job" checked> 測量助手</label><label><input type="radio" name="job"> 測量作業員</label><label><input type="radio" name="job"> 施工管理技術者</label><label><input type="radio" name="job"> 相談して決めたい</label></div></div>
      <div class="form-row"><label>お名前<span class="req">必須</span></label><input type="text" placeholder="例）山田 太郎"></div>
      <div class="form-row"><label>ふりがな<span class="req">必須</span></label><input type="text" placeholder="例）やまだ たろう"></div>
      <div class="form-row"><label>生年月日<span class="req">必須</span></label><input type="date"></div>
      <div class="form-row"><label>メールアドレス<span class="req">必須</span></label><input type="email" placeholder="example@example.com"></div>
      <div class="form-row"><label>電話番号<span class="req">必須</span></label><input type="tel" placeholder="例）090-1234-5678"></div>
      <div class="form-row"><label>お住まいの地域<span class="opt">任意</span></label><input type="text" placeholder="例）岡山県倉敷市"></div>
      <div class="form-row"><label>現在のご職業・学校名<span class="opt">任意</span></label><input type="text"></div>
      <div class="form-row"><label>保有資格<span class="opt">任意</span></label><input type="text" placeholder="例）普通自動車免許、測量士補"></div>
      <div class="form-row"><label>ご質問・ご希望など<span class="opt">任意</span></label><textarea placeholder="会社見学の希望日、聞いてみたいことなど"></textarea></div>
      <div class="form-row"><label><input type="checkbox"> <span><a href="design3-privacy.html" style="color:var(--blue); text-decoration:underline;">プライバシーポリシー</a>に同意する</span></label></div>
      <div style="margin-top:24px;"><button type="submit" class="btn">確認画面へ</button></div>
    </form>'''
tel = f'''    <div class="fade-target" style="display:flex; gap:40px; flex-wrap:wrap; align-items:center;">
      <div><div style="font-family:'Inter',sans-serif; font-size:clamp(28px,3vw,40px); font-weight:700; color:var(--blue);">086-423-1899</div><div style="font-size:14px; color:var(--muted);">平日 9:00〜17:00 ／「採用の件で」とお伝えください</div></div>
      <p style="flex:1; min-width:260px; font-size:15px; color:var(--txt-2);">フォームの入力が難しい方は、お電話でも受け付けています。担当：{CHK("要確認")}</p>
    </div>'''
body = (phero(REC + [(None, 'エントリー')], 'エントリー', 'ENTRY', '0263', 'Entry',
              '下記フォームに入力のうえ、送信してください。内容を確認し、担当者よりご連絡いたします。')
        + sibnav('recruit-entry')
        + sec(head('エントリーフォーム', 'Entry Form') + '\n' + form, 'Entry Form', 'ENTRY')
        + sec(head('お電話でのエントリー', 'Telephone') + '\n' + tel, 'Telephone', 'TEL', cls='tone'))
new_page('recruit-entry', 'エントリー', BANNER('エントリー', '/recruit/entry/'), body)
h = read('recruit-entry')
h = re.sub(r'<section class="cta3">.*?</section>\n', '', h, count=1, flags=re.S)  # 自分自身へのCTAは出さない
write('recruit-entry', h)

# ============================================================ ニュース詳細
art = f'''<section class="phero v3"><div class="wrap"><div class="pcrumb"><a href="design3-top.html">ホーム</a> ／ <a href="design3-news.html">ニュース</a> ／ 記事詳細</div></div></section>
<section style="padding-top:clamp(40px,5vw,72px);">
  <div class="wrap">
    <article class="article">
      <div class="meta"><time>2021.07.09</time><span class="cat">技術</span></div>
      <h2>3次元空撮地形構造物処理システムを導入しました</h2>
      <div class="eye"><img src="{photo('0224')}" alt=""></div>
      <p>本文はWordPressの投稿で更新する想定のサンプルです。{CHK("サンプル記事")}</p>
      <p>当社では、ドローンによる空撮データから地形や構造物の3次元モデルを生成するシステムを導入しました。広い範囲を短時間で計測でき、人が立ち入りにくい場所でも安全にデータを取得できます。</p>
      <h3>導入の目的</h3>
      <p>災害時の被災状況の把握や、造成・河川工事の起工測量など、スピードと安全性が求められる現場での活用を想定しています。</p>
      <figure><img src="{photo('0385')}" alt="" loading="lazy"><figcaption>点群データの処理画面</figcaption></figure>
      <h3>今後の取り組み</h3>
      <p>3Dレーザースキャナーとの併用により、より精度の高い成果品のご提供に努めてまいります。</p>
    </article>
    <div class="pager"><a href="design3-news-detail.html">← 前の記事</a><a href="design3-news.html">一覧に戻る</a><a href="design3-news-detail.html">次の記事 →</a></div>
  </div>
</section>
'''
new_page('news-detail', 'ニュース 記事詳細', BANNER('ニュース 記事詳細', '/news/xxxx/'), art)

# ============================================================ プライバシーポリシー
pol = f'''{phero([(None, 'プライバシーポリシー')], 'プライバシーポリシー', 'PRIVACY POLICY')}
<section style="padding-top:clamp(48px,5vw,80px);">
  <div class="wrap"><div class="policy">
    <p>株式会社第二開発技工（以下「当社」）は、お客様・応募者の個人情報を適切に取り扱うため、以下のとおりプライバシーポリシーを定めます。{CHK("文面要確認")}</p>
    <h3>1. 個人情報の取得</h3><p>当社は、お問い合わせ・採用エントリー等の際に、氏名・連絡先等の個人情報を適法かつ公正な手段により取得します。</p>
    <h3>2. 利用目的</h3><ol><li>お問い合わせへの回答・ご連絡のため</li><li>採用選考および応募者へのご連絡のため</li><li>業務上必要なご連絡・ご案内のため</li></ol>
    <h3>3. 第三者への提供</h3><p>法令に基づく場合を除き、ご本人の同意なく個人情報を第三者に提供することはありません。</p>
    <h3>4. 安全管理</h3><p>当社は、個人情報の漏えい・滅失・毀損を防止するため、必要かつ適切な安全管理措置を講じます。</p>
    <h3>5. 開示・訂正・削除</h3><p>ご本人から個人情報の開示・訂正・削除等のお申し出があった場合は、ご本人であることを確認のうえ、速やかに対応します。</p>
    <h3>6. お問い合わせ窓口</h3><p>株式会社第二開発技工<br>〒710-0845 岡山県倉敷市西富井446-2／TEL 086-423-1899</p>
    <p style="margin-top:40px; color:var(--muted);">制定日：— {CHK("要確認")}</p>
  </div></div>
</section>
'''
new_page('privacy', 'プライバシーポリシー', BANNER('プライバシーポリシー', '/privacy/'), pol)
print('new pages ok')
