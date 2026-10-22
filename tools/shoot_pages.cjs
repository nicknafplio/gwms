// Screenshots of selected dist pages (entry notice pre-accepted). usage: node shoot_pages.cjs page1 page2 ...
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const pg of process.argv.slice(2)) for (const [w, h, tag] of [[1440, 900, 'desktop'], [390, 844, 'mobile']]) {
    const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: tag === 'mobile' ? 2 : 1 });
    await c.addInitScript(() => { try { document.cookie = 'gwms_notice=1; path=/'; document.cookie = 'gwms_cookies=declined; path=/'; } catch (e) {} });
    const p = await c.newPage(); await p.goto((process.env.BASE || 'http://localhost:8766') + '/' + pg + '.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')); await p.waitForTimeout(500);
    await p.screenshot({ path: `preview/screenshots/dist-${pg}-${tag}.jpg`, fullPage: true, type: 'jpeg', quality: 80 }); await c.close();
  }
  await b.close();
})();
