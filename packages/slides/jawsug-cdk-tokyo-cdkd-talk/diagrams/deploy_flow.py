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
            + text(x + w / 2, y + 23, title, 14, GREEN, 700))


def role_line(d):
    return f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="2" stroke-linejoin="round" marker-end="url(#mRole)"/>'


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


TOP, BOTTOM = 20, 460
SEC = {k: [] for k in ("bootstrap", "link", "synth_frame", "source", "group", "publish", "trunk", "gap", "deploy", "legend")}
p = SEC["bootstrap"]

# CDK Bootstrap: 今回の流れで使うものだけ並べ、ほかは 1 か所にまとめる
p.append(group(15, TOP, 174, BOTTOM - TOP, "CDK Bootstrap"))
items = [
    ("s3", ["S3バケット"]),
    ("ecr", ["ECRリポジトリ"]),
    ("role", ["ファイル用", "パブリッシュロール"]),
    ("role", ["イメージ用", "パブリッシュロール"]),
    ("role", ["デプロイ用ロール"]),
    ("role", ["CloudFormation", "実行ロール"]),
]
for i, (name, lines) in enumerate(items):
    p.append(file_box(25, 56 + i * 54, 154, 46, name, lines, icon_size=26))
p += [text(102, 396 + 28, "ルックアップ用ロール、", 12), text(102, 396 + 44, "SSMパラメータ など", 12)]

# bootstrap → synth
p = SEC["link"]
p += [arrow("M189,110 H250"), text(219, 86, "先に"), text(219, 102, "作る")]

# synth
p = SEC["synth_frame"]
p.append(step(250, 200, "synth"))
p = SEC["source"]
p.append(node("code", 350, 58, 44, "ソースコード"))
p += [arrow("M350,126 V170"), text(358, 145, "合成して", anchor="start"), text(358, 161, "アセットを作る", anchor="start")]
GX = 263
p = SEC["group"]
p.append(group(GX, 170, 174, 276, "アセット"))
p.append(file_box(GX + 12, 206, 150, 70, "template", ["CloudFormation", "テンプレート"], strong=True))
p.append(file_box(GX + 12, 286, 150, 70, "asset", ["ファイル"], sub=["Lambdaのコード、", "画像など"]))
p.append(file_box(GX + 12, 366, 150, 70, "image", ["コンテナイメージ"], sub=["Dockerfileなど"]))

# publish
S3Y, ECRY = 82, 262
RIGHT = GX + 12 + 150
p = SEC["publish"]
p.append(step(545, 130, "publish"))
p.append(node("s3", 610, S3Y - 20, 40, "S3バケット"))
p.append(node("role", 610, S3Y + 53, 30, "ファイル用", "パブリッシュロール", label_size=12))
p.append(role_line(f"M594,{S3Y + 68} H556 V{S3Y + 3}"))
p.append(node("ecr", 610, ECRY - 20, 40, "ECRリポジトリ"))
p.append(node("role", 610, ECRY + 53, 30, "イメージ用", "パブリッシュロール", label_size=12))
p.append(role_line(f"M594,{ECRY + 68} H556 V{ECRY + 3}"))
p = SEC["trunk"]
# テンプレートとファイルはまとめて S3 へ、コンテナイメージだけ ECR へ
p.append(f'<path d="M{RIGHT},241 H457" fill="none" stroke="{INK}" stroke-width="2.5"/>')
p += [arrow(f"M{RIGHT},321 H457 V{S3Y} H590"), text(499, S3Y - 8, "パブリッシュ")]
p += [arrow(f"M{RIGHT},401 H470 V{ECRY} H590"), text(508, ECRY - 24, "ビルドして"), text(508, ECRY - 8, "push")]

# publish → deploy
DMID = 140
p = SEC["gap"]
p.append(arrow(f"M675,{DMID} H695"))

# deploy
p = SEC["deploy"]
p.append(step(695, 290, "deploy"))
p.append(node("template", 738, DMID - 50 - 24, 48, "新しい", "テンプレート"))
p.append(node("stack", 738, DMID + 50 - 24, 48, "スタックの", "状態"))
p.append(node("changeset", 912, DMID - 24, 48, "変更セット"))
p.append(node("stack", 912, 330, 48, "スタック"))
p.append(f'<path d="M762,{DMID - 50} H780 V{DMID + 50} H762" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p += [arrow(f"M780,{DMID} H888")]
p += [text(836, DMID - 44, "CloudFormationが"), text(836, DMID - 28, "比べて"), text(836, DMID - 12, "変更セットを作る")]
p += [arrow("M912,204 V330"), text(922, 240, "確認して", anchor="start"), text(922, 256, "反映する", anchor="start")]
p.append(node("role", 836, 196, 32, "デプロイ用", "ロール"))
p.append(role_line(f"M836,198 V{DMID + 3}"))
p.append(node("role", 790, 294, 32, "CloudFormation", "実行ロール"))
p.append(role_line("M808,310 H909"))

# 凡例
p = SEC["legend"]
p.append(role_line("M712,437 H752"))
p.append(text(760, 442, "その操作に使うロール", 12, anchor="start"))

defs = (f'<defs><marker id="mInk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
        f'<marker id="mRole" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{RED}"/></marker></defs>')
DIM = 0.14


def write(name, focus=None):
    body = []
    for key, parts in SEC.items():
        opacity = "" if focus is None or key in focus else f' opacity="{DIM}"'
        body.append(f"<g{opacity}>" + "".join(parts) + "</g>")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 480" width="100%" '
           f"font-family=\"'Noto Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', sans-serif\">\n{defs}\n" + "\n".join(body) + "\n</svg>\n")
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)


write("deploy-flow")
write("deploy-flow-bootstrap", {"bootstrap", "legend"})
write("deploy-flow-synth", {"synth_frame", "source", "group", "legend"})
write("deploy-flow-assets", {"group", "legend"})
write("deploy-flow-publish", {"group", "trunk", "publish", "legend"})
write("deploy-flow-deploy", {"gap", "deploy", "legend"})
