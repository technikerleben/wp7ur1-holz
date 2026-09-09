'use strict';
window.addEventListener('DOMContentLoaded',()=>{
 const q=new URLSearchParams(location.search),id=q.get('von');
 const allowed=/^A(?:[1-9]|10)$/.test(id||'');
 const bar=document.createElement('div');bar.className='app-return';
 const a=document.createElement('a');a.href='lernweg.html'+(allowed?'?auftrag='+id:'');a.textContent='← Zurück zum Lernweg';
 const p=document.createElement('span');p.textContent='📁 Schreibe deine Ergebnisse auf Papier.';
 bar.append(a,p);document.body.prepend(bar);
 // Successive hints: reveal only the next summary after the current hint is opened.
 const groups=new Map();document.querySelectorAll('details.tipp-details').forEach(d=>{const parent=d.parentElement;if(!groups.has(parent))groups.set(parent,[]);groups.get(parent).push(d);});
 groups.forEach(ds=>ds.forEach((d,i)=>{if(i)d.hidden=true;d.addEventListener('toggle',()=>{if(d.open&&ds[i+1])ds[i+1].hidden=false;});}));
});
