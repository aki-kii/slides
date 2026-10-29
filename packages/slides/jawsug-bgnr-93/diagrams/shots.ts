/**
 * 導入のスクショ（public/images/story/*.png）の定義。切り抜きと黒塗りは @slides/tools に任せる。
 *
 *   pnpm shots --in <スクショのフォルダ>
 *
 * new-03 の ID・ARN（アカウント ID を含む）・ロックトークンは黒塗りしてから切り出す。
 * IP アドレスは、見ると不安になるので第2・第3オクテットだけ黒塗りする（第1・第4オクテットとプレフィックスは残す）。
 * 座標は、スクショを縮小表示して拾った値（SCALE 倍すると元画像の座標）。
 */
import { defineShots, scaleBox, type Box } from '@slides/tools';

const SCALE = 1.28;

// IP アドレスが写っている範囲（元画像の座標）
const IP_BOXES: Record<string, Box[]> = {
  'old-03-ipset-detail.png': [[600, 1040, 830, 1505]],
  'new-03-ipset-detail.png': [[826, 1195, 1060, 1480]],
  'new-05-ipset-edit-addresses.png': [[678, 440, 925, 1110]],
  // 手順5の文の中の「203.0.113.12/32」「198.51.100.200/32」
  'manual-steps.png': [
    [690, 780, 950, 815],
    [990, 812, 1270, 848],
  ],
};

export default defineShots(async (shots) => {
  const load = (name: string) => shots.load(name, { ipBoxes: IP_BOXES[name] });

  // 手順書は本人が「作業手順」の見出しから No.1〜5 まで切り出した画像を使う。
  // 手順3の下に埋め込まれた「Create IP set」の画面は、本人が撮った旧コンソール（old-03）に差し替える。
  // 元の manual-steps.png は書き換えず、manual-steps-console.png として別名で書き出す。
  const sheet = await load('manual-steps.png');
  const box: Box = [578, 394, 1031, 732]; // 埋め込み画面の範囲（罫線の内側）
  // 左メニューの IP sets から IP アドレスの一覧までを、埋め込み画面と同じ縦横比で切り出す
  const old = (await load('old-03-ipset-detail.png')).crop(
    scaleBox([0, 0, 1580, 1178], SCALE),
  );
  sheet.paste(
    await old.resize(box[2] - box[0], box[3] - box[1]),
    box[0],
    box[1],
  );
  await shots.save(sheet, 'manual-steps-console.png');

  await shots.cutOut({
    image: sheet,
    out: 'manual-step5.png',
    crop: [578, 778, 1440, 878],
    maxWidth: 1440,
  });
  await shots.cutOut({
    image: await load('old-03-ipset-detail.png'),
    out: 'old-ipset-detail.png',
    crop: [330, 100, 1935, 1178],
    frames: [[1505, 612, 1856, 666]],
    scale: SCALE,
    maxWidth: 1600,
  });
  await shots.cutOut({
    image: await load('new-03-ipset-detail.png'),
    out: 'new-ipset-detail.png',
    crop: [440, 68, 1990, 1157],
    masks: [
      [1484, 266, 1932, 339],
      [1484, 394, 1932, 526],
      [1484, 581, 1932, 652],
    ],
    frames: [[1724, 80, 1958, 134]],
    scale: SCALE,
    maxWidth: 1600,
  });
  await shots.cutOut({
    image: await load('new-05-ipset-edit-addresses.png'),
    out: 'new-ipset-edit.png',
    crop: [480, 180, 1360, 1000],
    frames: [[505, 818, 1350, 876]],
    scale: SCALE,
    maxWidth: 1600,
  });
});
