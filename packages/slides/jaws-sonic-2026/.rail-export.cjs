/**
 * PipelineChecklist のレール画像 (public/images/dev-workflow/*.png) を背景透過 PNG に書き出すスクリプト。
 *
 *   # 1. 書き出し用エントリで dev サーバーを起動 (stdin を閉じると slidev が終了するので tail で保持)
 *   tail -f /dev/null | pnpm exec slidev .rail-export.md --port 3098
 *   # 2. 別シェルで実行
 *   node .rail-export.cjs public/images/dev-workflow
 *
 * .rail-export.md は 1スライド = 1状態。NAMES の順序をそのスライド順と揃えること。
 * slidev export は背景が白で焼き込まれるため、Playwright で
 * omitBackground: true のスクリーンショットを撮っている。
 */
const fs = require('node:fs');
const path = require('node:path');

const { chromium } = require('playwright-chromium');

const OUT = process.argv[2];
const BASE = process.argv[3] || 'http://localhost:3098';

// .rail-export.md のスライド順と 1:1 で対応する
const NAMES = [
  '1-file-edit',
  '1-file-edit-failed',
  '1-file-edit-done',
  '2-git-commit',
  '2-git-commit-failed',
  '2-git-commit-done',
  '3-git-push',
  '3-git-push-failed',
  '3-git-push-done',
  '4-create-pr',
  '4-create-pr-failed',
  '4-create-pr-done',
  '5-merge-pr',
  '5-merge-pr-failed',
  '6-all-done',
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
    .pipeline { padding: 20px !important; }
  `;

  fs.mkdirSync(OUT, { recursive: true });

  for (const [index, name] of NAMES.entries()) {
    const slide = index + 1;
    await page.goto(`${BASE}/${slide}`, { waitUntil: 'networkidle' });
    await page.addStyleTag({ content: transparentCss });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);

    // 前後のスライドも DOM に残るので、対象スライド配下の図に限定する
    const target = page.locator(`.slidev-page-${slide} .pipeline`).first();
    await target.screenshot({ path: path.join(OUT, `${name}.png`), omitBackground: true });
    const box = await target.boundingBox();
    console.log(`${name} ${Math.round(box.width)}x${Math.round(box.height)}`);
  }
  await browser.close();
})();
