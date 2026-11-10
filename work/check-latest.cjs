const {chromium}=require('playwright');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const assert=require('node:assert/strict');
(async()=>{
  const browser=await chromium.launch({channel:'chrome',headless:true});
  const page=await browser.newPage({viewport:{width:1360,height:900},reducedMotion:'reduce'});
  const errs=[];page.on('pageerror',e=>errs.push(e.message));
  await page.goto(pathToFileURL(path.resolve('outputs/Маршалкины.html')).href);
  await page.waitForSelector('.whole-dot');
  console.log('default branch',await page.locator('#kin-branch-name').innerText(),await page.locator('#kin-branch-map .kin-branch-node').count());
  await page.evaluate(()=>document.fonts.ready); await page.locator('#kin-whole').screenshot({path:'outputs/Древо-целиком.png'}); assert.equal(await page.locator('.whole-dot').count(),903); await page.locator(".whole-head[data-who=full-J104]").click();
  const inputs=await page.evaluate(()=>({n:fullPeople.length,gen:Math.max(...fullPeople.map(p=>p.gen)),f:fullPeople.filter(p=>p.faint).length,credits:document.querySelector('footer').innerText}));console.log(inputs);
  assert.equal(inputs.n,903);assert.equal(inputs.f,19);
  await page.locator('#kin-faint').click();assert.equal(await page.locator('#kin-pick option').count(),19);
  await page.evaluate(()=>window.focusPerson('full-R150'));await page.locator('#kin-focus .otherLink').click();assert.equal(await page.evaluate(()=>selectedPersonId),'J10');
  await page.locator('#kin-focus .otherLink').click();assert.equal(await page.evaluate(()=>selectedPersonId),'full-R150');
  await page.locator('.agebar').first().click();assert(await page.locator('#ageLedger tr[data-age]:visible').count()>0);
  await page.locator('#ageLedger .clearAge').click();assert.equal(await page.locator('#ageLedger tr[data-age]:visible').count(),96);
  await page.locator('#sheetAudit summary').click();await page.locator('#audRow').fill('704');await page.locator('#audGo').click();assert.match(await page.locator('#auditResults').innerText(),/Анна 09.12.1790/);
  await page.locator('#tq').fill('Давид');await page.locator('#groups .recordChip').first().click();assert(await page.locator('#kin-q').inputValue());
  for(const w of [375,1360]){
    await page.setViewportSize({width:w,height:900});await page.reload();await page.waitForSelector('.whole-dot');const dims=await page.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]);assert(dims[0]<=dims[1]+1,dims.toString());
  }
  assert.equal(await page.locator('.lifeRibbon').count(),11); assert.equal(await page.locator('.hx-epoch').count(),5); console.log('history height',await page.locator('.hx-epochs').evaluate(e=>e.offsetHeight)); assert.deepEqual(errs,[]);await browser.close();console.log('PASS');
})().catch(e=>{console.error(e);process.exit(1)});

