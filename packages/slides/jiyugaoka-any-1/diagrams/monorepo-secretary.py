"""みのるん式の図（diagrams/monorepo-secretary.svg）を作る。

左に僕（トモコレ風の本人アイコン）、真ん中にAI秘書（Muse の公式キャラクター Jolly）、右にGitリポジトリ。
僕がAI秘書に細かい依頼を雑多に投げ、AI秘書がGitリポジトリで情報やスキルを確認する流れ。
画像は MonorepoSecretaryFigure が ?raw で取り込めるよう、縮めた PNG を base64 で SVG に埋め込む。

    python3 diagrams/monorepo-secretary.py   # デッキのディレクトリで
"""

import base64
import io
from pathlib import Path

from PIL import Image

DECK = Path(__file__).resolve().parent.parent
OUT = DECK / "diagrams" / "monorepo-secretary.svg"

INK = "#2c3e50"
SUB = "#6b7684"
LINE = "#c9d0d9"
GREEN = "#0E8A6E"
GREEN_BG = "#e9f5f1"
FONT = "'Noto Sans JP', 'Hiragino Sans', sans-serif"


def png_data(path, crop=None, size=200):
    im = Image.open(path).convert("RGBA")
    if crop:
        im = im.crop(crop)
    im.thumbnail((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def avatar(cx, cy, r, href, clip_id):
    return (
        f'<clipPath id="{clip_id}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
        f'<image x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" href="{href}" '
        f'clip-path="url(#{clip_id})" preserveAspectRatio="xMidYMid slice"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="2"/>'
    )


def pill(x, y, text, font=13):
    w = len(text) * font + 22
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>'
        f'<text x="{x + w / 2}" y="{y + 15}" font-size="{font}" fill="{INK}" text-anchor="middle" '
        f'dominant-baseline="central">{text}</text>'
    )


def text(x, y, s, size, color=INK, weight=400, anchor="middle"):
    w = ' font-weight="700"' if weight == 700 else ""
    return f'<text x="{x}" y="{y}" font-size="{size}"{w} fill="{color}" text-anchor="{anchor}">{s}</text>'


me = png_data(DECK / "public/images/aboutme/me-icon.png", crop=(0, 120, 640, 760))
muse = png_data(DECK / "public/images/muse/jolly.png")

# 横の並び。僕 → AI秘書 → Gitリポジトリの2本の矢印が同じ長さになるよう、AI秘書の位置を計算で決める
# （僕のアイコンとGitリポジトリの枠は幅が違うので、中心ではなく要素の間の空きをそろえる）
CY = 160
ME_X, ME_R = 70, 56
MUSE_R = 60
REPO_X, REPO_W = 778, 212
TAIL_GAP = 6  # 矢印の根元と要素の間
HEAD_GAP = 3  # 矢じりの先と要素の間
A1_X1 = ME_X + ME_R + TAIL_GAP
A2_X2 = REPO_X - HEAD_GAP
# (MUSE_X - MUSE_R - HEAD_GAP) - A1_X1 == A2_X2 - (MUSE_X + MUSE_R + TAIL_GAP)
MUSE_X = (A1_X1 + A2_X2 + HEAD_GAP - TAIL_GAP) / 2
A1_X2 = MUSE_X - MUSE_R - HEAD_GAP
A2_X1 = MUSE_X + MUSE_R + TAIL_GAP
assert A1_X2 - A1_X1 == A2_X2 - A2_X1
REPO_CX = REPO_X + REPO_W / 2

# 僕からAI秘書への細かい依頼。カテゴリで整理せず、ばらけた位置に置く
requests = [
    (90, 26, "睡眠の記録"),
    (215, 26, "スライド作成の依頼"),
    (130, 74, "献立作成の依頼"),
    (300, 74, "体重の記録"),
    (120, 216, "筋トレの記録"),
    (250, 216, "買い物リスト作成"),
    (60, 264, "筋トレメニューの相談"),
    (248, 264, "食事の栄養チェック"),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 305" width="100%" font-family="{FONT}">',
    "<defs>"
    '<marker id="monorepo-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">'
    f'<path d="M0,0 L6,3 L0,6 Z" fill="{INK}"/></marker>'
    "</defs>",
    # 左: 僕
    avatar(ME_X, CY, ME_R, me, "monorepo-me"),
    text(ME_X, 244, "僕", 19, weight=700),
    # 依頼（僕 → AI秘書）
    *[pill(x, y, s, font=15) for x, y, s in requests],
    f'<line x1="{A1_X1}" y1="{CY}" x2="{A1_X2}" y2="{CY}" stroke="{INK}" stroke-width="2.5" marker-end="url(#monorepo-arr)"/>',
    text((A1_X1 + A1_X2) / 2, 150, "僕がAI秘書に依頼する", 15),
    # 真ん中: AI秘書（Muse の公式キャラクター Jolly）
    avatar(MUSE_X, CY, MUSE_R, muse, "monorepo-muse"),
    text(MUSE_X, 250, "AI秘書", 21, weight=700),
    text(MUSE_X, 277, "（Muse）", 16, color=SUB),
    # AI秘書 → Gitリポジトリ
    f'<line x1="{A2_X1}" y1="{CY}" x2="{A2_X2}" y2="{CY}" stroke="{INK}" stroke-width="2.5" marker-end="url(#monorepo-arr)"/>',
    text((A2_X1 + A2_X2) / 2, 128, "AI秘書が情報や", 14),
    text((A2_X1 + A2_X2) / 2, 147, "スキルを確認する", 14),
    # 右: Gitリポジトリ（主役の緑）
    f'<rect x="{REPO_X}" y="22" width="{REPO_W}" height="270" rx="14" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>',
    text(REPO_X + 18, 55, "Gitリポジトリ", 18, color=GREEN, weight=700, anchor="start"),
    f'<rect x="{REPO_X + 14}" y="70" width="184" height="98" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    text(REPO_CX, 98, "情報", 17, weight=700),
    text(REPO_CX, 124, "睡眠・体重・食事の記録", 13, color=SUB),
    text(REPO_CX, 147, "これまでに決めたこと", 13, color=SUB),
    f'<rect x="{REPO_X + 14}" y="180" width="184" height="98" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    text(REPO_CX, 208, "スキル", 17, weight=700),
    text(REPO_CX, 234, "記録の付け方", 13, color=SUB),
    text(REPO_CX, 257, "献立やスライドの作り方", 13, color=SUB),
    "</svg>",
]

OUT.write_text("\n".join(parts) + "\n")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
