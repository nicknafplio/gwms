const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8766';
(async () => {
  const b = await chromium.launch();
  for (const [name, w, h, touch] of [['desktop',1440,900,false],['mobile',390,844,true]]) {
    const c = await b.newContext({ viewport:{width:w,height:h}, hasTouch:touch, isMobile:touch }); await c.addInitScript(() => document.cookie = 'gwms_notice=1; path=/'; document.cookie = 'gwms_cookies=declined; path=/');
    const p = await c.newPage();
    for (const [slug, url] of [['home','/'],['funds','/funds/'],['ask','/ask-capital-india-entrepreneur-fund/']]) {
      await p.goto(BASE + url, { waitUntil:'networkidle' });
      await p.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading='eager')); await p.waitForTimeout(500);
      await p.evaluate(() => { const el = document.querySelector('[data-photo-fade]'); if (el) el.style.setProperty('--p', 1); });
      await p.screenshot({ path:`preview/screenshots/dist-${slug}-${name}.jpg`, type:'jpeg', quality:88, fullPage:true });
    }
  }
  await b.close();
})();
