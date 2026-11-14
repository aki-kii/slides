"""コンテナ支部 #31 の図を作る。

    python3 diagrams/charts.py   # パッケージのディレクトリで

public/images/ に次の SVG を書き出す。
- chart-breakdown.svg : 最初の分析（改善前の内訳）
- chart-soci.svg      : SOCI 後の振り返り（改善前と同じ項目を並べて比べる）
- chart-total.svg     : 全体の推移（改善前 → SOCI → 待たずに起動）
- soci-flow.svg       : いつもの起動と SOCI の起動の流れ
- soci-mechanism.svg  : SOCI でプル時・起動時に何を取るか

数字は life の構成まとめ（2026-11-15）の値。時間の棒はどの図も同じ縮尺にする。
"""

import base64
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / "public" / "images"
FONT = "'Noto Sans JP', 'Hiragino Sans', sans-serif"

INK = "#2c3e50"
MUTE = "#7f8c8d"
RED = "#e74c3c"
BLUE = "#3498db"
GREEN = "#27ae60"
ORANGE = "#e67e22"
GRAY = "#bdc3c7"

# 改善前とSOCI後の数字（秒）
BEFORE = {"total": 106, "pull": 37.5, "voice": 0.8, "bot": 1.5}
SOCI = {"total": 48.6, "pull": 3.3, "voice": 9.1, "bot": 4.7}
NOWAIT_TOTAL = 32.7

# 棒の縮尺（どの図も同じ）
BAR_X = 210
SCALE = 4.6  # px / 秒  （106秒 → 約488px）


def icon(name: str) -> str:
    raw = (HERE / "icons" / f"{name}.svg").read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()


ICON = {
    "task": icon("ecs-task"),
    "container": icon("ecs-container"),
}

# 項目: キー, ラベル, 色, アイコン
ITEMS = [
    ("total", "全体", INK, "task"),
    ("pull", "イメージの取得", BLUE, "task"),
    ("voice", "読み上げの起動", GREEN, "container"),
    ("bot", "botの起動", ORANGE, "container"),
]


def svg(w: int, h: int, body: list[str]) -> str:
    defs = (
        '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2c3e50"/></marker>'
        '<marker id="arrb" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#3498db"/></marker>'
        '<marker id="arrg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#27ae60"/></marker></defs>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{FONT}">'
        + defs
        + "".join(body)
        + "</svg>\n"
    )


def text(x, y, s, size=16, fill=INK, anchor="start", bold=False) -> str:
    b = ' font-weight="bold"' if bold else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}"{b}>{s}</text>'
    )


def rect(x, y, w, h, fill, rx=3, extra="") -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 3):.1f}" height="{h}" rx="{rx}" fill="{fill}"{extra}/>'


def row_label(y, label, ic, bold=False) -> list[str]:
    return [
        f'<image href="{ICON[ic]}" x="0" y="{y - 17}" width="22" height="22"/>',
        text(30, y, label, size=17, bold=bold),
    ]


def fmt(v: float) -> str:
    return f"約{v:.0f}秒" if v >= 100 else f"{v}秒"


def light(color: str) -> str:
    # 改善前の棒は同じ色を薄くして描く
    return {INK: "#aab7c4", BLUE: "#aed6f1", GREEN: "#a9dfbf", ORANGE: "#f5cba7"}[color]


# ---------------------------------------------------------------------------
# 最初の分析: 改善前の内訳
# ---------------------------------------------------------------------------
def chart_breakdown() -> str:
    body = []
    y = 30
    for key, label, color, ic in ITEMS:
        v = BEFORE[key]
        w = v * SCALE
        body += row_label(y + 19, label, ic, bold=key in ("total", "pull"))
        body.append(rect(BAR_X, y, w, 28, color))
        body.append(text(BAR_X + w + 10, y + 21, fmt(v), size=18, fill=color, bold=True))
        y += 46
    body.append(text(BAR_X, y + 10, "残りは、その他の起動処理", size=16, fill=MUTE))
    return svg(820, y + 20, body)


# ---------------------------------------------------------------------------
# SOCI 後の振り返り: 同じ項目を改善前と並べる
# ---------------------------------------------------------------------------
def chart_soci() -> str:
    body = []
    # 凡例
    body.append(rect(BAR_X, 6, 22, 16, "#aab7c4"))
    body.append(text(BAR_X + 30, 20, "改善前", size=16, fill=MUTE))
    body.append(rect(BAR_X + 110, 6, 22, 16, INK))
    body.append(text(BAR_X + 140, 20, "SOCIインデックスあり", size=16, fill=INK))
    y = 44
    for key, label, color, ic in ITEMS:
        b, a = BEFORE[key], SOCI[key]
        body += row_label(y + 30, label, ic, bold=True)
        body.append(rect(BAR_X, y, b * SCALE, 20, light(color)))
        body.append(text(BAR_X + b * SCALE + 8, y + 16, fmt(b), size=16, fill=MUTE))
        body.append(rect(BAR_X, y + 24, a * SCALE, 24, color))
        sign = "短縮" if a < b else "延びた"
        body.append(
            text(BAR_X + a * SCALE + 8, y + 42, f"{fmt(a)}（{sign}）", size=18, fill=color, bold=True)
        )
        y += 70
    return svg(820, y - 8, body)


# ---------------------------------------------------------------------------
# 全体の推移
# ---------------------------------------------------------------------------
def chart_total() -> str:
    rows = [
        ("改善前", BEFORE["total"], "#aab7c4", MUTE),
        ("SOCIインデックス", SOCI["total"], BLUE, BLUE),
        ("＋ 待たずに起動", NOWAIT_TOTAL, RED, RED),
    ]
    body = []
    y = 10
    for label, v, color, tcolor in rows:
        body.append(f'<image href="{ICON["task"]}" x="0" y="{y + 4}" width="22" height="22"/>')
        body.append(text(30, y + 21, label, size=17, bold=True))
        body.append(rect(BAR_X, y, v * SCALE, 30, color))
        body.append(text(BAR_X + v * SCALE + 10, y + 22, fmt(v), size=20, fill=tcolor, bold=True))
        y += 50
    return svg(820, y - 10, body)


# ---------------------------------------------------------------------------
# SOCI の流れ: いつもの起動と比べて、プルは速いが起動に時間がかかる
# ---------------------------------------------------------------------------
def soci_flow() -> str:
    x0 = 200
    body = []
    # いつもの起動
    body.append(text(0, 33, "いつもの起動", size=18, bold=True))
    body.append(rect(x0, 10, 380, 36, BLUE, rx=4))
    body.append(text(x0 + 190, 34, "プル：イメージを全部取得", size=17, fill="#fff", anchor="middle"))
    body.append(rect(x0 + 386, 10, 90, 36, GREEN, rx=4))
    body.append(text(x0 + 431, 34, "起動", size=17, fill="#fff", anchor="middle"))
    # SOCI
    body.append(text(0, 93, "SOCIインデックス", size=18, bold=True))
    body.append(rect(x0, 70, 130, 36, BLUE, rx=4))
    body.append(text(x0 + 65, 94, "プル：最小限", size=17, fill="#fff", anchor="middle"))
    body.append(rect(x0 + 136, 70, 210, 36, GREEN, rx=4))
    body.append(text(x0 + 241, 94, "起動", size=17, fill="#fff", anchor="middle"))
    body.append(text(x0 + 65, 130, "速くなる", size=17, fill=BLUE, anchor="middle", bold=True))
    body.append(text(x0 + 146, 130, "足りないファイルを取るので長くなる", size=17, fill=GREEN, bold=True))
    return svg(700, 142, body)


# ---------------------------------------------------------------------------
# SOCI の仕組み: プル時に取るもの、起動時に取るもの
# ---------------------------------------------------------------------------
def soci_mechanism() -> str:
    body = []
    # ECR（左）
    body.append(rect(0, 0, 450, 330, "#f8f9fa", rx=8, extra=' stroke="#dee2e6" stroke-width="2"'))
    body.append(text(16, 28, "ECRリポジトリ", size=17, fill=MUTE, bold=True))

    # SOCIインデックス + zTOC
    body.append(rect(16, 44, 418, 74, "#fff", rx=6, extra=' stroke="#3498db" stroke-width="2"'))
    body.append(text(30, 70, "SOCIインデックス", size=17, fill=BLUE, bold=True))
    for i in range(3):
        x = 30 + i * 90
        body.append(rect(x, 80, 80, 28, "#ebf5fb", rx=4, extra=' stroke="#3498db" stroke-width="1.5"'))
        body.append(text(x + 40, 100, "zTOC", size=16, fill=BLUE, anchor="middle"))
    body.append(text(300, 100, "（レイヤーの目次）", size=15, fill=MUTE))

    # イメージレイヤー
    body.append(text(16, 150, "イメージレイヤー", size=17, fill=INK, bold=True))
    # 大きいレイヤー（spanで区切る）
    for li, ly in enumerate((164, 222)):
        body.append(text(16, ly + 24, "大きい", size=15, fill=MUTE))
        for s in range(6):
            x = 70 + s * 60
            hl = li == 0 and s == 5
            fill = "#d5f5e3" if hl else "#fff"
            stroke = GREEN if hl else "#95a5a6"
            body.append(rect(x, ly, 56, 36, fill, rx=3, extra=f' stroke="{stroke}" stroke-width="{2.5 if hl else 1.5}"'))
            body.append(text(x + 28, ly + 24, "span", size=14, fill=GREEN if hl else MUTE, anchor="middle"))
    # 小さいレイヤー
    body.append(text(16, 304, "小さい", size=15, fill=MUTE))
    body.append(rect(70, 282, 116, 34, "#ebf5fb", rx=3, extra=' stroke="#3498db" stroke-width="2"'))
    body.append(text(128, 305, "まるごと", size=15, fill=BLUE, anchor="middle"))

    # コンテナ（右）
    cx = 640
    body.append(rect(cx, 110, 240, 120, "#fff", rx=8, extra=' stroke="#2c3e50" stroke-width="2"'))
    body.append(f'<image href="{ICON["container"]}" x="{cx + 16}" y="126" width="34" height="34"/>')
    body.append(text(cx + 60, 150, "コンテナ", size=18, bold=True))

    # ① プル時: インデックス・zTOC・小さいレイヤー → コンテナ
    body.append(f'<path d="M436,81 C520,81 540,130 {cx - 4},140" stroke="#3498db" stroke-width="2.5" fill="none" marker-end="url(#arrb)"/>')
    body.append(f'<path d="M188,299 C470,299 520,210 {cx - 4},200" stroke="#3498db" stroke-width="2.5" fill="none" marker-end="url(#arrb)"/>')
    body.append(text(468, 34, "① プル時：最小限だけ", size=17, fill=BLUE, bold=True))

    # ② 起動時: zTOC で探して span ごとに取得
    body.append(f'<path d="M430,182 L{cx - 4},182" stroke="#27ae60" stroke-width="2.5" fill="none" stroke-dasharray="6 4" marker-end="url(#arrg)"/>')
    body.append(text(cx + 120, 190, "足りないファイルを", size=15, fill=GREEN, anchor="middle"))
    body.append(text(cx + 120, 210, "zTOCで探して取得", size=15, fill=GREEN, anchor="middle"))
    body.append(text(442, 172, "② 起動時：spanごとに取得", size=15, fill=GREEN, bold=True))
    return svg(890, 332, body)


def main() -> None:
    files = {
        "chart-breakdown.svg": chart_breakdown(),
        "chart-soci.svg": chart_soci(),
        "chart-total.svg": chart_total(),
        "soci-flow.svg": soci_flow(),
        "soci-mechanism.svg": soci_mechanism(),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
