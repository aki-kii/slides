"""コンテナ支部 #31 の図を作る。

    python3 diagrams/charts.py   # パッケージのディレクトリで

public/images/ に次の SVG を書き出す。見た目は life の tasks/speaking/diagram-style.md に従う。
- bot-task.svg        : 音声botの構成（前のページの bot-overview.svg の bot の部分を開いて、1つのECSタスクに3つのコンテナ）
- chart-breakdown.svg : 最初の分析（改善前の起動の内訳を1本のタイムラインで）
- soci-terms.svg      : 仕組みの3つの言葉（レイヤー・span・zTOC）
- soci-compare.svg    : SOCIとは？ コンテナ起動の流れ（遅延読み込みなし と SOCI。pull・create・start をECSタスクの枠で囲む）
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


def ECS(x, y, s):
    return icon(AWS / "ecs.svg", x, y, s)


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

    # ECS Fargate の箱（前の図の座標 140,350 300x76）から、右のECSタスクへ細い点線でつなぐだけにする
    # （塗りの広がりと太い縁取りは「ちょっと大げさかも？」で外した。2026-11-16 本人）
    ex, ey, ew, eh = ox + 140 * k, oy + 350 * k, 300 * k, 76 * k
    px, py, pw, ph = 530, 14, 456, 392
    for y0, y1 in ((ey, py), (ey + eh, py + ph)):
        b.append(f'<line x1="{ex + ew:.1f}" y1="{y0:.1f}" x2="{px}" y2="{y1}" stroke="{DASH}" stroke-width="1.5" stroke-dasharray="5 4"/>')

    # ECSタスクの中身（前の図の ECS Fargate の箱と同じ色）
    b.append(box(px, py, pw, ph, stroke=OV_ECS, fill=OV_ECS_BG, rx=14))
    b.append(TASK(px + 20, py + 16, 30))
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
        ("other", prep, "ECSタスクの立ち上げ処理など", ""),
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


def chart_breakdown_after() -> str:
    # SOCIインデックスを入れた後の起動を、改善前と同じ並べ方でタイムラインにする（2026-11-16 ページ追加依頼）。
    # 秒数を書くのは実測のある全体・プル・読み上げ・botだけ。「コンテナ作成など」と最後の区間は改善前と同じ置き方。
    prep = SOCI["total"] - SOCI["pull"] - SOCI["voice"] - SOCI["bot"] - 8.0 - 0.9
    rows = [
        ("other", prep, "ECSタスクの立ち上げ処理など", ""),
        ("pull", SOCI["pull"], "イメージのプル", f"{SOCI['pull']}秒"),
        ("other", 8.0, "コンテナ作成など", ""),
        ("voice", SOCI["voice"], "読み上げコンテナの起動", f"{SOCI['voice']}秒"),
        ("bot", SOCI["bot"], "Discord botコンテナの起動", f"{SOCI['bot']}秒"),
        ("other", 0.9, "その他の起動処理", ""),
    ]
    color = {"other": "#c3cad3", "pull": RED, "voice": GREEN, "bot": GREEN}
    x0, width = 290, 610
    k = width / SOCI["total"]
    top, pitch, bh = 64, 34, 22
    b = []
    b.append(f'<path d="M{x0},38 L{x0},54 M{x0},46 L{x0 + width},46 M{x0 + width},38 L{x0 + width},54" stroke="{INK}" stroke-width="2" fill="none"/>')
    b.append(f'<rect x="{x0 + width / 2 - 80}" y="30" width="160" height="32" fill="#fff"/>')
    b.append(text(x0 + width / 2, 54, f"全体 {fmt(SOCI['total'], True)}", size=20, bold=True, anchor="middle"))
    bottom = top + len(rows) * pitch
    x = x0
    for i, (key, v, label, sec) in enumerate(rows):
        y = top + i * pitch + (pitch - bh) / 2
        w = max(v * k, 5)
        if i > 0:
            b.append(f'<path d="M{x:.1f},{y - (pitch - bh) - 2:.1f} L{x:.1f},{y:.1f}" stroke="{DASH}" stroke-width="1.5" stroke-dasharray="3 3"/>')
        b.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{bh}" rx="3" fill="{color[key]}"/>')
        main = key != "other"
        b.append(text(x0 - 16, y + bh / 2 + 6, label, size=18 if main else 16, fill={"pull": RED, "other": SUB}.get(key, GREEN), anchor="end", bold=main))
        if key == "pull":
            b.append(text(x + w + 10, y + bh / 2 + 7, sec, size=19, fill=RED, bold=True))
        elif sec:
            b.append(text(x + w + 10, y + bh / 2 + 7, sec, size=19, fill=GREEN, bold=True))
        x += w
    ay = bottom + 16
    b.append(arrow(f"M{x0},{ay} L{x0 + width - 2},{ay}", SUB, "Sub", 2))
    b.append(text(x0, ay + 26, "起動の開始", size=15, fill=SUB))
    b.append(text(x0 + width, ay + 26, "ボイスチャンネルに入る", size=15, fill=SUB, anchor="end"))
    return svg(1000, ay + 36, b)


# ---------------------------------------------------------------------------
# 仕組み①: 3つの言葉（レイヤー・span・zTOC）
# ---------------------------------------------------------------------------
def soci_terms() -> str:
    # 図を左、説明を右に置くので縦長に組む（2026-11-16 本人「図を左側、右側に説明にしたい」）。
    # レイヤー全体を「コンテナイメージ」の枠で囲み、コンテナのアイコンを付ける（同 本人）。
    b = []
    fx, fy, fw = 20, 10, 560
    # コンテナイメージの枠
    b.append(box(fx, fy, fw, 330, stroke=INK, fill="#f4f6f8", rx=14))
    b.append(CONTAINER(fx + 18, fy + 12, 34))
    b.append(text(fx + 62, fy + 37, "コンテナイメージ", size=19, bold=True))
    # レイヤーを重ねる（一番下のレイヤーを開いて span を見せる）
    lx, lw = fx + 20, fw - 40
    for i in range(2):
        y = fy + 62 + i * 52
        b.append(box(lx, y, lw, 42, rx=8))
        b.append(text(lx + lw / 2, y + 28, "レイヤー", size=17, fill=SUB, anchor="middle"))
    ly, lh = fy + 166, 144
    b.append(box(lx, ly, lw, lh, stroke=INK, rx=8))
    b.append(text(lx + 18, ly + 30, "レイヤー（TARアーカイブを圧縮したもの）", size=17, bold=True))
    n = 5
    sw = (lw - 36 - (n - 1) * 8) / n
    xs = []
    for i in range(n):
        x = lx + 18 + i * (sw + 8)
        xs.append(x)
        hl = i == 3
        b.append(box(x, ly + 50, sw, 48, stroke=GREEN if hl else LINE, fill=GREEN_BG if hl else "#fff", rx=6))
        b.append(text(x + sw / 2, ly + 81, "span", size=17, fill=GREEN if hl else SUB, anchor="middle", bold=hl, mono=True))
    b.append(text(lx + lw / 2, ly + 128, "zTOCがレイヤーをspanに区切っている", size=15, fill=GREEN, anchor="middle", bold=True))
    # 下: zTOC（レイヤーのインデックス）から span を指す
    zy = 380
    b.append(box(fx, zy, fw, 76, stroke=RED, fill=RED_BG, rx=10))
    b.append(text(fx + 18, zy + 30, "zTOC（レイヤーのインデックス）", size=17, fill=RED, bold=True))
    b.append(text(fx + 18, zy + 60, "どのファイルが、レイヤーの中のどこにあるか", size=15, fill=INK))
    sx = xs[3] + sw / 2
    b.append(arrow(f"M{sx:.1f},{zy - 2} L{sx:.1f},{ly + 100}", RED, "Red"))
    return svg(600, zy + 82, b)


# ---------------------------------------------------------------------------
# SOCIとは？: コンテナ起動の流れ（遅延読み込みなし と SOCI）
# ---------------------------------------------------------------------------
def soci_compare() -> str:
    # pull・create・start を縦に並べる（2026-11-16 本人「縦の図にして」）。説明はスライドの右側に置く。
    b = []
    W = 560
    # ECSタスク（pull・create・start を囲む。音声botの構成の図と同じ色）
    top, H = 10, 470
    b.append(box(70, top, W - 90, H - 20, stroke=OV_ECS, fill=OV_ECS_BG, rx=14))
    b.append(ECS(86, top + 10, 30))
    b.append(text(126, top + 32, "ECSタスク", size=17, fill="#B85700", bold=True))
    cols = [
        ("遅延読み込みなし", [("pull", 230), ("create", 62), ("start", 52)], 205,
         ["イメージ全体を取得して", "レイヤーを全部展開"]),
        ("SOCI", [("pull", 62), ("create", 62), ("start", 150)], 405,
         ["イメージ全体は", "取得しない"]),
    ]
    y0, cw = 104, 150
    for label, segs, cx, note in cols:
        b.append(text(cx, y0 - 22, label, size=19, bold=True, anchor="middle"))
        y = y0
        for k, h in segs:
            fill = RED if k == "pull" else (GREEN if k == "start" else SUB)
            b.append(f'<rect x="{cx - cw / 2}" y="{y}" width="{cw}" height="{h - 6}" rx="8" fill="{fill}"/>')
            b.append(text(cx, y + (h - 6) / 2 + 6, k, size=17, fill="#fff", anchor="middle", bold=True, mono=True))
            y += h
        for i, line in enumerate(note):
            b.append(text(cx, y + 18 + i * 21, line, size=15, fill=SUB, anchor="middle"))
    # 時間の流れ（上から下）
    b.append(arrow(f"M36,{y0} L36,{y0 + 340}", SUB, "Sub", 2))
    b.append(f'<text x="28" y="{y0 + 170}" font-size="14" fill="{SUB}" text-anchor="middle" '
             f'writing-mode="tb" glyph-orientation-vertical="0">時間</text>')
    return svg(W, H, b)


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
        if key == "total":
            # 全体で縮んだ分を図の中に書く（2026-11-16 本人「全体で29秒〜は図の中に入れよう」）
            ax, ex = BAR_X + av * SCALE, BAR_X + bv * SCALE
            b.append(bar(BAR_X, y + 24, av * SCALE, 26, color))
            b.append(text(ax - 10, y + 44, fmt(av, True), size=19, fill="#fff", anchor="end", bold=True))
            b.append(f'<rect x="{ax + 3:.1f}" y="{y + 25}" width="{ex - ax - 4:.1f}" height="24" rx="3" fill="#fff" '
                     f'stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 4"/>')
            b.append(text((ax + ex) / 2, y + 44, "全体で約29秒短縮", size=18, anchor="middle", bold=True))
        else:
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
        "chart-breakdown-after.svg": chart_breakdown_after(),
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
