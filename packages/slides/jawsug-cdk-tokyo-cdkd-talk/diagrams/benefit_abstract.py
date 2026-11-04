"""恩恵 ① の図（benefit-abstract.svg）。CDK の 1 行が、CloudFormation テンプレートの IAM ポリシーになることを見せる。

初心者支部で登壇したスライドの feature-structure.svg（コードの箱）と同じ形にする。

  AWS_ICONS=<アイコン置き場> python3 diagrams/benefit_abstract.py
"""
import os
import re

ICONS = os.environ["AWS_ICONS"].rstrip("/") + "/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "images", "benefit-abstract.svg")
INK, LINE, GREEN = "#2c3e50", "#c9d0d9", "#0E8A6E"
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


def box(x, y, w, h, icon_name, title):
    return [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
            icon(icon_name, x + 14, y + 12, 36), text(x + 60, y + 38, title, 18, weight="bold")]


YAML = ["Effect: Allow", "Action:", "  - s3:GetObject*", "  - s3:GetBucket*", "  - s3:List*",
        "Resource:", "  - !GetAtt MyBucket.Arn", '  - !Sub "${MyBucket.Arn}/*"']

body = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 290" width="100%" role="img" '
    'aria-label="AWS CDKのコード myBucket.grantRead(myFunction) の1行が、CloudFormationテンプレートでは読み取りの権限を並べたIAMポリシーになる">',
    '<!-- AWS Architecture Icons 2026-07-31 版（Icon-package_07312026） -->',
    f'<defs><marker id="ba-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>',
    # コードは p22 と同じ暗い背景にし、下にこのコードで作られる AWS リソースを並べる（2026-11-04 本人）
    icon("Res_Source-Code_48_Light.svg", 14, 40, 32), text(54, 64, "コード（AWS CDK）", 18, weight="bold"),
    '<rect x="10" y="80" width="380" height="66" rx="8" fill="#282a36" stroke="#44475a" stroke-width="1"/>',
    '<text x="28" y="120" font-family="\'Fira Code\', monospace" font-size="17">'
    '<tspan fill="#f8f8f2">myBucket.</tspan><tspan fill="#50fa7b">grantRead</tspan><tspan fill="#f8f8f2">(myFunction);</tspan></text>',
    text(14, 180, "このコードで作られるAWSリソース", 14, weight="bold"),
    text(14, 206, "・IAMポリシー（myFunction の実行ロールに付き、", 13),
    text(28, 226, "myBucket を読み取る権限を与える）", 13),
    f'<path d="M392,113 L476,113" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round" marker-end="url(#ba-a)"/>',
    text(434, 101, "合成", 14, anchor="middle"),
    *box(480, 10, 410, 270, "Res_AWS-CloudFormation_Template_48.svg", "CloudFormationテンプレート"),
    text(498, 84, "IAMポリシー（抜粋）", 14, color="#6b7684"),
    *[text(498, 112 + 22 * i, line, 15, family=MONO) for i, line in enumerate(YAML)],
    "</svg>",
]
open(OUT, "w", encoding="utf-8").write("\n".join(body) + "\n")
print(OUT)
