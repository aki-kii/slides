"""デプロイフロー図を SVG で組む。全体の図と、一部を強調した図を images/ に書き出す。
CloudFormation のデプロイの図（cfn-deploy.svg）も書き出す。CDK の図の deploy は、その前のページで説明するので CloudFormation のアイコンだけにする。

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


TOP, BOTTOM = 56, 356
SEC = {k: [] for k in ("outer", "bootstrap", "synth_frame", "source", "group", "publish", "trunk", "deploy", "gap")}
CFN = []  # CloudFormation のデプロイの図。cdk deploy の図には入れない

# cdk deploy が synth、publish、deploy の全体を動かす
p = SEC["outer"]
p.append(f'<rect x="167" y="18" width="920" height="350" rx="14" fill="#f5f7f9" stroke="{LINE}" stroke-width="2"/>')
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
MID = 210
p = SEC["synth_frame"]
p.append(step(175, 350, "synth"))
p = SEC["source"]
p.append(node("code", 235, MID - 22, 44, "ソースコード"))
p += [arrow(f"M261,{MID} H335"), text(298, MID - 10, "合成", 12)]
p = SEC["group"]
p.append(group(335, 66, 178, 278, "アセット"))
p.append(file_box(348, 102, 152, 64, "template", ["CloudFormation", "テンプレート"], strong=True, icon_size=28))
p.append(file_box(348, 178, 152, 64, "asset", ["ファイルアセット"], sub=["Lambdaのコード、", "画像など"], icon_size=28))
p.append(file_box(348, 254, 152, 64, "docker", ["Dockerfile"], icon_size=28))

# publish: テンプレートとファイルはまとめて S3 へ、コンテナイメージだけ ECR へ。どちらもまっすぐ進む
S3Y, ECRY = 134, 286
p = SEC["publish"]
p.append(step(539, 226, "publish"))
p += [icon("s3", 705, S3Y - 20, 40), text(705, S3Y - 28, "S3バケット", 13, INK, 700)]
p += [icon("ecr", 705, ECRY - 20, 40), text(700, ECRY - 28, "ECRリポジトリ", 13, INK, 700)]
p = SEC["trunk"]
p.append(f'<path d="M500,210 H519 V{S3Y}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p += [arrow(f"M500,{S3Y} H685"), text(612, S3Y - 10, "アップロード")]
p.append(role_chip(556, S3Y + 12, ["ファイル用", "パブリッシュロール"]))
p += [arrow(f"M500,{ECRY} H685"), text(612, ECRY - 10, "ビルド＆アップロード")]
p.append(role_chip(556, ECRY + 12, ["イメージ用", "パブリッシュロール"]))

# publish → deploy: アップロードしたアセットを deploy で使う
p = SEC["gap"]
p.append(f'<path d="M725,{ECRY} H752 V{S3Y}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
p.append(arrow(f"M725,{S3Y} H844"))

# deploy: CloudFormation のデプロイは前のページで説明するので、CloudFormation のアイコンだけで表す（2026-11-03 本人）
DMID = 186
p = SEC["deploy"]
p.append(step(779, 300, "deploy"))
p.append(icon("cfn", 880, S3Y - 32, 64))
p.append(text(880, S3Y + 52, "CloudFormation", 13, INK, 700))
p.append(text(880, S3Y + 68, "でデプロイ", 13, INK, 700))


# CloudFormation のデプロイ: IaC の図（iac-diff）と同じ形。あるべき姿と現在の状態を比べ、差分を反映する
def state_box(y, name, lines, fill):
    out = [f'<rect x="795" y="{y}" width="110" height="62" rx="10" fill="{fill}" stroke="{LINE}" stroke-width="2"/>',
           icon(name, 815, y + 15, 32)]
    for i, line in enumerate(lines):
        bold = i < len(lines) - 1
        out.append(text(835, y + 62 / 2 + 4 - 7 * (len(lines) - 1) + 14 * i, line, 11 if bold else 10, INK if bold else SUB, 700 if bold else None, "start"))
    return "".join(out)


p = CFN
p.append(state_box(103, "template", ["新しい", "テンプレート", "（あるべき姿）"], "#ffffff"))
p.append(state_box(207, "stack", ["スタックの", "状態", "（現在の状態）"], "#f5f7f9"))
p.append(text(914, DMID + 4, "比較", 11, anchor="end"))
p.append(arrow(f"M905,{S3Y} H920 V{DMID - 8} H950"))
p.append(arrow(f"M905,238 H920 V{DMID + 8} H950"))
p.append(icon("cfn", 970, DMID - 18, 36))
p.append(text(970, DMID + 34, "CloudFormation", 11, INK, 700))
p.append(green_arrow(f"M990,{DMID} H1030"))
p.append(f'<rect x="1030" y="{DMID - 46}" width="64" height="92" rx="10" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 4"/>')
p.append(text(1062, DMID - 27, "差分", 12, GREEN, 700))
p.append(icon("changeset", 1062, DMID - 18, 34))
p.append(text(1062, DMID + 34, "変更セット", 11, GREEN, 700))
p.append(green_arrow(f"M1094,{DMID} H1186"))
p += [text(1140, DMID - 9, "確認して", 11), text(1140, DMID + 6, "反映する", 11)]
p.append(f'<rect x="1186" y="{DMID - 46}" width="68" height="92" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="2"/>')
p.append(icon("stack", 1220, DMID - 34, 34))
p.append(text(1220, DMID + 18, "スタック", 11, INK, 700))
p.append(text(1220, DMID + 33, "実リソース", 10, SUB))

defs = (f'<defs><marker id="mInk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
        f'<marker id="mGreen" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{GREEN}"/></marker></defs>')
DIM = 0.14


# Bootstrap を上に置いたぶん、cdk deploy の枠全体をずらす
MOVE = 'transform="translate(-157,88)"'


def write(name, focus=None):
    """focus を渡すと、そのフェーズに寄った図にする。Bootstrap は出さず、cdk deploy の枠だけを切り出す。"""
    body = []
    for key, parts in SEC.items():
        if focus is not None and key == "bootstrap":
            continue
        opacity = "" if focus is None or key in focus else f' opacity="{DIM}"'
        move = "" if key == "bootstrap" else f" {MOVE}"
        body.append(f"<g{opacity}{move}>" + "".join(parts) + "</g>")
    box = "0 0 940 468" if focus is None else "0 96 940 370"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}" width="100%" '
           f"font-family=\"'Noto Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', sans-serif\">\n{defs}\n" + "\n".join(body) + "\n</svg>\n")
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(svg)


write("deploy-flow")
write("deploy-flow-synth", {"outer", "synth_frame", "source", "group"})
write("deploy-flow-assets", {"outer", "group"})
write("deploy-flow-publish", {"outer", "group", "trunk", "publish"})
write("deploy-flow-deploy", {"outer", "gap", "deploy"})

# CloudFormation のデプロイ: 図の部品だけを左上に寄せて切り出す
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 490 200" width="100%" '
       f"font-family=\"'Noto Sans JP', 'Noto Sans CJK JP', 'Hiragino Sans', sans-serif\">\n{defs}\n"
       '<g transform="translate(-780,-88)">' + "".join(CFN) + "</g>\n</svg>\n")
with open(os.path.join(OUT, "cfn-deploy.svg"), "w") as f:
    f.write(svg)
