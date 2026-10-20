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
  ok((await c.cookies()).length === 0, 'no cookies set before ACCEPT');
  await p.click('[data-notice-accept]'); await p.waitForTimeout(200);
  ok(!(await p.isVisible('#entry-notice')), 'ACCEPT closes the notice');
  await p.goto(BASE + '/funds.html', { waitUntil: 'networkidle' });
  ok(!(await p.isVisible('#entry-notice')), 'notice stays closed for the rest of the browser session');
  const ck = await c.cookies();
  ok(ck.length === 1 && ck[0].name === 'gwms_notice' && ck[0].sameSite === 'Lax' && ck[0].expires > Date.now() / 1000 + 29 * 86400, 'one first-party cookie after ACCEPT: ' + ck.map(k => k.name + ' (SameSite ' + k.sameSite + ')').join(', '));
  const p2 = await c.newPage(); await p2.goto(BASE + '/about-gwms.html', { waitUntil: 'networkidle' });
  ok(!(await p2.isVisible('#entry-notice')), 'notice stays closed on another page / later visit (cookie)'); await p2.close();
  // declining sets nothing
  const cd = await b.newContext(); const pd = await cd.newPage(); await pd.goto(BASE + '/', { waitUntil: 'networkidle' });
  ok((await cd.cookies()).length === 0, 'no cookie when the notice is merely shown / declined'); await cd.close();
  // e-mail obfuscation
  const cm = await b.newContext(); await cm.addInitScript(() => { document.cookie = 'gwms_notice=1; path=/'; });
  const pm = await cm.newPage(); await pm.goto(BASE + '/contact.html', { waitUntil: 'networkidle' });
  const raw = fs.readFileSync(path.join(DIST, 'contact.html'), 'utf8');
  ok(!/@globalwms\.com|mailto:[a-z]/i.test(raw), 'no e-mail address or mailto target in the served HTML of contact.html');
  ok(!/@globalwms\.com/i.test(await pm.content()), 'no e-mail address in the rendered DOM either');
  const linkText = await pm.textContent('a.mail >> nth=0'); ok(/ \[at\] globalwms\.com$/.test(linkText), 'shown as name [at] domain: ' + linkText);
  await cm.close();
  // --- every page: axe, console, third-party requests
  const hosts = new Set();
  const ALL = fs.readdirSync(DIST).filter(f => f.endsWith('.html')).sort();
  for (const pg of ALL.map(f => f === 'index.html' ? '/' : '/' + f)) {
    for (const [w, label] of [[1440, 'desktop'], [390, 'mobile']]) {
      const cx = await b.newContext({ viewport: { width: w, height: 900 } }); await cx.addInitScript(() => { try { document.cookie = 'gwms_notice=1; path=/'; } catch (e) {} });
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
  for (const n of ['david-parker', 'mike-kew', 'james-bottomley', 'simon-voysey', 'sarah-crow', 'jessica-french']) {
    const vcf = fs.readFileSync(path.join(DIST, 'vcards/' + n + '.vcf'), 'utf8');
    ok(/^BEGIN:VCARD\r\nVERSION:3\.0/.test(vcf) && /END:VCARD\r\n$/.test(vcf) && /\nFN:.+/.test(vcf) && /\nTITLE:.+/.test(vcf) && /\nTEL;.*:\+44\d{10}\r/.test(vcf) && /\nEMAIL;.*:[a-z.]+@globalwms\.com\r/.test(vcf), n + '.vcf is a complete vCard (name, title, mobile, e-mail)');
  }
  // --- link audit: every internal href/src in every page resolves to a file; every folder has a blank index.html
  const broken = []; let checked = 0;
  for (const f of ALL) {
    const html = fs.readFileSync(path.join(DIST, f), 'utf8');
    for (const m of html.matchAll(/(?:href|src)="([^"#]+)"/g)) {
      const u = m[1].split('?')[0]; if (/^(https?:|mailto:|tel:|data:)/.test(u)) continue;
      const base = f === '404.html' ? path.join(DIST, u.startsWith('/') ? u.slice(1) : u) : path.join(DIST, u);
      checked++; if (!fs.existsSync(base)) broken.push(f + ' -> ' + u);
    }
  }
  ok(broken.length === 0, `no broken internal links/assets (${checked} references in ${ALL.length} pages)` + (broken.length ? ': ' + broken.slice(0, 10).join('; ') : ''));
  const dirs = []; (function walk(d) { for (const e of fs.readdirSync(d, { withFileTypes: true })) if (e.isDirectory()) { dirs.push(path.join(d, e.name)); walk(path.join(d, e.name)); } })(DIST);
  const noIndex = dirs.filter(d => !fs.existsSync(path.join(d, 'index.html')));
  ok(noIndex.length === 0, `every folder has an index.html (${dirs.length} folders)` + (noIndex.length ? ': ' + noIndex.join(', ') : ''));
  await b.close(); console.log(fails ? `\n${fails} FAILED` : '\nall dist checks passed'); process.exit(fails ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
