"""「AWS CDKはOSS」の図（oss-cdk.svg）。左の AWS と右のコミュニティから、真ん中の aws/aws-cdk（GitHub）へ矢印を入れる。

2026-11-04 本人「とりあえず作ってみて」。貢献の割合や数は出さない。
アイコンは初心者支部で登壇したスライドの ai-validation.svg（AWS のロゴ、人のアイコン）と、
simple-icons の GitHub（https://cdn.jsdelivr.net/npm/simple-icons@13.21.0/icons/github.svg）を使う。

  GITHUB_ICON=<github.svg のパス> python3 diagrams/oss_flow.py
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "..", "public", "images")
SRC = open(os.path.join(IMAGES, "ai-validation.svg"), encoding="utf-8").read().split("\n")
GITHUB = open(os.environ["GITHUB_ICON"], encoding="utf-8").read()
INK, SUB, LINE, GREEN = "#2c3e50", "#6b7684", "#c9d0d9", "#0E8A6E"
SANS = "'Noto Sans JP', 'Hiragino Sans', sans-serif"
MONO = "'Fira Code', monospace"


def block(a, b):
    return "\n".join(SRC[a - 1:b])


def place(svg, x, y, size):
    return re.sub(r'<svg x="[\d.]+" y="[\d.]+" width="\d+" height="\d+"', f'<svg x="{x}" y="{y}" width="{size}" height="{size}"', svg, count=1)


def text(x, y, s, size, color=INK, weight="normal", family=SANS, anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}">{s}</text>')


def arrow(x1, x2, y):
    return (f'<path d="M{x1},{y} L{x2},{y}" fill="none" stroke="{INK}" stroke-width="2.5" '
            'stroke-linejoin="round" marker-end="url(#oss-a)"/>')


AWS_LOGO = block(31, 34)   # AWS のロゴ
USER = block(24, 26)       # 人のアイコン
gh_path = re.search(r'<path d="([^"]+)"', GITHUB).group(1)

body = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 220" width="100%" role="img" '
    'aria-label="AWSとコミュニティの両方から、GitHubのaws/aws-cdkリポジトリにコードが入っていく">',
    '<!-- AWS Architecture Icons 2026-07-31 版（Icon-package_07312026）、GitHub は simple-icons -->',
    f'<defs><marker id="oss-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>',
    # AWS
    f'<rect x="10" y="40" width="220" height="150" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    place(AWS_LOGO, 92, 58, 56),
    text(120, 144, "AWS", 17, weight="bold"),
    text(120, 168, "開発とメンテナンス", 13, SUB),
    # aws/aws-cdk
    f'<rect x="350" y="20" width="220" height="180" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="2"/>',
    f'<svg x="430" y="44" width="60" height="60" viewBox="0 0 24 24"><path d="{gh_path}" fill="#181717"/></svg>',
    text(460, 140, "aws/aws-cdk", 19, weight="bold", family=MONO),
    text(460, 166, "GitHub のリポジトリ", 13, SUB),
    # コミュニティ
    f'<rect x="690" y="40" width="220" height="150" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    place(USER, 734, 66, 44), place(USER, 778, 58, 44), place(USER, 822, 66, 44),
    text(800, 144, "コミュニティ", 17, weight="bold"),
    text(800, 168, "世界中のコントリビューター", 13, SUB),
    arrow(232, 346, 115), text(289, 103, "開発", 14),
    arrow(688, 574, 115), text(631, 103, "コントリビュート", 13),
    "</svg>",
]
svg = "\n".join(body) + "\n"
svg = re.sub(r'(id="|url\(#)([a-z]+\d+-)', r"\1oss-\2", svg)
open(os.path.join(IMAGES, "oss-cdk.svg"), "w", encoding="utf-8").write(svg)
print("oss-cdk")
