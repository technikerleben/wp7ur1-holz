(() => {
  "use strict";

  const QUESTIONS = [
    {
      topic:"Wald", level:"Einstieg",
      q:"Welche Aufgabe hat die Rinde eines Baumes?",
      a:["Sie schützt den Baum.","Sie transportiert Wasser.","Sie bildet die Äste.","Sie trocknet das Kernholz."],
      correct:0,
      hint:"Denkt an die äußerste Schicht des Baumes.",
      explain:"Die Rinde liegt außen und schützt den Baum."
    },
    {
      topic:"Wald", level:"Einstieg",
      q:"Welcher Teil des Baumes transportiert Wasser von den Wurzeln nach oben?",
      a:["Kernholz","Splintholz","Rinde","Borke"],
      correct:1,
      hint:"Gesucht ist die Schicht direkt unter der Rinde.",
      explain:"Das Splintholz transportiert Wasser und Nährstoffe von den Wurzeln zu den Blättern."
    },
    {
      topic:"Baumfällung", level:"Einstieg",
      q:"Wie nennt man das Entfernen der Äste nach dem Fällen?",
      a:["Trocknen","Stapeln","Entasten","Schälen"],
      correct:2,
      hint:"Der Fachbegriff beginnt mit „Ent…“.",
      explain:"Das Entfernen der Äste eines gefällten Baumes heißt Entasten."
    },
    {
      topic:"Baumfällung", level:"Grundwissen",
      q:"Warum wird die Rinde nach dem Fällen vom Stamm entfernt?",
      a:["Damit das Holz schwerer wird.","Damit das Holz besser trocknen kann.","Damit der Stamm länger wird.","Damit das Kernholz weicher wird."],
      correct:1,
      hint:"Überlegt, was vor der weiteren Verarbeitung mit der Feuchtigkeit passieren muss.",
      explain:"Die Rinde wird entfernt, damit das Holz besser trocknen kann."
    },
    {
      topic:"Transport", level:"Grundwissen",
      q:"Wohin wird ein vorbereiteter Baumstamm nach der Baumfällung gebracht?",
      a:["Direkt in den Baumarkt","Ins Sägewerk","Zurück in den Wald","In eine Möbelwerkstatt"],
      correct:1,
      hint:"Dort wird aus dem Stamm erst ein Brett.",
      explain:"Der vorbereitete Stamm wird ins Sägewerk gebracht."
    },
    {
      topic:"Transport", level:"Grundwissen",
      q:"Warum werden für den Transport von Baumstämmen große Maschinen und LKW eingesetzt?",
      a:["Weil die Stämme sehr schwer sind.","Weil Holz nicht nass werden darf.","Weil nur Maschinen den Wald verlassen dürfen.","Weil der Stamm dabei schon gesägt wird."],
      correct:0,
      hint:"Denkt an Masse und Größe eines ganzen Baumstamms.",
      explain:"Große Maschinen und LKW können die sehr schweren Baumstämme bewegen."
    },
    {
      topic:"Sägewerk", level:"Anwendung",
      q:"Welche Reihenfolge passt zur Arbeit im Sägewerk?",
      a:[
        "Trocknen → Sägen → Fällen",
        "Sägen → Trocknen → Weiterverarbeiten",
        "Transport → Pflanzen → Sägen",
        "Trocknen → Rinde wachsen lassen → Sägen"
      ],
      correct:1,
      hint:"Erst muss aus dem Stamm ein Brett werden. Danach wird seine Feuchtigkeit wichtig.",
      explain:"Im Sägewerk wird der Stamm zuerst in Bretter geschnitten. Danach werden die Bretter getrocknet."
    },
    {
      topic:"Sägewerk", level:"Anwendung",
      q:"Ein frisch gesägtes Brett ist noch sehr feucht. Warum sollte es noch nicht direkt verarbeitet werden?",
      a:[
        "Es könnte sich verziehen oder brechen.",
        "Es würde sofort zu Kernholz werden.",
        "Es wäre zu leicht für Möbel.",
        "Es könnte wieder Äste bilden."
      ],
      correct:0,
      hint:"Feuchtigkeit kann die Form und Stabilität des Holzes verändern.",
      explain:"Zu feuchtes Holz kann sich verziehen oder brechen. Deshalb werden Bretter nach dem Sägen getrocknet."
    },
    {
      topic:"Sägewerk", level:"Anwendung",
      q:"Welche Maschine wird in der Reihe als Beispiel dafür genannt, einen Stamm in Bretter zu schneiden?",
      a:["Blockbandsäge","Bohrmaschine","Drechselbank","Bandschleifer"],
      correct:0,
      hint:"Der Name verbindet den Holzblock mit einer Säge.",
      explain:"Als Beispiel wird die Blockbandsäge genannt."
    },
    {
      topic:"Weg des Holzes", level:"Zusammenhänge",
      q:"Welche Prozesskette beschreibt den Weg des Holzes am besten?",
      a:[
        "Wald → Baumarkt → Baumfällung → Sägewerk → Transport",
        "Baumfällung → Wald → Sägewerk → Baumarkt → Transport",
        "Wald → Baumfällung → Transport → Sägewerk → Baumarkt",
        "Sägewerk → Wald → Transport → Baumfällung → Baumarkt"
      ],
      correct:2,
      hint:"Startet dort, wo der Baum wächst, und endet dort, wo Bretter verkauft werden.",
      explain:"Die Unterrichtsreihe folgt der Kette Wald → Baumfällung → Transport → Sägewerk → Baumarkt."
    },
    {
      topic:"Wald & Sägewerk", level:"Zusammenhänge",
      q:"Welche Aussage verbindet Splintholz und Holztrocknung richtig?",
      a:[
        "Splintholz transportiert Wasser im lebenden Baum; nach dem Sägen muss Feuchtigkeit aus den Brettern heraus.",
        "Splintholz ist bereits trocken und muss deshalb im Sägewerk entfernt werden.",
        "Splintholz schützt außen den Baum; beim Trocknen wird daraus Rinde.",
        "Splintholz gibt nur Stabilität; Feuchtigkeit spielt dabei keine Rolle."
      ],
      correct:0,
      hint:"Vergleicht die Funktion im lebenden Baum mit dem Zustand eines frisch gesägten Brettes.",
      explain:"Im lebenden Baum transportiert Splintholz Wasser. Nach dem Sägen muss das Holz trocknen, damit es stabil verarbeitet werden kann."
    },
    {
      topic:"Baumfällung & Sägewerk", level:"Zusammenhänge",
      q:"Welche Vorbereitung des Stammes unterstützt die spätere Verarbeitung im Sägewerk am sinnvollsten?",
      a:[
        "Äste und Rinde entfernen.",
        "Neue Äste wachsen lassen.",
        "Den Stamm möglichst feucht halten.",
        "Den Stamm schon im Wald lackieren."
      ],
      correct:0,
      hint:"Denkt an Entasten und daran, warum die Rinde entfernt wird.",
      explain:"Entasten und das Entfernen der Rinde bereiten den Stamm auf Transport, Trocknung und weitere Verarbeitung vor."
    },
    {
      topic:"Baumarkt", level:"Transfer",
      q:"Ein Brett im Baumarkt ist gerade, trocken und ohne sichtbare Schäden. Welche Schritte aus der Prozesskette tragen dazu besonders bei?",
      a:[
        "Schneller Transport, Sägen und sorgfältiges Trocknen",
        "Nur die Baumfällung",
        "Nur das Entfernen der Äste",
        "Ausschließlich die Lagerung im Wald"
      ],
      correct:0,
      hint:"Gesucht sind mehrere Schritte, die Schäden vermeiden und die Formstabilität sichern.",
      explain:"Ein geeigneter Transport schützt den Stamm; Sägen erzeugt Bretter; Trocknen macht sie stabil und vermindert Verziehen."
    },
    {
      topic:"Baumarkt", level:"Transfer",
      q:"Warum ist die Qualitätsprüfung vor dem Verkauf ein sinnvoller letzter Schritt?",
      a:[
        "Damit geprüft wird, ob das Holz für die Nutzung geeignet ist.",
        "Damit aus Brettern wieder Baumstämme werden.",
        "Damit das Holz wieder feuchter wird.",
        "Damit die Rinde erneut anwächst."
      ],
      correct:0,
      hint:"Überlegt, was Käuferinnen und Käufer von einem Werkstoff erwarten.",
      explain:"Vor dem Verkauf wird die Qualität geprüft, damit geeignetes Holz angeboten wird."
    },
    {
      topic:"Gesamter Prozess", level:"Profi",
      q:"Welche Begründung beschreibt den gesamten Weg vom Baum zum nutzbaren Brett am vollständigsten?",
      a:[
        "Der Baum wird gefällt, vorbereitet und transportiert; im Sägewerk wird der Stamm gesägt und getrocknet; anschließend werden die Bretter geprüft und verkauft.",
        "Der Baum wird gefällt und direkt als fertiges Brett verkauft.",
        "Der Stamm wird zuerst getrocknet, danach wächst eine neue Rinde und erst dann wird er gesägt.",
        "Der Baum wird im Baumarkt gefällt und anschließend in den Wald transportiert."
      ],
      correct:0,
      hint:"Achtet darauf, ob Vorbereitung, Transport, Sägen, Trocknen und Verkauf in sinnvoller Reihenfolge vorkommen.",
      explain:"Die vollständige Prozesskette umfasst Fällen und Vorbereiten, Transport, Sägen, Trocknen sowie Prüfung und Verkauf."
    }
  ];

  const letters=["A","B","C","D"];
  const els={
    startView:document.getElementById("startView"),
    quizView:document.getElementById("quizView"),
    groupNameInput:document.getElementById("groupNameInput"),
    startButton:document.getElementById("startButton"),
    groupChip:document.getElementById("groupChip"),
    levelLabel:document.getElementById("levelLabel"),
    difficultyLabel:document.getElementById("difficultyLabel"),
    progressFill:document.getElementById("progressFill"),
    ladderList:document.getElementById("ladderList"),
    fiftyButton:document.getElementById("fiftyButton"),
    hintButton:document.getElementById("hintButton"),
    topicBadge:document.getElementById("topicBadge"),
    questionNumber:document.getElementById("questionNumber"),
    questionText:document.getElementById("questionText"),
    answers:document.getElementById("answers"),
    selectionStatus:document.getElementById("selectionStatus"),
    selectionHint:document.getElementById("selectionHint"),
    lockButton:document.getElementById("lockButton"),
    hintPanel:document.getElementById("hintPanel"),
    consensusModal:document.getElementById("consensusModal"),
    consensusAnswer:document.getElementById("consensusAnswer"),
    backToDiscussButton:document.getElementById("backToDiscussButton"),
    confirmAnswerButton:document.getElementById("confirmAnswerButton"),
    resultModal:document.getElementById("resultModal"),
    resultMark:document.getElementById("resultMark"),
    resultEyebrow:document.getElementById("resultEyebrow"),
    resultTitle:document.getElementById("resultTitle"),
    resultExplanation:document.getElementById("resultExplanation"),
    nextButton:document.getElementById("nextButton"),
    endModal:document.getElementById("endModal"),
    scoreText:document.getElementById("scoreText"),
    endMessage:document.getElementById("endMessage"),
    restartButton:document.getElementById("restartButton")
  };

  let index=0, selected=null, score=0, fiftyUsed=false, hintUsed=false, locked=false;

  function initLadder(){
    els.ladderList.innerHTML="";
    QUESTIONS.forEach((q,i)=>{
      const li=document.createElement("li");
      if([4,9,14].includes(i)) li.classList.add("check");
      li.dataset.i=String(i);
      li.innerHTML=`<span>${i+1}</span><span>${i<5?"Basis":i<10?"Fortgeschritten":"Profi"}</span>`;
      els.ladderList.appendChild(li);
    });
  }

  function render(){
    const q=QUESTIONS[index];
    selected=null; locked=false;
    els.topicBadge.textContent=q.topic;
    els.questionNumber.textContent=`Frage ${index+1}`;
    els.questionText.textContent=q.q;
    els.levelLabel.textContent=`Stufe ${index+1} von ${QUESTIONS.length}`;
    els.difficultyLabel.textContent=q.level;
    els.progressFill.style.width=`${(index/QUESTIONS.length)*100}%`;
    els.hintPanel.hidden=true;
    els.hintPanel.textContent="";
    els.selectionStatus.textContent="Wählt gemeinsam eine Antwort.";
    els.selectionHint.textContent="Antippen markiert nur eure Auswahl – noch wird nichts eingeloggt.";
    els.lockButton.disabled=true;
    els.answers.innerHTML="";

    q.a.forEach((text,i)=>{
      const b=document.createElement("button");
      b.type="button";
      b.className="answer";
      b.dataset.i=String(i);
      b.innerHTML=`<span class="letter">${letters[i]}</span><span>${text}</span>`;
      b.addEventListener("click",()=>selectAnswer(i));
      els.answers.appendChild(b);
    });

    els.fiftyButton.disabled=fiftyUsed;
    els.hintButton.disabled=hintUsed;
    updateLadder();
  }

  function updateLadder(){
    els.ladderList.querySelectorAll("li").forEach((li,i)=>{
      li.classList.toggle("current",i===index);
      li.classList.toggle("passed",i<index);
    });
  }

  function selectAnswer(i){
    if(locked) return;
    selected=i;
    [...els.answers.children].forEach((b,j)=>b.classList.toggle("selected",j===i));
    els.selectionStatus.textContent=`Ausgewählt: ${letters[i]}`;
    els.selectionHint.textContent="Beratet euch weiter. Erst „Antwort einloggen“ macht die Auswahl verbindlich.";
    els.lockButton.disabled=false;
  }

  function openConsensus(){
    if(selected===null||locked) return;
    const q=QUESTIONS[index];
    els.consensusAnswer.textContent=`${letters[selected]}: ${q.a[selected]}`;
    els.consensusModal.hidden=false;
    els.confirmAnswerButton.focus();
  }

  function confirm(){
    if(selected===null) return;
    els.consensusModal.hidden=true;
    locked=true;
    const q=QUESTIONS[index];
    const correct=selected===q.correct;
    if(correct) score++;

    [...els.answers.children].forEach((b,i)=>{
      b.disabled=true;
      if(i===q.correct) b.classList.add("reveal-correct");
      if(i===selected && !correct) b.classList.add("reveal-wrong");
    });

    els.resultMark.textContent=correct?"✓":"×";
    els.resultMark.className=`result-mark ${correct?"correct":"wrong"}`;
    els.resultEyebrow.textContent=correct?"Richtig":"Nicht richtig";
    els.resultTitle.textContent=correct?"Euer Konsens war richtig!":"Gute Beratung – diesmal lag die Gruppe daneben.";
    els.resultExplanation.textContent=q.explain;
    els.nextButton.textContent=index===QUESTIONS.length-1?"Ergebnis ansehen":"Nächste Frage";
    els.resultModal.hidden=false;
  }

  function next(){
    els.resultModal.hidden=true;
    if(index>=QUESTIONS.length-1){finish();return}
    index++;
    render();
  }

  function finish(){
    els.progressFill.style.width="100%";
    els.scoreText.textContent=`${score} / ${QUESTIONS.length}`;
    let msg="";
    if(score===15) msg="Volltreffer: Ihr habt die gesamte Prozesskette sicher im Blick.";
    else if(score>=12) msg="Sehr stark: Ihr könnt die meisten Zusammenhänge vom Wald bis zum Baumarkt erklären.";
    else if(score>=9) msg="Solide Leistung: Vieles sitzt schon. Schaut euch besonders die schwierigeren Zusammenhänge noch einmal an.";
    else msg="Gute Grundlage: Nutzt die Infokarten noch einmal und startet danach eine neue Runde.";
    els.endMessage.textContent=msg;
    els.endModal.hidden=false;
  }

  function useFifty(){
    if(fiftyUsed||locked) return;
    fiftyUsed=true;
    els.fiftyButton.disabled=true;
    const q=QUESTIONS[index];
    const wrong=[0,1,2,3].filter(i=>i!==q.correct);
    const keepWrong=wrong[Math.floor(Math.random()*wrong.length)];
    [...els.answers.children].forEach((b,i)=>{
      if(i!==q.correct && i!==keepWrong) b.classList.add("removed");
    });
    if(selected!==null && els.answers.children[selected].classList.contains("removed")){
      selected=null; els.lockButton.disabled=true;
      els.selectionStatus.textContent="Zwei Antworten sind weg. Wählt neu.";
    }
  }

  function useHint(){
    if(hintUsed||locked) return;
    hintUsed=true;
    els.hintButton.disabled=true;
    els.hintPanel.textContent=`Hinweis: ${QUESTIONS[index].hint}`;
    els.hintPanel.hidden=false;
  }

  function start(){
    const name=els.groupNameInput.value.trim()||"Lerngruppe";
    els.groupChip.textContent=name;
    index=0; selected=null; score=0; fiftyUsed=false; hintUsed=false; locked=false;
    els.startView.hidden=true; els.quizView.hidden=false;
    initLadder(); render();
  }

  function restart(){
    els.endModal.hidden=true;
    els.quizView.hidden=true;
    els.startView.hidden=false;
    els.startButton.focus();
  }

  els.startButton.addEventListener("click",start);
  els.lockButton.addEventListener("click",openConsensus);
  els.backToDiscussButton.addEventListener("click",()=>{els.consensusModal.hidden=true;els.lockButton.focus()});
  els.confirmAnswerButton.addEventListener("click",confirm);
  els.nextButton.addEventListener("click",next);
  els.fiftyButton.addEventListener("click",useFifty);
  els.hintButton.addEventListener("click",useHint);
  els.restartButton.addEventListener("click",restart);
})();