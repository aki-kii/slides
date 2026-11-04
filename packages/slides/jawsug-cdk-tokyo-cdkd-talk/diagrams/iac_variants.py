"""iac-diff.svg をもとに、言葉とアイコンを入れ替えた図を書き出す。

- iac-diff-ideal.svg: 「コード（あるべき姿）」の枠を緑で強調する（IaCのデプロイの仕組み）
- cfn-define.svg: 「IaCとは？」の図を CloudFormation に置き換える（テンプレート → CloudFormation → スタック。説明は名前の下）
- cfn-deploy.svg: IaCの仕組みの図を CloudFormation に置き換える（テンプレートと更新前のスタックを比べ、変更セットを同じスタックに反映する）

  AWS_ICONS=<アイコン置き場> python3 diagrams/iac_variants.py

アイコンは AWS Architecture Icons 2026-07-31 版。tasks/speaking/diagram-style.md に合わせる。
"""
import os
import re

from resource_swap import swap

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
    svg = swap("\n".join(body) + "\n")
    # 同じページに iac-diff.svg が並んでも id がぶつからないよう、元の図のアイコンの id に接頭辞を付ける
    svg = re.sub(r'(id="|url\(#)([a-z]+\d+-)', rf"\1{name}-\2", svg)
    with open(os.path.join(IMAGES, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    print(name)


# 1. あるべき姿を強調した IaC のデプロイの仕組み
ideal = list(LINES[:-1]) if LINES[-1] == "" else list(LINES)
ideal[3] = ideal[3].replace('stroke="#c9d0d9" stroke-width="2"', f'stroke="{GREEN}" stroke-width="3"')
ideal[7] = ideal[7].replace('fill="#2c3e50"', f'fill="{GREEN}"')
ideal[81] = retext(ideal[81], "実リソース", "AWSアカウント")  # 2026-11-04 本人
save("iac-diff-ideal", [l for l in ideal if l != ""])

# 2. CloudFormation とは？（テンプレート → CloudFormation → スタック）
# テンプレートとスタックの説明は、それぞれの名前の下に書く（2026-11-04 本人）
code = [LINES[3].replace('height="140"', 'height="174"'), icon(TEMPLATE, 32, 30, 28),
        retext(LINES[7], "コード（あるべき姿）", "CloudFormationテンプレート", 14),
        f'<text x="66" y="68" font-family="{FONT}" font-size="12" fill="{SUB}">AWSリソースの設定を</text>',
        f'<text x="66" y="83" font-family="{FONT}" font-size="12" fill="{SUB}">YAMLやJSONで書いたファイル</text>',
        '<g transform="translate(0,32)">', *plain_ecs(lines(9, 32, drop={31})), "</g>"]
tool = lines(57, 60, swap={57: icon(CFN, 376, 146, 64), 58: None, 59: None,
                           60: retext(LINES[59], "IaCのツール", "CloudFormation")})
stack = [LINES[76].replace('height="140"', 'height="174"'), icon(STACK, 744, 111, 28),
         retext(LINES[81], "実リソース", "スタック"),
         f'<text x="778" y="148" font-family="{FONT}" font-size="12" fill="{SUB}">AWSリソースをまとめて管理し、</text>',
         f'<text x="778" y="163" font-family="{FONT}" font-size="12" fill="{SUB}">今の状態を持つ単位</text>',
         '<g transform="translate(0,32)">', *plain_ecs(lines(83, 106, drop={105})), "</g>"]
# 矢印は短く、ラベルは名詞にして、IaCとは？の図と同じ並びにする（2026-11-04 本人）
save("cfn-define", head("0 0 810 210", "CloudFormationテンプレートであるべき姿を定義し、CloudFormationがそれを読んでスタックとしてリソースをプロビジョニングする") + [
    *code,
    arrow(272, 362, 107),
    text(317, 95, "読み込み", 14),
    '<g transform="translate(-8,-71)">', *tool, "</g>",
    arrow(438, 546, 107),
    text(492, 95, "プロビジョニング", 13),
    '<g transform="translate(-192,-90)">', *stack, "</g>",
    "</svg>",
])

# 3. CloudFormation のデプロイ
# スタックは状態を持つだけ。スタックへデプロイするようには見せず、スタックから AWS リソースへの矢印でデプロイを見せる（2026-11-04 本人）
DDB = "Arch_Amazon-DynamoDB_64.svg"
RES = [("Arch_Amazon-API-Gateway_64.svg", "API Gateway"), ("Arch_AWS-Lambda_64.svg", "Lambda"), (DDB, "DynamoDB")]
LINE, CLOUD_INK = "#c9d0d9", "#232F3E"


def rtext(x, y, s, size=13, color=INK, weight="normal", anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}">{s}</text>')


def g_arrow(d):
    return (f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linejoin="round" '
            'stroke-linecap="round" marker-end="url(#a-g)"/>')


def i_arrow(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round" '
            'stroke-linecap="round" marker-end="url(#a-i)"/>')


body = [f'<rect x="20" y="50" width="250" height="140" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
        icon(TEMPLATE, 32, 60, 28), rtext(66, 80, "テンプレート（あるべき姿）", 14, weight="bold")]
for k, (f, name) in enumerate(RES):
    cx = 68 + 72 * k
    body.append(icon(f, cx - 24, 98, 48))
    hi = f == DDB
    body.append(rtext(cx, 166, name, 13, GREEN if hi else INK, "bold" if hi else "normal", "middle"))
    if hi:
        body.append(f'<rect x="{cx - 30}" y="92" width="60" height="60" rx="10" fill="none" stroke="{GREEN}" stroke-width="3"/>')
body += [
    i_arrow("M272,120 L318,120"), rtext(295, 108, "読み込み", 12, anchor="middle"),
    icon(CFN, 326, 88, 64), rtext(358, 172, "CloudFormation", 13, weight="bold", anchor="middle"),
    g_arrow("M394,120 L436,120"), rtext(415, 108, "作成", 12, anchor="middle"),
    f'<rect x="440" y="58" width="104" height="124" rx="12" fill="#e9f5f1" stroke="{GREEN}" stroke-width="3" stroke-dasharray="7 5"/>',
    rtext(492, 84, "変更セット", 16, GREEN, "bold", "middle"),
    icon(DDB, 468, 94, 48), rtext(492, 166, "DynamoDB", 13, GREEN, "bold", "middle"),
    g_arrow("M548,120 L588,120"), rtext(568, 108, "反映", 12, anchor="middle"),
    f'<rect x="592" y="62" width="104" height="116" rx="12" fill="#ffffff" stroke="{INK}" stroke-width="2"/>',
    icon(STACK, 624, 76, 40), rtext(644, 140, "スタック", 15, weight="bold", anchor="middle"),
    rtext(644, 160, "状態を持つ", 12, SUB, anchor="middle"),
    # スタックの今の状態を CloudFormation が読んで比べる
    i_arrow("M644,180 L644,224 L358,224 L358,182"), rtext(501, 216, "今の状態", 12, anchor="middle"),
    f'<rect x="748" y="20" width="232" height="208" rx="12" fill="#ffffff" stroke="{CLOUD_INK}" stroke-width="2"/>',
]
cloud = lines(78, 82, swap={82: retext(LINES[81], "実リソース", "AWSアカウント")})
body.append('<g transform="translate(6,-90)">' + "".join(cloud) + "</g>")
for k, (f, name) in enumerate(RES):
    y = 52 + 58 * k
    body.append(icon(f, 800, y, 44))
    hi = f == DDB
    body.append(rtext(854, y + 28, name, 14, GREEN if hi else INK, "bold" if hi else "normal"))
    body.append((g_arrow if hi else i_arrow)(f"M698,120 C730,120 760,{y + 22} 794,{y + 22}"))
body.append(rtext(724, 252, "スタックが AWS リソースをデプロイして管理する", 12, SUB, anchor="middle"))
save("cfn-deploy", head("0 0 1000 262", "CloudFormationがテンプレートとスタックの今の状態を比べて変更セットを作り、スタックに反映する。スタックからAPI Gateway、Lambda、DynamoDBがデプロイされる") + body + ["</svg>"])
