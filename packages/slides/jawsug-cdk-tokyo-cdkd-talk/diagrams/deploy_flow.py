"""デプロイフロー図を SVG で組む。全体の図と、一部を強調した図を images/ に書き出す。

  AWS_ICONS=<アイコン置き場> python3 diagrams/deploy_flow.py

アイコンは AWS Architecture Icons 2026-07-31 版。tasks/speaking/diagram-style.md に合わせる。
"""
import os
import re

S = os.environ["AWS_ICONS"].rstrip("/") + "/"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "images")

INK, SUB, LINE = "#2c3e50", "#6b7684", "#c9d0d9"
GREEN, GREEN_BG = "#0E8A6E", "#e9f5f1"
RED, RED_BG = "#DD344C", "#fdecee"
MONO = "'Fira Code', monospace"

ICON = {
    "code": "Res_Source-Code_48_Light.svg",
    "asset": "Res_Document_48_Light.svg",
    "s3": "Res_Amazon-Simple-Storage-Service_Bucket_48.svg",
    "ecr": "Res_Amazon-Elastic-Container-Registry_Registry_48.svg",
    "role": "Res_AWS-Identity-Access-Management_Role_48.svg",
    "image": "Res_Amazon-Elastic-Container-Registry_Image_48.svg",
    "template": "Res_AWS-CloudFormation_Template_48.svg",
    "changeset": "Res_AWS-CloudFormation_Change-Set_48.svg",
    "stack": "Res_AWS-CloudFormation_Stack_48.svg",
}
_n = [0]


def icon(name, cx, y, size):
    _n[0] += 1
    prefix = f"i{_n[0]}-"
    s = open(S + ICON[name]).read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    body = re.sub(r'<title>.*?</title>', '', body, flags=re.S)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f'url(#{i})', f'url(#{prefix}{i})')
    return f'<svg x="{cx - size / 2}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{body.strip()}</svg>'


def text(x, y, s, size=12, color=SUB, weight=None, anchor="middle", family=None):
    w = f' font-weight="{weight}"' if weight else ""
    f = f' font-family="{family}"' if family else ""
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"{w}{f} fill="{color}">{s}</text>'


def node(name, cx, y, size, *labels, label_size=13):
    out = [icon(name, cx, y, size)]
    for i, label in enumerate(labels):
        out.append(text(cx, y + size + 18 + 16 * i, label, label_size, INK, 700))
    return "".join(out)


def arrow(d):
    return f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round" marker-end="url(#mInk)"/>'


def step(x, w, title, ja=None):
    out = [f'<rect x="{x}" y="{TOP}" width="{w}" height="{BOTTOM - TOP}" rx="14" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
           text(x + 16, TOP + 28, title, 17, INK, 700, "start", MONO)]
    if ja:
        out.append(text(x + 16 + len(title) * 10.5 + 2, TOP + 28, ja, 14, INK, 700, "start"))
    return "".join(out)


def group(x, y, w, h, title):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>'
            + text(x + 12, y + 23, title, 14, GREEN, 700, "start"))


def role_chip(x, y, lines):
    """流れの矢印の横に添える、その操作に使うロール。"""
    out = [icon("role", x + 10, y + (15 * len(lines) - 20) / 2, 20)]
    for i, line in enumerate(lines):
        out.append(text(x + 24, y + 11 + 15 * i, line, 11, SUB, None, "start"))
    return "".join(out)


def file_box(x, y, w, h, name, lines, strong=False, icon_size=30, sub=()):
    line, fill, color = (RED, RED_BG, RED) if strong else (LINE, "#ffffff", INK)
    pad = 8 + icon_size
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{line}" stroke-width="2"/>',
           icon(name, x + 6 + icon_size / 2, y + (h - icon_size) / 2, icon_size)]
    first = y + h / 2 + 4 - 7.5 * (len(lines) + len(sub) - 1)
    for i, s in enumerate(lines):
        out.append(text(x + pad + 2, first + 15 * i, s, 12, color, 700, "start"))
    for i, s in enumerate(sub):
        out.append(text(x + pad + 2, first + 15 * (len(lines) + i), s, 11, SUB, None, "start"))
    return "".join(out)


TOP, BOTTOM = 20, 412
SEC = {k: [] for k in ("bootstrap", "link", "synth_frame", "source", "group", "publish", "trunk", "gap", "deploy")}
p = SEC["bootstrap"]

# CDK Bootstrap: 今回の流れで使うものだけ並べ、ほかは 1 か所にまとめる
p.append(group(15, TOP, 150, BOTTOM - TOP, "CDK Bootstrap"))
items = [
    ("s3", ["S3バケット"]),
    ("ecr", ["ECRリポジトリ"]),
    ("role", ["ファイル用", "パブリッシュロール"]),
    ("role", ["イメージ用", "パブリッシュロール"]),
    ("role", ["デプロイ用ロール"]),
    ("role", ["CloudFormation", "実行ロール"]),
]
for i, (name, lines) in enumerate(items):
    y = 58 + i * 47
    p.append(icon(name, 39, y + 4, 26))
    first = y + 21 - 7.5 * (len(lines) - 1)
    for k, line in enumerate(lines):
        p.append(text(57, first + 15 * k, line, 11, INK, 700, "start"))
p += [text(90, 366, "ルックアップ用ロール、", 11), text(90, 382, "SSMパラメータ など", 11)]

# bootstrap → synth
p = SEC["link"]
p += [arrow("M165,110 H205"), text(185, 80, "先に"), text(185, 96, "作る")]

# synth
p = SEC["synth_frame"]
p.append(step(205, 180, "synth"))
p = SEC["source"]
p.append(node("code", 270, 56, 40, "ソースコード"))
p += [arrow("M270,118 V158"), text(278, 135, "合成して", anchor="start"), text(278, 151, "アセットを作る", anchor="start")]
p = SEC["group"]
p.append(group(212, 158, 166, 240, "アセット"))
p.append(file_box(220, 194, 150, 60, "template", ["CloudFormation", "テンプレート"], strong=True, icon_size=28))
p.append(file_box(220, 262, 150, 60, "asset", ["ファイル"], sub=["Lambdaのコード、", "画像など"], icon_size=28))
p.append(file_box(220, 330, 150, 60, "image", ["コンテナイメージ"], sub=["Dockerfileなど"], icon_size=28))

# publish: テンプレートとファイルはまとめて S3 へ、コンテナイメージだけ ECR へ。どちらもまっすぐ進む
S3Y, ECRY = 258, 360
p = SEC["publish"]
p.append(step(410, 235, "publish"))
p.append(node("s3", 597, S3Y - 20, 40, "S3バケット"))
p.append(node("ecr", 597, ECRY - 20, 40, "ECRリポジトリ"))
p = SEC["trunk"]
p.append(f'<path d="M370,224 H392 V292 H370" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p += [arrow(f"M392,{S3Y} H577"), text(495, S3Y - 8, "パブリッシュ")]
p.append(role_chip(418, S3Y + 8, ["ファイル用", "パブリッシュロール"]))
p += [arrow(f"M370,{ECRY} H577"), text(495, ECRY - 8, "ビルドしてpush")]
p.append(role_chip(418, ECRY + 8, ["イメージ用", "パブリッシュロール"]))

# publish → deploy
DMID = 135
p = SEC["gap"]
p.append(arrow(f"M645,{DMID} H665"))

# deploy
p = SEC["deploy"]
p.append(step(665, 320, "deploy"))
p.append(node("template", 712, DMID - 50 - 22, 44, "新しい", "テンプレート"))
p.append(node("stack", 712, DMID + 50 - 22, 44, "スタックの", "状態"))
p.append(node("changeset", 925, DMID - 22, 44, "変更セット"))
p.append(node("stack", 925, 304, 44, "スタック"))
p.append(f'<path d="M734,{DMID - 50} H752 V{DMID + 50} H734" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p += [arrow(f"M752,{DMID} H901")]
p += [text(826, DMID - 44, "CloudFormationが"), text(826, DMID - 28, "比べて"), text(826, DMID - 12, "変更セットを作る")]
p.append(role_chip(772, DMID + 8, ["デプロイ用ロール"]))
p += [arrow("M925,196 V304"), text(935, 240, "確認して", anchor="start"), text(935, 256, "反映する", anchor="start")]
p.append(role_chip(812, 236, ["CloudFormation", "実行ロール"]))

defs = (f'<defs><marker id="mInk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>')
DIM = 0.14


def write(name, focus=None):
    body = []
    for key, parts in SEC.items():
        opacity = "" if focus is None or key in focus else f' opacity="{DIM}"'
        body.append(f"<g{opacity}>" + "".join(parts) + "</g>")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 432" width="100%" '
           f"font-family=\"'Noto Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', sans-serif\">\n{defs}\n" + "\n".join(body) + "\n</svg>\n")
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)


write("deploy-flow")
write("deploy-flow-bootstrap", {"bootstrap"})
write("deploy-flow-synth", {"synth_frame", "source", "group"})
write("deploy-flow-assets", {"group"})
write("deploy-flow-publish", {"group", "trunk", "publish"})
write("deploy-flow-deploy", {"gap", "deploy"})
