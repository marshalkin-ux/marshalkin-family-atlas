const fs=require('fs'),{chromium}=require('C:/Users/marsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});try{const page=await browser.newPage({viewport:{width:1250,height:750}});page.on('pageerror',console.error);
const old=fs.readFileSync('outputs/Маршалкины.html','utf8'),data=JSON.parse(old.match(/const \[people,groups\]=([^\n]+);/)[1]);data.push(data[0]);
let html=fs.readFileSync('work/story.html','utf8').replace('{{DATA}}',JSON.stringify(data)).replace('{{TREE}}','<h2 id="tree">Древо</h2>').replace('{{HISTORY}}',fs.readFileSync('work/history-section.html','utf8')).replace('{{CASES}}',fs.readFileSync('work/cases-section.html','utf8'));
await page.setContent(html);await page.screenshot({path:'work/hero-check.png'});console.log(await page.locator('#matches').innerText(),await page.locator('#folioOak path').count());
await page.setViewportSize({width:375,height:810});console.log('mobile',await page.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]));}finally{await browser.close()}})();
