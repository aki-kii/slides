/**
 * スクショを切り抜き・黒塗り・縮小するための、RGB の生画素を持つ画像。
 * 読み書きと縮小だけ sharp に任せ、塗りや切り抜きは画素を直接いじる（結果を毎回同じにするため）。
 */
import sharp from 'sharp';

/** [左, 上, 右, 下]。右と下はその画素を含まない（切り抜き）か含む（塗り）かを関数ごとに書く */
export type Box = readonly [number, number, number, number];

/** Python の round() と同じく、ちょうど .5 のときは偶数に寄せる */
export function roundHalfEven(v: number): number {
  const r = Math.round(v);
  return Math.abs(v % 1) === 0.5 && r % 2 !== 0 ? r - 1 : r;
}

/** 表示座標 → 元画像の座標（Read などで縮小表示した画像から位置を拾ったとき用） */
export function scaleBox(box: Box, k: number): Box {
  return box.map((v) => roundHalfEven(v * k)) as unknown as Box;
}

export class RawImage {
  constructor(
    public data: Buffer,
    public width: number,
    public height: number,
  ) {}

  static async load(path: string): Promise<RawImage> {
    const { data, info } = await sharp(path)
      .removeAlpha()
      .toColourspace('srgb')
      .raw()
      .toBuffer({ resolveWithObject: true });
    return new RawImage(data, info.width, info.height);
  }

  clone(): RawImage {
    return new RawImage(Buffer.from(this.data), this.width, this.height);
  }

  /** [x0, y0, x1, y1] を塗る（x1, y1 の画素も含む） */
  fill(box: Box, rgb: readonly [number, number, number] = [0, 0, 0]): this {
    const [x0, y0, x1, y1] = box;
    for (let y = Math.max(0, y0); y <= Math.min(this.height - 1, y1); y++) {
      for (let x = Math.max(0, x0); x <= Math.min(this.width - 1, x1); x++) {
        const i = (y * this.width + x) * 3;
        this.data[i] = rgb[0];
        this.data[i + 1] = rgb[1];
        this.data[i + 2] = rgb[2];
      }
    }
    return this;
  }

  /** [左, 上, 右, 下) で切り抜く。はみ出したところは黒で埋める */
  crop(box: Box): RawImage {
    const [l, t, r, b] = box;
    const w = r - l;
    const h = b - t;
    const out = Buffer.alloc(w * h * 3);
    for (let y = 0; y < h; y++) {
      const sy = t + y;
      if (sy < 0 || sy >= this.height) continue;
      for (let x = 0; x < w; x++) {
        const sx = l + x;
        if (sx < 0 || sx >= this.width) continue;
        this.data.copy(
          out,
          (y * w + x) * 3,
          (sy * this.width + sx) * 3,
          (sy * this.width + sx) * 3 + 3,
        );
      }
    }
    return new RawImage(out, w, h);
  }

  /** (x, y) に別の画像を重ねる */
  paste(other: RawImage, x: number, y: number): this {
    for (let row = 0; row < other.height; row++) {
      const ty = y + row;
      if (ty < 0 || ty >= this.height) continue;
      other.data.copy(
        this.data,
        (ty * this.width + x) * 3,
        row * other.width * 3,
        (row + 1) * other.width * 3,
      );
    }
    return this;
  }

  async resize(width: number, height: number): Promise<RawImage> {
    const { data, info } = await sharp(this.data, {
      raw: { width: this.width, height: this.height, channels: 3 },
    })
      .resize(width, height, { kernel: 'lanczos3', fit: 'fill' })
      .raw()
      .toBuffer({ resolveWithObject: true });
    return new RawImage(data, info.width, info.height);
  }

  /** 幅が maxWidth を超えるときだけ、縦横比を保って縮める */
  async fitWidth(maxWidth: number): Promise<RawImage> {
    if (this.width <= maxWidth) return this;
    return this.resize(
      maxWidth,
      roundHalfEven((this.height * maxWidth) / this.width),
    );
  }

  async save(path: string): Promise<void> {
    await sharp(this.data, {
      raw: { width: this.width, height: this.height, channels: 3 },
    })
      .png({ compressionLevel: 9 })
      .toFile(path);
  }

  /** 明るさ（Pillow の "L" 変換と同じ式） */
  luma(x: number, y: number): number {
    const i = (y * this.width + x) * 3;
    return (
      (this.data[i] * 19595 +
        this.data[i + 1] * 38470 +
        this.data[i + 2] * 7471 +
        0x8000) >>
      16
    );
  }

  /**
   * box の中の IP アドレスを行ごとに探し、第2・第3オクテットを黒塗りする。
   * 行の中で、幅が狭く下の方にだけ濃い画素がある文字を「.」とみなし、1〜3個目の「.」の間を塗る。
   */
  maskIpOctets(box: Box, threshold = 110): this {
    const [x0, y0, x1, y1] = box;
    const w = x1 - x0;
    const h = y1 - y0;
    const dark = (x: number, y: number) =>
      this.luma(x0 + x, y0 + y) < threshold;
    const rowHasDark = Array.from({ length: h }, (_, y) => {
      for (let x = 0; x < w; x++) if (dark(x, y)) return true;
      return false;
    });
    for (const [a, b] of runs(rowHasDark).filter(([s, e]) => e - s >= 8)) {
      const lineH = b - a;
      const colHasDark = Array.from({ length: w }, (_, x) => {
        for (let y = a; y < b; y++) if (dark(x, y)) return true;
        return false;
      });
      const dots: [number, number][] = [];
      for (const [s, e] of runs(colHasDark)) {
        let top = Infinity;
        for (let y = a; y < b && top === Infinity; y++) {
          for (let x = s; x < e; x++) {
            if (dark(x, y)) {
              top = y - a;
              break;
            }
          }
        }
        if (e - s <= Math.max(3, lineH * 0.3) && top >= lineH * 0.6)
          dots.push([s, e]);
      }
      if (dots.length < 3) continue;
      const [d1, d2, d3] = dots;
      for (const [l, r] of [
        [d1[1], d2[0]],
        [d2[1], d3[0]],
      ]) {
        this.fill([x0 + l, y0 + a - 2, x0 + r - 1, y0 + b + 1]);
      }
    }
    return this;
  }
}

/** true が続く区間を [始まり, 終わり) で返す */
function runs(flags: boolean[]): [number, number][] {
  const out: [number, number][] = [];
  let start = -1;
  flags.forEach((v, i) => {
    if (v && start < 0) start = i;
    if (!v && start >= 0) {
      out.push([start, i]);
      start = -1;
    }
  });
  if (start >= 0) out.push([start, flags.length]);
  return out;
}

/** 切り抜いた画像の中で、枠を CSS の % で重ねるための位置（スライドの赤枠用） */
export function framePercent(frame: Box, crop: Box): string {
  const w = crop[2] - crop[0];
  const h = crop[3] - crop[1];
  const l = frame[0] - crop[0];
  const t = frame[1] - crop[1];
  const r = frame[2] - crop[0];
  const b = frame[3] - crop[1];
  const pct = (v: number) => `${((v / 1) * 100).toFixed(1)}%`;
  return `left:${pct(l / w)} top:${pct(t / h)} width:${pct((r - l) / w)} height:${pct((b - t) / h)}`;
}
