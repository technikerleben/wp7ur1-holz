/* Ergänzung zum Navigator. Eigenständiger Übungsstand; verändert keine A1–A10-Häkchen. */
(() => {
  'use strict';
  const topics=window.HOLZ_VORBEREITUNG;
  const $=id=>document.getElementById(id);
  const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const normalize=s=>String(s).normalize('NFKC').trim().replace(/\s+/g,' ').toLocaleLowerCase('de');
  const berlinDay=(date=new Date())=>new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Berlin',year:'numeric',month:'2-digit',day:'2-digit'}).format(date);
  const noticeDay=day=>['2026-11-01','2026-11-02'].includes(day);
  const validKey=value=>normalize(value)==='mappe';
  function grade(q,answers){
    if(q.type==='choice')return answers.length===q.correct.length&&q.correct.every(i=>answers.includes(i));
    return q.fields.every((f,i)=>f.answers.some(a=>normalize(a)===normalize(answers[i]||'')));
  }
  // Kleine reine Funktionen für Datums-, Lösungs- und Antwortprüfungen.
  window.HOLZ_PREP_RULES=Object.freeze({berlinDay,noticeDay,validKey,grade});
  const storeKey='hbg_holz_vorbereitung_2026_11_v1';
  let phase=0,checks=[false,false,false],question='',active=false;
  try{const saved=JSON.parse(localStorage.getItem(storeKey));if(saved){if(Number.isInteger(saved.phase)&&saved.phase>=0&&saved.phase<=4)phase=saved.phase;if(Array.isArray(saved.checks))checks=checks.map((_,i)=>saved.checks[i]===true);if(typeof saved.question==='string')question=saved.question.slice(0,1000);}}catch{}
  function save(){try{localStorage.setItem(storeKey,JSON.stringify({phase,checks,question}));}catch{}}
  const names=['Mappe startklar','Wissen wecken','Gezielt üben','Auf Papier üben','Prüfen und klären'],times=[5,8,15,10,7],icons=['📁','🧠','📱','✍️','📁'];
  let topicIndex=null,qIndex=0,retry=false,feedback=false,lastOK=false,answers=[],firstResults=[];
  const nav=()=>`<div class="prep-controls"><button type="button" data-prep="exit">🧭 Zum normalen Lernweg</button><span>Dein Schritt und deine Abschluss-Checkliste bleiben auf diesem Gerät gespeichert.</span></div>`;
  function links(ids){return ids.map(id=>`<a href="materialien/a${id}.pdf" target="_blank" rel="noopener">A${id} öffnen ↗</a>`).join(' · ');}
  function render(focus=true){
    const panel=$('exam-prep');
    let html=`${nav()}<p class="eyebrow">VORBEREITUNG · SCHRITT ${phase+1} VON 5 · ETWA ${times[phase]} MINUTEN</p><h2 id="prep-title">${icons[phase]} ${names[phase]}</h2><ol class="prep-steps" aria-label="Dein Vorbereitungsweg">${names.map((n,i)=>`<li ${i===phase?'aria-current="step"':''}>${i+1}. ${n}</li>`).join('')}</ol><div class="prep-work"><strong>${icons[phase]} Jetzt: ${['mit deiner Mappe arbeiten','erinnern und besprechen','hier digital üben · Mappe erlaubt','auf Papier arbeiten · iPad schließen','Mappe prüfen und Fragen klären'][phase]}</strong></div>`;
    if(phase===0)html+=`<p class="prep-instruction">Lege deine Unterlagen zu A1–A8 bereit. Ordne sie nach Auftragsnummern. Prüfe, ob deine Ergebnisse eingetragen sind. Melde fehlende Blätter deiner Lehrkraft.</p><ul><li>A1/A2: Stamm und Jahresringe</li><li>A3/A4: Produktionsweg und Schnittplan</li><li>A5/A6: Prüfprotokoll und Prüfbericht</li><li>A7/A8: Holzfeuchte und Holzfehler</li></ul><p>Markiere die Bereiche mit vorhandenen Trennblättern oder kleinen Haftzetteln. Du sollst schnell etwas finden können.</p><details><summary>Ein Blatt fehlt? Druckvorlagen öffnen</summary><p>Die Dateien öffnen sich in einem neuen Tab. Bitte deine Lehrkraft um einen Ausdruck.</p><p>${links([1,2,3,4,5,6,7,8])}</p><a href="materialien/holzforscher-mappe.pdf" target="_blank" rel="noopener">Ganze Mappe öffnen ↗</a></details>`;
    if(phase===1)html+=`<p class="prep-instruction">Schließe deine Mappe kurz. Erkläre einem Partner, was du noch weißt. Wenn du allein übst, sprich leise oder notiere Stichwörter auf Papier.</p><ul class="prep-prompts"><li>Welche Aufgaben haben Borke, Bast, Kambium und Splintholz? Was zeigen Jahresringe? <small>A1/A2</small></li><li>Wie wird aus einem Baum ein Brett? Worauf achtest du beim Schnittplan? <small>A3/A4</small></li><li>Welche Eigenschaften habt ihr geprüft? Wie verbindest du Beobachtung, Eigenschaft und Verwendung? <small>A5/A6</small></li><li>Was bedeuten Quellen und Schwinden? Wie erkennst du Ast, Riss und Verwerfen? <small>A7/A8</small></li></ul><p><strong>Öffnet danach eure Mappen.</strong> Ergänzt und verbessert eure Erklärungen. Wähle für den nächsten Schritt den Bereich, bei dem du noch unsicher bist.</p>`;
    if(phase===2)html+=quiz();
    if(phase===3)html+=`<p class="prep-instruction">Übe etwa 10 Minuten wie in der Klassenarbeit: Bearbeite die Mini-Probe auf Papier. Nutze deine gedruckten Unterlagen und Notizen zum Nachschlagen.</p><div class="prep-paper"><strong>1. Aufgaben bereitlegen</strong><p>Nutze den Ausdruck deiner Lehrkraft. Du kannst die Druckvorlage vorher öffnen und drucken. Wenn du keinen Ausdruck hast, übertrage zuerst die sechs Aufgaben auf ein leeres Blatt.</p><a class="button" href="vorbereitung-papier.html" target="_blank" rel="noopener">📄 Mini-Probe öffnen / drucken ↗</a><strong>2. iPad schließen</strong><p>Bearbeite die Aufgaben mit Stift und Mappe. Suche gezielt die passende Information.</p><strong>3. Zur Kontrolle zurückkehren</strong><p>Öffne das iPad erst wieder, wenn du fertig bist. Gehe dann hier weiter.</p></div><p>Die Mini-Probe ist eine Übung. Sie enthält eigene Beispiele und keine Aufgaben der Klassenarbeit.</p>`;
    if(phase===4)html+=`<p class="prep-instruction">Vergleiche deine Papierantworten mit der Lösung. Verbessere deine Antworten und deine Unterlagen.</p><details><summary>✓ Lösungen zur Mini-Probe ansehen</summary><ol><li>Borke; Kambium. Die Borke schützt außen, das Kambium ermöglicht Dickenwachstum.</li><li>B. Ein schmaler Jahresring zeigt weniger Dickenzuwachs. Die Ursache bleibt offen.</li><li>3 – 1 – 4 – 2. Baum → Fällen → Transport zum Sägewerk → Einschnitt.</li><li>B und C. Der Plan muss den Auftrag erfüllen. Die Schnittbreite erzeugt Späne.</li><li>B; flacher. Der Vergleich gilt bei gleicher Münze und gleichem Druck. Eine kleine Druckspur spricht für höhere Härte; das ist für eine belastete Oberfläche günstig.</li><li>Wasser; Schwinden; 2 – 3 – 1. Wasserabgabe senkt die Masse. Kleinerwerden heißt Schwinden. Zweigansatz = Ast, verbogen = Verwerfen, offener Spalt = Riss.</li></ol></details><p><strong>Wie hat das Nachschlagen geklappt?</strong> Hast du die passende Information schnell gefunden und für deine Antwort genutzt?</p><div class="prep-checks">${['Meine Unterlagen sind vollständig und geordnet.','Ich finde wichtige Informationen zu A1–A8.','Ich kann mit meinen Unterlagen kurze Prüfungsaufgaben lösen.'].map((s,i)=>`<label><input type="checkbox" data-ready="${i}" ${checks[i]?'checked':''}> ${s}</label>`).join('')}</div><label for="prep-question"><strong>Meine offene Frage:</strong></label><textarea id="prep-question" maxlength="1000" rows="3" placeholder="Notiere deine Frage. Kläre sie vor Stundenende mit deiner Lehrkraft.">${esc(question)}</textarea><p>Wenn dir noch etwas fehlt: Gehe zum passenden Schritt zurück oder frage deine Lehrkraft. Eine offene Frage ist ein guter nächster Lernschritt.</p><p class="prep-reminder"><strong>Mittwoch mitbringen:</strong> vollständige Mappe, weitere erlaubte Papierunterlagen und Schreibzeug. Die Klassenarbeit dauert 30 Minuten. Dein iPad bleibt geschlossen. Pflicht: A1–A8; eine freiwillige Bonusaufgabe zu A9/A10.</p><p id="prep-finish-status" role="status"></p><button type="button" class="primary" data-prep="finish">Vorbereitung abschließen</button>`;
    html+=`<div class="tools prep-footer">${phase>0?'<button type="button" data-prep="back">← Vorheriger Schritt</button>':''}${phase<4?`<button type="button" class="primary" data-prep="next">${phase===2?'Mit der Auswahl fertig · zur Papierphase':'Erledigt · weiter'} →</button>`:''}</div>`;
    panel.innerHTML=html;save();if(focus)panel.focus({preventScroll:true});
  }
  function quiz(){
    if(topicIndex===null)return `<p class="prep-instruction">Wähle einen Bereich, bei dem du noch unsicher bist. Nutze deine Mappe. Du erhältst nach jeder Antwort eine Erklärung und bei Bedarf eine ähnliche zweite Aufgabe.</p><div class="prep-topic-grid">${topics.map((t,i)=>`<button type="button" data-topic="${i}"><strong>${esc(t.title)}</strong><span>${esc(t.scope)} · 3 kurze Aufgaben</span></button>`).join('')}</div><p>Du musst nicht alle Bereiche schaffen. Wähle gezielt und verbessere deine Mappe.</p>`;
    const t=topics[topicIndex];
    if(qIndex>=t.questions.length)return `<h3>${esc(t.title)} · Runde beendet</h3><p>Im ersten Versuch hast du ${firstResults.filter(Boolean).length} von ${t.questions.length} Aufgaben vollständig gelöst. Nachschlagen in der Mappe ist erlaubt. Ähnliche zweite Aufgaben zählen separat als Übung.</p><p>Ergänze jetzt die Hinweise, die dir in deiner Mappe gefehlt haben.</p><button type="button" data-prep="topics">Anderen Bereich wählen</button>`;
    const q=(retry?t.retries:t.questions)[qIndex];
    const mode=q.type==='choice'?(q.multi?'Mehrere Antworten sind richtig.':'Nur eine Antwort ist richtig.'):q.type==='order'?'Trage nur die passenden Zahlen ein.':'Ergänze nur die fehlenden Wörter.';
    let fields='';
    if(q.type==='choice')fields=q.options.map((s,i)=>`<label class="prep-option"><input type="${q.multi?'checkbox':'radio'}" name="answer" value="${i}" ${feedback?'disabled':''} ${answers.includes(i)?'checked':''}> ${String.fromCharCode(65+i)}: ${esc(s)}</label>`).join('');
    else fields=q.fields.map((f,i)=>`<label class="prep-field">${esc(f.label)}<input name="field-${i}" aria-label="${esc(f.label)}" autocomplete="off" ${q.type==='order'?'inputmode="numeric"':''} ${feedback?'disabled':''} value="${esc(answers[i]||'')}"></label>`).join('');
    let result='';
    if(feedback){
      const correct=q.type==='choice'?q.correct.map(i=>String.fromCharCode(65+i)+': '+q.options[i]).join(' · '):q.fields.map((f,i)=>`${f.label} ${f.answers[0]}${normalize(answers[i]||'')===normalize(f.answers[0])?' ✓':''}`).join(' · ');
      const optionFeedback=q.type==='choice'?q.options.map((s,i)=>`<li>${String.fromCharCode(65+i)}: ${q.correct.includes(i)?(answers.includes(i)?'Richtig gewählt':'Diese passende Antwort fehlt'):(answers.includes(i)?'Diese Auswahl passt nicht':'Richtig nicht gewählt')}.</li>`).join(''):q.fields.map((f,i)=>`<li>${esc(f.label)} Deine Antwort: ${esc(answers[i]||'offen')} · ${f.answers.some(a=>normalize(a)===normalize(answers[i]||''))?'passt':'passend: '+esc(f.answers[0])}.</li>`).join('');
      result=`<div class="prep-feedback ${lastOK?'is-correct':''}" role="status"><strong>${lastOK?'✓ Das passt.':'Schau dir diese Stelle noch einmal an.'}</strong><ul>${optionFeedback}</ul><p>${esc(q.explanation)}</p><p><strong>Schlage nach: ${esc(q.sheet)}.</strong> Ergänze dort bei Bedarf eine kurze Notiz.</p><p>Passende Lösung: ${esc(correct)}</p></div><button type="button" class="primary" data-prep="quiz-next">${!lastOK&&!retry?'Eine ähnliche Aufgabe üben →':'Nächste Aufgabe →'}</button>`;
    }
    return `<p class="eyebrow">${esc(t.title)} · ${retry?'ÄHNLICHE ZWEITE AUFGABE':'AUFGABE '+(qIndex+1)+' VON '+t.questions.length}</p><form id="prep-answer"><fieldset><legend>${esc(q.prompt)}</legend><p><strong>${mode}</strong></p>${fields}</fieldset>${!feedback?'<p id="prep-answer-error" role="status"></p><div class="tools"><button class="primary" type="submit">Antwort prüfen</button><button type="button" data-prep="unknown">Ich weiß es noch nicht · Erklärung ansehen</button></div>':''}</form>${result}<button type="button" class="prep-small" data-prep="topics">Zur Themenauswahl</button>`;
  }
  function start(){active=true;document.body.classList.add('prep-active');$('exam-prep').hidden=false;render();}
  function exit(){active=false;document.body.classList.remove('prep-active');$('exam-prep').hidden=true;$('exam-start').focus();}
  $('exam-start').addEventListener('click',start);
  $('exam-overview').addEventListener('click',()=>{$('overview').close();start();});
  // Vorhandene Navigation bleibt verfügbar und führt zurück in den normalen Lernweg.
  for(const id of ['nav-back','nav-overview','overview-open'])$(id).addEventListener('click',()=>{if(active)exit();});
  $('exam-prep').addEventListener('click',event=>{
    const pick=event.target.closest('[data-topic]');if(pick){topicIndex=Number(pick.dataset.topic);qIndex=0;retry=false;feedback=false;answers=[];firstResults=[];render();return;}
    const action=event.target.closest('[data-prep]')?.dataset.prep;if(!action)return;
    if(action==='exit'){exit();return;}
    if(action==='next'||action==='back'){phase+=action==='next'?1:-1;render();return;}
    if(action==='topics'){topicIndex=null;render();return;}
    if(action==='quiz-next'){if(!lastOK&&!retry)retry=true;else{qIndex++;retry=false;}answers=[];feedback=false;render();return;}
    if(action==='unknown'){answers=[];feedback=true;lastOK=false;if(!retry)firstResults[qIndex]=false;render();return;}
    if(action==='finish'){const ok=checks.every(Boolean)&&!question.trim();$('prep-finish-status').textContent=ok?'✓ Deine Vorbereitung ist abgeschlossen. Packe deine Unterlagen für Mittwoch ein.':'Prüfe noch offene Punkte und kläre deine Frage mit deiner Lehrkraft. Du kannst danach hierher zurückkehren.';}
  });
  $('exam-prep').addEventListener('submit',event=>{
    if(event.target.id!=='prep-answer')return;event.preventDefault();const q=(retry?topics[topicIndex].retries:topics[topicIndex].questions)[qIndex];const data=new FormData(event.target);
    answers=q.type==='choice'?data.getAll('answer').map(Number):q.fields.map((_,i)=>String(data.get('field-'+i)||''));
    if(!answers.length||answers.some(a=>String(a).trim()==='')){$('prep-answer-error').textContent='Wähle eine Antwort oder fülle jedes Feld aus. Du kannst auch „Ich weiß es noch nicht“ wählen.';return;}
    lastOK=grade(q,answers);if(!retry)firstResults[qIndex]=lastOK;feedback=true;render();
  });
  $('exam-prep').addEventListener('change',event=>{if(event.target.matches('[data-ready]')){checks[Number(event.target.dataset.ready)]=event.target.checked;save();}});
  $('exam-prep').addEventListener('input',event=>{if(event.target.id==='prep-question'){question=event.target.value;save();}});
  const notice=$('exam-notice'),memory=new Set(),ackPrefix='hbg_holz_pruefung_gelesen_';
  notice.addEventListener('cancel',event=>event.preventDefault());
  function showNotice(){
    const day=berlinDay();if(!noticeDay(day)||memory.has(day))return;
    try{if(localStorage.getItem(ackPrefix+day)==='mappe')return;}catch{}
    if(notice.open)return;
    document.querySelectorAll('dialog[open]').forEach(d=>d.close());$('exam-key').value='';$('exam-key-feedback').textContent='';notice.showModal();$('exam-key').focus();
  }
  $('exam-unlock').addEventListener('submit',event=>{
    event.preventDefault();if(!validKey($('exam-key').value)){$('exam-key-feedback').textContent='Lies noch einmal nach: Wo sammelst du deine Unterlagen?';$('exam-key').setAttribute('aria-invalid','true');$('exam-key').focus();return;}
    const day=berlinDay();memory.add(day);try{localStorage.setItem(ackPrefix+day,'mappe');}catch{}
    $('exam-key').removeAttribute('aria-invalid');notice.close();start();const success=document.createElement('p');success.className='prep-success';success.textContent='🔓 Prüflabor geöffnet! Starte jetzt deine Vorbereitung.';$('exam-prep').prepend(success);
  });
  window.addEventListener('pageshow',showNotice);document.addEventListener('visibilitychange',()=>{if(!document.hidden)showNotice();});
  showNotice();
})();
