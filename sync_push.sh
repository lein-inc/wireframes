#!/bin/bash
# 各案件のプレビューを lein-inc/wireframes に同期してpushする（必ずこのスクリプト経由で行うこと）
set -e
cd "$(dirname "$0")"
TOKEN="$1"
MSG="${2:-デザイン更新}"
[ -z "$TOKEN" ] && { echo "usage: sync_push.sh <github_token> [commit message]"; exit 1; }
rsync -a --delete --exclude='bk/' --exclude='_shot_tmp.html' \
  /Users/apple/site/oumidoryoukou/design /Users/apple/site/oumidoryoukou/design2 /Users/apple/site/oumidoryoukou/wier ./oumidoryoukou/
# belife（BELIEF inc. 不動産買取LP）— wp-export/バックアップは公開対象外
rsync -a --delete --exclude='wp-export/' --exclude='*.bak_*' --exclude='.DS_Store' \
  /Users/apple/site/belife ./
# beljapan（Localステージングの静的ミラー / build_stg_share.sh で生成）
rsync -a --delete --exclude='.DS_Store' \
  /Users/apple/site/beljapan-stg/ ./beljapan/
# 第二開発技工（d2-kaihatu）— 暫定ミラー。本来の公開先は lein-inc/d2-kaihatu-wireframe
#   （そちらは sekilein に push 権限が無いため、権限付与までの暫定）
#   ビルド用スクリプト・社内メモ・キャプチャ(13MB・未参照)は公開対象外
rsync -a --delete \
  --exclude='.git/' --exclude='captures/' --exclude='_build.py' --exclude='_inject_gate.py' \
  --exclude='_auth_gate.html' --exclude='CHANGELOG.md' --exclude='.gitignore' \
  --exclude='引き継ぎ_*.md' --exclude='.DS_Store' \
  /Users/apple/site/dainigikou/wf/ ./d2-kaihatu/

git add -A
if git diff --cached --quiet; then echo "no changes"; exit 0; fi
git -c user.name="seki" -c user.email="naofumi@le-in.net" commit -q -m "$MSG

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
git push -q "https://${TOKEN}@github.com/lein-inc/wireframes.git" main
echo "LEIN_PUSHED"
