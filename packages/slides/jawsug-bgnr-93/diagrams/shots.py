"""導入のスクショを切り出し、IDやARNを黒塗りして public/images/story/ に置く。

  python3 diagrams/shots.py /workspace/bgnr93/console-shots public/images/story

new-03 の ID・ARN（アカウント ID を含む）・ロックトークンは黒塗りしてから切り出す。
"""
import sys
from PIL import Image, ImageDraw
SRC, OUT = sys.argv[1], sys.argv[2]
K = 1.28  # Read で見た表示座標 → 元画像

def px(box, k=K):
    return tuple(round(v * k) for v in box)

def make(name, out, crop, masks=(), frames=(), k=K, width=1600):
    im = Image.open(f"{SRC}/{name}").convert("RGB")
    d = ImageDraw.Draw(im)
    for m in masks:
        d.rectangle(px(m, k), fill="black")
    c = px(crop, k)
    im = im.crop(c)
    w, h = im.size
    for f in frames:
        f = px(f, k)
        l, t, r, b = f[0] - c[0], f[1] - c[1], f[2] - c[0], f[3] - c[1]
        print(f"{out} frame: left:{l/w*100:.1f}% top:{t/h*100:.1f}% width:{(r-l)/w*100:.1f}% height:{(b-t)/h*100:.1f}%")
    if w > width:
        im = im.resize((width, round(h * width / w)), Image.LANCZOS)
    im.save(f"{OUT}/{out}", optimize=True)
    print(out, im.size)

# 手順書は本人が「作業手順」の見出しから No.1〜5 まで切り出した画像を使う。
# 手順3の下に埋め込まれた「Create IP set」の画面は、本人が撮った旧コンソール（old-03）に差し替える。
# 元の manual-steps.png は書き換えず、manual-steps-console.png として別名で書き出す。
def manual_with_old_console():
    sheet = Image.open(f"{SRC}/manual-steps.png").convert("RGB")
    box = (578, 394, 1031, 732)  # 埋め込み画面の範囲（罫線の内側）
    w, h = box[2] - box[0], box[3] - box[1]
    shot = Image.open(f"{SRC}/old-03-ipset-detail.png").convert("RGB")
    # 左メニューの IP sets から IP アドレスの一覧までを、埋め込み画面と同じ縦横比で切り出す
    shot = shot.crop(px((0, 0, 1580, 1178))).resize((w, h), Image.LANCZOS)
    sheet.paste(shot, box[:2])
    sheet.save(f"{OUT}/manual-steps-console.png", optimize=True)
    print("manual-steps-console.png", sheet.size)


manual_with_old_console()
make("manual-steps.png", "manual-step5.png", (578, 778, 1440, 878), k=1, width=1440)
make("old-03-ipset-detail.png", "old-ipset-detail.png", (330, 100, 1935, 1178),
     frames=[(1505, 612, 1856, 666)])
make("new-03-ipset-detail.png", "new-ipset-detail.png", (440, 68, 1990, 1157),
     masks=[(1484, 266, 1932, 339), (1484, 394, 1932, 526), (1484, 581, 1932, 652)],
     frames=[(1724, 80, 1958, 134)])
make("new-05-ipset-edit-addresses.png", "new-ipset-edit.png", (480, 180, 1360, 1000),
     frames=[(505, 818, 1350, 876)])
