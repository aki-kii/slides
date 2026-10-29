/**
 * スクショの定義ファイルから使う、読み込み・切り抜き・黒塗り・書き出しの手順。
 *
 *   export default defineShots(async (shots) => {
 *     await shots.cutOut({ source: 'console.png', out: 'console.png', crop: [0, 0, 800, 600] });
 *   });
 *
 * 入力と出力のフォルダは CLI の引数で渡す（定義ファイルには書かない）。
 */
import { join } from 'node:path';
import { RawImage, framePercent, scaleBox, type Box } from './image.ts';

export interface CutOutOptions {
  /** 入力フォルダの中のファイル名。image を渡したときは不要 */
  source?: string;
  /** すでに読み込んで加工した画像を使うとき */
  image?: RawImage;
  out: string;
  crop: Box;
  /** 黒塗りする範囲（ID や ARN など） */
  masks?: Box[];
  /** スライドで赤枠を重ねる範囲。切り抜き後の % を表示する */
  frames?: Box[];
  /** crop・masks・frames の座標に掛ける倍率（縮小表示から拾った座標を元画像に戻す） */
  scale?: number;
  /** この幅を超えるときだけ縮める */
  maxWidth?: number;
}

export interface Shots {
  inDir: string;
  outDir: string;
  /** 入力フォルダから読み込む。ipBoxes の中の IP アドレスは第2・第3オクテットを黒塗りする */
  load(name: string, options?: { ipBoxes?: Box[] }): Promise<RawImage>;
  save(image: RawImage, name: string): Promise<void>;
  cutOut(options: CutOutOptions): Promise<RawImage>;
}

export type ShotsDefinition = (shots: Shots) => Promise<void>;

export function defineShots(definition: ShotsDefinition): ShotsDefinition {
  return definition;
}

export function createShots(inDir: string, outDir: string): Shots {
  const shots: Shots = {
    inDir,
    outDir,
    async load(name, options = {}) {
      const image = await RawImage.load(join(inDir, name));
      for (const box of options.ipBoxes ?? []) image.maskIpOctets(box);
      return image;
    },
    async save(image, name) {
      await image.save(join(outDir, name));
      console.log(`${name} (${image.width}, ${image.height})`);
    },
    async cutOut(o) {
      const k = o.scale ?? 1;
      let image = o.image ?? (await shots.load(o.source!));
      for (const m of o.masks ?? []) image.fill(scaleBox(m, k));
      const crop = scaleBox(o.crop, k);
      image = image.crop(crop);
      for (const f of o.frames ?? []) {
        console.log(`${o.out} frame: ${framePercent(scaleBox(f, k), crop)}`);
      }
      if (o.maxWidth) image = await image.fitWidth(o.maxWidth);
      await shots.save(image, o.out);
      return image;
    },
  };
  return shots;
}
