"""コンテナ支部 #31 の図を作る。

    python3 diagrams/charts.py   # パッケージのディレクトリで

public/images/ に次の SVG を書き出す。見た目は life の tasks/speaking/diagram-style.md に従う。
- bot-task.svg        : 音声botの構成（前のページの bot-overview.svg の bot の部分を開いて、1つのECSタスクに3つのコンテナ）
- chart-breakdown.svg : 最初の分析（改善前の起動の内訳を1本のタイムラインで）
- soci-lifecycle.svg  : SOCIとは？（pull → create → start と、それぞれで読むもの）
- soci-terms.svg      : 仕組みの3つの言葉（レイヤー・span・zTOC）
- soci-compare.svg    : コンテナ起動の流れ（遅延読み込みなし と SOCI）
- soci-mechanism.svg  : プル時と起動時に、どこから何を取得するか
- chart-soci.svg      : SOCI後の振り返り（改善前と同じ項目を並べて比べる）
- wait-before.svg     : Discord botコンテナが読み上げコンテナの読み込み完了を待って起動していた
- wait-after.svg      : Discord botコンテナが待たずに起動する
- chart-total.svg     : 全体の推移（改善前 → SOCI → 待たずに起動）

数字は life の container-31 README の構成まとめ（2026-11-15）の値。全体は 2026-11-16 の本人の決定で約77秒（改善前）・約49秒（SOCI）。
色は意味で使う: イメージのプル＝赤、コンテナの起動＝緑、その他＝灰色、全体＝濃い文字色。
"""

import re
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "public" / "images"
AWS = HERE.parent / "public" / "images" / "aws"
FONT = "'Noto Sans JP', 'Hiragino Sans', sans-serif"
MONO = "'Fira Code', monospace"

INK = "#2c3e50"
SUB = "#6b7684"
LINE = "#c9d0d9"
GREEN, GREEN_BG = "#0E8A6E", "#e9f5f1"
RED, RED_BG = "#DD344C", "#fdecee"
DASH = "#aab2bd"
OTHER = "#e3e7ec"

# 改善前とSOCI後の数字（秒）
# 全体はヘルスチェックを改善した後の値（2026-11-16 本人。ヘルスチェックの説明は話に入れない）
BEFORE = {"total": 77, "pull": 37.5, "voice": 0.8, "bot": 1.5}
SOCI = {"total": 49, "pull": 3.3, "voice": 9.1, "bot": 4.7}
NOWAIT_TOTAL = 32.7


# ---------------------------------------------------------------------------
# 部品
# ---------------------------------------------------------------------------
_n = 0


def icon(path: Path, x, y, size) -> str:
    """アイコンの SVG を埋め込む。id とクラス名に接頭辞を付けてぶつからないようにする。"""
    global _n
    _n += 1
    prefix = f"i{_n}-"
    s = path.read_text()
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = re.search(r"<svg[^>]*>(.*)</svg>", s, re.S).group(1)
    body = re.sub(r"<title>.*?</title>", "", body)
    for i in set(re.findall(r'id="([^"]+)"', body)):
        body = body.replace(f'id="{i}"', f'id="{prefix}{i}"').replace(f"url(#{i})", f"url(#{prefix}{i})")
    body = re.sub(r"\.cls-(\d)", rf".{prefix}cls-\1", body).replace('class="cls-', f'class="{prefix}cls-')
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{body.strip()}</svg>'


def ECR(x, y, s):
    return icon(AWS / "ecr.svg", x, y, s)


def CONTAINER(x, y, s):
    return icon(AWS / "ecs-container.svg", x, y, s)


def TASK(x, y, s):
    return icon(HERE / "icons" / "ecs-task.svg", x, y, s)


def FARGATE(x, y, s):
    return icon(AWS / "fargate.svg", x, y, s)


def svg(w: int, h: int, body: list[str]) -> str:
    marks = "".join(
        f'<marker id="m{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" '
        f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
        for n, c in (("Ink", INK), ("Sub", SUB), ("Red", RED), ("Green", GREEN))
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" font-family="{FONT}">'
        f"<defs>{marks}</defs>" + "".join(body) + "</svg>\n"
    )


def text(x, y, s, size=16, fill=INK, anchor="start", bold=False, mono=False) -> str:
    b = ' font-weight="700"' if bold else ""
    f = f' font-family="{MONO}"' if mono else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{b}{f}>{s}</text>'


def box(x, y, w, h, stroke=LINE, fill="#ffffff", rx=12, dash=False) -> str:
    d = ' stroke-dasharray="7 5"' if dash else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"{d}/>'


def bar(x, y, w, h, fill, rx=3) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 4):.1f}" height="{h}" rx="{rx}" fill="{fill}"/>'


def arrow(d, color=INK, mark="Ink", width=2.5) -> str:
    return (
        f'<path d="{d}" stroke="{color}" stroke-width="{width}" fill="none" stroke-linejoin="round" '
        f'marker-end="url(#m{mark})"/>'
    )


def pill(cx, cy, label, fill=INK, w=96) -> str:
    """ライフサイクルの段階（pull / create / start）のラベル。"""
    return (
        f'<rect x="{cx - w / 2:.1f}" y="{cy - 16:.1f}" width="{w}" height="32" rx="16" fill="{fill}"/>'
        + text(cx, cy + 6, label, size=16, fill="#fff", anchor="middle", bold=True, mono=True)
    )


def fmt(v: float, about: bool = False) -> str:
    """全体の秒数は「約77秒」のように丸めて言う。"""
    return f"約{v:.0f}秒" if about else f"{v}秒"


# ---------------------------------------------------------------------------
# 音声botの構成: 前のページの図（bot-overview.svg）の bot の部分を開いて、ECSタスクの中身を見せる
# ---------------------------------------------------------------------------
# bot-overview.svg に合わせる色と形（ECS Fargate の箱、文字起こし・読み上げの矢印、Discord の枠）
OV_ECS, OV_ECS_BG = "#E67E22", "#FEF5EC"
OV_DISCORD, OV_STT, OV_TTS = "#5865F2", "#2F6FB3", "#8B5CF6"


def _overview_parts() -> tuple[str, str, str]:
    """bot-overview.svg から、defs・図の中身・bot の部分（音声bot 2つ・矢印・ECS Fargate の箱）を取り出す。"""
    src = (OUT / "bot-overview.svg").read_text()
    defs = re.search(r"<defs>(.*?)</defs>", src, re.S).group(1)
    body = re.search(r"</defs>(.*)</svg>", src, re.S).group(1)
    picks = []
    for begin, stop in (
        ('<clipPath id="c270">', ">音声bot</text>"),
        ('<clipPath id="c580">', ">音声bot</text>"),
        ('<rect x="140" y="350"', ">音声botが動く</text>"),
    ):
        i = body.index(begin)
        picks.append(body[i : body.index(stop, i) + len(stop)])
    picks += re.findall(r'<path d="M(?:270|580),292[^>]*/>', body)
    return defs, body, "".join(picks)


def _prefix_ids(s: str, prefix: str) -> str:
    s = re.sub(r'\bid="([^"]+)"', rf'id="{prefix}\1"', s)
    return re.sub(r"url\(#([^)]+)\)", rf"url(#{prefix}\1)", s)


def bot_task() -> str:
    b = []
    defs, body, picks = _overview_parts()
    k, ox, oy = 0.62, 0, 72  # 前の図を縮めて左に置く
    # 前の図は薄く敷き、bot の部分だけ元の濃さで重ねる
    b.append(f'<defs>{_prefix_ids(defs, "ov-")}</defs>')
    b.append(f'<g transform="translate({ox} {oy}) scale({k})" opacity="0.28">{_prefix_ids(body, "ov-")}</g>')
    b.append(f'<g transform="translate({ox} {oy}) scale({k})">{_prefix_ids(picks, "hl-")}</g>')

    # ECS Fargate の箱（前の図の座標 140,350 300x76）から、右のECSタスクへ広げる
    ex, ey, ew, eh = ox + 140 * k, oy + 350 * k, 300 * k, 76 * k
    px, py, pw, ph = 530, 14, 456, 392
    b.append(
        f'<polygon points="{ex + ew:.1f},{ey:.1f} {px},{py} {px},{py + ph} {ex + ew:.1f},{ey + eh:.1f}" '
        f'fill="{OV_ECS}" fill-opacity="0.10"/>'
    )
    for y0, y1 in ((ey, py), (ey + eh, py + ph)):
        b.append(f'<line x1="{ex + ew:.1f}" y1="{y0:.1f}" x2="{px}" y2="{y1}" stroke="{OV_ECS}" stroke-width="1.5" stroke-opacity="0.7"/>')
    b.append(f'<rect x="{ex - 3:.1f}" y="{ey - 3:.1f}" width="{ew + 6:.1f}" height="{eh + 6:.1f}" rx="10" fill="none" stroke="{OV_ECS}" stroke-width="2.5"/>')

    # ECSタスクの中身（前の図の ECS Fargate の箱と同じ色）
    b.append(box(px, py, pw, ph, stroke=OV_ECS, fill=OV_ECS_BG, rx=14))
    b.append(FARGATE(px + 20, py + 16, 30))
    b.append(text(px + 60, py + 39, "音声botのECSタスク（Fargate）", size=18, fill="#B85700", bold=True))
    items = [
        ("Discord botコンテナ", "Discordとやりとりする", OV_DISCORD),
        ("読み上げコンテナ", "VOICEVOX", OV_TTS),
        ("文字起こしコンテナ", "", OV_STT),
    ]
    for i, (name, note, color) in enumerate(items):
        x, y, w, h = px + 24, py + 66 + i * 106, pw - 48, 92
        b.append(box(x, y, w, h, stroke=color))
        b.append(CONTAINER(x + 18, y + h / 2 - 28, 56))
        if note:
            b.append(text(x + 92, y + 40, name, size=20, bold=True))
            b.append(text(x + 92, y + 67, note, size=15, fill=SUB))
        else:
            b.append(text(x + 92, y + h / 2 + 7, name, size=20, bold=True))
    return svg(1000, 420, b)


# ---------------------------------------------------------------------------
# 最初の分析: 改善前の内訳
# ---------------------------------------------------------------------------
def chart_breakdown() -> str:
    # 改善前の起動を、区間ごとに1段ずつ下へずらしたタイムラインで並べる（2026-11-16 修正依頼84）。
    # 順番と「その他」の長さは LT #40 の記録
    # （準備 → 取得 37.5秒 → 取得後 8.0秒 → 読み上げコンテナの起動 0.8秒 → Discord botコンテナの起動 1.5秒 → VC接続 0.9秒）による。
    # 「コンテナ作成」は取得後 8.0秒の中にあるが、単独の実測値はないので秒数を書かず、灰色（その他の起動処理）の段として位置だけ見せる。
    # ヘルスチェック待ちは改善済みの値を出すので区切りに入れない（2026-11-16 本人）。
    # 全体が約77秒になるよう、最初の「その他」の長さを残りで決める。
    prep = BEFORE["total"] - BEFORE["pull"] - BEFORE["voice"] - BEFORE["bot"] - 8.0 - 0.9
    rows = [
        ("other", prep, "その他の起動処理", ""),
        ("pull", BEFORE["pull"], "イメージのプル", f"{BEFORE['pull']}秒"),
        ("other", 8.0, "コンテナ作成など", ""),
        ("voice", BEFORE["voice"], "読み上げコンテナの起動", f"{BEFORE['voice']}秒"),
        ("bot", BEFORE["bot"], "Discord botコンテナの起動", f"{BEFORE['bot']}秒"),
        ("other", 0.9, "その他の起動処理", ""),
    ]
    color = {"other": "#c3cad3", "pull": RED, "voice": GREEN, "bot": GREEN}
    x0, width = 290, 610
    k = width / BEFORE["total"]
    top, pitch, bh = 64, 34, 22
    b = []
    # 全体
    b.append(f'<path d="M{x0},38 L{x0},54 M{x0},46 L{x0 + width},46 M{x0 + width},38 L{x0 + width},54" stroke="{INK}" stroke-width="2" fill="none"/>')
    b.append(f'<rect x="{x0 + width / 2 - 80}" y="30" width="160" height="32" fill="#fff"/>')
    b.append(text(x0 + width / 2, 54, f"全体 {fmt(BEFORE['total'], True)}", size=20, bold=True, anchor="middle"))
    bottom = top + len(rows) * pitch
    x = x0
    for i, (key, v, label, sec) in enumerate(rows):
        y = top + i * pitch + (pitch - bh) / 2
        w = max(v * k, 5)
        # 区間の境目を縦の点線でつなぎ、時間の流れを追えるようにする
        if i > 0:
            b.append(f'<path d="M{x:.1f},{y - (pitch - bh) - 2:.1f} L{x:.1f},{y:.1f}" stroke="{DASH}" stroke-width="1.5" stroke-dasharray="3 3"/>')
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{bh}" rx="3" fill="{color[key]}"/>')
        main = key != "other"
        b.append(text(x0 - 16, y + bh / 2 + 6, label, size=18 if main else 16, fill={"pull": RED, "other": SUB}.get(key, GREEN), anchor="end", bold=main))
        if key == "pull":
            b.append(text(x + w / 2, y + bh / 2 + 7, sec, size=19, fill="#fff", anchor="middle", bold=True))
        elif sec:
            b.append(text(x + w + 10, y + bh / 2 + 7, sec, size=19, fill=GREEN, bold=True))
        x += w
    ay = bottom + 16
    b.append(arrow(f"M{x0},{ay} L{x0 + width - 2},{ay}", SUB, "Sub", 2))
    b.append(text(x0, ay + 26, "起動の開始", size=15, fill=SUB))
    b.append(text(x0 + width, ay + 26, "ボイスチャンネルに入る", size=15, fill=SUB, anchor="end"))
    return svg(1000, ay + 36, b)


# ---------------------------------------------------------------------------
# SOCIとは？: pull → create → start
# ---------------------------------------------------------------------------
def layers(x, y, w, n=3, h=22, gap=6, picks=()) -> list[str]:
    """イメージレイヤーを重ねた絵。picks の (段, 位置) に必要なファイルの印を付ける。"""
    out = []
    for i in range(n):
        yy = y + i * (h + gap)
        out.append(f'<rect x="{x}" y="{yy}" width="{w}" height="{h}" rx="4" fill="#f4f6f8" stroke="{LINE}" stroke-width="2"/>')
    for row, pos in picks:
        yy = y + row * (h + gap)
        out.append(f'<rect x="{x + pos:.1f}" y="{yy + 5}" width="22" height="{h - 10}" rx="2" fill="{GREEN}"/>')
    return out


def soci_lifecycle() -> str:
    b = []
    # ECRリポジトリ
    b.append(box(20, 20, 960, 150, rx=14))
    b.append(ECR(40, 34, 30))
    b.append(text(80, 56, "ECRリポジトリ", size=17, bold=True))
    # SOCIインデックス（左）
    b.append(box(60, 78, 220, 72, stroke=RED, fill=RED_BG, rx=10))
    b.append(text(170, 121, "SOCIインデックス", size=17, fill=RED, bold=True, anchor="middle"))
    # コンテナイメージ（右）
    b.append(text(420, 98, "コンテナイメージ", size=16, bold=True))
    b += layers(420, 108, 520, n=2, h=20, gap=6, picks=[(0, 398), (1, 120)])
    # ライフサイクル
    cy = 262
    xs = {"pull": 170, "create": 500, "start": 830}
    pc = {"pull": RED, "create": SUB, "start": GREEN}
    for k, cx in xs.items():
        b.append(pill(cx, cy, k, fill=pc[k]))
    b.append(arrow(f"M{xs['pull'] + 50},{cy} L{xs['create'] - 52},{cy}"))
    b.append(arrow(f"M{xs['create'] + 50},{cy} L{xs['start'] - 52},{cy}"))
    notes = {"pull": "イメージを持ってくる", "create": "コンテナの器を用意する", "start": "コンテナを起動する"}
    for k, cx in xs.items():
        b.append(text(cx, cy + 46, notes[k], size=17, fill=SUB, anchor="middle"))
    # 読むもの
    b.append(arrow(f"M170,152 L170,{cy - 18}", RED, "Red"))
    b.append(text(184, 214, "最低限だけ読み込む", size=17, fill=RED, bold=True))
    b.append(arrow(f"M830,156 L830,{cy - 18}", GREEN, "Green"))
    b.append(text(816, 214, "必要なファイルを読み取る", size=17, fill=GREEN, bold=True, anchor="end"))
    return svg(1000, 326, b)


# ---------------------------------------------------------------------------
# 仕組み①: 3つの言葉（レイヤー・span・zTOC）
# ---------------------------------------------------------------------------
def soci_terms() -> str:
    b = []
    # 左: イメージはレイヤーを重ねたもの
    b.append(text(110, 92, "コンテナイメージ", size=17, bold=True, anchor="middle"))
    for i in range(3):
        y = 108 + i * 50
        hl = i == 2
        b.append(box(30, y, 160, 42, stroke=INK if hl else LINE, fill="#f4f6f8", rx=6))
        b.append(text(110, y + 28, "レイヤー", size=17, fill=INK if hl else SUB, anchor="middle", bold=hl))
    b.append(f'<path d="M190,208 L300,108 M190,250 L300,300" stroke="{DASH}" stroke-width="2" stroke-dasharray="6 5" fill="none"/>')
    # 右: 1つのレイヤー（TARアーカイブを圧縮したもの）を span に区切る
    lx, lw = 300, 670
    b.append(box(lx, 108, lw, 192, stroke=INK, fill="#f4f6f8", rx=10))
    b.append(text(lx + 18, 136, "レイヤー（TARアーカイブを圧縮したもの）", size=17, bold=True))
    n = 6
    sw = (lw - 36 - (n - 1) * 8) / n
    xs = []
    for i in range(n):
        x = lx + 18 + i * (sw + 8)
        xs.append(x)
        hl = i == 4
        b.append(box(x, 210, sw, 52, stroke=GREEN if hl else LINE, fill=GREEN_BG if hl else "#fff", rx=6))
        b.append(text(x + sw / 2, 243, "span", size=17, fill=GREEN if hl else SUB, anchor="middle", bold=hl, mono=True))
    b.append(text(lx + lw / 2, 288, "span：zTOCがレイヤーを区切った単位", size=15, fill=GREEN, anchor="middle", bold=True))
    # 上: zTOC（レイヤーのインデックス）
    zx, zw = 560, 410
    b.append(box(zx, 4, zw, 76, stroke=RED, fill=RED_BG, rx=10))
    b.append(text(zx + 18, 32, "zTOC（レイヤーのインデックス）", size=17, fill=RED, bold=True))
    b.append(text(zx + 18, 62, "どのファイルが、レイヤーの中のどこにあるか", size=15, fill=INK))
    sx = xs[4] + sw / 2
    b.append(arrow(f"M{sx:.1f},82 L{sx:.1f},206", RED, "Red"))
    return svg(1000, 306, b)


# ---------------------------------------------------------------------------
# 仕組み②: コンテナ起動の流れ（遅延読み込みなし と SOCI）
# ---------------------------------------------------------------------------
def soci_compare() -> str:
    b = []
    x0 = 230
    rows = [
        ("遅延読み込みなし", [("pull", 380), ("create", 110), ("start", 90)], 40,
         "イメージ全体を取得して、レイヤーを全部展開。ファイルが全部そろってからコンテナを作成"),
        ("SOCI", [("pull", 110), ("create", 110), ("start", 250)], 170,
         "イメージ全体は取得しない。全てのレイヤーを取得していない状態でコンテナを作成"),
    ]
    for label, segs, y, note in rows:
        b.append(text(20, y + 8, label, size=19, bold=True))
        x = x0
        for k, w in segs:
            fill = RED if k == "pull" else (GREEN if k == "start" else SUB)
            b.append(f'<rect x="{x}" y="{y - 22}" width="{w - 6}" height="44" rx="8" fill="{fill}"/>')
            b.append(text(x + (w - 6) / 2, y + 7, k, size=17, fill="#fff", anchor="middle", bold=True, mono=True))
            x += w
        b.append(text(x0, y + 52, note, size=16, fill=SUB))
    return svg(1000, 236, b)


# ---------------------------------------------------------------------------
# 仕組み③: プル時と起動時に何を取得するか
# ---------------------------------------------------------------------------
def soci_mechanism() -> str:
    b = []
    # ECRリポジトリ
    b.append(box(20, 20, 560, 400, rx=14))
    b.append(ECR(40, 34, 30))
    b.append(text(80, 56, "ECRリポジトリ", size=17, bold=True))
    # SOCIインデックス
    b.append(box(44, 80, 512, 92, stroke=RED, fill=RED_BG, rx=10))
    b.append(text(62, 106, "SOCIインデックス", size=16, fill=RED, bold=True))
    for i in range(3):
        x = 62 + i * 100
        b.append(f'<rect x="{x}" y="122" width="86" height="34" rx="6" fill="#fff" stroke="{RED}" stroke-width="2"/>')
        b.append(text(x + 43, 145, "zTOC", size=15, fill=RED, anchor="middle", bold=True, mono=True))
    b.append(text(366, 145, "レイヤーのインデックス", size=15, fill=SUB))
    # レイヤー
    b.append(text(44, 206, "レイヤー", size=16, bold=True))
    # 小さいレイヤー（丸ごと）
    b.append(f'<rect x="44" y="222" width="512" height="38" rx="6" fill="#f4f6f8" stroke="{LINE}" stroke-width="2"/>')
    b.append(text(300, 247, "10MiB未満の小さいレイヤー", size=16, fill=SUB, anchor="middle"))
    # 大きいレイヤー（span に区切る）
    for r, y in enumerate((280, 336)):
        for i in range(6):
            x = 44 + i * 86
            hl = r == 0 and i == 5
            b.append(
                f'<rect x="{x}" y="{y}" width="80" height="40" rx="6" fill="{GREEN_BG if hl else "#f4f6f8"}" '
                f'stroke="{GREEN if hl else LINE}" stroke-width="2"/>'
            )
            b.append(text(x + 40, y + 26, "span", size=15, fill=GREEN if hl else SUB, anchor="middle", bold=hl, mono=True))
    b.append(text(300, 404, "zTOCがレイヤーをspanに区切っている", size=15, fill=SUB, anchor="middle"))
    # 右: プル時 / 起動時
    b.append(box(700, 90, 270, 120))
    b.append(pill(835, 126, "pull", fill=RED))
    b.append(text(835, 182, "最小限のファイルを取得", size=18, anchor="middle", bold=True))
    b.append(box(700, 270, 270, 120))
    b.append(pill(835, 306, "start", fill=GREEN))
    b.append(text(835, 352, "足りないものを", size=18, anchor="middle", bold=True))
    b.append(text(835, 376, "span単位で取得", size=18, anchor="middle", bold=True))
    b.append(arrow("M556,126 L698,126", RED, "Red"))
    b.append(arrow("M556,241 L630,241 L630,174 L698,174", RED, "Red"))
    b.append(arrow("M556,300 L698,300", GREEN, "Green"))
    b.append(text(627, 288, "zTOCから探す", size=15, fill=GREEN, anchor="middle", bold=True))
    return svg(1000, 440, b)


# ---------------------------------------------------------------------------
# SOCI後の振り返り
# ---------------------------------------------------------------------------
BAR_X, SCALE = 230, 7.6  # 77秒 → 約585px


def chart_soci() -> str:
    items = [("total", "全体", INK), ("pull", "イメージのプル", RED), ("voice", "読み上げコンテナの起動", GREEN), ("bot", "Discord botコンテナの起動", GREEN)]
    # 項目名が長い（「Discord botコンテナの起動」）ので、この図だけ棒の始まりを右に寄せる
    BAR_X = 310
    b = []
    b.append(bar(BAR_X, 6, 22, 16, LINE))
    b.append(text(BAR_X + 30, 20, "改善前", size=16, fill=SUB))
    b.append(bar(BAR_X + 110, 6, 22, 16, INK))
    b.append(text(BAR_X + 140, 20, "SOCIインデックスを使った起動", size=16, fill=SUB))
    y = 46
    for key, label, color in items:
        bv, av = BEFORE[key], SOCI[key]
        b.append(text(20, y + 33, label, size=20, bold=True))
        b.append(bar(BAR_X, y, bv * SCALE, 18, LINE))
        b.append(text(BAR_X + bv * SCALE + 10, y + 16, fmt(bv, key == "total"), size=17, fill=SUB))
        b.append(bar(BAR_X, y + 24, av * SCALE, 26, color))
        b.append(text(BAR_X + av * SCALE + 10, y + 45, fmt(av, key == "total"), size=21, fill=color, bold=True))
        y += 76
    return svg(1000, y - 12, b)


# ---------------------------------------------------------------------------
# 待つ／待たない
# ---------------------------------------------------------------------------
def lanes(after: bool) -> str:
    b = []
    lx, x0 = 20, 230
    yv, yb = 60, 160  # 読み上げコンテナの段 / Discord botコンテナの段
    for y, name in ((yv, "読み上げ"), (yb, "Discord bot")):
        b.append(CONTAINER(lx, y - 20, 40))
        b.append(text(lx + 52, y - 3, name, size=19, bold=True))
        b.append(text(lx + 52, y + 20, "コンテナ", size=19, bold=True))
    # 読み上げコンテナ: 読み込み
    b.append(bar(x0, yv - 20, 420, 40, GREEN, rx=8))
    b.append(text(x0 + 210, yv + 7, "読み込み", size=19, fill="#fff", anchor="middle", bold=True))
    done = x0 + 420
    if not after:
        b.append(f'<path d="M{x0},{yb} L{done - 6},{yb}" stroke="{DASH}" stroke-width="2.5" stroke-dasharray="7 5"/>')
        b.append(f'<rect x="{x0 + 150}" y="{yb - 30}" width="120" height="24" fill="#fff"/>')
        b.append(text(x0 + 210, yb - 12, "待つ", size=17, fill="#8a94a3", anchor="middle"))
        b.append(arrow(f"M{done},{yv + 22} L{done},{yb - 22}", INK, "Ink", 2))
        b.append(text(done + 12, (yv + yb) / 2 + 6, "読み込み完了", size=16, fill=SUB))
        b.append(bar(done, yb - 20, 120, 40, INK, rx=8))
        b.append(text(done + 60, yb + 7, "起動", size=19, fill="#fff", anchor="middle", bold=True))
        b.append(arrow(f"M{done + 122},{yb} L{done + 168},{yb}", INK, "Ink", 2))
        b.append(text(done + 176, yb + 6, "VCに入る", size=18, bold=True))
    else:
        b.append(bar(x0, yb - 20, 120, 40, INK, rx=8))
        b.append(text(x0 + 60, yb + 7, "起動", size=19, fill="#fff", anchor="middle", bold=True))
        b.append(arrow(f"M{x0 + 122},{yb} L{x0 + 156},{yb}", INK, "Ink", 2))
        b.append(text(x0 + 162, yb + 6, "VCに入る", size=17, bold=True))
        b.append(box(x0 + 262, yb - 22, 158, 44, rx=10))
        b.append(text(x0 + 341, yb + 6, "声や文章をためる", size=16, anchor="middle"))
        b.append(arrow(f"M{x0 + 422},{yb} L{done + 60},{yb}", INK, "Ink", 2))
        b.append(arrow(f"M{done},{yv + 22} L{done},{yb - 24}", INK, "Ink", 2))
        b.append(text(done + 70, yb + 6, "準備ができたら流す", size=18, bold=True))
    ay = 230
    b.append(arrow(f"M{x0},{ay} L{980},{ay}", SUB, "Sub", 2))
    b.append(text(980, ay + 24, "時間", size=14, fill=SUB, anchor="end"))
    return svg(1000, ay + 34, b)


# ---------------------------------------------------------------------------
# 全体の推移
# ---------------------------------------------------------------------------
def chart_total() -> str:
    rows = [
        ("改善前", BEFORE["total"], LINE, SUB, fmt(BEFORE["total"], True)),
        ("SOCIインデックス", SOCI["total"], INK, INK, fmt(SOCI["total"], True)),
        ("＋ 待たずに起動", NOWAIT_TOTAL, INK, INK, fmt(NOWAIT_TOTAL)),
    ]
    b = []
    y = 10
    for label, v, color, tcolor, vl in rows:
        b.append(text(20, y + 30, label, size=19, bold=True))
        b.append(bar(BAR_X, y, v * SCALE, 42, color, rx=4))
        b.append(text(BAR_X + v * SCALE + 12, y + 30, vl, size=22, fill=tcolor, bold=True))
        y += 66
    return svg(1000, y - 14, b)


def main() -> None:
    out = {
        "bot-task.svg": bot_task(),
        "chart-breakdown.svg": chart_breakdown(),
        "soci-lifecycle.svg": soci_lifecycle(),
        "soci-terms.svg": soci_terms(),
        "soci-compare.svg": soci_compare(),
        "soci-mechanism.svg": soci_mechanism(),
        "chart-soci.svg": chart_soci(),
        "wait-before.svg": lanes(after=False),
        "wait-after.svg": lanes(after=True),
        "chart-total.svg": chart_total(),
    }
    for name, s in out.items():
        (OUT / name).write_text(s)
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
