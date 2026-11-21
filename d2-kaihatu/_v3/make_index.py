#!/usr/bin/env python3
"""index.html の v2 見出しの上に v3.1 ブロック（_v3/index_block_v31.html）と v3 ブロック（_v3/index_block.html）を差し込む。何度実行しても同じ
  再生成の順番: python3 _build.py && python3 _inject_gate.py && python3 _v3/make_index.py
  （_build.py は design3-*.html を触らない。design3 は直接編集のソース）"""
import os, re
WF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = (open(os.path.join(WF, '_v3', 'index_block_v31.html')).read().rstrip('\n') + '\n'
         + open(os.path.join(WF, '_v3', 'index_block.html')).read())
p = os.path.join(WF, 'index.html')
html = open(p).read()
html = re.sub(r'<!-- V3_BLOCK -->.*?<!-- /V3_BLOCK -->\n?', '', html, flags=re.S)
anchor = '<div class="wrap">\n  <h2 style="font-size:22px; margin-top:48px; padding-bottom:12px; border-bottom:2px solid #333;">\n    新デザイン案 v2'
assert anchor in html, 'index.html の v2 見出しが見つからない'
html = html.replace(anchor, '<!-- V3_BLOCK -->\n' + BLOCK.rstrip('\n') + '\n<!-- /V3_BLOCK -->\n' + anchor, 1)
open(p, 'w').write(html)
print('index: v3 ブロックを差し込み')
