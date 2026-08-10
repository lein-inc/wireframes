# 近江度量衡 Webサイト デザイン実装仕様書

TOP（`index.html`）と下層ページ（`company.html` ほか）で確立した実装ルール。**新規ページ・仮ページはこの仕様に沿って実装調整する。**

---

## 0. ファイル構成と役割

| ファイル | 役割 |
|---|---|
| `site.css` | 下層ページ共通スタイル（トークン・ヘッダー・ヒーロー・フッター・全コンポーネント）|
| `site.js` | 下層ページ共通JS。**ヘッダー/フッターを注入**、ナビ挙動、出現アニメ、ドロワー |
| `index.html` | TOP。自己完結（インラインCSS/JS、動画FV、ピン留めスクロール等の特殊演出）|
| `products.html` / `product-agri.html` / `products-grain/industry/other.html` | 製品ページ。index_8シェル由来のインラインCSS＋各ページ独自CSS |

**下層ページは原則 `site.css`＋`site.js` を読み込むだけ**でヘッダー/フッター/共通部品が揃う。製品ページのみ独自シェル（歴史的経緯）。

---

## 1. デザイントークン（`:root`）

```css
--paper:#ffffff;   /* 背景・白 */
--ink:#000000;     /* 文字・黒地 */
--red:#ff0000;     /* アクセント（唯一の有彩色）*/
--line:#000;       /* 罫線 */
--frame:28px;      /* 基準余白（SP:16px）*/
--en:"Geist","Oswald",sans-serif;                                  /* 英字 */
--jp:"Gen Interface JP","Noto Sans JP","Hiragino Sans",system-ui;  /* 和文ゴシック（本文）*/
--mincho:"Noto Serif JP","Hiragino Mincho ProN",serif;             /* 和文明朝（見出し）*/
```

- **色は白・黒・赤の3色のみ**。グレーは黒の透明度（`rgba(0,0,0,.x)` / `rgba(255,255,255,.x)`）で表現。中間グレーの直値（#333等）は使わない。
- 罫線は **0.5px**（`border:0.5px solid var(--line)`）。赤アクセントの下線・帯は対象外。

### フォント読み込み（全ページ共通・`<head>`）
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Oswald:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;700;900&family=Noto+Serif+JP:wght@400;500;600;700;900&display=swap" rel="stylesheet">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/gen-interface-jp@latest/cdn/all.css">
```
※ `site.css`を使わない製品ページで明朝を使う場合、`--mincho`未定義のため **`font-family:"Noto Serif JP",serif` を直書き**する。

---

## 2. フォント運用ルール

| 用途 | フォント | 例 |
|---|---|---|
| 見出し（和文メイン）| **明朝** `--mincho` weight 600 | セクション見出し・ヒーロー見出し |
| 英字（ショルダー・ラベル・数字）| **Geist** `--en` | ( COMPANY )・年号・01 |
| 本文・説明文 | **ゴシック** `--jp` weight 400〜500 | リード文・カード本文 |
| 強い和文ラベル（ナビ・タグ・CTA）| ゴシック `--jp` weight 700〜900 | 会社案内・募集要項 |

---

## 3. 見出しルール（最重要）

**「日本語メイン（明朝・大）＋（英語）サブ（小・括弧付き）」**。英語を大見出しにしない。

```html
<div class="sec-head rv">
  <h2 class="sec-jp">会社案内</h2>     <!-- 日本語メイン（明朝・大）-->
  <p class="sec-ttl">Company</p>      <!-- 英語サブ（小・( )は CSS で付与）-->
</div>
```
```css
.sec-jp{font-family:var(--mincho);font-weight:600;font-size:clamp(2rem,4.2vw,3.9rem);letter-spacing:.04em;line-height:1.15}
.sec-ttl{font-family:var(--en);font-weight:500;font-size:clamp(.78rem,1vw,1rem);letter-spacing:.24em;text-transform:uppercase;opacity:.55;margin-top:14px}
.sec-ttl::before{content:"( "} .sec-ttl::after{content:" )"}
.sec-head{margin-bottom:52px}
```
- 順序は **必ず 日本語→英語**（明朝が上、括弧英語が下）。
- 見出し頭の赤ドット等は付けない。
- 暗色セクションでは `.section--ink .sec-jp{color:#fff}`。

---

## 4. 共通ヘッダー（浮遊・分離型グローバルナビ）

`site.js` が `#site-header` に注入。**上下左右18px（SP12px）浮いた透明バー。ロゴ＝左（座布団なし）／メニュー＝右付け白ボックス／お問い合わせ＝黒ボックス、間は背景が透ける。**

- **ロゴの色**：暗色ヒーロー上は**白**（`filter:brightness(0) invert(1)`）→ ヒーローを抜ける／白ヒーローのページでは**赤**（`.nav.is-logo-red`）。`site.js`が自動切替。
- **メニュー**：白ボックス（`background:#fff;border:0.5px;border-right:0`）、リンクは黒 12.5px weight600、ホバーで赤＋下線。
- **お問い合わせ**：黒ボックス（`background:var(--ink)`）、ホバー赤。
- **メガメニュー**：`.nitem:hover .mega` で白パネル展開（top:18+64px）。
- **下スクロールで自動格納**（`.nav.is-hidden` `translateY(calc(-100% - 22px))`）。
- **レスポンシブ**：〜1100pxでメニュー→ハンバーガー（白ボックス）＋ドロワー。〜900pxでナビ余白12px・お問い合わせ格納。
- `window.OMI_ACTIVE="company"` を指定すると該当ナビに赤下線（`.is-active`）。

キー: `products / service / delivery / company / history / recruit`。

---

## 5. ページヒーロー（`.phero`）

**黒地＝背景写真を透過（薄い黒膜）／日本語メイン＋（英語）サブ／0.5px方眼／左下に段差。**

```html
<section class="phero">
  <div class="phero__photo" style="background-image:url(photo-industry.jpg)"></div>
  <div class="phero__lines" aria-hidden="true"></div>
  <div class="phero__in">
    <p class="crumb"><a href="index.html">TOP</a> &rsaquo; 会社案内</p>
    <span class="phero__jp">会社案内</span>       <!-- 日本語メイン明朝・大 -->
    <span class="phero__en">Company</span>        <!-- ( 英語 ) 小 -->
    <p class="phero__lead">…リード文（1〜2行）…</p>
  </div>
</section>
```
主要値（`site.css`）:
- `padding:210px 7vw 110px` / `background:var(--ink)`
- `.phero__photo`：`filter:grayscale(.08) contrast(1.02)` ＋ `::after` に **薄い黒膜 `rgba(8,9,8,.56)`**
- `.phero__lines`：FVと同じ **0.5px方眼（縦横・白22%）**
- `.phero__jp`：明朝 600 `clamp(2.6rem,5.6vw,4.9rem)`／`.phero__en`：Geist 500 小・`( )`／`.phero__lead`：14px lh2.1 白80% max660
- `.crumb`：Geist 12px .2em uppercase 白60%
- **左下の段差（全ページ統一・clip-path方式）**：`.phero`に`clip-path`で階段状の輪郭を切り出し、**背景写真がひと続きで段差まで映る**（製品ページと共通）。
```css
.phero{clip-path:polygon(0 0,100% 0,100% calc(100% - 54px),24% calc(100% - 54px),24% 100%,0 100%)}
/* SP: calc(100% - 34px) / 40% */
```
- **段差は全ページ共通で付ける**（ルール）。ヒーロー直下が**暗色セクション**のページ（納入実績＝黒数字帯、ヒストリー＝暗色トンネル 等）は、段差の切り抜きが白く抜けてギャップに見えるので、**そのページの `body` 背景を黒にして段差の抜けを黒で埋める**（＝次の暗色セクションへシームレスに繋がる）：
```html
<link rel="stylesheet" href="site.css">
<style id="pagebg">body{background:var(--ink)}</style>
```
※ 直下が白/灰のページ → body は既定の白（段差の抜けも白で自然）。直下が黒のページ → body を黒に。どちらでも段差自体は残す。
※ `.phero--flush`（段差なし）も用意はあるが、原則は上記の body 背景切替で段差を保つ。

### 特殊ヒーロー
- **採用TOP**：大タイポ明朝の独自FV（`rct-fv`）。白ヒーローのためロゴは常時赤。
- **ヒストリー**：`.phero`（暗色）＋直下に透視スクロール `.hc-scene`（奥→手前・写真背景・ブラー黒透過カード）。ロゴはトンネル末尾まで白維持。

---

## 6. フッター

`site.js` が `#site-footer` に注入。
- **マーキー帯 `.strip`**（40vh）：`.strip__bg`（`photo-grain.jpg`＋暗幕）の上に「We Measure the Future」が流れる。
- **黒のCONTACTパネル**（`.foot__contact`）が帯に食い込み右端ベタ付け。
- **フッターナビ**（3カラム：ブランド／サイトリンク2列／CONTACT）。
- **赤の採用バナー `.foot__recruit`**（「いきるの単位とは、なんだろう。」）→ 著作権バー。

---

## 7. セクション枠・背景の使い分け

```css
.section{padding:120px 7vw}          /* 標準 */
.section--tight{padding:86px 7vw}    /* 詰め */
.section--gray{background:#f2f2f2}   /* 薄灰（交互リズム）*/
.section--ink{background:var(--ink);color:#fff}  /* 黒（強調・数字帯）*/
.container{max-width:1200px;margin:0 auto}
.divider{height:0.5px;background:var(--line);opacity:.5}
```
- 標準は**白**。セクションの交互リズムに**薄灰**、数字帯・CTA・締めに**黒**。
- 製品ページのリズム＝ヒーロー黒 → Lineup白 → Flow/独自セクション黒 → Features白 → CTA黒。

---

## 8. 共通コンポーネント（`site.css`）

| クラス | 用途 |
|---|---|
| `.btn` / `.btn--outline` / `.btn--white` | ボタン（赤地白字／枠線／白地）。矢印は `<i class="arrow-i">→</i>` |
| `.card` + `.grid-2/3/4` | 汎用カード（番号・タイトル・本文）|
| `.stat-row` + `.stat` | 数字タイル（Geist大数字＋赤単位）|
| `.base-cards` + `.base-card` | 拠点カード（タグ・住所・TEL・Mapembed）|
| `.ptable` | 会社概要テーブル（`th`210px）|
| `.timeline` / `.tl-era` / `.tl-item` | 縦タイムライン（赤丸ノード）|
| `.flow` + `.flow__step` | 6分割の工程フロー（赤トップ罫線＋番号）|
| `.news-list` + `.news-row` | ニュース一覧（日付＋細罫線タグ｜＋タイトル）|
| `.entry-split` + `.entry-card--new/mid` | 新卒(赤)/中途(黒)の2枚パネル（ホバー展開）|
| `.form` | フォーム（ガワ）。`.form__ctrl` `.form__label .req` |
| `.prose` | 規約等の本文（番号付き）|
| `.ph` (`--wide/--sq/--por`) | **画像プレースホルダ（斜線ハッチ＋ラベル）** |

見出しは全て §3（`.sec-jp`＋`.sec-ttl`）を使う。

---

## 9. 出現アニメ

```html
<div class="sec-head rv">…</div>
<div class="grid-3 rv rv-d1">…</div>
```
```css
.rv{opacity:0;transform:translateY(34px);transition:.8s cubic-bezier(.2,.7,.2,1)}
.rv.is-in{opacity:1;transform:none}
.rv-d1{transition-delay:.12s} .rv-d2{.24s} .rv-d3{.36s}
```
`site.js`のIntersectionObserverが`.rv`→`.is-in`。段差表示は`rv-d1/d2/d3`。
※ 自動操作タブでは発火しないことがある（実ブラウザでは正常）。

---

## 10. インタラクション一覧

- **ヘッダー**：下スクロールで格納／ロゴ白⇄赤自動切替（`site.js`）。
- **メガメニュー**：ホバー展開。
- **出現アニメ**：スクロールで下からフェードイン。
- **ホバー展開パネル**（採用の新卒/中途）：ホバーで`flex-grow`拡大＋背景写真を透過オーバーレイ（`opacity 0→.34`）＋説明文フェードイン。
- **透視スクロール**（ヒストリー）：`position:sticky`＋`perspective`でカードが奥→手前へ。年代ごと背景写真クロスフェード。
- **マーキー**：フッター帯・採用の英字帯。

---

## 11. レスポンシブ

- ブレークポイント：**1100px**（ナビ→ハンバーガー）・**900px**（段組み1カラム化・余白縮小）・640px（微調整）。
- 段組みは`@media(max-width:900px)`で`grid-template-columns:1fr`に集約（`site.css`末尾に一括定義済み）。
- 高さは固定しない。画像は`aspect-ratio`＋`cover`。
- 横スクロール禁止（幅広要素は`overflow-x:auto`で内部スクロール）。

---

## 12. 新規ページ実装レシピ（下層ページ）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ページ名｜近江度量衡株式会社</title>
  <!-- ▼フォント読み込み（§1）をコピペ▼ -->
  <link rel="stylesheet" href="site.css">
  <!-- 必要ならページ固有CSSを <style> で追記（クラス名は既存と衝突させない）-->
</head>
<body>
  <div id="site-header"></div>

  <section class="phero">
    <div class="phero__photo" style="background-image:url(写真.jpg)"></div>
    <div class="phero__lines" aria-hidden="true"></div>
    <div class="phero__in">
      <p class="crumb"><a href="index.html">TOP</a> &rsaquo; ページ名</p>
      <span class="phero__jp">ページ名（和文）</span>
      <span class="phero__en">English</span>
      <p class="phero__lead">リード文。</p>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="sec-head rv"><h2 class="sec-jp">見出し</h2><p class="sec-ttl">Heading</p></div>
      <!-- .rv を付けたコンテンツ（card / grid / stat-row 等）-->
    </div>
  </section>

  <div id="site-footer"></div>
  <script>window.OMI_ACTIVE="company";</script>   <!-- 該当ナビキー -->
  <script src="site.js"></script>
</body>
</html>
```
チェックリスト：
1. フォント読み込み＋`site.css`／`site.js` を入れたか
2. ヒーローは **写真＋薄い黒膜＋日本語メイン＋（英語）＋段差** か
3. セクション見出しは **日本語明朝＋（英語）** の順か
4. コンテンツに `.rv`（必要なら `rv-d1/2/3`）を付けたか
5. `window.OMI_ACTIVE` を設定したか
6. 交互リズム（白／薄灰／黒）と余白（`.section` 120px）を守ったか
7. 375px で横スクロールが出ないか

---

## 13. 素材・プレースホルダ運用

- 未支給の画像は **`.ph`（斜線ハッチ＋ラベル）** か `phero__photo` にダミー写真。
- 使用可能な写真：`photo-industry / photo-grain / photo-agri / photo-others`、`stat-facilities / stat-service`、`hist.jpg〜hist4.jpg`、`prod-millistar / prod-rollerstar`、`agri-step1〜9`、`shiga.webp`、`clogos/c01〜20.svg`。
- ロゴ：`logo_r.png`（暗色上は`filter`で白化）。

---

## 14. リンク・命名規約

- リンクは相対 `.html`。納入実績＝`delivery.html`。
- 製品：一覧`products.html`／詳細`product-agri / products-grain / products-industry / products-other .html`。
- パンくずは `TOP › ページ名`（製品は `TOP / Products / 分野`）。
- ナビ/フッターの製品リンクは各詳細ページへ直結（`site.js`・各ページで統一）。

---

## 補足：やってはいけない

- 英語を大見出しにする（必ず和文メイン）。
- 中間グレー直値・1px超の太い罫線・白黒赤以外の色。
- 高さ固定・中途半端な幅での勝手な縦積み。
- 見出し頭の赤マーク。段差を持つセクションに `overflow:hidden`（段差が切れる）。
