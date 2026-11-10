from pathlib import Path
p=Path('work/test-kin-full.cjs');s=p.read_text('utf8').replace("+'</script>'+template", "+'</script>'+template+fs.readFileSync('work/cases-section.html','utf8')+fs.readFileSync('work/history-section.html','utf8')")
s=s.replace("check(await page.locator('#kin-pick option').count()", """await page.locator('#kin-faint').click();
check(await page.locator('#kin-pick option').count()===19,'exactly 19 faint cards filterable');
await page.locator('#kin-faint').click();
await page.locator('[onclick*="full-P461"]').first().click();
check(await page.evaluate(()=>selectedPersonId)==='full-P461','case selection');
check(await page.locator('.kin-card a[href^="#kin-story-"]').count()>0,'biography return link');
check(await page.locator('#kin-pick option').count()""")
s=s.replace("window.fullPeople.filter((_,i)=>i%10===0).every(p=>window.focusPerson(p.id))","window.fullPeople.every(p=>window.focusPerson(p.id,false,false))").replace("sample throughout full dataset traversable","all 902 full cards traversable")
p.write_text(s,'utf8')
