import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,w,h in (('desktop',1440,900),('mobile',390,844)):
            ctx=await b.new_context(viewport={'width':w,'height':h})
            pg=await ctx.new_page()
            reqs=[]; pg.on('request',lambda r:reqs.append(r.url))
            await pg.goto('https://globalwms.com/',wait_until='networkidle')
            await pg.wait_for_timeout(1500)
            await pg.screenshot(path=f'raw/shots/live-home-{name}-first-visit.png')
            ck=await ctx.cookies()
            if name=='desktop':
                print('cookies on first visit:',[(c['name'],c['domain']) for c in ck])
                print('3rd-party hosts:',sorted({r.split('/')[2] for r in reqs if 'globalwms.com' not in r}))
                print('visible cpnb bar:',await pg.locator('.cpnb-outer').count())
            await pg.evaluate("document.querySelector('#prcd') && document.querySelector('#prcd').click()")
            await pg.wait_for_timeout(600)
            await pg.screenshot(path=f'raw/shots/live-home-{name}.png')
            await pg.goto('https://globalwms.com/ask-capital-india-entrepreneur-fund',wait_until='networkidle')
            await pg.screenshot(path=f'raw/shots/live-fund-{name}.png',full_page=True)
            if name=='desktop':
                await pg.goto('https://globalwms.com/',wait_until='networkidle')
                await pg.hover('text=Funds'); await pg.wait_for_timeout(500)
                await pg.screenshot(path='raw/shots/live-menu-funds-desktop.png')
        await b.close()
asyncio.run(main())
