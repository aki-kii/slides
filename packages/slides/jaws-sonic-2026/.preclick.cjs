const { chromium } = require('playwright-chromium');
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 })).newPage();
  await p.goto('http://localhost:3097/7', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1200);
  await p.screenshot({ path: out });
  await b.close();
})();
