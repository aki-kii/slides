# JAWS-UG CDK支部 × 東京支部コラボ cdkdハンズオンの発表（2026-11-05）

Google スライドに取り込むため、Slidev ではなく .pptx で組んでいる。

```bash
AWS_ICONS=<アイコン置き場> python3 diagrams/deploy_flow.py   # images/*.svg を作る
python3 build_deck.py cdk-talk.pptx                          # cdk-talk.pptx を作る
```

`images/*.png` は `images/*.svg` を書き出したもの。`build_deck.py` はこの PNG を貼る。

仮の箇所には右上に「仮」の札（図形名 `kari`）を付け、理由をスピーカーノートに書いている。
