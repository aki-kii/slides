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
    "cfn": "Arch_AWS-CloudFormation_64.svg",
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


def green_arrow(d):
    return f'<path d="{d}" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linejoin="round" marker-end="url(#mGreen)"/>'


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


TOP, BOTTOM = 56, 348
SEC = {k: [] for k in ("outer", "bootstrap", "link", "synth_frame", "source", "group", "publish", "trunk", "deploy", "gap")}

# cdk deploy が synth、publish、deploy の全体を動かす
p = SEC["outer"]
p.append(f'<rect x="165" y="18" width="1003" height="340" rx="14" fill="#f5f7f9" stroke="{LINE}" stroke-width="2"/>')
p.append(text(181, 43, "cdk deploy", 16, INK, 700, "start", MONO))
p.append(text(285, 43, "全体を順に動かす", 12, SUB, None, "start"))

# CDK Bootstrap: 今回の流れで使うものだけ並べ、ほかは 1 か所にまとめる
p = SEC["bootstrap"]
p.append(group(10, 18, 125, 340, "CDK Bootstrap"))
items = [
    ("s3", ["S3バケット"]),
    ("ecr", ["ECRリポジトリ"]),
    ("role", ["ファイル用", "パブリッシュ", "ロール"]),
    ("role", ["イメージ用", "パブリッシュ", "ロール"]),
    ("role", ["デプロイ用", "ロール"]),
    ("role", ["CloudFormation", "実行ロール"]),
]
y = 52
for name, lines in items:
    height = 14 * len(lines) + 12
    p.append(icon(name, 27, y + (height - 22) / 2, 22))
    first = y + height / 2 + 4 - 7 * (len(lines) - 1)
    for k, line in enumerate(lines):
        p.append(text(42, first + 14 * k, line, 11, INK, 700, "start"))
    y += height + 5
p += [text(72, 326, "ルックアップ用ロール、", 10), text(72, 341, "SSMパラメータ など", 10)]

# bootstrap → cdk deploy の枠
p = SEC["link"]
p += [arrow("M135,188 H165"), text(150, 164, "先に"), text(150, 180, "作る")]

# synth: ソースコード → 合成 → アセットを横に並べる
MID = 204
p = SEC["synth_frame"]
p.append(step(173, 316, "synth"))
p = SEC["source"]
p.append(node("code", 222, MID - 22, 44, "ソースコード"))
p += [arrow(f"M246,{MID} H305"), text(274, MID - 38, "合成して", 11), text(274, MID - 23, "アセットを", 11), text(274, MID - 8, "作る", 11)]
p = SEC["group"]
p.append(group(305, 64, 174, 254, "アセット"))
p.append(file_box(317, 100, 150, 64, "template", ["CloudFormation", "テンプレート"], strong=True, icon_size=28))
p.append(file_box(317, 172, 150, 64, "asset", ["ファイル"], sub=["Lambdaのコード、", "画像など"], icon_size=28))
p.append(file_box(317, 244, 150, 64, "image", ["コンテナイメージ"], sub=["Dockerfileなど"], icon_size=28))

# publish: テンプレートとファイルはまとめて S3 へ、コンテナイメージだけ ECR へ。どちらもまっすぐ進む
S3Y, ECRY = 132, 276
p = SEC["publish"]
p.append(step(499, 206, "publish"))
p += [icon("s3", 655, S3Y - 20, 40), text(655, S3Y - 26, "S3バケット", 13, INK, 700)]
p += [icon("ecr", 655, ECRY - 20, 40), text(650, ECRY - 26, "ECRリポジトリ", 13, INK, 700)]
p = SEC["trunk"]
p.append(f'<path d="M467,204 H482 V{S3Y}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p += [arrow(f"M467,{S3Y} H635"), text(562, S3Y - 8, "パブリッシュ")]
p.append(role_chip(506, S3Y + 8, ["ファイル用", "パブリッシュロール"]))
p += [arrow(f"M467,{ECRY} H635"), text(562, ECRY - 8, "ビルドしてpush")]
p.append(role_chip(506, ECRY + 8, ["イメージ用", "パブリッシュロール"]))

# publish → deploy: アップロードしたアセットを deploy で使う
p = SEC["gap"]
p.append(f'<path d="M675,{ECRY} H702 V{S3Y}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p.append(arrow(f"M675,{S3Y} H727"))

# deploy: IaC の図（iac-diff）と同じ形にする。あるべき姿と現在の状態を比べ、差分を反映する
DMID = 182
p = SEC["deploy"]
p.append(step(715, 445, "deploy"))
p.append(text(808, 84, "アップロードしたアセットを使う", 12, SUB, None, "start"))


def state_box(y, name, lines, fill):
    out = [f'<rect x="727" y="{y}" width="110" height="62" rx="10" fill="{fill}" stroke="{LINE}" stroke-width="2"/>',
           icon(name, 747, y + 15, 32)]
    for i, line in enumerate(lines):
        bold = i < len(lines) - 1
        out.append(text(767, y + 62 / 2 + 4 - 7 * (len(lines) - 1) + 14 * i, line, 11 if bold else 10, INK if bold else SUB, 700 if bold else None, "start"))
    return "".join(out)


p.append(state_box(101, "template", ["新しい", "テンプレート", "（あるべき姿）"], "#ffffff"))
p.append(state_box(201, "stack", ["スタックの", "状態", "（現在の状態）"], "#f5f7f9"))
p.append(text(846, DMID + 4, "比較", 11, anchor="end"))
p.append(arrow(f"M837,132 H852 V{DMID - 8} H876"))
p.append(arrow(f"M837,232 H852 V{DMID + 8} H876"))
p.append(icon("cfn", 895, DMID - 18, 36))
p.append(text(895, DMID + 32, "CloudFormation", 11, INK, 700))
p.append(role_chip(858, DMID + 42, ["デプロイ用", "ロール"]))
p.append(green_arrow(f"M915,{DMID} H945"))
p.append(f'<rect x="945" y="{DMID - 42}" width="62" height="84" rx="10" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 4"/>')
p.append(text(976, DMID - 25, "差分", 12, GREEN, 700))
p.append(icon("changeset", 976, DMID - 18, 34))
p.append(text(976, DMID + 32, "変更セット", 11, GREEN, 700))
p.append(green_arrow(f"M1007,{DMID} H1087"))
p += [text(1047, DMID - 24, "確認して", 11), text(1047, DMID - 9, "反映する", 11)]
p.append(icon("role", 1047, DMID + 8, 18))
p += [text(1047, DMID + 39, "CloudFormation", 10), text(1047, DMID + 52, "実行ロール", 10)]
p.append(f'<rect x="1087" y="{DMID - 42}" width="65" height="84" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
p.append(icon("stack", 1119.5, DMID - 30, 34))
p.append(text(1119.5, DMID + 19, "スタック", 11, INK, 700))
p.append(text(1119.5, DMID + 33, "実リソース", 10, SUB))

defs = (f'<defs><marker id="mInk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
        f'<marker id="mGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker></defs>')
DIM = 0.14


def write(name, focus=None):
    body = []
    for key, parts in SEC.items():
        opacity = "" if focus is None or key in focus else f' opacity="{DIM}"'
        body.append(f"<g{opacity}>" + "".join(parts) + "</g>")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1176 376" width="100%" '
           f"font-family=\"'Noto Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', sans-serif\">\n{defs}\n" + "\n".join(body) + "\n</svg>\n")
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)


write("deploy-flow")
write("deploy-flow-bootstrap", {"bootstrap"})
write("deploy-flow-synth", {"outer", "synth_frame", "source", "group"})
write("deploy-flow-assets", {"outer", "group"})
write("deploy-flow-publish", {"outer", "group", "trunk", "publish"})
write("deploy-flow-deploy", {"outer", "gap", "deploy"})
