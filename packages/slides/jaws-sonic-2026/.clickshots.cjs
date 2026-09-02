const { chromium } = require('playwright-chromium');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push(String(e)));
  await p.goto('http://localhost:3097/7', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1200);
  for (const i of [0, 1, 2]) {
    await p.screenshot({ path: `${out}/click-${i}.png` });
    const t = await p.locator('.slidev-page-7 .agent-title .bubble').first().innerText();
    console.log(`click ${i}: "${t.trim()}"`);
    await p.keyboard.press('ArrowRight');
    await p.waitForTimeout(700);
  }
  if (errs.length) console.log('CONSOLE ERRORS:', errs.slice(0, 5));
  await b.close();
})();
