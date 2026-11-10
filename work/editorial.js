(()=>{
const template=document.querySelector('#editorial-scenes');
const sources={'manuscript.jpg':'.origins img[alt^="Вертикальная"]','painting.jpg':'.o-painting img','tree-painting.png':'.painted-tree img','war.jpg':'#world-war .revision-figure img'};
for(const img of template.content.querySelectorAll('img')){const original=document.querySelector(sources[img.dataset.source]);if(original)img.src=original.src}

for(const scene of [...template.content.children]){const target=document.getElementById(scene.dataset.before);if(target)(target.id==='tree'?(target.closest('.atlasTree')||target):target).before(scene)}
template.remove();
const progress=document.querySelector('#reading-progress'),scenes=[...document.querySelectorAll('.editorial-scene')],active=new Set(),reduce=matchMedia('(prefers-reduced-motion: reduce)'),mobile=matchMedia('(max-width: 760px)');
const observer=new IntersectionObserver(entries=>{for(const e of entries)e.isIntersecting?active.add(e.target):active.delete(e.target);schedule()},{rootMargin:'120px'});scenes.forEach(s=>observer.observe(s));
let pending=false;function update(){pending=false;const range=document.documentElement.scrollHeight-innerHeight;progress.style.transform='scaleX('+Math.max(0,Math.min(1,range?scrollY/range:0))+')';for(const scene of active){const img=scene.querySelector('.parallax-image');if(reduce.matches||mobile.matches){img.style.transform='none';continue}const r=scene.getBoundingClientRect(),delta=Math.max(-65,Math.min(65,(innerHeight/2-r.top-r.height/2)*.12));img.style.transform=`translate3d(0,${delta.toFixed(2)}px,0)`}}
function schedule(){if(!pending){pending=true;requestAnimationFrame(update)}}
addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});reduce.addEventListener('change',()=>{scenes.forEach(s=>s.querySelector('img').style.transform='none');schedule()});mobile.addEventListener('change',schedule);schedule();
})();
