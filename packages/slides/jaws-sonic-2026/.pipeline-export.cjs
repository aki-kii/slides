/**
 * PipelinePyramid を背景透過 PNG に書き出すスクリプト。
 *
 *   # 1. 書き出し用エントリで dev サーバーを起動 (stdin を閉じると slidev が終了するので tail で保持)
 *   tail -f /dev/null | pnpm exec slidev .pipeline-export.md --port 3099
 *   # 2. 別シェルで実行
 *   node .pipeline-export.cjs public/images/dev-workflow
 *
 * slidev export は背景が白で焼き込まれるため、Playwright で
 * omitBackground: true のスクリーンショットを撮っている。
 */
const fs = require('node:fs');
const path = require('node:path');

const { chromium } = require('playwright-chromium');

const OUT = process.argv[2];
const BASE = process.argv[3] || 'http://localhost:3099';
// 撮影対象。names を複数並べるとクリックを進めながら連番で撮れる
const SHOTS = [
  { slide: 1, selector: '.pyramid', dir: '', names: ['pyramid'] },
];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    deviceScaleFactor: 4,
  });
  const page = await ctx.newPage();

  // 図だけを透過で撮れるように、背景を塗っている祖先要素をすべて透明にする。
  // .pipeline の padding は scoped CSS (属性セレクタ) の方が詳細度が高いので !important で上書きする
  const transparentCss = `
    html, body, #app, #page-root, #slideshow, #slide-container, #slide-content,
    .slidev-layout, .slidev-page, .slidev-slide-container,
    .slidev-slide-content { background: transparent !important; }
    .pipeline, .pyramid { padding: 20px !important; }
  `;

  for (const { slide, selector, dir, names } of SHOTS) {
    const outDir = path.join(OUT, dir);
    fs.mkdirSync(outDir, { recursive: true });

    await page.goto(`${BASE}/${slide}`, { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: transparentCss });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(500);

    // 前後のスライドも DOM に残るので、対象スライド配下の図に限定する
    const target = page.locator(`.slidev-page-${slide} ${selector}`).first();
    for (const name of names) {
      await page.waitForTimeout(250);
      await target.screenshot({ path: path.join(outDir, `${name}.png`), omitBackground: true });
      const box = await target.boundingBox();
      console.log(`${path.join(dir, name)} ${Math.round(box.width)}x${Math.round(box.height)}`);
      await page.keyboard.press('ArrowRight'); // 次のクリック状態へ
    }
  }
  await browser.close();
})();
