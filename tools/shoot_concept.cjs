const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const [name, w, h, touch] of [['desktop',1440,900,false],['mobile',390,844,true]]) {
    const c = await b.newContext({ viewport:{width:w,height:h}, hasTouch:touch, isMobile:touch });
    const p = await c.newPage();
    p.on('console', m => { if (m.type()==='error') errs.push(m.text()); }); p.on('requestfailed', r => errs.push('FAILED '+r.url()));
    await p.goto(BASE + '/concept-home/', { waitUntil:'networkidle' });
    await p.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading='eager'));
    await p.waitForTimeout(600);
    await p.screenshot({ path:`preview/screenshots/concept-home-${name}.jpg`, type:'jpeg', quality:88, fullPage:true });
  }
  console.log('errors:', errs.length ? errs : 'none'); await b.close();
})();
