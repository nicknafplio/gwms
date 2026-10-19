// Checks specific to the deployable site (dist/): entry notice, axe on every page, errors, links/assets.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const BASE = process.env.BASE || 'http://localhost:8766'; const DIST = process.env.DIST || 'dist';
const AXE = fs.readFileSync(process.env.AXE_PATH, 'utf8');
let fails = 0; const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };
(async () => {
  const b = await chromium.launch();
  // --- Entry notice
  let c = await b.newContext({ viewport: { width: 1440, height: 900 } }); let p = await c.newPage();
  const errs = []; p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); p.on('pageerror', e => errs.push(e.message)); p.on('requestfailed', r => errs.push('FAILED ' + r.url()));
  await p.goto(BASE + '/', { waitUntil: 'networkidle' });
  ok(await p.isVisible('#entry-notice'), 'entry notice shown on first visit');
  ok(await p.evaluate(() => document.activeElement && document.activeElement.hasAttribute('data-notice-accept')), 'focus starts on ACCEPT');
  ok((await p.textContent('#entry-notice')).includes('deals exclusively with Intermediaries'), 'notice wording present (verbatim from live site)');
  await p.evaluate(AXE); let r = await p.evaluate(() => axe.run(document, { runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice'] }));
  ok(r.violations.length === 0, 'axe with notice open: ' + (r.violations.map(v => v.id).join(',') || '0 violations'));
  await p.keyboard.press('Escape'); ok(await p.isVisible('#entry-notice'), 'Escape does not dismiss the notice');
  ok((await p.getAttribute('.notice__decline', 'href')) === 'https://google.com', 'DECLINE links to https://google.com');
  await p.screenshot({ path: 'preview/screenshots/dist-entry-notice.png' });
  await p.click('[data-notice-accept]'); await p.waitForTimeout(200);
  ok(!(await p.isVisible('#entry-notice')), 'ACCEPT closes the notice');
  await p.goto(BASE + '/funds/', { waitUntil: 'networkidle' });
  ok(!(await p.isVisible('#entry-notice')), 'notice stays closed for the rest of the browser session');
  ok((await c.cookies()).length === 0, 'no cookies set (' + (await c.cookies()).length + ')');
  // --- every page: axe, console, third-party requests
  const hosts = new Set();
  for (const pg of ['/', '/funds/', '/ask-capital-india-entrepreneur-fund/', '/404.html']) {
    for (const [w, label] of [[1440, 'desktop'], [390, 'mobile']]) {
      const cx = await b.newContext({ viewport: { width: w, height: 900 } }); await cx.addInitScript(() => { try { sessionStorage.setItem('gwms-notice-accepted', '1'); } catch (e) {} });
      const q = await cx.newPage(); const e2 = []; q.on('console', m => { if (m.type() === 'error') e2.push(m.text()); }); q.on('pageerror', e => e2.push(e.message)); q.on('requestfailed', rq => e2.push('FAILED ' + rq.url()));
      q.on('request', rq => hosts.add(new URL(rq.url()).host));
      await q.goto(BASE + pg, { waitUntil: 'networkidle' }); await q.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')); await q.waitForTimeout(400);
      await q.evaluate(AXE); const rr = await q.evaluate(() => axe.run(document, { runOnly: ['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice'] }));
      const ov = await q.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      const imgs = await q.evaluate(() => [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src));
      ok(rr.violations.length === 0 && e2.length === 0 && ov <= 0 && imgs.length === 0, `${pg} ${label}: axe ${rr.violations.length ? rr.violations.map(v => v.id + '(' + v.nodes.length + ')').join(',') : '0'}, console/network errors ${e2.length}, overflow ${ov}px, broken images ${imgs.length}`);
      rr.violations.forEach(v => v.nodes.slice(0, 2).forEach(n => console.log('    ', v.id, n.target.join(' '), (n.failureSummary || '').split('\n')[1])));
      await cx.close();
    }
  }
  ok([...hosts].every(h => h.startsWith('localhost')), 'no third-party requests: ' + [...hosts].join(', '));
  // --- link audit (built pages only)
  const pages = ['index.html', 'funds/index.html', 'ask-capital-india-entrepreneur-fund/index.html'];
  const missing = new Map(); const internalOk = new Set();
  for (const f of pages) {
    const html = fs.readFileSync(path.join(DIST, f), 'utf8');
    for (const m of html.matchAll(/(?:href|src)="([^"#]+)"/g)) {
      const u = m[1]; if (/^(https?:|mailto:|tel:|data:)/.test(u)) continue;
      const target = path.normalize(path.join(DIST, path.dirname(f), u));
      if (fs.existsSync(target)) internalOk.add(u); else { const k = u.replace(/^(\.\.\/)+/, '').replace(/^\.\//, '').replace(/\/index\.html$/, ''); missing.set(k, (missing.get(k) || 0) + 1); }
    }
  }
  console.log('INFO internal references that resolve:', internalOk.size);
  console.log('INFO links to pages not built yet (' + missing.size + '):', [...missing.keys()].sort().join(', '));
  const assetMissing = [...missing.keys()].filter(k => /\.(css|js|webp|png|svg|jpg|woff2|ico)$/.test(k));
  ok(assetMissing.length === 0, 'no missing assets (css/js/images/fonts)' + (assetMissing.length ? ': ' + assetMissing.join(', ') : ''));
  await b.close(); console.log(fails ? `\n${fails} FAILED` : '\nall dist checks passed'); process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
