import * as THREE from 'three';
import {SVGRenderer} from 'three/examples/jsm/renderers/SVGRenderer.js';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';

const $=id=>document.getElementById(id);
const keys=['aussehen','gewicht','haerte','wasser'];
const chapters=[
 {title:'Aussehen und Maserung',icon:'🔎',paper:'Beschreibe Farbe und Maserung deiner echten Proben auf A5.1.',lead:'Die Kamera zeigt dir Oberseite, Seitenfläche und Stirnseite.'},
 {title:'Masse vergleichen',icon:'⚖️',paper:'Wiege deine echten Proben. Trage ihre Masse in Gramm auf A5.1 ein.',lead:'Erst 0 g prüfen, dann jede Probe einzeln auflegen und ablesen.'},
 {title:'Härte prüfen',icon:'🪙',paper:'Prüfe deine echten Proben nach der Anleitung. Notiere die Druckspuren auf A5.1.',lead:'Dieselbe Münze, dieselbe Belastung und eine vergleichbare Prüfstelle.'},
 {title:'Wasseraufnahme beobachten',icon:'💧',paper:'Prüfe deine echten Proben. Notiere nach 60 Sekunden deine Beobachtungen auf A5.1.',lead:'Gleiche Tropfen auf gleich vorbereiteten Flächen. 60 Sekunden werden im Zeitraffer gezeigt.'}
];
const woods=[{name:'Fichte',color:'#dab67a',dark:'#a17e49',mass:65,spur:'deutliche Spur',water:'teilweise eingezogen'}, {name:'Buche',color:'#b98765',dark:'#885636',mass:125,spur:'leichte Spur',water:'Tropfen steht'}, {name:'Akazie',color:'#83613a',dark:'#4d3219',mass:135,spur:'leichte Spur',water:'teilweise eingezogen'}];
const initial=keys.indexOf(new URLSearchParams(location.search).get('station'));
let chapter=initial<0?0:initial, elapsed=0, playing=false, last=0, lastUI=0, failed=false, renderer, scene, camera, controls;
const duration=48, meshes=[], homes=[-255,0,255], rows=[];let scale,coin,drops=[],pipettes=[],marks=[],ruler;let svgMode=false;const screenLabels=[];
const smooth=t=>{t=THREE.MathUtils.clamp(t,0,1);return t*t*(3-2*t);};
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;

function woodTexture(w,end=false){
 const c=document.createElement('canvas');c.width=c.height=256;const ctx=c.getContext('2d');ctx.fillStyle=w.color;ctx.fillRect(0,0,256,256);ctx.strokeStyle=w.dark;ctx.globalAlpha=.36;
 let seed=woods.indexOf(w)+4;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
 if(end){for(let i=0;i<21;i++){ctx.beginPath();ctx.ellipse(118,290,22+i*12,24+i*12,0,0,Math.PI*2);ctx.lineWidth=1+(i%4===0);ctx.stroke();}}
 else for(let i=0;i<40;i++){let y=i*7;ctx.beginPath();ctx.moveTo(0,y);for(let x=0;x<=256;x+=8)ctx.lineTo(x,y+Math.sin(x/45+i*.8)*3+rand()*2);ctx.lineWidth=i%5===0?1.8:.7;ctx.stroke();}
 const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;return tex;
}
function box(x,y,z,color){return new THREE.Mesh(new THREE.BoxGeometry(x,y,z),new THREE.MeshStandardMaterial({color,roughness:.75}));}
function label(text,width=210,bg='#fffaf0',fg='#392c1d'){
 const c=document.createElement('canvas');c.width=768;c.height=144;const ctx=c.getContext('2d');ctx.fillStyle=bg;ctx.fillRect(0,0,768,144);ctx.fillStyle=fg;ctx.font='bold 62px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,384,72);
 const tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;const sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,depthTest:false}));sprite.scale.set(width,width*144/768,1);return sprite;
}
function setup(){
 const host=$('film-world');scene=new THREE.Scene();scene.background=new THREE.Color('#ece7dc');scene.fog=new THREE.Fog('#ece7dc',1150,2100);
 camera=new THREE.PerspectiveCamera(36,1,1,3000);camera.position.set(650,650,880);
 try{renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;}catch(error){svgMode=true;renderer=new SVGRenderer();renderer.setQuality('low');}host.prepend(renderer.domElement);renderer.domElement.setAttribute('aria-label','Animierte Werkbank mit drei beschrifteten Holzproben');renderer.domElement.setAttribute('role','img');
 controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,30,0);controls.enableDamping=true;controls.enablePan=false;controls.minDistance=260;controls.maxDistance=1500;controls.maxPolarAngle=Math.PI*.48;
 controls.addEventListener('start',()=>{if(playing){playing=false;updateUI();}});
 scene.add(new THREE.HemisphereLight('#fff8e8','#645944',2.7));const sun=new THREE.DirectionalLight('#ffffff',3);sun.position.set(0,850,500);sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);sun.shadow.camera.left=-650;sun.shadow.camera.right=650;sun.shadow.camera.top=650;sun.shadow.camera.bottom=-650;scene.add(sun);if(svgMode){sun.intensity=.6;scene.add(new THREE.AmbientLight('#ffffff',.45));}
 const bench=box(1000,28,470,'#c8b39a');bench.position.y=-24;bench.receiveShadow=true;scene.add(bench);const edge=box(1000,44,20,'#9c8164');edge.position.set(0,-40,225);scene.add(edge);
 for(let i=0;i<3;i++){
  const w=woods[i],g=new THREE.Group(),side=new THREE.MeshStandardMaterial({map:woodTexture(w),roughness:.8}),end=new THREE.MeshStandardMaterial({map:woodTexture(w,true),roughness:.8});
  const sample=new THREE.Mesh(new THREE.BoxGeometry(200,18,50),[end,end,side,side,side,side]);sample.castShadow=true;sample.receiveShadow=true;if(svgMode){side.color.set(w.color);end.color.set(w.color);}g.add(sample);if(svgMode){for(let k=0;k<7;k++){const points=[];for(let x=-98;x<=98;x+=7)points.push(new THREE.Vector3(x,9.3,-22+k*7+Math.sin(x/37+k)*1.2));const grain=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color:w.dark,transparent:true,opacity:.45}));g.add(grain);}}g.position.set(homes[i],0,45);scene.add(g);meshes.push(g);
  const name=label(w.name,190);name.position.set(homes[i],0,125);scene.add(name);if(svgMode){name.visible=false;const tag=document.createElement('span');tag.className='film-3d-label';tag.textContent=w.name;host.append(tag);screenLabels.push({sprite:name,tag});}
  const mark=new THREE.Mesh(new THREE.CircleGeometry(7,24),new THREE.MeshStandardMaterial({color:'#4d3421',transparent:true,opacity:.7}));mark.rotation.x=-Math.PI/2;mark.position.set(0,9.2,0);g.add(mark);marks.push(mark);
  const drop=new THREE.Mesh(new THREE.SphereGeometry(8,24,16),new THREE.MeshStandardMaterial({color:'#3488cc',transparent:true,opacity:.82,roughness:.1}));g.add(drop);drops.push(drop);
  const pip=new THREE.Group();const tube=new THREE.Mesh(new THREE.CylinderGeometry(4,4,62,16),new THREE.MeshStandardMaterial({color:'#e1edf4',transparent:true,opacity:.8}));const bulb=new THREE.Mesh(new THREE.SphereGeometry(9,16,12),new THREE.MeshStandardMaterial({color:'#367aaf'}));bulb.position.y=37;pip.add(tube,bulb);pip.position.set(homes[i],100,45);scene.add(pip);pipettes.push(pip);
 }
 scale=new THREE.Group();const foot=box(235,22,145,'#7d8d92');const tray=box(220,7,100,'#e4e8e5');tray.position.y=17;scale.add(foot,tray);scale.position.set(0,0,-105);scene.add(scale);
 coin=new THREE.Group();const cm=new THREE.Mesh(new THREE.CylinderGeometry(16,16,3,36),new THREE.MeshStandardMaterial({color:'#c6b784',metalness:.65,roughness:.34}));cm.rotation.z=Math.PI/2;coin.add(cm);const rim=new THREE.Mesh(new THREE.TorusGeometry(15.2,.7,8,36),new THREE.MeshStandardMaterial({color:'#817550',metalness:.7}));rim.rotation.y=Math.PI/2;coin.add(rim);scene.add(coin);
 ruler=new THREE.Group();const rb=box(210,1,12,'#e7d09a');ruler.add(rb);for(let j=0;j<=20;j++){const tick=box(.7,.7,j%5===0?9:5,'#3e3425');tick.position.set(-100+j*10,1,0);ruler.add(tick);}ruler.position.set(0,13,90);scene.add(ruler);
 new ResizeObserver(()=>{const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}).observe(host);
 renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();fallback('Die 3D-Ansicht wurde unterbrochen. Du kannst die Prüfschritte weiterhin lesen. Lade die Seite für den Film neu.');});
 if(svgMode){const loop=ms=>{frame(ms);requestAnimationFrame(loop);};requestAnimationFrame(loop);}else renderer.setAnimationLoop(frame);
}
function pose(){
 const t=elapsed, index=Math.min(2,Math.floor(t/14)),local=t-index*14;
 meshes.forEach((g,i)=>{g.position.set(homes[i],0,45);g.rotation.set(0,0,0);marks[i].visible=false;drops[i].visible=false;pipettes[i].visible=false;});scale.visible=chapter===1;coin.visible=chapter===2&&t<42;ruler.visible=chapter===0;
 let target=new THREE.Vector3(0,15,20),eye=new THREE.Vector3(650,650,880);
 if(chapter===0){
  const ix=Math.min(2,Math.floor(t/12));if(t<36){meshes[ix].rotation.y=reduced?0:Math.sin((t%12)/12*Math.PI*2)*.65;meshes[ix].position.y=30;target.set(homes[ix],15,45);eye.set(homes[ix]+210,230,360);}ruler.position.x=t<36?homes[ix]:0;
 }else if(chapter===1&&t<42){
  let q=local<4?smooth(local/4):local<10?1:1-smooth((local-10)/4);meshes[index].position.set(THREE.MathUtils.lerp(homes[index],0,q),q*28+Math.sin(q*Math.PI)*90,THREE.MathUtils.lerp(45,-105,q));target.set(0,25,-75);eye.set(380,330,430);
 }else if(chapter===2){
  if(t<42){target.set(homes[index],5,45);eye.set(homes[index]+135,150,230);let press=smooth((local-3)/3)*(1-smooth((local-9)/3));coin.position.set(homes[index],72-press*46,45);marks[index].visible=local>7;marks[index].scale.set(index===0?1.4:.65,index===0?1:.45,1);}
  for(let i=0;i<3;i++)marks[i].visible=t>=(i*14+7);
 }else if(chapter===3){
  pipettes.forEach(p=>{p.visible=t<9;p.position.y=100-smooth(t/3)*28+smooth((t-6)/3)*70;});
  drops.forEach((d,i)=>{d.visible=t>=4;let progress=smooth((t-8)/36),absorbed=i===1?.1:.6;d.position.set(0,16,0);d.scale.set(1+progress*.65,1-progress*absorbed,1+progress*.65);d.material.opacity=.82-progress*absorbed*.6;});eye.set(420,600,660);
 }
 if(playing){camera.position.lerp(eye,reduced?1:.065);controls.target.lerp(target,reduced?1:.065);}controls.update();
}
function stage(){
 const t=elapsed,i=Math.min(2,Math.floor(t/14)),local=t-i*14;
 if(t>=duration)return 'Prüfschritt fertig. Jetzt an deinen echten Proben arbeiten.';
 if(chapter===0)return t<36?woods[Math.floor(t/12)].name+' ansehen: Oberseite, Seitenfläche und Stirnseite.':'Alle drei Proben vergleichen: Welche Unterschiede fallen dir auf?';
 if(chapter===1)return t>=42?'Vergleiche die Massen. Gleiche Größe und ähnliche Trockenheit sind wichtig.':local<4?'Waage zeigt 0 g. '+woods[i].name+' wird aufgelegt.':local<10?woods[i].name+': '+woods[i].mass+' g · Simulationswert.':'Wert festhalten. Probe von der Waage nehmen.';
 if(chapter===2)return t>=42?'Vergleiche die Druckspuren. Eine tiefere Spur spricht hier für weicheres Holz.':local<3?woods[i].name+' liegt flach auf der Unterlage.':local<9?'Die Münzkante drückt mit gleicher Belastung auf '+woods[i].name+'.':woods[i].name+': '+woods[i].spur+' · Beispielbeobachtung.';
 const sec=Math.round(THREE.MathUtils.clamp((t-8)/36,0,1)*60);return t<8?'Drei gleich große Tropfen werden gleichzeitig aufgesetzt.':'Zeitraffer · '+sec+' von 60 Sekunden: Beobachte Tropfen und benetzte Fläche.';
}
function updateUI(){
 const c=chapters[chapter];$('film-title').textContent=c.icon+' '+c.title;$('film-lead').textContent=c.lead;$('film-caption').textContent=stage();$('film-play').textContent=playing?'Ⅱ Pause':elapsed>=duration?'↻ Noch einmal ansehen':elapsed>0?'▶ Fortsetzen':'▶ Film starten';$('film-play').setAttribute('aria-pressed',String(playing));$('film-progress').value=elapsed;$('film-time').textContent=Math.floor(elapsed)+' / '+duration+' s';
 $('film-paper').hidden=elapsed<duration;$('film-paper-task').textContent=c.paper;$('film-next').textContent=chapter<3?'Nächster Prüfschritt →':'Zum Auftrag A6 →';$('film-next').hidden=elapsed<duration;
 $('film-position').textContent='Kapitel '+(chapter+1)+' von 4';$('film-chapters').querySelectorAll('button').forEach((b,i)=>{b.setAttribute('aria-current',i===chapter?'step':'false');b.classList.toggle('film-active',i===chapter);});
 const labels=chapter===0?['Aussehen','Maserung','Vergleich']:chapter===1?['Holzart','Masse','Stand']:chapter===2?['Holzart','Druckspur','Stand']:['Holzart','Nach 60 Sekunden','Stand'];
 $('film-table-head').innerHTML=labels.map(x=>'<th scope="col">'+x+'</th>').join('');
 $('film-results').innerHTML=woods.map((w,i)=>{const ready=chapter===0?elapsed>=(i+1)*12:chapter===1?elapsed>=i*14+8:chapter===2?elapsed>=i*14+10:elapsed>=44;const value=chapter===0?['hell · deutliche Linien','rötlich · feine Linien','braun · deutliche Linien'][i]:chapter===1?w.mass+' g':chapter===2?w.spur:w.water;return '<tr><th scope="row">'+w.name+'</th><td>'+ (ready?value:'—')+'</td><td>'+ (ready?'Beispiel':'noch offen')+'</td></tr>';}).join('');
 if(scale){const ix=Math.min(2,Math.floor(elapsed/14)),lt=elapsed-ix*14;const text=chapter===1&&elapsed<42&&lt>=4&&lt<10?woods[ix].mass+' g':'0 g';if(scale.userData.displayText===text)return;scale.userData.displayText=text;const old=scale.getObjectByName('display');if(old){scale.remove(old);old.material.map.dispose();old.material.dispose();}const screen=label(text,105,'#162b2a','#c9f2d0');screen.name='display';screen.position.set(0,8,85);scale.add(screen);if(svgMode){screen.visible=false;let reading=scale.userData.reading;if(!reading){const tag=document.createElement('span');tag.className='film-3d-label film-scale-reading';$('film-world').append(tag);reading={sprite:screen,tag};screenLabels.push(reading);scale.userData.reading=reading;}reading.sprite=screen;reading.tag.textContent=text;}}
}
function select(n){chapter=n;elapsed=0;playing=false;updateUI();if(!failed)pose();document.dispatchEvent(new CustomEvent('prueflabor:chapter',{detail:keys[n]}));}
function frame(ms){const dt=last?Math.min((ms-last)/1000,.12):0;last=ms;if(playing){elapsed=Math.min(duration,elapsed+dt);if(elapsed>=duration){playing=false;updateUI();$('film-paper').focus({preventScroll:true});}if(ms-lastUI>200||!playing){updateUI();lastUI=ms;}}pose();renderer.render(scene,camera);if(svgMode){const host=$('film-world');screenLabels.forEach(({sprite,tag})=>{tag.hidden=sprite.name==='display'&&chapter!==1;const p=new THREE.Vector3();sprite.getWorldPosition(p);p.project(camera);tag.style.left=((p.x+1)/2*host.clientWidth)+'px';tag.style.top=((-p.y+1)/2*host.clientHeight)+'px';});}}
function fallback(message){failed=true;playing=false;$('film-error').hidden=false;$('film-error').textContent=message;$('film-play').disabled=true;$('film-repeat').disabled=true;$('film-progress').disabled=true;$('film-show-steps').hidden=false;}
$('film-chapters').innerHTML=chapters.map((c,i)=>'<button type="button" data-chapter="'+i+'" class="film-chip">'+c.icon+' '+(i+1)+' '+c.title+'</button>').join('');
$('film-chapters').addEventListener('click',e=>{const b=e.target.closest('[data-chapter]');if(b)select(Number(b.dataset.chapter));});
$('film-play').onclick=()=>{if(elapsed>=duration)elapsed=0;playing=!playing;updateUI();};
$('film-repeat').onclick=()=>{elapsed=0;playing=true;updateUI();};
$('film-progress').oninput=e=>{elapsed=Number(e.target.value);playing=false;updateUI();if(!failed)pose();};
$('film-next').onclick=()=>{if(chapter<3){select(chapter+1);playing=true;updateUI();}else location.href='lernweg.html?auftrag=A6';};
$('film-reset-view').onclick=()=>{camera.position.set(650,650,880);controls.target.set(0,15,20);controls.update();};
$('film-show-steps').onclick=()=>{$('stations').scrollIntoView({behavior:'smooth'});};
document.addEventListener('visibilitychange',()=>{if(document.hidden&&playing){playing=false;updateUI();}});
try{setup();}catch(error){console.error('Prüflabor-Film:',error);fallback('Dein Browser kann die 3D-Ansicht gerade nicht anzeigen. Nutze die vollständigen Stationsanleitungen darunter.');}
updateUI();if(!failed)pose();
// State exposed read-only for diagnostics and regression verification.
Object.defineProperty(window,'prueflaborFilm',{get:()=>({chapter,elapsed,playing,duration,failed,svgMode,dimensions:[200,50,18]})});
