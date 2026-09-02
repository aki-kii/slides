const { chromium } = require('playwright-chromium');
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({viewport:{width:1280,height:800}})).newPage();
  await p.goto('http://localhost:3098/9', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(400);
  const out = await p.evaluate(() => {
    const pipe = document.querySelector('.slidev-page-9 .pipeline');
    const step = pipe.querySelector('.pipeline-step');
    const label = step.querySelector('.label');
    const rail = step.querySelector('.rail');
    const cs = getComputedStyle(label);
    return {
      pipe: [pipe.getBoundingClientRect().width, pipe.getBoundingClientRect().height],
      step: [step.getBoundingClientRect().width, step.getBoundingClientRect().height],
      label: [label.getBoundingClientRect().width, label.getBoundingClientRect().height],
      rail: [rail.getBoundingClientRect().width, rail.getBoundingClientRect().height],
      labelFs: cs.fontSize, labelLh: cs.lineHeight, labelPad: cs.padding,
      pipeGap: getComputedStyle(pipe).gap,
      pipeFs: getComputedStyle(pipe).fontSize,
      family: cs.fontFamily,
    };
  });
  console.log(JSON.stringify(out, null, 2));
  await b.close();
})();
