# BELIEF 本番TOP：売買成約実績マップ＋REVIEW（口コミ）反映手順

対象：`belief-inc.com` / テーマ `belief`（親・稼働中）/ ファイル **`index.php`**
※本番TOPは固定ページではなくテーマテンプレートで描画されているため、本文編集では入りません。

## 0. 事前バックアップ（必須）

1. 管理画面 → 外観 → テーマファイルエディター → テーマ `belief` → `index.php`（テーマのためのテンプレート）
2. エディタ内で **⌘A → ⌘C** で全文コピー
3. `/Users/apple/site/belife/index_php_backup_YYYYMMDD.txt` として保存

SSH/FTPが無いため、壊した場合の復旧手段はこのバックアップの貼り戻ししかありません。**必ず先に取ること。**

## 1. ブロックA（売買成約実績マップ）を貼る

貼り付け元：`prod_insert_A_map.html`

挿入位置：下記コメント行の **直前**

```
<!-- ======= info /  ======= -->
<section class="info">
```

つまり `.newArrival` セクションの `</section>` と `<!-- ======= info` の間。

## 2. ブロックB（REVIEW／口コミ）を貼る

貼り付け元：`prod_insert_B_review.html`

挿入位置：下記コメント行の **直前**

```
<!-- ======= service /  ======= -->
<section class="service">
```

つまり `.voice` セクションの `</section>` と `<!-- ======= service` の間。

## 3. 更新して確認

1. 「ファイルを更新」
2. TOPをスーパーリロード（⌘+Shift+R）。KUSANAGI のキャッシュ層（`x-b-cache`）があるので、反映が見えない場合は少し待つかキャッシュクリア
3. 確認ポイント
   - 新着物件の下に「売買成約実績」→ マップ＋直近の成約実績テーブルが出る
   - お客様の声の下に「REVIEW／お客様の声」（クリーム背景＋金の罫線）→ 口コミ4件
   - SPで マップ 1180px / 口コミ 480px の高さになっている

## 補足

- CSSはブロックA内の `<style>` にまとめて入れています（`.bf-add*` に隔離、テーマCSSには触れません）。ブロックBだけ貼るとスタイルが当たりません。**Aを先に**。
- 埋め込みは買取LP `/real-estate-sale/` と同一のものです
  - マップ `https://iqra.cloud/embed/b9d67029005df4801eb2`
  - 口コミ `https://embed.i-user-voice.com/34a6fc4fd03ad4c004aa`
- マップは `lein-inc.github.io` の静的プレビュー上では真っ白になりますが、`belief-inc.com` 上では正常表示します（親ドメイン依存）。プレビューで見えなくても本番では問題ありません。
- PHPロジックには一切触れません（HTMLとstyleの追加のみ）ので、白画面（構文エラー）のリスクは低い構成です。

## 元データ

- プレビュー（先方OK済み）：`top-preview.html` → `https://lein-inc.github.io/wireframes/belife/top-preview.html`（PW `leinbelife0526`）
- 先方確定（2026-08-05）：口コミは現状の4件でOK／マップは現状のものでOK
