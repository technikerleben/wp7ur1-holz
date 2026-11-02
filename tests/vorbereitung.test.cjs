const {JSDOM}=require('jsdom'),fs=require('fs'),assert=require('node:assert/strict');
const root=require('path').join(__dirname,'..')+'/';
function setup(when='2026-11-01T10:00:00Z',memory={}){
 const dom=new JSDOM(fs.readFileSync(root+'lernweg.html','utf8'),{url:'https://wp7ur1-holz.vercel.app/lernweg.html',runScripts:'outside-only'}),w=dom.window;
 let now=when;const RealDate=w.Date;w.Date=class extends RealDate{constructor(...args){super(...(args.length?args:[now]));}};
 w.HTMLDialogElement.prototype.showModal=function(){this.setAttribute('open','');};w.HTMLDialogElement.prototype.close=function(){this.removeAttribute('open');};
 for(const [k,v]of Object.entries(memory))w.localStorage.setItem(k,v);
 for(const f of ['kurs-daten.js','lernweg.js','vorbereitung-daten.js','vorbereitung.js'])w.eval(fs.readFileSync(root+f,'utf8'));
 const $=s=>w.document.querySelector(s),click=s=>{assert.ok($(s),'element '+s);$(s).click();},submit=s=>$(s).dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));
 return {dom,w,$,click,submit,day:v=>{now=v;w.dispatchEvent(new w.Event('pageshow'));},unlock:value=>{$('#exam-key').value=value;submit('#exam-unlock');},memory:()=>Object.fromEntries(Object.keys(w.localStorage).map(k=>[k,w.localStorage.getItem(k)]))};
}
for(const date of ['2026-10-31T12:00:00Z','2026-11-03T12:00:00Z','2026-11-04T12:00:00Z']){const t=setup(date);assert.equal(t.$('#exam-notice').open,false);t.dom.window.close();}
let t=setup();assert.equal(t.$('#exam-notice').open,true);
assert.equal(t.$('#exam-notice').dispatchEvent(new t.w.Event('cancel',{cancelable:true})),false);assert.equal(t.$('#exam-notice').open,true);
assert.equal(t.$('#exam-key').dispatchEvent(new t.w.KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true})),false);
t.unlock('iPad');assert.equal(t.$('#exam-notice').open,true);assert.match(t.$('#exam-key-feedback').textContent,/Wo sammelst/);assert.equal(t.w.localStorage.getItem('hbg_holz_pruefung_gelesen_2026-11-01'),null);
t.unlock('  mApPe  ');assert.equal(t.$('#exam-notice').open,false);assert.equal(t.$('#exam-prep').hidden,false);assert.match(t.$('#exam-prep').textContent,/Prüflabor geöffnet/);
let mem=t.memory(),reloaded=setup('2026-11-01T12:00:00Z',mem);assert.equal(reloaded.$('#exam-notice').open,false);reloaded.day('2026-11-02T08:00:00Z');assert.equal(reloaded.$('#exam-notice').open,true);reloaded.unlock('MAPPE');reloaded.day('2026-11-03T08:00:00Z');assert.equal(reloaded.$('#exam-notice').open,false);reloaded.dom.window.close();
assert.equal(t.w.HOLZ_PREP_RULES.berlinDay(new t.w.Date('2026-11-01T23:30:00Z')),'2026-11-02');
t.click('[data-prep="next"]');t.click('[data-prep="next"]');
const R=t.w.HOLZ_PREP_RULES;let total=0;
for(let i=0;i<4;i++){
 const topic=t.w.HOLZ_VORBEREITUNG[i];t.click(`[data-topic="${i}"]`);
 for(let j=0;j<3;j++){
  const q=topic.questions[j];
  // Incomplete submissions must not receive feedback.
  t.submit('#prep-answer');assert.match(t.$('#prep-answer-error').textContent,/Wähle/);
  // First unknown attempt leads to explanation then the matching retry.
  t.click('[data-prep="unknown"]');assert.match(t.$('.prep-feedback').textContent,/Schlage nach/);t.click('[data-prep="quiz-next"]');
  const variant=topic.retries[j];
  if(variant.type==='choice')variant.correct.forEach(n=>t.click(`input[name="answer"][value="${n}"]`));
  else variant.fields.forEach((f,n)=>{t.$(`[name="field-${n}"]`).value=f.answers[0];});
  t.submit('#prep-answer');assert.ok(t.$('.is-correct'));t.click('[data-prep="quiz-next"]');
  for(const item of [q,variant]){
   const good=item.type==='choice'?item.correct:item.fields.map(f=>f.answers[0]);assert.equal(R.grade(item,good),true);assert.equal(R.grade(item,[]),false);
   if(item.type==='choice'&&item.multi)assert.equal(R.grade(item,item.options.map((_,n)=>n)),false);
   total++;
  }
 }
 assert.match(t.$('#exam-prep').textContent,/Runde beendet/);t.click('[data-prep="topics"]');
}
t.click('[data-prep="next"]');assert.ok(t.$('a[href="materialien/mini-probe-vorbereitung.pdf"]'));assert.match(t.$('#exam-prep').textContent,/Goodnotes/);assert.match(t.$('#exam-prep').textContent,/Danach vergleichen/);t.click('[data-prep="next"]');assert.match(t.$('#exam-prep').textContent,/Lösungen zur Mini-Probe/);assert.match(t.$('#exam-prep').textContent,/direkt in der PDF/);
for(let n=0;n<3;n++)t.click(`[data-ready="${n}"]`);t.click('[data-prep="finish"]');assert.match(t.$('#prep-finish-status').textContent,/abgeschlossen/);
assert.equal(JSON.parse(t.w.localStorage.getItem('hbg_holz_navigator_v2')).done.length,0);
t.click('[data-prep="exit"]');assert.equal(t.$('#exam-prep').hidden,true);assert.ok(!t.w.document.body.classList.contains('prep-active'));
t.dom.window.close();
// Storage denial does not block a correct unlock, and the in-memory acknowledgement holds for this visit.
t=setup();Object.defineProperty(t.w,'localStorage',{get(){throw Error('denied');}});t.unlock('Mappe');assert.equal(t.$('#exam-notice').open,false);t.day('2026-11-01T11:00:00Z');assert.equal(t.$('#exam-notice').open,false);t.dom.window.close();
console.log(`PASS: date boundaries, Berlin midnight, both reminder days, no escape dismissal, wrong/correct key, daily persistence, ${total} task keys, partial answers, all-topic UI flow, retries, paper and solutions, checklist, original course progress, blocked storage.`);
