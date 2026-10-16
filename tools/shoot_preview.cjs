const { chromium } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
const OUT = 'preview/screenshots/';
(async () => {
  const b = await chromium.launch();
  const errs = [];
  async function ctx(w, h, touch) {
    const c = await b.newContext({ viewport: { width: w, height: h }, hasTouch: !!touch, isMobile: !!touch, deviceScaleFactor: 1 });
    const p = await c.newPage();
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('pageerror', e => errs.push(e.message));
    p.on('requestfailed', r => errs.push('FAILED ' + r.url()));
    return p;
  }
  // Desktop
  let p = await ctx(1440, 900);
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  await p.screenshot({ path: OUT + 'home-desktop.png' });
  await p.screenshot({ path: OUT + 'home-desktop-full.png', fullPage: true });
  await p.click('#funds-btn'); await p.waitForTimeout(150);
  await p.screenshot({ path: OUT + 'megamenu-funds-desktop.png' });
  await p.keyboard.press('Escape'); await p.click('#about-btn'); await p.waitForTimeout(150);
  await p.screenshot({ path: OUT + 'megamenu-about-desktop.png' });
  await p.goto(BASE + '/ask-capital-india-entrepreneur-fund/', { waitUntil: 'networkidle' });
  await p.screenshot({ path: OUT + 'fund-desktop-full.png', fullPage: true });
  // Mobile
  p = await ctx(390, 844, true);
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  await p.screenshot({ path: OUT + 'home-mobile.png' });
  await p.screenshot({ path: OUT + 'home-mobile-full.png', fullPage: true });
  await p.tap('.nav-toggle'); await p.waitForTimeout(150);
  await p.screenshot({ path: OUT + 'menu-mobile-closed-sections.png' });
  await p.tap('#funds-btn'); await p.waitForTimeout(150);
  await p.screenshot({ path: OUT + 'megamenu-funds-mobile.png' });
  await p.goto(BASE + '/ask-capital-india-entrepreneur-fund/', { waitUntil: 'networkidle' });
  await p.screenshot({ path: OUT + 'fund-mobile-full.png', fullPage: true });
  // Tablet
  p = await ctx(820, 1100, true);
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  await p.screenshot({ path: OUT + 'home-tablet.png' });
  console.log('console/network errors:', errs.length ? errs : 'none');
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
