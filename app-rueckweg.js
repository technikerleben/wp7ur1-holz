'use strict';
window.addEventListener('DOMContentLoaded',()=>{
 const script=document.querySelector('script[src$="app-rueckweg.js"]');
 const root=new URL('.',script.src),q=new URLSearchParams(location.search),id=q.get('von');
 const allowed=/^A(?:[1-9]|10)$/.test(id||'');
 const tasks=window.HOLZ_KURS?.tasks||[],task=tasks.find(t=>t.id===id);
 const index=q.get('schritt'),step=task&&(index==='extra'?task.extra:/^\d+$/.test(index||'')?task.steps[Number(index)]:null);
 const file=location.pathname.split('/').pop(),practice=file==='pruefstation.html';
 const titles={'baumscheibe.html':'Baumscheibe','produktionskette.html':'Produktionskette','schnittplan.html':'Schnittplan','pruefstation.html':'Prüflabor','holzfehler.html':'Holzfehler','steckbriefe.html':'Holzberatung','zwischencheck.html':'Holz-Check','kompetenzcheck.html':'Kompetenzcheck'};
 const title=titles[file]||'Holz-Spiel';
 document.body.classList.add('learning-app');if(location.pathname.includes('/Spiel/'))document.body.classList.add('learning-game');
 const bar=document.createElement('nav');bar.className='app-return';bar.setAttribute('aria-label','App und Rückweg zum Navigator');
 const label=document.createElement('div');label.className='app-return__identity';
 const icon=document.createElement('span');icon.className='app-return__icon';icon.textContent='📱';icon.setAttribute('aria-hidden','true');
 const words=document.createElement('div'),strong=document.createElement('strong'),sub=document.createElement('span');strong.textContent='Du bist in einer App';sub.textContent=title+(allowed?' · Auftrag '+id:'');words.append(strong,sub);label.append(icon,words);
 const a=document.createElement('a'),url=new URL('lernweg.html',root);if(allowed)url.searchParams.set('auftrag',id);a.href=url.href;a.textContent='🧭 Zurück '+(allowed?'zu '+id+' im Lernweg':'zum Lernweg');
 bar.append(label,a);document.body.prepend(bar);
 const guide=document.createElement('aside');guide.className='app-work-guide';guide.setAttribute('aria-label','Dein Arbeitsort');
 const heading=document.createElement('strong');heading.textContent=practice?'🔬 Jetzt an der Holzprobe arbeiten · 📄 A5.1 bereitlegen':'📱 Jetzt in dieser App arbeiten';guide.append(heading);
 const instruction=document.createElement('p');instruction.textContent=step?.text||(practice?'Lies die Anleitung hier. Untersuche deine Holzprobe und notiere die Ergebnisse auf A5.1.':file==='zwischencheck.html'?'Bearbeite die Aufgaben digital. Deine Übungsempfehlung notierst du anschließend auf U.1.':file==='kompetenzcheck.html'?'Bearbeite den Check hier und beachte die Hinweise zu deiner Mappe.':'Bearbeite die Aufgabe hier. Danach führt dich der grüne Knopf zurück zum Lernweg.');guide.append(instruction);
 if(step){const next=document.createElement('p');next.className='app-work-guide__next';const nextStep=index!=='extra'?task.steps[Number(index)+1]:null;next.textContent=nextStep?'Danach im Lernweg: '+nextStep.text:'Danach: Kehre zum Lernweg zurück und bestätige deinen Arbeitsschritt.';guide.append(next);}
 bar.after(guide);
 const groups=new Map();document.querySelectorAll('details.tipp-details').forEach(d=>{const parent=d.parentElement;if(!groups.has(parent))groups.set(parent,[]);groups.get(parent).push(d);});
 groups.forEach(ds=>ds.forEach((d,i)=>{if(i)d.hidden=true;d.addEventListener('toggle',()=>{if(d.open&&ds[i+1])ds[i+1].hidden=false;});}));
});
