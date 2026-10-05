import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {SVGRenderer} from 'three/examples/jsm/renderers/SVGRenderer.js';
const $=id=>document.getElementById(id);
const woods=[{name:'Fichte',mass:65,color:0xd9b77d,mark:'deutliche',depth:5},{name:'Buche',mass:125,color:0xbb8b6b,mark:'leichte',depth:2},{name:'Akazie',mass:135,color:0x98724c,mark:'leichte',depth:2}];
const traces=[
 {name:'Ast',hint:'Im Brett sitzt eine dunkle, runde Stelle. Die Fasern laufen um sie herum.',definition:'Ast: Hier saß einmal ein Zweig am Stamm. Die Holzfasern laufen um diese Stelle herum. Nicht jeder Ast macht ein Brett unbrauchbar.'},
 {name:'Riss',hint:'Eine schmale Öffnung zieht sich durch das Holz. Beim Trocknen kann so eine Spur entstehen.',definition:'Riss: Das Holz ist an einer Stelle aufgerissen. Das kann zum Beispiel passieren, wenn es ungleichmäßig trocknet.'},
 {name:'Verwerfen',hint:'Das Brett liegt nicht mehr flach auf dem Tisch. Es biegt sich beim Trocknen.',definition:'Verwerfen: Das Brett verändert seine Form, zum Beispiel wird es krumm. Ungleichmäßiges Schwinden kann dazu führen.'},
 {name:'Schwinden',hint:'Das Holz gibt gebundenes Wasser ab. Das Brett wird schmaler.',definition:'Schwinden: Wenn Holz gebundenes Wasser verliert, wird es kleiner. Quer zur Faser verändert es sich stärker als längs.'},
 {name:'Quellen',hint:'Das Holz nimmt Wasser auf. Das Brett wird breiter.',definition:'Quellen: Wenn Holz gebundenes Wasser aufnimmt, wird es größer. Quer zur Faser verändert es sich stärker als längs.'}
];
function shuffle(array){const a=[...array];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
let cases,caseIndex=0,phase='wood',evidence=new Set(),action=null,finished=false,wood,trace;
let svgMode=false,renderer;
const host=$('scene'),scene=new THREE.Scene();scene.background=new THREE.Color(0xedf3ed);
const camera=new THREE.PerspectiveCamera(38,1,1,2500);
try{renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));}catch{svgMode=true;renderer=new SVGRenderer();renderer.setQuality('low');}
renderer.domElement.setAttribute('role','img');renderer.domElement.setAttribute('aria-label','Drehbares 3D-Prüflabor mit Holzprobe, Waage und Münztest');host.prepend(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.enablePan=false;controls.minDistance=280;controls.maxDistance=1000;controls.maxPolarAngle=Math.PI*.48;
function resetView(){camera.position.set(390,360,520);controls.target.set(0,30,0);controls.update();}
resetView();$('reset-view').onclick=resetView;
scene.add(new THREE.HemisphereLight(0xffffff,0x627766,1.35));const light=new THREE.DirectionalLight(0xffffff,.9);light.position.set(200,350,200);scene.add(light);
const mat=(color)=>new THREE.MeshLambertMaterial({color});
function box(w,h,d,color,parent,x=0,y=0,z=0){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d,w>190?12:1,h>80?6:1,d>180?8:1),mat(color));m.position.set(x,y,z);parent.add(m);return m;}
function line(points,color,parent){const l=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p))),new THREE.LineBasicMaterial({color}));parent.add(l);return l;}
const lab=new THREE.Group();scene.add(lab);const tabletop=new THREE.Mesh(new THREE.PlaneGeometry(470,255,12,8),mat(0xe7d8b9));tabletop.rotation.x=-Math.PI/2;tabletop.position.y=5;lab.add(tabletop);
for(const x of [-185,185])for(const z of [-85,85])box(14,70,14,0x697f75,lab,x,-45,z);
// Scale on the left, coin press on the right; the sample itself is 200 × 50 × 18 mm.
box(105,16,90,0x4f746c,lab,-125,13,-30);box(95,7,80,0xbac8c6,lab,-125,25,-30);box(65,13,3,0x163d39,lab,-125,13,16);
box(75,10,75,0x80938d,lab,150,11,-25);box(12,130,12,0x556f6a,lab,182,76,-48);box(70,10,12,0x556f6a,lab,153,139,-48);
const coinRig=new THREE.Group();lab.add(coinRig);coinRig.position.set(150,95,-25);
const coin=new THREE.Mesh(new THREE.CylinderGeometry(15,15,4,24),mat(0xd2a748));coinRig.add(coin);box(6,50,6,0x94a4a0,coinRig,0,26,0);
const sample=new THREE.Group();lab.add(sample);
const plank=new THREE.Mesh(new THREE.BoxGeometry(200,18,50,24,1,4),mat(0xd9b77d));sample.add(plank);
const originals=Float32Array.from(plank.geometry.attributes.position.array);
const grain=new THREE.Group();sample.add(grain);
for(let i=0;i<8;i++){const z=-21+i*6;for(let x=-96;x<85;x+=30)line([[x,10,z],[x+28,10,z+Math.sin(x)*.8]],0x91704b,grain);}
const knot=new THREE.Group();sample.add(knot);knot.position.set(-35,9.5,0);
for(let r=5;r<=17;r+=4){const points=[];for(let i=0;i<=32;i++){const t=i/32*Math.PI*2;points.push([Math.cos(t)*r,0,Math.sin(t)*r*.6]);}line(points,0x68472a,knot);}
const crack=line([[-99,9.7,12],[-65,9.7,10],[-30,9.7,14],[0,9.7,11],[38,9.7,13]],0x372e27,sample);
const dent=new THREE.Mesh(new THREE.CylinderGeometry(8,8,.8,20),mat(0x775334));sample.add(dent);dent.position.set(45,9.4,0);
const weather=new THREE.Group();lab.add(weather);
for(let i=0;i<7;i++){const drop=new THREE.Mesh(new THREE.SphereGeometry(4,8,6),mat(0x53a3c1));drop.scale.y=1.6;drop.position.set(-75+i*24,78+(i%2)*10,5);weather.add(drop);}
const magnifier=new THREE.Group();lab.add(magnifier);
const rim=[];for(let i=0;i<=32;i++){const t=i/32*Math.PI*2;rim.push([Math.cos(t)*23,0,Math.sin(t)*23]);}line(rim,0xa57725,magnifier);box(7,5,35,0x315f56,magnifier,0,0,39);
const guide=new THREE.Group();lab.add(guide);box(200,.8,50,0xcbd9d6,guide,0,5,40);
function restoreSample(){sample.position.set(0,18,45);sample.scale.set(1,1,1);sample.rotation.set(0,0,0);plank.geometry.attributes.position.array.set(originals);plank.geometry.attributes.position.needsUpdate=true;plank.geometry.computeVertexNormals();plank.material.color.setHex(wood.color);grain.visible=true;knot.visible=false;crack.visible=false;dent.visible=false;weather.visible=false;guide.visible=false;magnifier.visible=false;coinRig.position.y=95;}
function setTraceVisual(t,p){restoreSample();magnifier.visible=true;magnifier.position.set(-75+p*150,55,45);grain.visible=t.name!=='Verwerfen';if(t.name==='Ast')knot.visible=true;if(t.name==='Riss')crack.visible=true;if(t.name==='Verwerfen'){const pos=plank.geometry.attributes.position;for(let i=0;i<pos.count;i++){pos.setY(i,originals[i*3+1]+p*22*Math.pow(originals[i*3]/100,2));}pos.needsUpdate=true;plank.geometry.computeVertexNormals();}if(t.name==='Quellen'||t.name==='Schwinden'){guide.visible=true;sample.scale.z=1+(t.name==='Quellen'?1:-1)*.28*p;weather.visible=t.name==='Quellen';for(let i=0;i<weather.children.length;i++)weather.children[i].position.y=30+((i*13+p*90)%65);}}
function buttons(names,handler){$('choices').replaceChildren();for(const name of names){const b=document.createElement('button');b.className='choice';b.textContent=name;b.onclick=()=>handler(name);$('choices').append(b);}}
function feedback(s){$('feedback').textContent=s;}
function refreshEvidence(){const el=$('clues');el.replaceChildren();for(const type of evidence){const p=document.createElement('p');p.className='rounded-xl bg-teal-50 p-3 text-sm';p.textContent=type==='weigh'?`⚖️ ${wood.mass} g bei 180 cm³ → Dichte etwa ${(wood.mass/180).toFixed(2).replace('.',',')} g/cm³. Gleiches Volumen, ähnliche Feuchte: Mehr Masse bedeutet höhere Dichte.`:`🪙 Eine ${wood.mark} Münzspur. Gleiche Münze, gleicher Druck: Eine tiefere Spur spricht hier für geringere Härte. Das ist kein genormter Härtetest.`;el.append(p);}if(evidence.size===2){$('intro').textContent='Beide Spuren sind gesichert. Welches Etikett passt zu dieser Spielprobe? Schau bei Bedarf ins Spielarchiv.';buttons(woods.map(w=>w.name),chooseWood);feedback('Dichte und Härte sind unterschiedliche Eigenschaften. Vergleiche die Hinweise mit dem Spielarchiv.');}}
function startStation(type){if(phase!=='wood')return;action={type,start:performance.now(),duration:2600};restoreSample();$('weigh').disabled=true;$('coin').disabled=true;$('readout').textContent=type==='weigh'?'Die Waage wird auf null gestellt …':'Gleiche Münze · gleicher Druck …';}
$('weigh').onclick=()=>startStation('weigh');$('coin').onclick=()=>startStation('coin');
function chooseWood(name){if(name!==wood.name){feedback(`Fast eine Spur! Suche im Spielarchiv die Kombination aus ${wood.mass} g und ${wood.mark}r Münzspur. Du darfst beliebig oft kombinieren.`);return;}phase='wood-done';buttons([],()=>{});feedback(`Etikett gefunden: ${wood.name}! Jetzt wartet ein Brett mit einer neuen Spur auf dich.`);$('next').textContent='Brettspur untersuchen →';$('next').hidden=false;}
function startTrace(){phase='trace';evidence.clear();$('clues').replaceChildren();$('next').hidden=true;$('weigh').disabled=true;$('coin').disabled=true;$('scene-title').textContent=`Fall ${caseIndex+1} · Die Brettspur`;$('intro').textContent=trace.hint;feedback('Welche Spur erkennst du? Das Spurenbuch hilft dir beim Kombinieren.');buttons(traces.map(t=>t.name),chooseTrace);playTrace(trace);}
function playTrace(t){action={type:'trace',trace:t,start:performance.now(),duration:3000};$('readout').textContent=(t.name==='Quellen'||t.name==='Schwinden'||t.name==='Verwerfen')?'Zeitraffer · Veränderung stark vergrößert':'Die Lupe wandert über das Brett …';}
function chooseTrace(name){if(name!==trace.name){feedback(`Lies die Spur noch einmal: ${trace.hint} Öffne bei Bedarf das Spurenbuch.`);return;}phase='trace-done';action=null;setTraceVisual(trace,1);$('readout').textContent=trace.name;buttons([],()=>{});feedback(`Spur erkannt! ${trace.definition}`);$('next').textContent=caseIndex===2?'Fallakten abschließen →':'Nächste Probe →';$('next').hidden=false;}
$('next').onclick=()=>{if(phase==='wood-done')startTrace();else if(phase==='trace-done'){caseIndex++;if(caseIndex<3)loadCase();else finish();}else if(phase==='done')newGame();};
function loadCase(){finished=false;phase='wood';wood=cases[caseIndex].wood;trace=cases[caseIndex].trace;evidence.clear();action=null;restoreSample();$('progress').textContent=`${caseIndex+1} / 3`;$('scene-title').textContent=`Probe ${'ABC'[caseIndex]} · Dein Labortisch`;$('intro').textContent='Untersuche die namenlose Probe. Zwei Stationen geben dir die Spuren.';$('clues').replaceChildren();$('choices').replaceChildren();$('next').hidden=true;$('weigh').disabled=false;$('coin').disabled=false;$('readout').textContent='Mit einem Finger drehen · mit zwei Fingern zoomen';feedback('Kein Countdown. Keine Punktabzüge. Hinweise helfen dir weiter.');$('definition').textContent='';}
function finish(){phase='done';finished=true;action=null;$('progress').textContent='3 / 3 ✓';$('mission').textContent='Alle Etiketten zurück! Deine drei Fallakten sind abgeschlossen. Du kannst weiter im Spurenbuch stöbern oder eine neue Runde spielen.';$('intro').textContent='Du hast Masse und Volumen zur Dichte verbunden, Härte mit der Münzspur verglichen und drei Brettspuren erkannt.';feedback('Holz nimmt Feuchtigkeit auf und gibt sie ab. Quellen und Schwinden gehören dazu. Ast, Riss und Verwerfen beschreiben andere Spuren.');$('next').textContent='Neue Fallakten öffnen ↻';$('next').hidden=false;$('lexicon').open=true;}
function newGame(){const ws=shuffle(woods),ts=shuffle(traces);cases=ws.map((w,i)=>({wood:w,trace:ts[i]}));caseIndex=0;$('mission').textContent='Drei Proben, keine Etiketten! Sammle Hinweise im Labor und finde ihre Namen. Du kannst alles in Ruhe ausprobieren.';loadCase();}
for(const t of traces){const b=document.createElement('button');b.className='rounded-full bg-stone-100 px-4 py-2 font-bold hover:bg-amber-100';b.textContent=t.name;b.onclick=()=>{if(phase==='wood'&&action)return; // Never interrupt an active measurement.
$('definition').textContent=t.definition;if(phase==='wood'){action=null;restoreSample();setTraceVisual(t,1);$('readout').textContent=`Spurenbuch: ${t.name} · Station wählen zum Weitermachen`;}else if(phase==='trace'){playTrace(trace);$('readout').textContent='Deine Fallspur bleibt sichtbar · Worterklärung im Spurenbuch';}else playTrace(t);};$('terms').append(b);}
function resize(){const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();}new ResizeObserver(resize).observe(host);resize();
let hiddenAt=null;document.addEventListener('visibilitychange',()=>{if(document.hidden)hiddenAt=performance.now();else if(hiddenAt!==null){if(action)action.start+=performance.now()-hiddenAt;hiddenAt=null;}});
function frame(now){requestAnimationFrame(frame);if(document.hidden)return;if(action){const a=action,p=Math.min(1,(now-a.start)/a.duration),smooth=p*p*(3-2*p);if(a.type==='weigh'){sample.position.set(-125*smooth,18+14*smooth+Math.sin(p*Math.PI)*55,45-75*smooth);if(p>.75)$('readout').textContent=`${wood.mass} g · Volumen 180 cm³`;}else if(a.type==='coin'){sample.position.set(150*smooth,18,45-70*smooth);coinRig.position.y=95-66*Math.sin(p*Math.PI/2);dent.visible=p>.7;dent.scale.set(wood.depth/5,1,wood.depth/5);dent.position.x=0;}else setTraceVisual(a.trace,smooth);if(p===1){action=null;if(a.type==='weigh'||a.type==='coin'){evidence.add(a.type);$('weigh').disabled=false;$('coin').disabled=false;$('readout').textContent=a.type==='weigh'?`${wood.mass} g · Dichte ≈ ${(wood.mass/180).toFixed(2).replace('.',',')} g/cm³`:`${wood.mark[0].toUpperCase()+wood.mark.slice(1)} Münzspur`;refreshEvidence();}else $('readout').textContent=phase==='trace'?'Welche Spur zeigt das Brett?':`Spurenbuch: ${a.trace.name}`;}}controls.update();renderer.render(scene,camera);}
Object.defineProperty(window,'holzdetektive',{get:()=>({caseIndex,phase,evidence:[...evidence],finished,svgMode,camera:camera.position.toArray(),dimensions:[200,50,18],animation:action?.type??null})});
newGame();requestAnimationFrame(frame);
