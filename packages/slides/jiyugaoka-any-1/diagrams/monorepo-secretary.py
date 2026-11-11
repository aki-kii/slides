"""みのるん式の図（diagrams/monorepo-secretary.svg）を作る。

左に僕（トモコレ風の本人アイコン）、真ん中にAI秘書（Muse の公式キャラクター Jolly）、右にGitHubのlifeリポジトリ。
僕がAI秘書に細かい依頼を吹き出しでたくさん投げている様子。矢印は描かない。
画像は MonorepoSecretaryFigure が ?raw で取り込めるよう、縮めた PNG を base64 で SVG に埋め込む。

    python3 diagrams/monorepo-secretary.py   # デッキのディレクトリで
"""

import base64
import io
import re
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


def request_bubble(x, y, text, font=15, toward_y=None):
    """依頼の吹き出し。(x, y) を左上とした高さ 30 の角丸の箱に、左（僕の方）を向くしっぽを付ける。"""
    w = len(text) * font + 22
    h, r = 30, 10
    cy = y + h / 2
    # しっぽの先は左へ 10、僕のアイコンの高さの方へ少し傾ける
    tip_y = cy + (4 if toward_y is not None and toward_y > cy else -4 if toward_y is not None else 0)
    d = (
        f"M{x + r},{y} H{x + w - r} Q{x + w},{y} {x + w},{y + r} V{y + h - r} Q{x + w},{y + h} {x + w - r},{y + h} "
        f"H{x + r} Q{x},{y + h} {x},{y + h - r} V{cy + 5} L{x - 10},{tip_y} L{x},{cy - 5} V{y + r} Q{x},{y} {x + r},{y} Z"
    )
    return (
        f'<path d="{d}" fill="#ffffff" stroke="{LINE}" stroke-width="2" stroke-linejoin="round"/>'
        f'<text x="{x + w / 2}" y="{cy}" font-size="{font}" fill="{INK}" text-anchor="middle" '
        f'dominant-baseline="central">{text}</text>'
    )


def github_mark(x, y, size, color=INK):
    # simple-icons@13.21.0 の GitHub のマーク（public/images/icons/github.svg）を単色で埋め込む
    src = (DECK / "public/images/icons/github.svg").read_text()
    d = re.search(r'<path d="([^"]+)"', src).group(1)
    # 入れ子の <svg> は MonorepoSecretaryFigure の CSS（svg を幅 100% にする）が効いてしまうので、<g> で縮めて置く
    return f'<g transform="translate({x} {y}) scale({size / 24})"><path d="{d}" fill="{color}"/></g>'


def text(x, y, s, size, color=INK, weight=400, anchor="middle"):
    w = ' font-weight="700"' if weight == 700 else ""
    return f'<text x="{x}" y="{y}" font-size="{size}"{w} fill="{color}" text-anchor="{anchor}">{s}</text>'


me = png_data(DECK / "public/images/aboutme/me-icon.png", crop=(0, 120, 640, 760))
muse = png_data(DECK / "public/images/muse/jolly.png")

# 横の並び。AI秘書の位置は、矢印があったころに2本の矢印を同じ長さにした位置（x=452）のまま
CY = 160
ME_X, ME_R = 70, 56
MUSE_X, MUSE_R = 452, 60
REPO_X, REPO_W = 778, 212
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
    (254, 264, "食事の栄養チェック"),
]

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 305" width="100%" font-family="{FONT}">',
    # 左: 僕
    avatar(ME_X, CY, ME_R, me, "monorepo-me"),
    text(ME_X, 244, "僕", 19, weight=700),
    # 僕からの依頼の吹き出し（矢印は描かない）
    *[request_bubble(x, y, s, toward_y=CY) for x, y, s in requests],
    # 真ん中: AI秘書（Muse の公式キャラクター Jolly）
    avatar(MUSE_X, CY, MUSE_R, muse, "monorepo-muse"),
    text(MUSE_X, 250, "AI秘書", 21, weight=700),
    text(MUSE_X, 277, "（Muse）", 16, color=SUB),
    # 右: Gitリポジトリ（主役の緑）
    f'<rect x="{REPO_X}" y="22" width="{REPO_W}" height="270" rx="14" fill="{GREEN_BG}" stroke="{GREEN}" stroke-width="2"/>',
    github_mark(REPO_X + 16, 34, 26),
    text(REPO_X + 50, 55, "GitHub", 18, color=GREEN, weight=700, anchor="start"),
    # 枠に収まるよう2行に分ける
    text(REPO_X + 16, 80, "lifeリポジトリ", 13, weight=700, anchor="start"),
    text(REPO_X + 16, 98, "（モノレポ/Private）", 13, color=SUB, anchor="start"),
    f'<rect x="{REPO_X + 14}" y="110" width="184" height="80" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    text(REPO_CX, 133, "情報", 17, weight=700),
    text(REPO_CX, 157, "睡眠・体重・食事の記録", 13, color=SUB),
    text(REPO_CX, 178, "これまでに決めたこと", 13, color=SUB),
    f'<rect x="{REPO_X + 14}" y="200" width="184" height="80" rx="12" fill="#ffffff" stroke="{LINE}" stroke-width="2"/>',
    text(REPO_CX, 223, "スキル", 17, weight=700),
    text(REPO_CX, 247, "記録の付け方", 13, color=SUB),
    text(REPO_CX, 268, "献立やスライドの作り方", 13, color=SUB),
    "</svg>",
]

OUT.write_text("\n".join(parts) + "\n")
print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
