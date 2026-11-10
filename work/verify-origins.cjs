const {chromium}=require('playwright');
const fs=require('fs'),assert=require('assert/strict');
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});
 const p=await b.newPage({viewport:{width:1440,height:1000}});
 const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(process.env.ATLAS_URL||require('url').pathToFileURL(require('path').resolve('outputs/index.html')).href);
 assert.equal(await p.locator('#origins').count(),0);
 await p.fill('#pw',fs.readFileSync('outputs/Пароль к семейному атласу.txt','utf8').trim());await p.click('#unlock');
 await p.waitForSelector('#origins');
 assert.equal(await p.locator('main > section').first().getAttribute('id'),'origins');
 await p.locator('a[href="#origins"]').first().click();
 await p.locator('#origins').evaluate(e=>e.scrollIntoView({block:'start'}));
 await p.screenshot({path:'work/origins-desktop.png'});
 assert.equal(await p.locator('#origins img').count(),8);
 for(const button of await p.locator('[data-origin-view]').all()){
  await button.click();await p.locator('#origin-viewer[open]').waitFor();
  await p.waitForFunction(()=>document.querySelector('#origin-viewer-image').naturalWidth>0);
  const before=await p.locator('#origin-viewer-image').evaluate(e=>e.width);
  await p.click('#origin-zoom-in');
  assert(await p.locator('#origin-viewer-image').evaluate(e=>e.width)>before);
  await p.keyboard.press('Escape');assert.equal(await p.locator('#origin-viewer[open]').count(),0);
 }
 await p.locator('.o-root').click();assert.match(await p.locator('#kin-focus').innerText(),/Макар/);
 await p.setViewportSize({width:390,height:844});
 await p.locator('#origins').evaluate(e=>e.scrollIntoView({block:'start'}));
 await p.screenshot({path:'work/origins-mobile.png'});
 assert(await p.locator('#origins').evaluate(e=>e.scrollWidth<=e.clientWidth+1));
 assert.equal(await p.locator('.whole-dot').count(),903);
 assert.deepEqual(errors,[]);
 await b.close();console.log('Origin chapter, all 6 image viewers, zoom, Escape, person links, encrypted access and mobile width passed.');
})().catch(e=>{console.error(e);process.exit(1)});
