"""IaC の定義の図（iac-define.svg）を、iac-diff.svg の部品から組む。
「ソフトウェア開発フレームワーク」は発表で説明しないので、図にも入れない（2026-11-04 本人）。

「コードでインフラストラクチャを定義し、プロビジョニングする」を、
コード → IaCのツール → AWSアカウント の横並びで見せる。矢印は短く、ラベルは名詞にする（2026-11-04 本人）。
iac-diff.svg と同じ箱とアイコンを使うので、次のページの図と見た目がそろう。

  python3 diagrams/iac_define.py
"""
import os
import re

from resource_swap import swap

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "..", "public", "images")
SRC = os.path.join(IMAGES, "iac-diff.svg")
OUT = os.path.join(IMAGES, "iac-define.svg")

INK = "#2c3e50"
SUB = "#6b7684"
FONT = "'Noto Sans JP', 'Hiragino Sans', sans-serif"

lines = open(SRC, encoding="utf-8").read().split("\n")


def take(a, b, drop=()):
    """iac-diff.svg の a〜b 行目（1 始まり）を取り出す。drop の行は除く。"""
    return [lines[i - 1] for i in range(a, b + 1) if i not in drop]


def plain_ecs(block):
    # iac-diff では ECS が差分なので緑の太字。ここでは差分の話をしないので、ほかと同じ字にする
    return [l.replace('font-weight="bold" fill="#0E8A6E"', 'font-weight="normal" fill="#2c3e50"') for l in block]


def text(x, y, s, size=14, color=INK, weight="normal"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="middle">{s}</text>')


def arrow(x1, x2, y):
    return (f'<path d="M{x1},{y} L{x2},{y}" fill="none" stroke="{INK}" stroke-width="2.5" '
            'stroke-linejoin="round" stroke-linecap="round" marker-end="url(#a-i)"/>')


code = plain_ecs(take(4, 32, drop={31}))  # 31 行目は ECS を囲む緑の枠
code = [l.replace(">コード（あるべき姿）<", ">コード<") for l in code]
tool = take(57, 60)
infra = plain_ecs(take(77, 106, drop={105}))  # 105 行目は ECS を囲む緑の枠
infra = [l.replace(">実リソース<", ">AWSアカウント<") for l in infra]

body = [
    lines[0].replace('viewBox="0 0 1000 366"', 'viewBox="0 0 810 196"').replace(
        re.search(r'aria-label="[^"]*"', lines[0]).group(0),
        'aria-label="コードでインフラストラクチャを定義し、IaCのツールがそれを読んでAWSアカウントにプロビジョニングする"'),
    lines[1],
    lines[2],
    *code,
    arrow(272, 362, 90),
    text(317, 78, "適用", size=14),
    '<g transform="translate(-8,-88)">',
    *tool,
    "</g>",
    arrow(438, 546, 90),
    text(492, 78, "プロビジョニング", size=13),
    '<g transform="translate(-192,-90)">',
    *infra,
    "</g>",
    "</svg>",
]
svg = swap("\n".join(body) + "\n")
# 同じページに iac-diff.svg が並んでも id がぶつからないよう、アイコンの id に接頭辞を付ける
svg = re.sub(r'(id="|url\(#)([a-z]+\d+-)', r"\1def-\2", svg)
open(OUT, "w", encoding="utf-8").write(svg)
print(OUT)
