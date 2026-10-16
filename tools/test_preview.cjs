const { chromium } = require('playwright');
const fs = require('fs');
const AXE = fs.readFileSync(process.env.AXE_PATH, 'utf8');
const BASE = process.env.BASE || 'http://localhost:8765';
let fails = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
async function axe(p, label) {
  await p.evaluate(AXE);
  const r = await p.evaluate(() => axe.run(document, { runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice'] }));
  const v = r.violations.map(x => `${x.id}(${x.nodes.length})`);
  ok(v.length === 0, `axe ${label}: ${v.length ? v.join(', ') : '0 violations'} [${r.passes.length} rules passed]`);
  r.violations.forEach(x => x.nodes.slice(0,2).forEach(n => console.log('   ', x.id, n.target.join(' '), '-', n.failureSummary.split('\n')[1])));
}
(async () => {
  const b = await chromium.launch();
  for (const [name, w, h, touch] of [['desktop',1440,900,false],['mobile',390,844,true]]) {
    const c = await b.newContext({ viewport:{width:w,height:h}, hasTouch:touch, isMobile:touch });
    const p = await c.newPage();
    for (const path of ['/', '/ask-capital-india-entrepreneur-fund/']) {
      await p.goto(BASE + path, { waitUntil: 'networkidle' });
      await axe(p, `${name} ${path} closed`);
      if (name === 'mobile') await p.tap('.nav-toggle'); 
      await p.click('#funds-btn');
      await axe(p, `${name} ${path} funds open`);
      await p.click('#about-btn');
      await axe(p, `${name} ${path} about open`);
      // horizontal overflow
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      ok(ov <= 0, `${name} ${path} no horizontal scroll (overflow ${ov}px)`);
    }
    await c.close();
  }
  // Keyboard behaviour (desktop)
  const c = await b.newContext({ viewport:{width:1440,height:900} });
  const p = await c.newPage();
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  const active = () => p.evaluate(() => document.activeElement && (document.activeElement.id || document.activeElement.textContent.trim().slice(0,40)));
  await p.keyboard.press('Tab'); ok(await p.evaluate(()=>document.activeElement.className.includes('skip-link')), 'first Tab stop is the skip link');
  await p.keyboard.press('Tab'); await p.keyboard.press('Tab'); // logo, Platforms
  await p.keyboard.press('Tab');
  ok(await active() === 'funds-btn', 'Tab order reaches Funds button after logo and Platforms');
  await p.keyboard.press('Enter');
  ok(await p.getAttribute('#funds-btn','aria-expanded') === 'true' && await p.isVisible('#funds'), 'Enter opens Funds panel (aria-expanded=true)');
  await p.keyboard.press('Tab');
  ok((await active()).startsWith('1OAK'), 'Tab moves into first link of the panel');
  await p.keyboard.press('Escape');
  ok(await p.getAttribute('#funds-btn','aria-expanded') === 'false' && !(await p.isVisible('#funds')) && await active() === 'funds-btn', 'Escape closes panel and returns focus to its button');
  await p.keyboard.press('Space');
  ok(await p.getAttribute('#funds-btn','aria-expanded') === 'true', 'Space opens panel');
  await p.keyboard.press('Enter');
  ok(await p.getAttribute('#funds-btn','aria-expanded') === 'false', 'Enter on open trigger closes it');
  await p.keyboard.press('ArrowDown');
  ok((await active()).startsWith('1OAK'), 'ArrowDown opens and focuses first link');
  for (let i=0;i<7;i++) await p.keyboard.press('Tab');
  ok((await active()).startsWith('Investment Management') && await p.getAttribute('#funds-btn','aria-expanded') === 'false', 'tabbing past the last panel link closes the panel and lands on the next nav item');
  await p.click('#funds-btn'); await p.click('#about-btn');
  ok(await p.getAttribute('#funds-btn','aria-expanded') === 'false' && await p.getAttribute('#about-btn','aria-expanded') === 'true', 'opening a second panel closes the first');
  await p.mouse.click(700, 700);
  ok(await p.getAttribute('#about-btn','aria-expanded') === 'false', 'click outside closes panel');
  await p.hover('#funds-btn'); await p.waitForTimeout(400);
  ok(await p.getAttribute('#funds-btn','aria-expanded') === 'false', 'hover alone does not open a panel (no hover-only behaviour)');
  await c.close();
  // Mobile: Escape
  const cm = await b.newContext({ viewport:{width:390,height:844}, hasTouch:true, isMobile:true });
  const m = await cm.newPage(); await m.goto(BASE + '/', { waitUntil: 'networkidle' });
  ok(!(await m.isVisible('#site-nav')), 'mobile: menu hidden until opened');
  await m.tap('.nav-toggle'); ok(await m.isVisible('#site-nav') && await m.getAttribute('.nav-toggle','aria-expanded')==='true', 'mobile: toggle opens menu, aria-expanded=true');
  await m.tap('#funds-btn'); ok(await m.isVisible('#funds'), 'mobile: Funds accordion expands on tap');
  await m.keyboard.press('Escape'); ok(!(await m.isVisible('#funds')) && await m.isVisible('#site-nav'), 'mobile: first Escape collapses the section');
  await m.keyboard.press('Escape'); ok(!(await m.isVisible('#site-nav')), 'mobile: second Escape closes the menu');
  await cm.close();
  // No JavaScript
  const cn = await b.newContext({ viewport:{width:1440,height:900}, javaScriptEnabled:false });
  const n = await cn.newPage(); await n.goto(BASE + '/', { waitUntil: 'networkidle' });
  const vis = await n.evaluate(() => [...document.querySelectorAll('#site-nav li:not(.site-nav__item--home) a')].filter(a => a.offsetParent !== null).length);
  const total = await n.evaluate(() => document.querySelectorAll('#site-nav li:not(.site-nav__item--home) a').length);
  ok(vis === total, `no-JS (desktop): all ${total} navigation links visible (Home item is mobile-only) (${vis})`);
  await n.screenshot({ path: 'preview/screenshots/home-no-js.png' });
  await cn.close();
  await b.close();
  console.log(fails ? `\n${fails} FAILED` : '\nall checks passed'); process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
