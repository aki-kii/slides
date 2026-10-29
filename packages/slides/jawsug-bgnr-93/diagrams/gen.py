#!/usr/bin/env python3
"""#93 の図を SVG で組む（life の tasks/speaking/diagram-style.md に合わせる）。

  python3 diagrams/gen.py   # public/images/*.svg に書き出す

AWS のアイコンは AWS Architecture Icons 2026-07-31 版（Icon-package_07312026）。
置き場は環境変数 AWS_ICONS（既定は /srv/kiro-work/research/aws-icons/pkg）。
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "public", "images")
PKG = os.environ.get("AWS_ICONS", "/srv/kiro-work/research/aws-icons/pkg")
ARCH = f"{PKG}/Architecture-Service-Icons_07312026"
GROUP = f"{PKG}/Architecture-Group-Icons_07312026"
RES = f"{PKG}/Resource-Icons_07312026"
GEN = f"{RES}/Res_General-Icons/Res_48_Light"

I = {
    "waf": f"{ARCH}/Arch_Security-Identity-Compliance/64/Arch_AWS-WAF_64.svg",
    "elb": f"{ARCH}/Arch_Networking-Content-Delivery/64/Arch_Elastic-Load-Balancing_64.svg",
    "ecs": f"{ARCH}/Arch_Containers/64/Arch_Amazon-Elastic-Container-Service_64.svg",
    "console": f"{ARCH}/Arch_Management-Governance/64/Arch_AWS-Management-Console_64.svg",
    "cli": f"{ARCH}/Arch_Developer-Tools/64/Arch_AWS-Command-Line-Interface_64.svg",
    "sdk": f"{ARCH}/Arch_Developer-Tools/64/Arch_AWS-Tools-and-SDKs_64.svg",
    "lambda": f"{ARCH}/Arch_Compute/64/Arch_AWS-Lambda_64.svg",
    "dynamodb": f"{ARCH}/Arch_Databases/64/Arch_Amazon-DynamoDB_64.svg",
    "cloud": f"{GROUP}/AWS-Cloud-logo_32.svg",
    "office": f"{GEN}/Res_Office-building_48_Light.svg",
    "user": f"{GEN}/Res_User_48_Light.svg",
    "code": f"{GEN}/Res_Source-Code_48_Light.svg",
    "doc": f"{GEN}/Res_Document_48_Light.svg",
    "toolkit": f"{GEN}/Res_Toolkit_48_Light.svg",
    "generic": f"{GEN}/Res_Generic-Application_48_Light.svg",
    "git": f"{GEN}/Res_Git-Repository_48_Light.svg",
}

JP = "'Noto Sans JP', 'Hiragino Sans', sans-serif"
MONO = "'Fira Code', monospace"
INK, SUB, LINE = "#2c3e50", "#6b7684", "#c9d0d9"
GREEN, GREEN_BG = "#0E8A6E", "#e9f5f1"
RED, RED_BG = "#DD344C", "#fdecee"
GRAY = "#8a94a3"

_n = 0


def find(path):
    """パッケージのフォルダ名の揺れ（カテゴリ名）に強くする。"""
    if os.path.exists(path):
        return path
    name = os.path.basename(path)
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


def arrow(d, color=INK, width=2.5, dash=None):
    mid = {INK: "i", GREEN: "g", RED: "r", GRAY: "x"}[color]
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} '
            f'stroke-linejoin="round" stroke-linecap="round" marker-end="url(#a-{mid})"/>')


def svg(w, h, body, label):
    defs = "".join(
        f'<marker id="a-{m}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
        f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for m, c in (("i", INK), ("g", GREEN), ("r", RED), ("x", GRAY)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" '
            f'aria-label="{label}">\n<!-- AWS Architecture Icons 2026-07-31 版（Icon-package_07312026） -->\n'
            f'<defs>{defs}</defs>\n' + "\n".join(body) + "\n</svg>\n")


def service(key, cx, cy, name, sub=None, size=64, mono_sub=False, fs=18, ss=15):
    out = [inner(key, cx - size // 2, cy - size // 2, size)]
    y = cy + size // 2 + fs + 4
    out.append(t(cx, y, name, fs, "bold"))
    if sub:
        out.append(t(cx, y + ss + 6, sub, ss, color=SUB, mono=mono_sub))
    return out


def write(name, content):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print(name)


# ---------------------------------------------------------------- 導入: 構成
def story_architecture():
    b = []
    for i, name in enumerate(["A社", "B社", "C社"]):
        y = 50 + i * 80
        b.append(inner("office", 30, y, 48))
        b.append(t(92, y + 32, name, 18, "bold", anchor="start"))
    b.append(t(70, 304, "お客さんの会社", 15, color=SUB))
    b.append('<rect x="200" y="10" width="790" height="320" rx="14" fill="none" stroke="#232F3E" stroke-width="2"/>')
    b.append(inner("cloud", 200, 10, 30))
    b.append(t(238, 31, "AWS Cloud", 17, "bold", "#232F3E", "start"))
    b += service("waf", 330, 100, "WAF", "IPセット")
    b += service("elb", 610, 100, "ALB")
    b += service("ecs", 880, 100, "業務システム", "(ECS)")
    b.append(arrow("M144,140 L292,108"))
    b.append(t(214, 104, "アクセスする", 16))
    b.append(arrow("M366,100 L572,100"))
    b.append(t(470, 88, "許可した会社だけ通す", 16))
    b.append(arrow("M646,100 L842,100"))
    b.append(t(744, 88, "リクエストを渡す", 16))
    x0, y0 = 226, 196
    b.append(f'<rect x="{x0}" y="{y0}" width="300" height="118" rx="10" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
    b.append(t(x0 + 14, y0 + 24, "IPセット", 14, "bold", SUB, "start"))
    for i, (who, ip) in enumerate([("A社", "203.0.113.12/32"), ("B社", "203.0.113.128/28"), ("C社", "192.0.2.10/32")]):
        yy = y0 + 52 + i * 24
        b.append(t(x0 + 22, yy, who, 16, anchor="start"))
        b.append(t(x0 + 80, yy, ip, 16, mono=True, anchor="start"))
    b.append(f'<rect x="{x0 + 10}" y="{y0 + 33}" width="280" height="25" rx="6" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    b.append(t(x0 + 316, y0 + 52, "A社のIPアドレスを変更する", 17, "bold", RED, "start"))
    write("story-architecture.svg", svg(1000, 340, b, "取引先からのアクセスをWAFのIPセットで許可している構成"))


# ---------------------------------------------------------------- 導入: 画面
def pane(x, y, w, h, title, icon):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
         f'<line x1="{x}" y1="{y + 46}" x2="{x + w}" y2="{y + 46}" stroke="{LINE}" stroke-width="2"/>',
         inner(icon, x + 14, y + 8, 30),
         t(x + 54, y + 30, title, 17, "bold", anchor="start")]
    return o


def ip_rows(x, y, rows, w=380):
    o = []
    for i, ip in enumerate(rows):
        yy = y + i * 34
        o.append(f'<rect x="{x}" y="{yy}" width="{w}" height="26" rx="6" fill="#f5f7f9" stroke="{LINE}" stroke-width="1.5"/>')
        o.append(t(x + 16, yy + 19, ip, 17, mono=True, anchor="start"))
    return o


# 実際の IP セット（partner-allowed-ips）と同じ並び。A社は 203.0.113.12、B社は 203.0.113.128/28
ROWS = ["198.51.100.7/32", "203.0.113.80/32", "192.0.2.24/32", "192.0.2.10/32", "203.0.113.12/32", "198.51.100.45/32", "203.0.113.128/28"]
A_NEW = "198.51.100.200/32"
# A社（203.0.113.12）と見間違えてB社の行（203.0.113.128/28）を消し、A社の新しい値を足した後の一覧
AFTER = ROWS[:6] + [None, A_NEW]


CONSOLE_BLUE = "#0972d3"


def edit_rows(x, y, rows, step=34, marks=None):
    """7枚目の実スクショ（IP セットを編集）と同じ形：入力欄＋「削除」ボタン、下に「IP アドレスの追加」。
    rows の None は消えた行（赤い点線の空欄）。marks は {行番号: (印, 色)} で、行の右に添える。"""
    marks = marks or {}
    o = [t(x, y + 16, "IP アドレス (CIDR 表記)", 14, "bold", anchor="start")]
    for i, ip in enumerate(rows):
        yy = y + 28 + i * step
        if ip is None:
            o.append(f'<rect x="{x}" y="{yy}" width="478" height="26" rx="6" fill="{RED_BG}" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4"/>')
        else:
            o.append(f'<rect x="{x}" y="{yy}" width="400" height="26" rx="6" fill="#ffffff" stroke="{GRAY}" stroke-width="1.5"/>')
            o.append(t(x + 12, yy + 18, ip, 15, anchor="start"))
            o.append(f'<rect x="{x + 414}" y="{yy}" width="64" height="26" rx="13" fill="#ffffff" stroke="{CONSOLE_BLUE}" stroke-width="2"/>')
            o.append(t(x + 446, yy + 18, "削除", 13, "bold", CONSOLE_BLUE))
        if i in marks:
            label, color = marks[i]
            o.append(t(x + 488, yy + 18, label, 14, "bold", color, "start"))
    yy = y + 28 + len(rows) * step + 2
    o.append(f'<rect x="{x}" y="{yy}" width="150" height="26" rx="13" fill="#ffffff" stroke="{CONSOLE_BLUE}" stroke-width="2"/>')
    o.append(t(x + 75, yy + 18, "IP アドレスの追加", 13, "bold", CONSOLE_BLUE))
    return o


def story_screens():
    # ⑤ 事件
    b = pane(20, 6, 600, 350, "マネジメントコンソール　IP セットを編集", "console")
    b += edit_rows(48, 58, [ip for ip in AFTER if ip])
    for i, (who, msg, c, bg) in enumerate([("A社", "接続できる", GREEN, GREEN_BG),
                                           ("B社", "接続できない", RED, RED_BG)]):
        y = 40 + i * 120
        b.append(inner("office", 670, y + 6, 40))
        b.append(t(690, y + 66, who, 13, "bold"))
        b.append(f'<rect x="724" y="{y}" width="256" height="52" rx="14" fill="{bg}" stroke="{c}" stroke-width="2"/>')
        b.append(t(852, y + 33, msg, 16, "bold", c))
    write("story-incident.svg", svg(1000, 360, b, "IPセットの編集画面。B社の行が消えて、A社の新しい値が入っている。A社は接続でき、B社は接続できない"))

    # ⑥ 元の値が分からない
    b = pane(20, 6, 600, 350, "マネジメントコンソール　IP セットを編集", "console")
    # A社の旧と新が両方残り、B社の行が消えている
    b += edit_rows(48, 52, AFTER, step=31, marks={
        4: ("A社（旧）", INK), 6: ("B社（削除）", RED), 7: ("A社（新）", INK)})
    b += pane(680, 14, 300, 220, "手順書", "doc")
    b.append(t(704, 92, "B社の元の値", 16, color=SUB, anchor="start"))
    b.append(f'<rect x="704" y="104" width="252" height="40" rx="8" fill="none" stroke="{RED}" stroke-width="3" stroke-dasharray="7 5"/>')
    b.append(t(830, 131, "？", 20, "bold", RED))
    b.append(t(704, 176, "4. 現在の設定値を控える", 15, color=SUB, anchor="start"))
    b.append(t(704, 204, "→ 未実施", 15, "bold", RED, "start"))
    write("story-lost.svg", svg(1000, 360, b, "IPセットの編集画面。A社の旧と新のIPアドレスが両方残り、B社の行が消えている。手順4で控えるはずだったB社の元の値は、どこにも残っていない"))


# ---------------------------------------------------------------- 1部: デプロイの仕組み（差分）
def iac_diff():
    b = []
    res = [("waf", "AWS WAF"), ("elb", "ALB"), ("ecs", "Amazon ECS")]

    def row(x, y, items, empty=None, hl=None):
        o = []
        for i, (k, n) in enumerate(items):
            xx = x + i * 72
            if k == empty:
                # 差分になるところ。足りない枠を緑の破線で見せる
                o.append(f'<rect x="{xx}" y="{y}" width="48" height="48" rx="8" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2.5" stroke-dasharray="6 4"/>')
            else:
                o.append(inner(k, xx, y, 48))
                if k == hl:
                    o.append(f'<rect x="{xx - 6}" y="{y - 6}" width="60" height="60" rx="10" fill="none" stroke="{GREEN}" stroke-width="3"/>')
            o.append(t(xx + 24, y + 68, n, 13, "bold" if k in (empty, hl) else "normal", GREEN if k in (empty, hl) else INK))
        return o

    # コード（あるべき姿）
    b.append(f'<rect x="20" y="20" width="250" height="140" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
    b.append(inner("code", 32, 30, 28))
    b.append(t(66, 50, "コード（あるべき姿）", 16, "bold", anchor="start"))
    b += row(44, 68, res, hl="ecs")
    # 現在の状態
    b.append(f'<rect x="20" y="210" width="250" height="140" rx="12" fill="#f5f7f9" stroke="{LINE}" stroke-width="2"/>')
    b.append(inner("cloud", 32, 220, 28))
    b.append(t(66, 240, "現在の状態", 16, "bold", anchor="start"))
    b += row(44, 258, res, empty="ecs")
    # IaCのツールで比較
    b.append(inner("toolkit", 376, 146, 64))
    b.append(t(408, 232, "IaCのツール", 16, "bold"))
    b.append(arrow("M276,90 L330,90 L330,166 L370,166"))
    b.append(arrow("M276,280 L330,280 L330,196 L370,196"))
    b.append(t(316, 186, "比較", 15, anchor="end"))
    # 差分（ここだけを大きく見せる）
    b.append(arrow("M446,178 L520,178", GREEN))
    b.append(f'<rect x="528" y="104" width="148" height="150" rx="12" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="3" stroke-dasharray="7 5"/>')
    b.append(t(602, 134, "差分", 20, "bold", GREEN))
    b.append(inner("ecs", 566, 148, 72))
    b.append(f'<rect x="{566 - 6}" y="{148 - 6}" width="84" height="84" rx="12" fill="none" stroke="{GREEN}" stroke-width="3"/>')
    b.append(t(602, 244, "Amazon ECS", 14, "bold", GREEN))
    # デプロイ → 実リソース
    b.append(arrow("M682,178 L736,178", GREEN))
    b.append(t(709, 166, "デプロイ", 14, "bold", GREEN))
    b.append(f'<rect x="742" y="110" width="244" height="140" rx="12" fill="#ffffff" stroke="#232F3E" stroke-width="2"/>')
    b.append(inner("cloud", 742, 110, 28))
    b.append(t(778, 130, "実リソース", 16, "bold", "#232F3E", "start"))
    b += row(764, 156, res, hl="ecs")
    write("iac-diff.svg", svg(1000, 366, b, "IaCのツールが、コードのあるべき姿と現在の状態を比較し、その差分だけを実リソースへデプロイする"))


# ---------------------------------------------------------------- 2部: アップデート
def ai_updates():
    items = [("2025-11", ["CloudFormation", "早期バリデーション"]),
             ("2025-11", ["CloudFormation", "Language Server"]),
             ("2025-11", ["AWS IaC", "MCP Server"]),
             ("2026-04", ["cdk diagnose", "（プレビュー）"]),
             ("2026-06", ["cdk validate", "（プレビュー）"]),
             ("2026-06", ["Terraform MCP Server", "GA"]),
             ("2026-07", ["cdk lsp", "（プレビュー）"])]
    b = []
    y = 160
    b.append(arrow(f"M10,{y} L990,{y}", INK))
    xs = [90 + i * 136 for i in range(len(items))]
    for i, ((ym, lines), x) in enumerate(zip(items, xs)):
        up = i % 2 == 0
        b.append(f'<circle cx="{x}" cy="{y}" r="7" fill="#ffffff" stroke="{GREEN}" stroke-width="3"/>')
        if up:
            b.append(t(x, y + 32, ym, 15, "bold", SUB, mono=True))
            b.append(f'<line x1="{x}" y1="{y - 9}" x2="{x}" y2="{y - 40}" stroke="{LINE}" stroke-width="2"/>')
            for j, ln in enumerate(reversed(lines)):
                b.append(t(x, y - 52 - j * 22, ln, 15))
        else:
            b.append(t(x, y - 20, ym, 15, "bold", SUB, mono=True))
            b.append(f'<line x1="{x}" y1="{y + 9}" x2="{x}" y2="{y + 40}" stroke="{LINE}" stroke-width="2"/>')
            for j, ln in enumerate(lines):
                b.append(t(x, y + 64 + j * 22, ln, 15))
    write("ai-updates.svg", svg(1000, 300, b, "AIがIaCのツールを使いやすくなるアップデート"))


# ---------------------------------------------------------------- 3部: 学び方
def learning_steps():
    b = []
    steps = [("toolkit", ["環境のセットアップ"], "AIに任せてもよい"),
             ("lambda", ["Lambda関数を作る"], "新規作成"),
             ("lambda", ["ソースコードや", "設定を変更する"], "設定変更"),
             ("dynamodb", ["DynamoDBから", "値を取得する"], "他リソースとの連携")]
    xs = [110, 370, 630, 890]
    for (k, names, sub), x in zip(steps, xs):
        b.append(inner(k, x - 36, 44, 72))
        y = 144
        for n in names:
            b.append(t(x, y, n, 20, "bold"))
            y += 26
        b.append(t(x, y - 2, sub, 16, color=SUB))
    for a, c in zip(xs, xs[1:]):
        b.append(arrow(f"M{a + 56},80 L{c - 56},80", GREEN))
    b.append(f'<path d="M300,228 L300,240 L960,240 L960,228" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-linejoin="round"/>')
    b.append(t(630, 272, "最小限のリソースから、少しずつ範囲を広げる", 20, "bold", GREEN))
    write("learning-steps.svg", svg(1000, 286, b, "AIと一緒にサーバーレス構成を少しずつ育てる"))


# ---------------------------------------------------------------- 1部: 特徴
def feature_reproducibility():
    b = []
    # 手作業: 1 回のデプロイの中で、リソースの設定変更を繰り返す
    b.append(t(20, 30, "手作業", 20, "bold", anchor="start"))
    b += service("user", 52, 104, "人間", size=48, fs=16)
    b.append(f'<rect x="104" y="44" width="486" height="146" rx="12" fill="none" stroke="{GRAY}" stroke-width="2" stroke-dasharray="7 5"/>')
    b.append(t(118, 66, "1回のデプロイ", 15, "bold", SUB, "start"))
    res = [("waf", "AWS WAF"), ("elb", "ALB"), ("ecs", "Amazon ECS")]
    xs = [200, 350, 500]
    for (k, n), x in zip(res, xs):
        b.append(inner(k, x - 24, 80, 48))
        b.append(t(x, 148, n, 15, "bold"))
    b.append(arrow("M84,104 L170,104"))
    b.append(arrow("M230,104 L320,104"))
    b.append(arrow("M380,104 L470,104"))
    b.append(t(273, 94, "設定を変える", 12))
    b.append(t(427, 94, "設定を変える", 12))
    b.append(t(127, 94, "変える", 12))
    b.append(f'<rect x="316" y="72" width="68" height="88" rx="10" fill="none" stroke="{RED}" stroke-width="2.5"/>')
    b.append(t(350, 180, "どこかで間違える", 15))
    # IaC
    b.append(f'<rect x="10" y="210" width="580" height="190" rx="14" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>')
    b.append(t(28, 240, "IaC", 20, "bold", GREEN, "start"))
    for i, n in enumerate(["新人", "ベテラン"]):
        y = 282 + i * 74
        b.append(inner("user", 34, y - 22, 44))
        b.append(t(92, y + 6, n, 16, "bold", anchor="start"))
        b.append(arrow(f"M166,{y} L222,{308 + (i * 2 - 1) * 6}", GREEN))
    b += service("code", 258, 308, "同じコード", size=48, fs=16)
    b.append(arrow("M292,308 L352,308", GREEN))
    for r in range(2):
        y = 250 + r * 58
        for j, (k, _) in enumerate(res):
            b.append(inner(k, 370 + j * 48, y, 38))
    b.append(t(441, 392, "同じ結果", 17, "bold", GREEN))
    write("feature-reproducibility.svg", svg(600, 410, b, "手作業では1回のデプロイの中で設定変更を繰り返すのでどこかで間違えるが、IaCは誰がやっても同じ結果になる"))


def resources_row(x, y, size=36, gap=58):
    o = []
    for i, k in enumerate(["waf", "elb", "ecs"]):
        o.append(inner(k, x + i * gap, y, size))
        if i < 2:
            o.append(arrow(f"M{x + i * gap + size + 3},{y + size // 2} L{x + (i + 1) * gap - 4},{y + size // 2}"))
    return o


def feature_change_management():
    # 左：レビューしたソースコードをデプロイ（見出しはスライド側）
    b = []
    b += service("user", 60, 56, "レビュー", size=44, fs=15)
    b.append(arrow("M92,56 L166,56", GREEN))
    b += service("code", 210, 56, "ソースコード", size=48, fs=15)
    b.append(arrow("M210,112 L210,176", GREEN))
    b.append(t(222, 150, "デプロイ", 15, "bold", GREEN, "start"))
    b += resources_row(134, 186)
    write("feature-cm-deploy.svg", svg(330, 232, b, "レビューしたソースコードを、WAF・ALB・ECSへデプロイする"))

    # 右：戻すときは、前のコミットに戻して再度デプロイ
    b = []
    y = 60
    b.append(inner("git", 10, y - 24, 48))
    b.append(f'<line x1="96" y1="{y}" x2="236" y2="{y}" stroke="{INK}" stroke-width="2.5"/>')
    b.append(f'<circle cx="96" cy="{y}" r="11" fill="#ffffff" stroke="{GREEN}" stroke-width="3"/>')
    b.append(f'<circle cx="236" cy="{y}" r="11" fill="#ffffff" stroke="{GRAY}" stroke-width="3"/>')
    b.append(t(96, y + 34, "前のコミット", 15, "bold", GREEN))
    b.append(t(236, y + 34, "今のコミット", 15, color=GRAY))
    b.append(arrow(f"M236,{y - 16} C220,{y - 42} 112,{y - 42} 98,{y - 18}", GRAY))
    b.append(t(166, y - 40, "戻す", 15, color=SUB))
    b.append(arrow(f"M96,{y + 44} L96,204 L126,204", GREEN))
    b.append(t(108, 150, "再度デプロイ", 15, "bold", GREEN, "start"))
    b += resources_row(134, 186)
    write("feature-cm-rollback.svg", svg(330, 232, b, "戻すときは、前のコミットに戻して、WAF・ALB・ECSへ再度デプロイする"))


def feature_structure():
    b = []
    # リソースの関連（左・メイン）
    b.append(t(8, 30, "リソース同士の関連を追える", 16, anchor="start"))
    for i, (k, n) in enumerate([("waf", "AWS WAF"), ("elb", "ALB"), ("ecs", "Amazon ECS")]):
        y = 62 + i * 118
        b.append(inner(k, 24, y, 56))
        b.append(t(94, y + 34, n, 17, "bold", anchor="start"))
        if i < 2:
            b.append(arrow(f"M52,{y + 60} L52,{y + 114}"))
    # コード（右・CDK）
    b.append(arrow("M214,210 L198,210"))
    b.append(f'<rect x="220" y="40" width="600" height="360" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
    b.append(inner("code", 234, 52, 36))
    b.append(t(280, 78, "コード（AWS CDK）", 18, "bold", anchor="start"))
    rows = [
        (INK, "const alb = new ApplicationLoadBalancer(this, 'Alb', {"),
        (INK, "  vpc,"),
        (INK, "  internetFacing: true,"),
        (INK, "});"),
        (INK, ""),
        (GREEN, "// 取引先のシステムがHTTPでしか連携できないため、HTTPを許可する"),
        (INK, "alb.addListener('Http', {"),
        (INK, "  port: 80,"),
        (INK, "  protocol: ApplicationProtocol.HTTP,"),
        (INK, "});"),
    ]
    y = 128
    for c, line in rows:
        if c == GREEN:
            # 日本語のコメントは等幅フォントだと字形が崩れるので、本文のフォントで描く（字下げぶんだけずらす）
            indent = (len(line) - len(line.lstrip())) * 10.2
            b.append(t(238 + indent, y, line.strip(), 17, color=c, anchor="start"))
        elif line:
            b.append(t(238, y, line.replace(" ", "&#160;"), 17, color=c, anchor="start", mono=True))
        y += 25.5
    write("feature-structure.svg", svg(830, 410, b, "WAF・ALB・ECSの関連が分かる構成と、ALBを定義したAWS CDKのコード。あえてHTTPを許可する設定に、その意図をコメントで残している"))


def feature_reuse():
    def chain(keys, x, y, size=32, gap=58):
        o = []
        for i, k in enumerate(keys):
            o.append(inner(k, x + i * gap, y, size))
            if i < len(keys) - 1:
                o.append(arrow(f"M{x + i * gap + size + 3},{y + size // 2} L{x + (i + 1) * gap - 4},{y + size // 2}"))
        return o

    # 左：同じコードのまま、別の環境にもデプロイ（見出しはスライド側）
    b = []
    b += service("code", 40, 136, "同じコード", size=48, fs=14)
    for i, env in enumerate(["開発環境", "本番環境"]):
        y = 34 + i * 112
        b.append(f'<rect x="112" y="{y}" width="210" height="84" rx="12" fill="#ffffff" stroke="#232F3E" stroke-width="2"/>')
        b.append(inner("cloud", 112, y, 24))
        b.append(t(144, y + 18, env, 14, "bold", "#232F3E", "start"))
        b += chain(["waf", "elb", "ecs"], 140, y + 38)
        b.append(arrow(f"M68,136 L86,136 L104,{y + 50}", GREEN))
    write("feature-reuse-envs.svg", svg(330, 240, b, "同じコードのまま、WAF・ALB・ECSの構成を開発環境と本番環境にデプロイする"))

    # 右：共通する部分を切り出して、他の構成に組み込む
    b = []
    b.append(f'<rect x="90" y="6" width="150" height="88" rx="12" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>')
    b.append(t(165, 30, "共通する部分", 15, "bold", GREEN))
    b += chain(["elb", "ecs"], 119, 46, size=36, gap=56)
    b.append(arrow("M165,98 L165,128", GREEN))
    b.append(t(177, 118, "組み込む", 15, "bold", GREEN, "start"))
    b.append(f'<rect x="14" y="134" width="302" height="106" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>')
    b.append(t(30, 158, "他の構成", 15, "bold", anchor="start"))
    b.append(f'<rect x="28" y="168" width="132" height="60" rx="10" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="7 5"/>')
    b += chain(["elb", "ecs"], 42, 180, size=36, gap=58)
    b.append(arrow("M160,198 L204,198"))
    b.append(inner("dynamodb", 212, 176, 40))
    b.append(t(232, 232, "Amazon DynamoDB", 11, color=SUB))
    write("feature-reuse-parts.svg", svg(330, 248, b, "ALBとECSの共通する部分を切り出して、DynamoDBを使う他の構成に組み込む"))


# ---------------------------------------------------------------- 2部: AI に向いている理由
def ai_badge(cx, cy, size=56):
    """AI（コーディングエージェントなど）。特定の製品に寄せないよう、文字だけの印にする。"""
    h = size // 2
    return [f'<rect x="{cx - h}" y="{cy - h}" width="{size}" height="{size}" rx="14" fill="{INK}"/>',
            t(cx, cy + 9, "AI", 24, "bold", "#ffffff")]


def code_box(x, y, w, h, rows):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
         inner("code", x + 12, y + 10, 30),
         t(x + 50, y + 32, "コード", 17, "bold", anchor="start")]
    yy = y + 64
    for r in rows:
        if r[0] == "res":
            o.append(inner(r[1], x + 18, yy - 18, 28))
            o.append(t(x + 56, yy + 2, r[2], 15, anchor="start"))
        elif r[0] == "comment":
            o.append(t(x + 18, yy + 2, r[1], 15, "bold", GREEN, "start"))
        else:
            o.append(f'<rect x="{x + 18}" y="{yy - 6}" width="{r[1]}" height="12" rx="6" fill="#e3e7ec"/>')
        yy += 36
    return o


ALB_CODE = [
    (INK, "const alb = new ApplicationLoadBalancer(this, 'Alb', {"),
    (INK, "  vpc,"),
    (INK, "  internetFacing: true,"),
    (INK, "});"),
    (INK, ""),
    (GREEN, "// 取引先のシステムがHTTPでしか連携できないため、HTTPを許可する"),
    (INK, "alb.addListener('Http', {"),
    (INK, "  port: 80,"),
    (INK, "  protocol: ApplicationProtocol.HTTP,"),
    (INK, "});"),
]


def cdk_code(x, y, w, rows, title="コード（AWS CDK）"):
    """feature_structure() と同じ書き方で CDK のコードを描く。"""
    h = 76 + len(rows) * 19.5
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
         inner("code", x + 14, y + 12, 36),
         t(x + 60, y + 38, title, 18, "bold", anchor="start")]
    yy = y + 80
    for c, line in rows:
        if c == GREEN:
            # 日本語のコメントは等幅フォントだと字形が崩れるので、本文のフォントで描く
            o.append(t(x + 16, yy, line.strip(), 13, color=c, anchor="start"))
        elif line:
            o.append(t(x + 16, yy, line.replace(" ", "&#160;"), 13, color=c, anchor="start", mono=True))
        yy += 19.5
    return o


def ai_context():
    b = cdk_code(10, 20, 470, ALB_CODE)
    b.append(t(245, 316, "アーキテクチャ全体と、設定の意図", 15, "bold"))
    b += ai_badge(620, 140)
    b.append(arrow("M488,140 L584,140", GREEN))
    b.append(t(536, 126, "コードを渡す", 15, color=GREEN))
    b.append(t(620, 200, "現状と意図が伝わる", 15, "bold", GREEN))
    # AWS を読みに行く（時間とトークンがかかる）
    b.append(inner("cloud", 836, 116, 48))
    b.append(t(860, 188, "AWSのリソース", 15, "bold"))
    b.append(arrow("M656,140 L826,140", GRAY, dash="7 5"))
    b.append(f'<circle cx="741" cy="140" r="16" fill="#ffffff" stroke="{RED}" stroke-width="3"/>')
    b.append(f'<path d="M734,133 L748,147 M748,133 L734,147" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
    b.append(t(741, 98, "MCPやCLIでAWSを読み取ると", 14, color=SUB))
    b.append(t(741, 118, "時間もトークンもかかる", 14, color=SUB))
    write("ai-context.svg", svg(940, 330, b, "CDKのコードにはアーキテクチャ全体と設定の意図が書いてあり、AIにはコードを渡せば伝わる。AWSをMCPやCLIで読みに行くと時間もトークンもかかる"))


def ai_validation():
    b = []
    # 自己フィードバックのハーネス
    b.append(f'<rect x="10" y="20" width="420" height="270" rx="16" fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="8 6"/>')
    b.append(t(30, 48, "自己フィードバックするハーネス", 16, "bold", GREEN, "start"))
    b += ai_badge(70, 130)
    b.append(arrow("M102,130 L164,130"))
    b.append(t(133, 116, "書く", 15))
    b.append(inner("code", 170, 102, 56))
    b.append(t(198, 186, "コード", 16, "bold"))
    b.append(arrow("M232,130 L294,130"))
    b.append(inner("toolkit", 300, 102, 56))
    b.append(t(328, 186, "検証", 16, "bold"))
    b.append(t(328, 208, "lint・validateなど", 13, color=SUB))
    # エラーを返して AI が直す
    b.append(arrow("M328,222 L328,256 L70,256 L70,166", RED))
    b.append(t(199, 246, "エラー → AIが自分で直す", 15, "bold", RED))
    # 通ったら、人間が差分を見る
    b.append(arrow("M362,130 L582,130"))
    b.append(t(472, 116, "検証を通過", 15))
    b.append(inner("user", 590, 102, 56))
    b.append(t(618, 186, "人間", 16, "bold"))
    b.append(t(618, 208, "デプロイ前に差分を見る", 13, color=SUB))
    b.append(arrow("M652,130 L766,130", GREEN))
    b.append(t(709, 116, "デプロイ", 15, "bold", GREEN))
    b.append(inner("cloud", 774, 102, 56))
    b.append(t(802, 186, "AWS", 16, "bold"))
    b.append(t(802, 208, "壊れたものが届かない", 13, color=SUB))
    write("ai-validation.svg", svg(880, 300, b, "AIが書いたコードを検証し、エラーがあればAIが自分で直す。検証を通ったら、人間がデプロイ前に差分を見てからデプロイする"))


SG_CODE = [
    (INK, "const sg = new ec2.SecurityGroup(this, 'BastionSg', {"),
    (INK, "  vpc,"),
    (INK, "  allowAllOutbound: true,"),
    (INK, "});"),
    (INK, ""),
    (RED, "sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22));"),
]


def ai_safety():
    b = []
    # 危うい行の下地（コードより先に描いて、文字の下に敷く）
    b.append(f'<rect x="22" y="{20 + 80 + 5 * 19.5 - 15}" width="526" height="22" rx="4" fill="{RED_BG}"/>')
    b += cdk_code(10, 20, 550, SG_CODE)
    hl_y = 20 + 80 + 5 * 19.5 - 4
    # スキャン結果の吹き出し
    b.append(f'<path d="M560,{hl_y} L592,{hl_y - 14} L592,{hl_y + 14} z" fill="{RED_BG}" stroke="{RED}" stroke-width="2" stroke-linejoin="round"/>')
    b.append(f'<rect x="590" y="{hl_y - 40}" width="340" height="80" rx="14" fill="{RED_BG}" stroke="{RED}" stroke-width="2"/>')
    b.append(f'<rect x="588" y="{hl_y - 12}" width="6" height="24" fill="{RED_BG}"/>')
    b.append(t(760, hl_y - 6, "全世界からのSSHを許可しています", 18, "bold", RED))
    b.append(t(760, hl_y + 22, "受信元 0.0.0.0/0 → TCP 22", 13, color=RED, mono=True))
    # 同じコードを、2つのタイミングでスキャンする
    for x, when, how, tool in ((60, "書いているとき", "cdk synth のときにルールでチェック", "cdk-nag"),
                               (320, "あとでレビュー", "リポジトリ全体をまとめてスキャン", "Checkov など")):
        b.append(arrow(f"M{x + 110},244 L{x + 110},220", GREEN))
        b.append(f'<rect x="{x}" y="248" width="220" height="70" rx="12" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>')
        b.append(t(x + 110, 271, when, 16, "bold", GREEN))
        b.append(t(x + 110, 290, how, 12, color=INK))
        b.append(t(x + 110, 308, tool, 12, color=SUB))
    write("ai-safety.svg", svg(940, 324, b, "セキュリティグループで22番ポートを0.0.0.0/0に開けているCDKのコードを、書いているときはcdk-nag、あとでレビューするときはCheckovなどでスキャンし、全世界からのSSHを許可していると指摘される"))


def ai_permission():
    b = []
    b += ai_badge(50, 70)
    b.append(arrow("M82,70 L170,70"))
    b.append(t(126, 56, "書く", 15))
    b.append(inner("code", 176, 42, 56))
    b.append(t(204, 126, "コード", 16, "bold"))
    b.append(arrow("M238,70 L326,70"))
    b.append(inner("git", 332, 42, 56))
    b.append(t(360, 126, "リポジトリ", 16, "bold"))
    b.append(arrow("M394,70 L482,70"))
    b.append(inner("toolkit", 488, 42, 56))
    b.append(t(516, 126, "CI/CD", 16, "bold"))
    b.append(arrow("M550,70 L670,70", GREEN))
    b.append(t(610, 56, "デプロイ", 15, "bold", GREEN))
    b.append(inner("cloud", 676, 42, 56))
    b.append(t(704, 126, "AWS", 16, "bold"))
    # AI から AWS へは直接さわらない
    b.append(arrow("M50,102 L50,180 L704,180 L704,142", GRAY, dash="7 5"))
    b.append(f'<circle cx="377" cy="180" r="20" fill="#ffffff" stroke="{RED}" stroke-width="3"/>')
    b.append(f'<path d="M368,171 L386,189 M386,171 L368,189" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
    b.append(t(377, 228, "AIにAWSの権限は渡さない", 16, "bold"))
    write("ai-permission.svg", svg(760, 240, b, "AIはコードを書くだけで、デプロイはCI/CDが行う。AIにAWSの権限を渡さなくて済む"))


if __name__ == "__main__":
    story_architecture()
    story_screens()
    iac_diff()
    ai_updates()
    learning_steps()
    feature_reproducibility()
    feature_change_management()
    feature_structure()
    feature_reuse()
    ai_context()
    ai_validation()
    ai_safety()
    ai_permission()
