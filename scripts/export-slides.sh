#!/usr/bin/env bash
# 講師用。Node.js、Chrome/Chromium、日本語フォントが必要。
# 初回: npm install --prefix .slide-tools @marp-team/marp-cli
# VS CodeのMarp拡張からPDFを出力する方法でも構いません。
set -euo pipefail
cd "$(dirname "$0")/.."
MARP_COMMAND="${MARP_COMMAND:-.slide-tools/node_modules/.bin/marp}"
for slides in session{01..08}/slides.md; do
  "$MARP_COMMAND" "$slides" --pdf --allow-local-files -o "${slides%.md}.pdf"
done
