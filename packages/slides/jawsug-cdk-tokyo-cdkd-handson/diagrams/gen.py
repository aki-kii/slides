#!/usr/bin/env python3
"""cdkd ハンズオン（2026-11-05）のトーク用に、cdk deploy の流れの図を SVG で組む。

  AWS_ICONS=<アイコン置き場> python3 diagrams/gen.py   # public/images/*.svg に書き出す

life の tasks/speaking/diagram-style.md に合わせる。#93 の図の組み方（inner() でアイコンを埋め込む）を真似た。
AWS のアイコンは AWS Architecture Icons 2026-07-31 版（Icon-package_07312026）。
アイコン置き場は環境変数 AWS_ICONS で渡す（下の階層も含めてファイル名で探す）。

- cdk-deploy-flow.svg … cdk deploy の三段（合成 → アセットのアップロード → デプロイ）
- cdk-deploy-flow-diff.svg … 同じ配置に cdk diff（前回デプロイしたテンプレートとの比較）を足したもの
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "public", "images")
PKG = os.environ.get("AWS_ICONS")

I = {
    "cdk": "Arch_AWS-Cloud-Development-Kit_64.svg",
    "cfn": "Arch_AWS-CloudFormation_64.svg",
    "s3": "Arch_Amazon-Simple-Storage-Service_64.svg",
    "ecr": "Arch_Amazon-Elastic-Container-Registry_64.svg",
    "lambda": "Arch_AWS-Lambda_64.svg",
    "iam": "Arch_AWS-Identity-and-Access-Management_64.svg",
    "doc": "Res_Document_48_Light.svg",
    "code": "Res_Source-Code_48_Light.svg",
}

JP = "'Noto Sans JP', 'Hiragino Sans', sans-serif"
MONO = "'Fira Code', monospace"
INK, SUB, LINE = "#2c3e50", "#6b7684", "#c9d0d9"
GREEN, GREEN_BG = "#0E8A6E", "#e9f5f1"
GRAY = "#8a94a3"
SOFT_BG = "#f5f7f9"

_n = 0


def find(name):
    """パッケージのフォルダ名の揺れ（カテゴリ名）に強くするため、ファイル名だけで探す。"""
    for root, _, files in os.walk(PKG):
        if "__MACOSX" in root:
            continue
        if name in files:
            return os.path.join(root, name)
    raise FileNotFoundError(name)


def inner(key, x, y, size):
    """diagram-style.md の inner()。id とクラス名に接頭辞を付けて埋め込む。"""
    global _n
    _n += 1
    prefix = f"{key}{_n}-"
    s = open(find(I[key])).read()
    s = re.sub(r'<\?xml[^>]*\?>', '', s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f'url(#{i})', f'url(#{prefix}{i})')
    body = re.sub(r'\.cls-(\d)', rf'.{prefix}cls-\1', body).replace('class="cls-', f'class="{prefix}cls-')
    body = re.sub(r'<title>.*?</title>', '', body, flags=re.S)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{body.strip()}</svg>'


def t(x, y, s, size=15, weight="normal", color=INK, anchor="middle", mono=False):
    fam = MONO if mono else JP
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}">{s}</text>')


def arrow(d, color=INK, width=2.5, both=False):
    mid = {INK: "i", GREEN: "g", GRAY: "x"}[color]
    start = f' marker-start="url(#a-{mid})"' if both else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linejoin="round" stroke-linecap="round"{start} marker-end="url(#a-{mid})"/>')


def svg(w, h, body, label):
    defs = "".join(
        f'<marker id="a-{m}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for m, c in (("i", INK), ("g", GREEN), ("x", GRAY)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" '
            f'aria-label="{label}">\n<!-- AWS Architecture Icons 2026-07-31 版（Icon-package_07312026） -->\n'
            f'<defs>{defs}</defs>\n' + "\n".join(body) + "\n</svg>\n")


def box(x, y, w, h, key, name, sub=None, icon=44, rx=10):
    """白地の箱。中にアイコン、下に名前（と補足）。"""
    cx = x + w // 2
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
         inner(key, cx - icon // 2, y + 12, icon),
         t(cx, y + icon + 32, name, 14, "bold")]
    if sub:
        o.append(t(cx, y + icon + 48, sub, 11, color=SUB))
    return o


def cmd_jp(x, y, cmd, jp, size=13, color=INK, weight="normal", anchor="start"):
    """「cdk bootstrapで作った」のように、コマンド名（Fira Code）に日本語を続ける。"""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">'
            f'<tspan font-family="{MONO}">{cmd}</tspan><tspan font-family="{JP}">{jp}</tspan></text>')


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print(name)


def deploy_flow(with_diff):
    """A（三段だけ）と B（cdk diff を足したもの）を同じ配置で描く。共通部分の座標は変えない。"""
    global _n
    _n = 0
    b = []

    # cdk deploy が三段をまとめて包む（上のブラケット）
    b.append(f'<path d="M14,46 L14,34 L986,34 L986,46" fill="none" stroke="{SUB}" stroke-width="2" stroke-linejoin="round"/>')
    b.append(f'<rect x="430" y="18" width="140" height="32" rx="16" fill="#ffffff" stroke="{SUB}" stroke-width="2"/>')
    b.append(t(500, 40, "cdk deploy", 17, "bold", INK, mono=True))

    # 段の見出し
    b.append(t(197, 82, "① 合成（synth）", 16, "bold"))
    b.append(t(540, 82, "② アセットのアップロード", 16, "bold"))
    b.append(t(824, 82, "③ デプロイ", 16, "bold"))

    # ① 合成: CDKアプリ → cdk.out（テンプレートとアセット）
    b += box(24, 214, 100, 100, "cdk", "CDKアプリ", "コード", icon=48, rx=12)
    b.append(f'<rect x="226" y="96" width="148" height="334" rx="14" fill="{SOFT_BG}" stroke="{LINE}" stroke-width="2"/>')
    b.append(t(240, 120, "cdk.out", 16, "bold", INK, "start", mono=True))
    b += box(236, 132, 128, 96, "doc", "テンプレート", "CloudFormation")
    b += box(236, 300, 128, 96, "code", "アセット", "Lambdaのコードなど")
    b.append(arrow("M124,264 L222,264"))
    b.append(t(173, 252, "CDKが合成する", 12))

    # ② アセットのアップロード: アセット → cdk bootstrap で作った S3バケット（Docker イメージなら ECRリポジトリ）
    b.append(f'<rect x="452" y="262" width="178" height="168" rx="14" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
    b.append(cmd_jp(466, 286, "cdk bootstrap", "で作った", 12, SUB))
    b += box(483, 300, 116, 88, "s3", "S3バケット")
    b.append(inner("ecr", 470, 400, 20))
    b.append(t(498, 410, "Dockerイメージなら", 10.5, color=SUB, anchor="start"))
    b.append(t(498, 425, "ECRリポジトリ", 10.5, color=SUB, anchor="start"))
    b.append(arrow("M364,344 L479,344"))
    b.append(t(421, 334, "アセットを上げる", 12))

    # ③ デプロイ: テンプレート → CloudFormation → スタック（リソースと、前回デプロイしたテンプレートを持つ）
    b.append(inner("cfn", 796, 152, 56))
    b.append(t(824, 230, "CloudFormation", 15, "bold"))
    b.append(arrow("M364,180 L790,180"))
    b.append(t(574, 170, "テンプレートを渡す", 13))
    b.append(arrow("M824,240 L824,296", GREEN))
    b.append(t(836, 256, "変更セットを作って実行する", 11.5, "bold", GREEN, "start"))
    b.append(t(836, 271, "CreateChangeSet", 10, color=SUB, anchor="start", mono=True))
    b.append(t(836, 284, "ExecuteChangeSet", 10, color=SUB, anchor="start", mono=True))
    b.append(f'<rect x="660" y="300" width="330" height="148" rx="14" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>')
    b.append(inner("cfn", 674, 310, 28))
    b.append(t(710, 330, "スタック", 16, "bold", GREEN, "start"))
    b.append(t(784, 330, "状態を持つ", 12, color=SUB, anchor="start"))
    b += box(670, 344, 110, 96, "doc", "テンプレート", "前回デプロイした", icon=36)
    b += box(788, 344, 92, 96, "lambda", "Lambda関数", icon=36)
    b += box(888, 344, 92, 96, "iam", "IAMロール", icon=36)

    if with_diff:
        # cdk diff: 新しく合成したテンプレートと、スタックが持つ前回デプロイしたテンプレートを比べる（補助線）
        b.append(arrow("M300,232 L300,252 L644,252 L644,392 L666,392", GRAY, width=2, both=True))
        b.append(cmd_jp(510, 246, "cdk diff", "：前回デプロイしたテンプレートと比べる", 11, SUB, anchor="middle"))
        label = ("cdk deployは、CDKアプリを合成してcdk.outにテンプレートとアセットを作り、アセットをS3バケットに上げ、"
                 "CloudFormationが変更セットを作って実行してスタックを作る・更新する。"
                 "cdk diffは、新しく合成したテンプレートとスタックが持つ前回デプロイしたテンプレートを比べる")
        name = "cdk-deploy-flow-diff.svg"
    else:
        label = ("cdk deployは、CDKアプリを合成してcdk.outにテンプレートとアセットを作り、アセットをS3バケットに上げ、"
                 "CloudFormationが変更セットを作って実行してスタックを作る・更新する")
        name = "cdk-deploy-flow.svg"
    write(name, svg(1000, 460, b, label))


if __name__ == "__main__":
    if not PKG:
        sys.exit("環境変数 AWS_ICONS にアイコン置き場を指定してください")
    deploy_flow(False)
    deploy_flow(True)
