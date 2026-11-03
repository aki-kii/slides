"""iac-diff.svg をもとに、言葉とアイコンを入れ替えた図を書き出す。

- iac-diff-ideal.svg: 「コード（あるべき姿）」の枠を緑で強調する（IaCのデプロイの仕組み）
- cfn-define.svg: 「IaCとは？」の図を CloudFormation に置き換える（テンプレート → CloudFormation → スタック）
- cfn-deploy.svg: IaCのデプロイの仕組みの図を CloudFormation に置き換える（テンプレートとスタックを比べ、変更セットを反映する）

  AWS_ICONS=<アイコン置き場> python3 diagrams/iac_variants.py

アイコンは AWS Architecture Icons 2026-07-31 版。tasks/speaking/diagram-style.md に合わせる。
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(HERE, "..", "public", "images")
ICONS = os.environ["AWS_ICONS"].rstrip("/") + "/"

INK, SUB, GREEN = "#2c3e50", "#6b7684", "#0E8A6E"
FONT = "'Noto Sans JP', 'Hiragino Sans', sans-serif"

LINES = open(os.path.join(IMAGES, "iac-diff.svg"), encoding="utf-8").read().split("\n")
_n = [0]


def icon(name, x, y, size):
    _n[0] += 1
    prefix = f"v{_n[0]}-"
    s = open(ICONS + name).read()
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})")
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{body.strip()}</svg>'


TEMPLATE = "Res_AWS-CloudFormation_Template_48.svg"
STACK = "Res_AWS-CloudFormation_Stack_48.svg"
CFN = "Arch_AWS-CloudFormation_64.svg"


def text(x, y, s, size=14, color=INK, weight="normal"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="middle">{s}</text>')


def arrow(x1, x2, y):
    return (f'<path d="M{x1},{y} L{x2},{y}" fill="none" stroke="{INK}" stroke-width="2.5" '
            'stroke-linejoin="round" stroke-linecap="round" marker-end="url(#a-i)"/>')


def lines(a, b, swap=None, drop=()):
    """iac-diff.svg の a〜b 行目（1 始まり）。swap は {行: 置き換える文字列}。drop の行は除く。"""
    swap = swap or {}
    out = []
    for i in range(a, b + 1):
        if i in drop:
            continue
        out.append(swap.get(i, LINES[i - 1]))
    return [l for l in out if l is not None]


def retext(line, old, new, size=None):
    assert f">{old}<" in line, (old, line[:80])
    line = line.replace(f">{old}<", f">{new}<")
    return re.sub(r'font-size="\d+"', f'font-size="{size}"', line) if size else line


def head(view, label):
    first = LINES[0].replace('viewBox="0 0 1000 366"', f'viewBox="{view}"')
    first = first.replace(re.search(r'aria-label="[^"]*"', first).group(0), f'aria-label="{label}"')
    return [first, LINES[1], LINES[2]]


def plain_ecs(block):
    return [l.replace('font-weight="bold" fill="#0E8A6E"', 'font-weight="normal" fill="#2c3e50"') for l in block]


def save(name, body):
    svg = "\n".join(body) + "\n"
    # 同じページに iac-diff.svg が並んでも id がぶつからないよう、元の図のアイコンの id に接頭辞を付ける
    svg = re.sub(r'(id="|url\(#)([a-z]+\d+-)', rf"\1{name}-\2", svg)
    with open(os.path.join(IMAGES, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print(name)


# 1. あるべき姿を強調した IaC のデプロイの仕組み
ideal = list(LINES[:-1]) if LINES[-1] == "" else list(LINES)
ideal[3] = ideal[3].replace('stroke="#c9d0d9" stroke-width="2"', f'stroke="{GREEN}" stroke-width="3"')
ideal[7] = ideal[7].replace('fill="#2c3e50"', f'fill="{GREEN}"')
save("iac-diff-ideal", [l for l in ideal if l != ""])

# 2. CloudFormation とは？（テンプレート → CloudFormation → スタック）
code = plain_ecs(lines(4, 32, drop={31}, swap={
    5: icon(TEMPLATE, 32, 30, 28), 6: None, 7: None,
    8: retext(LINES[7], "コード（あるべき姿）", "CloudFormationテンプレート", 14),
}))
tool = lines(57, 60, swap={57: icon(CFN, 376, 146, 64), 58: None, 59: None,
                           60: retext(LINES[59], "IaCのツール", "CloudFormation")})
stack = plain_ecs(lines(77, 106, drop={105}, swap={
    78: icon(STACK, 744, 111, 28), 79: None, 80: None, 81: None,
    82: retext(LINES[81], "実リソース", "スタック"),
}))
save("cfn-define", head("0 0 1000 196", "CloudFormationテンプレートであるべき姿を定義し、CloudFormationがそれを読んでスタックとしてリソースをプロビジョニングする") + [
    *code,
    text(145, 186, "あるべき姿のコード", 14, SUB),
    arrow(272, 370, 90),
    text(321, 78, "読み込む", 14),
    '<g transform="translate(0,-88)">', *tool, "</g>",
    arrow(446, 738, 90),
    text(592, 78, "プロビジョニングする", 15),
    '<g transform="translate(0,-90)">', *stack, "</g>",
    text(864, 186, "実リソースのまとまり", 14, SUB),
    "</svg>",
])

# 3. CloudFormation のデプロイ（テンプレートとスタックの状態を比べ、変更セットを反映する）
save("cfn-deploy", head("0 0 1000 366", "CloudFormationが新しいテンプレートとスタックの現在の状態を比較し、差分の変更セットをスタックの実リソースへ反映する") + lines(4, 106, swap={
    5: icon(TEMPLATE, 32, 30, 28), 6: None, 7: None,
    8: retext(LINES[7], "コード（あるべき姿）", "テンプレート（あるべき姿）", 14),
    34: icon(STACK, 32, 220, 28), 35: None, 36: None, 37: None,
    38: retext(LINES[37], "現在の状態", "スタック（現在の状態）"),
    57: icon(CFN, 376, 146, 64), 58: None, 59: None,
    60: retext(LINES[59], "IaCのツール", "CloudFormation"),
    66: retext(LINES[65], "差分", "変更セット", 18),
    76: retext(LINES[75], "デプロイ", "反映する", 12),
    78: icon(STACK, 744, 111, 28), 79: None, 80: None, 81: None,
    82: retext(LINES[81], "実リソース", "スタック（実リソース）"),
}) + ["</svg>"])
