"""みのるん式の図（diagrams/monorepo-secretary.svg）を作る。

左に僕（トモコレ風の本人アイコン）、真ん中にAI秘書（まめだいふく）、右にGitリポジトリ。
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
muse = png_data(DECK / "public/images/muse/mamedaifuku.png")

# 僕からAI秘書への細かい依頼。カテゴリで整理せず、ばらけた位置に置く
requests = [
    (160, 26, "睡眠の記録"),
    (290, 26, "スライド作成の依頼"),
    (200, 74, "献立作成の依頼"),
    (372, 74, "体重の記録"),
    (156, 216, "筋トレの記録"),
    (300, 216, "買い物リスト作成"),
    (176, 264, "食事の栄養チェック"),
    (346, 264, "筋トレメニューの相談"),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 305" width="100%" font-family="{FONT}">',
    "<defs>"
    '<marker id="monorepo-arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">'
    f'<path d="M0,0 L6,3 L0,6 Z" fill="{INK}"/></marker>'
    "</defs>",
    # 左: 僕
    avatar(80, 160, 56, me, "monorepo-me"),
    text(80, 244, "僕", 19, weight=700),
    # 依頼（僕 → AI秘書）
    *[pill(x, y, s, font=15) for x, y, s in requests],
    f'<line x1="142" y1="160" x2="514" y2="160" stroke="{INK}" stroke-width="2.5" marker-end="url(#monorepo-arr)"/>',
    text(328, 150, "僕がAI秘書に依頼する", 15),
    # 真ん中: AI秘書（まめだいふく）
    avatar(580, 160, 60, muse, "monorepo-muse"),
    text(580, 250, "AI秘書", 21, weight=700),
    text(580, 277, "（Muse）", 16, color=SUB),
    # AI秘書 → Gitリポジトリ
    f'<line x1="644" y1="160" x2="772" y2="160" stroke="{INK}" stroke-width="2.5" marker-end="url(#monorepo-arr)"/>',
    text(708, 128, "AI秘書が情報や", 14),
    text(708, 147, "スキルを確認する", 14),
    # 右: Gitリポジトリ（主役の緑）
    f'<rect x="775" y="22" width="212" height="270" rx="14" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>',
    text(793, 55, "Gitリポジトリ", 18, color=GREEN, weight=700, anchor="start"),
    f'<rect x="789" y="70" width="184" height="98" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    text(881, 98, "情報", 17, weight=700),
    text(881, 124, "睡眠・体重・食事の記録", 13, color=SUB),
    text(881, 147, "これまでに決めたこと", 13, color=SUB),
    f'<rect x="789" y="180" width="184" height="98" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    text(881, 208, "スキル", 17, weight=700),
    text(881, 234, "記録の付け方", 13, color=SUB),
    text(881, 257, "献立やスライドの作り方", 13, color=SUB),
    "</svg>",
]

OUT.write_text("\n".join(parts) + "\n")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
