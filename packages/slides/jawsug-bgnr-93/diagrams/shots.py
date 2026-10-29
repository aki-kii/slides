"""導入のスクショを切り出し、IDやARNを黒塗りして public/images/story/ に置く。"""

  python3 diagrams/shots.py /workspace/bgnr93/console-shots public/images/story

new-03 の ID・ARN（アカウント ID を含む）・ロックトークンは黒塗りしてから切り出す。
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

make("manual-sheet.png", "manual-sheet.png", (0, 0, 1609, 1500), k=1, width=1609)
make("manual-sheet.png", "manual-step5.png", (412, 806, 992, 852), k=1, width=1609)
make("old-03-ipset-detail.png", "old-ipset-detail.png", (330, 100, 1935, 1178),
     frames=[(1505, 612, 1856, 666)])
make("new-03-ipset-detail.png", "new-ipset-detail.png", (440, 68, 1990, 1157),
     masks=[(1484, 266, 1932, 339), (1484, 394, 1932, 526), (1484, 581, 1932, 652)],
     frames=[(1724, 80, 1958, 134)])
make("new-05-ipset-edit-addresses.png", "new-ipset-edit.png", (480, 180, 1960, 1000),
     frames=[(505, 818, 1350, 876)])
