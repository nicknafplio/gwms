const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
(async () => {
  const b = await chromium.launch();
  let c = await b.newContext({ viewport:{width:1440,height:900} }); let p = await c.newPage();
  await p.goto(BASE + '/concept-home/', { waitUntil:'networkidle' });
  await p.click('#funds-btn'); await p.waitForTimeout(200);
  await p.screenshot({ path:'preview/screenshots/concept-megamenu-funds-desktop.jpg', type:'jpeg', quality:90 });
  await p.keyboard.press('Escape'); await p.click('#about-btn'); await p.waitForTimeout(200);
  await p.screenshot({ path:'preview/screenshots/concept-megamenu-about-desktop.jpg', type:'jpeg', quality:90 });
  c = await b.newContext({ viewport:{width:390,height:844}, hasTouch:true, isMobile:true }); p = await c.newPage();
  await p.goto(BASE + '/concept-home/', { waitUntil:'networkidle' });
  await p.tap('.nav-toggle'); await p.tap('#funds-btn'); await p.waitForTimeout(200);
  await p.screenshot({ path:'preview/screenshots/concept-megamenu-funds-mobile.jpg', type:'jpeg', quality:90 });
  await b.close();
})();
