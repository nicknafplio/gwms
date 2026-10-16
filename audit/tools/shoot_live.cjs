const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch();
  for (const [name,w,h] of [['desktop',1440,900],['mobile',390,844]]) {
    const ctx=await b.newContext({viewport:{width:w,height:h}});
    const pg=await ctx.newPage(); const reqs=[]; pg.on('request',r=>reqs.push(r.url()));
    await pg.goto('https://globalwms.com/',{waitUntil:'networkidle'}); await pg.waitForTimeout(1500);
    await pg.screenshot({path:`raw/shots/live-home-${name}-first-visit.png`});
    if(name==='desktop'){
      console.log('cookies:',(await ctx.cookies()).map(c=>c.name+'@'+c.domain));
      console.log('3rd-party hosts:',[...new Set(reqs.filter(r=>!r.includes('globalwms.com')).map(r=>new URL(r).host))]);
      console.log('cpnb bar elements:',await pg.locator('.cpnb-outer').count());
    }
    const acc=pg.locator('#prcd'); if(await acc.count()){ await acc.first().click({force:true}).catch(()=>{}); }
    await pg.waitForTimeout(600); await pg.screenshot({path:`raw/shots/live-home-${name}.png`});
    await pg.goto('https://globalwms.com/ask-capital-india-entrepreneur-fund',{waitUntil:'networkidle'});
    await pg.screenshot({path:`raw/shots/live-fund-${name}.png`,fullPage:true});
    if(name==='desktop'){
      await pg.goto('https://globalwms.com/',{waitUntil:'networkidle'});
      await pg.hover('#nav >> text=Funds'); await pg.waitForTimeout(500);
      await pg.screenshot({path:'raw/shots/live-menu-funds-desktop.png'});
    }
    await ctx.close();
  }
  await b.close();
})().catch(e=>{console.error(e.message);process.exit(1)});
