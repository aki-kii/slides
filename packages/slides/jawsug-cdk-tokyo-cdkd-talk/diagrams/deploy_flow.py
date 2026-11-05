"""デプロイフロー図を SVG で組む。全体の図と、一部を強調した図を images/ に書き出す。
CDK の図の deploy は、その前のページ（cfn-deploy.svg、diagrams/iac_variants.py）で説明するので CloudFormation のアイコンだけにする。
CDK Bootstrap は図に出さない。アセットの中も強調しない（2026-11-03 本人）。
フェーズごとのページは作らず、各フェーズの枠の下に短い補足を付ける（2026-11-03 本人、round 6）。

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
    "docker": os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker.svg"),
    "cfn": "Arch_AWS-CloudFormation_64.svg",
    "template": "Res_AWS-CloudFormation_Template_48.svg",
    "changeset": "Res_AWS-CloudFormation_Change-Set_48.svg",
    "stack": "Res_AWS-CloudFormation_Stack_48.svg",
}
_n = [0]


def icon(name, cx, y, size):
    _n[0] += 1
    prefix = f"i{_n[0]}-"
    s = open(os.path.join(S, ICON[name])).read()
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


TOP, BOTTOM = 56, 414
DY = 46  # 各フェーズの名前の下に補足の行を置くぶん、中身を下げる
SEC = {k: [] for k in ("outer", "bootstrap", "synth_frame", "source", "group", "publish", "trunk", "deploy", "gap")}

# cdk deploy が synth、publish、deploy の全体を動かす
p = SEC["outer"]
p.append(f'<rect x="167" y="18" width="820" height="406" rx="14" fill="#f5f7f9" stroke="{LINE}" stroke-width="2"/>')
p.append(text(183, 43, "cdk deploy", 16, INK, 700, "start", MONO))

# CDK Bootstrap: 図の上に横並びで置く。今回の流れで使うものだけ並べ、ほかは etc… にする
p = SEC["bootstrap"]
p.append(group(10, 12, 920, 82, "CDK Bootstrap"))
p.append(f'<rect x="132" y="20" width="84" height="22" rx="11" fill="{GREEN}"/>')
p.append(text(174, 35, "初回のみ作成", 11, "#ffffff", 700))
items = [
    (26, "s3", ["S3バケット"]),
    (150, "ecr", ["ECRリポジトリ"]),
    (294, "role", ["ファイル用", "パブリッシュロール"]),
    (446, "role", ["イメージ用", "パブリッシュロール"]),
    (598, "role", ["デプロイ用", "ロール"]),
    (706, "role", ["CloudFormation", "実行ロール"]),
]
for x, name, lines in items:
    p.append(icon(name, x + 12, 56, 24))
    first = 72 - 7 * (len(lines) - 1)
    for k, line in enumerate(lines):
        p.append(text(x + 30, first + 14 * k, line, 11, INK, 700, "start"))
p.append(text(870, 72, "etc…", 12, SUB, None, "start"))

# synth: ソースコード → 合成 → アセットを横に並べる
MID = 210 + DY
p = SEC["synth_frame"]
p.append(step(175, 350, "synth"))
p.append(text(191, TOP + 50, "ソースコードからアセットを合成する", 12, SUB, None, "start"))
p = SEC["source"]
p.append(node("code", 235, MID - 22, 44, "ソースコード"))
p += [arrow(f"M261,{MID} H335"), text(298, MID - 10, "合成", 12)]
p = SEC["group"]
p.append(group(335, 66 + DY, 178, 278, "アセット"))
# S3 へ上げるものは 1 つの枠にまとめ、出ていく矢印も 1 本にする（2026-11-04 本人）
FILES_Y, FILES_H = 140, 148
p.append(f'<rect x="348" y="{FILES_Y}" width="152" height="{FILES_H}" rx="10" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
for name, y, labels in (("template", FILES_Y + 10, ["CloudFormation", "テンプレート"]),
                         ("code", FILES_Y + 52, ["Lambdaの", "ソースコード"]),
                         ("asset", FILES_Y + 92, ["S3に配信する", "静的ファイル"])):
    p.append(icon(name, 368, y, 26))
    first = y + 13 + 4 - 7 * (len(labels) - 1)
    for i, label in enumerate(labels):
        p.append(text(386, first + 14 * i, label, 12, INK, 700, "start"))
p.append(text(386, FILES_Y + FILES_H - 14, "など…", 12, SUB, None, "start"))
p.append(file_box(348, 254 + DY, 152, 64, "docker", ["Dockerfile"], sub=["LambdaやECSで使う", "コンテナイメージ"], icon_size=28))

# publish: テンプレートとファイルはまとめて S3 へ、コンテナイメージだけ ECR へ。どちらもまっすぐ進む
S3Y, ECRY = 134 + DY, 286 + DY
p = SEC["publish"]
p.append(step(539, 226, "publish"))
p.append(text(555, TOP + 50, "アセットをAWSにアップロードする", 12, SUB, None, "start"))
p += [icon("s3", 705, S3Y - 20, 40), text(705, S3Y - 28, "S3バケット", 13, INK, 700)]
p += [icon("ecr", 705, ECRY - 20, 40), text(700, ECRY - 28, "ECRリポジトリ", 13, INK, 700)]


def bootstrap_tag(cx, y):
    """cdk bootstrap で作られるものに付ける札（2026-11-03 本人）。"""
    return (f'<rect x="{cx - 35}" y="{y}" width="70" height="18" rx="9" fill="{GREEN}"/>'
            + text(cx, y + 13, "bootstrap", 11, "#ffffff", 700, "middle", MONO))


p += [bootstrap_tag(705, S3Y - 64), bootstrap_tag(700, ECRY - 64)]
p = SEC["trunk"]
p += [arrow(f"M500,{S3Y} H685"), text(612, S3Y - 10, "アップロード")]  # まっすぐ S3 へ（2026-11-04 本人）
p.append(role_chip(556, S3Y + 12, ["ファイル用", "パブリッシュロール"]))
p.append(bootstrap_tag(615, S3Y + 46))  # ロールも bootstrap で作られる（2026-11-04 本人）
p += [arrow(f"M500,{ECRY} H685"), text(612, ECRY - 10, "ビルド＆アップロード")]
p.append(role_chip(556, ECRY + 12, ["イメージ用", "パブリッシュロール"]))
p.append(bootstrap_tag(615, ECRY + 46))

# publish → deploy: アップロードしたアセットを deploy で使う
p = SEC["gap"]
p.append(f'<path d="M725,{ECRY} H752 V{S3Y}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p.append(arrow(f"M725,{S3Y} H844"))

# deploy: CloudFormation のデプロイは前のページで説明するので、CloudFormation のアイコンだけで表す（2026-11-03 本人）
DMID = 186
p = SEC["deploy"]
p.append(step(779, 200, "deploy"))
p.append(text(795, TOP + 50, "AWSリソースをデプロイする", 12, SUB, None, "start"))
p.append(icon("cfn", 880, S3Y - 32, 64))
# CloudFormation を通じてデプロイすることを出す（2026-11-04 本人）
p.append(text(880, S3Y + 52, "CloudFormation", 13, INK, 700))
# deploy で使う2つのロール。CDK CLI がデプロイ用ロールで CloudFormation を呼び、CloudFormation が実行ロールでリソースを作る（2026-11-05 本人）
p.append(role_chip(822, S3Y + 74, ["デプロイ用ロール"]))
p.append(bootstrap_tag(880, S3Y + 98))
p.append(role_chip(822, S3Y + 132, ["CloudFormation", "実行ロール"]))
p.append(bootstrap_tag(880, S3Y + 170))


defs = (f'<defs><marker id="mInk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
        f'<marker id="mGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker></defs>')
DIM = 0.14


# Bootstrap を上に置いたぶん、cdk deploy の枠全体をずらす
MOVE = 'transform="translate(-157,88)"'


def write(name, focus=None):
    """focus を渡すと、そのフェーズに寄った図にする。どの図も cdk deploy の枠だけを切り出す。"""
    body = []
    for key, parts in SEC.items():
        if key == "bootstrap":
            continue
        opacity = "" if focus is None or key in focus else f' opacity="{DIM}"'
        move = "" if key == "bootstrap" else f" {MOVE}"
        body.append(f"<g{opacity}{move}>" + "".join(parts) + "</g>")
    box = "0 96 840 426"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" width="100%" '
           f"font-family=\"'Noto Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', sans-serif\">\n{defs}\n" + "\n".join(body) + "\n</svg>\n")
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)


write("deploy-flow")

