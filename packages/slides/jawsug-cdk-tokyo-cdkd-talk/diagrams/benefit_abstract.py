"""恩恵（特徴 ②）の図（benefit-abstract.svg）。CDK の 1 行と、それで作られる AWS リソース、テンプレートの IAM ポリシーを並べる。

初心者支部で登壇したスライドの feature-structure.svg（コードの箱）と同じ形にする。
2026-11-04 本人: 文字がぼやけて見えるので、縮めずにほぼ等倍で表示できる大きさの文字にし、作られるリソースは文ではなく図で見せる。

  AWS_ICONS=<アイコン置き場> python3 diagrams/benefit_abstract.py
"""
import os
import re

ICONS = os.environ["AWS_ICONS"].rstrip("/") + "/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "images", "benefit-abstract.svg")
INK, SUB, LINE, GREEN = "#2c3e50", "#6b7684", "#c9d0d9", "#0E8A6E"
SANS = "'Noto Sans JP', 'Hiragino Sans', sans-serif"
MONO = "'Fira Code', monospace"
_n = [0]


def icon(name, x, y, size):
    _n[0] += 1
    prefix = f"ba{_n[0]}-"
    s = open(ICONS + name).read()
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})")
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{body.strip()}</svg>'


def text(x, y, s, size, color=INK, weight="normal", family=SANS, anchor="start"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(" ", "&#160;")
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}">{s}</text>')


def arrow(x1, x2, y, color=INK):
    return (f'<path d="M{x1},{y} L{x2},{y}" fill="none" stroke="{color}" stroke-width="2.5" '
            f'stroke-linejoin="round" marker-end="url(#ba-{"g" if color == GREEN else "a"})"/>')


def node(name, cx, y, label, sub, color=INK):
    return [icon(name, cx - 24, y, 48), text(cx, y + 70, label, 15, color, "bold", anchor="middle"),
            text(cx, y + 90, sub, 13, SUB, family=MONO, anchor="middle")]


YAML = ["Effect: Allow", "Action:", "  - s3:GetObject*", "  - s3:GetBucket*", "  - s3:List*",
        "Resource:", "  - !GetAtt MyBucket.Arn", '  - !Sub "${MyBucket.Arn}/*"']

body = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 330" width="100%" role="img" '
    'aria-label="AWS CDKのコード myBucket.grantRead(myFunction) の1行で、Lambda関数の実行ロールに、S3バケットを読み取るIAMポリシーが付く。CloudFormationテンプレートでは、そのIAMポリシーが読み取りの権限を並べた形になる">',
    '<!-- AWS Architecture Icons 2026-07-31 版（Icon-package_07312026） -->',
    f'<defs><marker id="ba-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
    f'<marker id="ba-g" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker></defs>',
    # コード（p22 と同じ暗い背景）
    icon("Res_Source-Code_48_Light.svg", 6, 6, 32), text(46, 30, "コード（AWS CDK）", 18, weight="bold"),
    '<rect x="6" y="46" width="430" height="64" rx="8" fill="#282a36"/>',
    f'<text x="26" y="86" font-family="{MONO}" font-size="20">'
    '<tspan fill="#f8f8f2">myBucket.</tspan><tspan fill="#50fa7b">grantRead</tspan><tspan fill="#f8f8f2">(myFunction);</tspan></text>',
    # このコードで作られる AWS リソース
    text(6, 152, "このコードで作られるAWSリソース", 15, weight="bold"),
    *node("Arch_AWS-Lambda_64.svg", 50, 172, "Lambda関数", "myFunction"),
    arrow(80, 130, 196), text(105, 186, "使う", 12, anchor="middle"),
    *node("Res_AWS-Identity-Access-Management_Role_48.svg", 160, 172, "実行ロール", ""),
    arrow(250, 196, 196, GREEN), text(223, 186, "付く", 12, GREEN, "bold", anchor="middle"),
    *node("Res_AWS-Identity-Access-Management_Permissions_48.svg", 280, 172, "IAMポリシー", "grantRead", GREEN),
    f'<rect x="250" y="166" width="60" height="60" rx="10" fill="none" stroke="{GREEN}" stroke-width="3"/>',
    arrow(310, 368, 196, GREEN), text(339, 186, "読み取り", 12, GREEN, "bold", anchor="middle"),
    *node("Res_Amazon-Simple-Storage-Service_Bucket_48.svg", 396, 172, "S3バケット", "myBucket"),
    # 合成すると、テンプレートでは IAM ポリシーがこう書かれる
    arrow(440, 520, 78), text(480, 66, "合成", 14, anchor="middle"),
    f'<rect x="524" y="6" width="430" height="318" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    icon("Res_AWS-CloudFormation_Template_48.svg", 540, 18, 36),
    text(586, 44, "CloudFormationテンプレート", 18, weight="bold"),
    text(544, 82, "IAMポリシー（抜粋）", 15, SUB),
    *[text(544, 116 + 25 * i, line, 17, family=MONO) for i, line in enumerate(YAML)],
    "</svg>",
]
open(OUT, "w", encoding="utf-8").write("\n".join(body) + "\n")
print(OUT)
