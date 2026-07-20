#!/bin/bash
# 近江デザインを lein-inc/wireframes に同期してpushする（必ずこのスクリプト経由で行うこと）
set -e
cd "$(dirname "$0")"
TOKEN="$1"
MSG="${2:-デザイン更新}"
[ -z "$TOKEN" ] && { echo "usage: sync_push.sh <github_token> [commit message]"; exit 1; }
rsync -a --delete --exclude='bk/' --exclude='_shot_tmp.html' \
  /Users/apple/site/oumidoryoukou/design /Users/apple/site/oumidoryoukou/wier ./oumidoryoukou/
git add -A
if git diff --cached --quiet; then echo "no changes"; exit 0; fi
git -c user.name="seki" -c user.email="naofumi@le-in.net" commit -q -m "$MSG

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
git push -q "https://${TOKEN}@github.com/lein-inc/wireframes.git" main
echo "LEIN_PUSHED"
