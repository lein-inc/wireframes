#!/usr/bin/env python3
"""【初回のみ・11/11実行済】デザイン案 v3 の初期版を design2-*.html から派生生成した
  以後 design3-*.html は直接編集のソース（_v3/apply_*.py で変更・バックアップは _v3/bk_*/）
  v1(design-*) / v2(design2-*) はそのまま残し、design3-*.html と css/design3.css を追加する
  使い方: python3 _build.py && python3 _inject_gate.py && python3 _v3/build.py
  ・撮影写真は ../photos/_original/S1200xxx.jpeg を長辺1800pxに縮小して img/photo/ へ（既存はスキップ）
  ・index.html 先頭に v3 ブロックを差し込む（_build.py で index が作り直されても再実行で復活）
"""
import os, re, glob, shutil
from PIL import Image, ImageOps

WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(WF, '..', 'photos', '_original')
PHOTO = os.path.join(WF, 'img', 'photo')

# design2 のダミー番号(img/dummy/NN.jpg) → 撮影写真番号。未撮影のカットはダミーのまま残す
DUMMY2PHOTO = {
    '23': '0055',  # 代表 ポートレート
    '26': '0336',  # 測量助手（標尺）
    '04': '0290',  # 測量作業員（TS）
    '21': '0183',  # 施工管理（現場指示・電話）※ナンバー注意
    '24': '0553',  # 社員写真01（インタビューA）
    '25': '0635',  # 社員写真02（インタビューB）
    '47': '0662',  # 社員写真03（執務風景）
    '28': '0389',  # 道路設計（CAD）
    '29': '0386',  # 河川設計（点群）
    '30': '0393',  # 土地造成（CAD）
    '05': '0314',  # 工事測量現場
    '08': '0342',  # 公共測量（レベル）
    '07': '0303',  # 工事測量（TS）
    '06': '0287',  # TS
    '09': '0158',  # GNSS
    '14': '0213',  # DRONE
    '19': '0089',  # 3D SCAN
    '16': '0260',  # 迅速な被災把握（ドローン引き）
    '15': '0092',  # 非接触計測（3Dスキャナー）
    '31': '0385',  # 3Dモデル生成（点群画面）
    '44': '0256',  # 地域活動（代用：チームで上空確認）
    '20': '0682',  # 現代のテクノロジー（機材ブツ撮り）
    '01': '0224',  # ドローン空撮
    '17': '0129',  # 3Dスキャナー（代表＋社員）
    '12': '0144',  # GNSS 現場カット
    # 未撮影 → ダミー継続: 39 ボーリング / 40 動植物 / 41 水質・大気 / 42 騒音・振動 / 38 深浅測量 / 43 被災地 / 36 伊能忠敬 / 03 工程アニメ
}

# img/eng*.jpg（v2の仮写真）を出現順に置き換える
ENG_SEQ = {
    'design2-top.html': ['0290', '0389', '0183',            # SERVICE 3枚（測量/調査設計/施工管理）
                         '0373',                            # FOUNDER 円形
                         '0553', '0290', '0635', '0213', '0401', '0137', '0662', '0350',   # 社員写真帯
                         '0157', '0647', '0094', '0413', '0089', '0336', '0224', '0412',
                         '0273', '0553'],                   # RECRUIT 大判＋円形
    'design2-service.html': ['0224', '0314', '0389', '0183'],
    'design2-recruit.html': ['0273'],
}

def photo(n):
    return f'img/photo/S120{n}.jpg'

def make_photo(n):
    dst = os.path.join(WF, photo(n))
    if os.path.exists(dst): return
    im = ImageOps.exif_transpose(Image.open(os.path.join(ORIG, f'S120{n}.jpeg')))
    im.thumbnail((1800, 1800))
    im.convert('RGB').save(dst, quality=82, optimize=True, progressive=True)
    print('photo:', os.path.basename(dst))

def convert(name, html):
    html = html.replace('design2-', 'design3-').replace('css/design2.css', 'css/design3.css')
    # 上部の帯: v2表記 → v3表記
    html = html.replace('DESIGN v2 | TOPページ ブラッシュアップ案（構成・FVはv1踏襲／演出・画像・レイアウトを調整） ／ 写真はダミー・本番は実写差替',
                        'DESIGN v3 | TOPページ（v2に10/9撮影の実写を反映）')
    html = html.replace('DESIGN v2 |', 'DESIGN v3 |').replace('（ブラッシュアップ版・写真はダミー）', '（v3・実写反映／未撮影カットはダミー）')
    html = re.sub(r'img/dummy/(\d+)\.jpg',
                  lambda m: photo(DUMMY2PHOTO[m.group(1)]) if m.group(1) in DUMMY2PHOTO else m.group(0), html)
    if name in ENG_SEQ:
        seq = iter(ENG_SEQ[name])
        html = re.sub(r'img/eng\d_[a-z]+\.jpg', lambda m: photo(next(seq)), html)
    return html

def main():
    import sys
    if os.path.exists(os.path.join(WF, 'design3-top.html')) and '--force' not in sys.argv:
        sys.exit('design3-*.html は 11/11 以降 直接編集のソースです。上書きする場合のみ --force')
    os.makedirs(PHOTO, exist_ok=True)
    for n in set(DUMMY2PHOTO.values()) | {p for v in ENG_SEQ.values() for p in v}:
        make_photo(n)
    shutil.copy(os.path.join(WF, 'css', 'design2.css'), os.path.join(WF, 'css', 'design3.css'))
    for f in sorted(glob.glob(os.path.join(WF, 'design2-*.html'))):
        name = os.path.basename(f)
        out = os.path.join(WF, name.replace('design2-', 'design3-'))
        open(out, 'w').write(convert(name, open(f).read()))
        print('page:', os.path.basename(out))
    inject_index()

V3_BLOCK = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index_block.html')).read()

def inject_index():
    p = os.path.join(WF, 'index.html')
    html = open(p).read()
    html = re.sub(r'<!-- V3_BLOCK -->.*?<!-- /V3_BLOCK -->\n?', '', html, flags=re.S)
    anchor = '<div class="wrap">\n  <h2 style="font-size:22px; margin-top:48px; padding-bottom:12px; border-bottom:2px solid #333;">\n    新デザイン案 v2'
    assert anchor in html, 'index.html の v2 見出しが見つからない'
    html = html.replace(anchor, '<!-- V3_BLOCK -->\n' + V3_BLOCK.rstrip('\n') + '\n<!-- /V3_BLOCK -->\n' + anchor, 1)
    open(p, 'w').write(html)
    print('index: v3 ブロックを差し込み')

if __name__ == '__main__':
    main()
