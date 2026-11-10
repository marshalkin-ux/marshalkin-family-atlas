from pathlib import Path
p=Path('work/tree-section.html');s=p.read_text('utf8').replace('mapW=1000,mapH=610,cx=500,cy=305','mapW=1000,mapH=435,cx=500,cy=217.5').replace('aspect-ratio:1000/610','aspect-ratio:1000/435')
a=s.index('const separation=Math.min');b=s.index('\n}',a)
s=s[:a]+'''const low=-Math.PI*.92;
for(let i=0;i<pts.length;i++){const pt=pts[i];const even=low+Math.PI*2*(i+.5)/pts.length;
const a=pts.length>25?pt.a*.76+even*.24:pt.a;
pt.x=cx+Math.cos(a)*480*radius;pt.y=cy+Math.sin(a)*196*radius}
''' +s[b:]
s=s.replace("view.z>=5","view.z>=4").replace("const before=view.z;view.z=", "const before=view.z;view.z=")
s=s.replace("font:12px Georgia,serif}","font:13px Georgia,serif}")
p.write_text(s,'utf8')
