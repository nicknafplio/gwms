// Serves every page with the Content-Security-Policy from dist/.htaccess and fails on any violation.
// Also exercises the cookie bar (Accept loads Google Analytics, stubbed) and the menus.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const BASE = process.env.BASE || 'http://localhost:8766'; const DIST = process.env.DIST || 'dist';
const csp = fs.readFileSync(path.join(DIST, '.htaccess'), 'utf8').match(/Content-Security-Policy "([^"]+)"/)[1];
let fails = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
(async () => {
  const b = await chromium.launch(); const bad = [];
  const pages = fs.readdirSync(DIST).filter(f => f.endsWith('.html')).sort();
  for (const mode of ['first-visit', 'accepted']) {
    const c = await b.newContext({ viewport: { width: 1280, height: 900 } });
    if (mode === 'accepted') await c.addInitScript(() => { document.cookie = 'gwms_notice=1; path=/'; document.cookie = 'gwms_cookies=accepted; path=/'; });
    await c.route(/googletagmanager\.com|google-analytics\.com/, r => r.fulfill({ status: 200, contentType: 'application/javascript', body: 'window.__ga=1' }));
    await c.route(BASE + '/**', async r => { const resp = await r.fetch(); await r.fulfill({ response: resp, headers: { ...resp.headers(), 'content-security-policy': csp } }); });
    for (const f of pages) {
      const p = await c.newPage(); p.on('console', m => { if (/Content Security Policy|Refused to/i.test(m.text())) bad.push(mode + ' ' + f + ': ' + m.text().slice(0, 160)); });
      await p.goto(BASE + '/' + (f === 'index.html' ? '' : f), { waitUntil: 'networkidle' });
      if (mode === 'first-visit' && f === 'index.html') { await p.click('[data-notice-accept]'); await p.click('[data-cookie-accept]'); await p.waitForTimeout(300); ok(await p.evaluate(() => !!window.gtag), 'Accept loads GA under the policy (gtag defined)'); }
      if (f === 'index.html') { await p.click('.site-nav button[aria-controls]').catch(() => {}); await p.waitForTimeout(400); }
      await p.close();
    }
    await c.close();
  }
  ok(bad.length === 0, `no Content-Security-Policy violations on ${pages.length} pages x 2 visits` + (bad.length ? ': ' + bad.slice(0, 5).join(' | ') : ''));
  await b.close(); console.log(fails ? `\n${fails} FAILED` : '\nCSP check passed'); process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
