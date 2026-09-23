(() => {
  "use strict";

  const ZONES = [
    { number: 1, name: "Wald", card: "Der Wald", icon: "🌲" },
    { number: 2, name: "Baumfällung", card: "Baumfällung", icon: "🪵" },
    { number: 3, name: "Transport", card: "Transport", icon: "🚛" },
    { number: 4, name: "Sägewerk", card: "Im Sägewerk", icon: "⚙️" },
    { number: 5, name: "Baumarkt", card: "Der Baumarkt", icon: "🪚" }
  ];

  const PLAYER_COLORS = ["#2469a0", "#c9423a", "#278354", "#7456a7", "#d57a24"];
  const DICE_GLYPHS = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"];
  const FIELDS_PER_ZONE = 8;

  const TASKS = {
    malen: {
      name: "Malaufgabe",
      symbol: "✎",
      instruction: "Zieh eine rote Karte.",
      colorName: "rot"
    },
    quiz: {
      name: "Quizfrage",
      symbol: "?",
      instruction: "Zieh eine gelbe Karte.",
      colorName: "gelb"
    },
    pantomime: {
      name: "Pantomime",
      symbol: "◯",
      instruction: "Zieh eine blaue Karte.",
      colorName: "blau"
    }
  };

  const yPatterns = [
    [78, 65, 50, 35, 23, 34, 50, 66],
    [72, 57, 42, 28, 20, 32, 49, 66],
    [73, 59, 44, 31, 24, 36, 52, 68],
    [74, 59, 44, 29, 21, 33, 49, 65],
    [72, 57, 42, 29, 22, 35, 51, 67]
  ];

  const fields = [];
  const localX = [2.1, 4.35, 6.65, 8.95, 11.25, 13.55, 15.85, 18.15];

  for (let zone = 0; zone < 5; zone += 1) {
    const zoneStart = zone * 20;
    for (let local = 0; local < FIELDS_PER_ZONE; local += 1) {
      fields.push({
        index: fields.length,
        zone,
        x: zoneStart + localX[local],
        y: yPatterns[zone][local]
      });
    }
  }

  const els = {
    setupView: document.getElementById("setupView"),
    gameView: document.getElementById("gameView"),
    restartButton: document.getElementById("restartButton"),
    countButtons: document.getElementById("countButtons"),
    playerInputs: document.getElementById("playerInputs"),
    startButton: document.getElementById("startButton"),
    board: document.getElementById("board"),
    fieldsLayer: document.getElementById("fields"),
    tokensLayer: document.getElementById("tokens"),
    trackSvg: document.getElementById("trackSvg"),
    trackLine: document.getElementById("trackLine"),
    playerStrip: document.getElementById("playerStrip"),
    turnToken: document.getElementById("turnToken"),
    currentPlayerName: document.getElementById("currentPlayerName"),
    turnLocation: document.getElementById("turnLocation"),
    rollButton: document.getElementById("rollButton"),
    rollLabel: document.getElementById("rollLabel"),
    diceFace: document.getElementById("diceFace"),
    taskPlaceholder: document.getElementById("taskPlaceholder"),
    taskCard: document.getElementById("taskCard"),
    taskSymbol: document.getElementById("taskSymbol"),
    rolledNumber: document.getElementById("rolledNumber"),
    taskName: document.getElementById("taskName"),
    taskInstruction: document.getElementById("taskInstruction"),
    successButton: document.getElementById("successButton"),
    failButton: document.getElementById("failButton"),
    gameHint: document.getElementById("gameHint"),
    eventOverlay: document.getElementById("eventOverlay"),
    eventIcon: document.getElementById("eventIcon"),
    eventKicker: document.getElementById("eventKicker"),
    eventTitle: document.getElementById("eventTitle"),
    eventText: document.getElementById("eventText"),
    eventButton: document.getElementById("eventButton")
  };

  if (!els.board || !els.trackSvg || !els.trackLine) return;

  let selectedPlayerCount = 2;
  let players = [];
  let currentPlayerIndex = 0;
  let phase = "setup";
  let visitedZones = new Set();
  let pendingZoneIntros = [];
  let pendingCompletion = null;
  let eventAction = null;
  let diceTimer = null;

  buildTrack();
  wireSetup();
  wireGame();

  function buildTrack() {
    const underLine = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
    underLine.setAttribute("id", "trackLineUnder");
    els.trackSvg.insertBefore(underLine, els.trackLine);

    const points = fields.map((field) => `${field.x},${field.y}`).join(" ");
    underLine.setAttribute("points", points);
    els.trackLine.setAttribute("points", points);

    fields.forEach((field) => {
      const node = document.createElement("span");
      node.className = "field";
      if (field.index % FIELDS_PER_ZONE === 0) node.classList.add("section-start");
      node.style.left = `${field.x}%`;
      node.style.top = `${field.y}%`;
      node.dataset.field = String(field.index + 1);
      els.fieldsLayer.appendChild(node);
    });
  }

  function wireSetup() {
    els.countButtons.addEventListener("click", (event) => {
      const button = event.target.closest("[data-count]");
      if (!button) return;
      selectedPlayerCount = clamp(Number(button.dataset.count), 2, 5);

      els.countButtons.querySelectorAll("[data-count]").forEach((item) => {
        const isSelected = Number(item.dataset.count) === selectedPlayerCount;
        item.classList.toggle("selected", isSelected);
        item.setAttribute("aria-pressed", String(isSelected));
      });

      els.playerInputs.querySelectorAll("[data-player-row]").forEach((row) => {
        row.hidden = Number(row.dataset.playerRow) >= selectedPlayerCount;
      });
    });

    els.startButton.addEventListener("click", startGame);
  }

  function wireGame() {
    els.rollButton.addEventListener("click", rollDice);
    els.successButton.addEventListener("click", () => resolveTask(true));
    els.failButton.addEventListener("click", () => resolveTask(false));
    els.eventButton.addEventListener("click", () => {
      if (typeof eventAction === "function") {
        const action = eventAction;
        eventAction = null;
        action();
      }
    });

    els.restartButton.addEventListener("click", () => {
      if (window.confirm("Die laufende Runde beenden und neu starten?")) {
        resetToSetup();
      }
    });
  }

  function startGame() {
    const rows = [...els.playerInputs.querySelectorAll("[data-player-row]")].slice(0, selectedPlayerCount);

    players = rows.map((row, index) => {
      const input = row.querySelector("input");
      const typed = input.value.trim();
      return {
        id: index,
        name: typed || `Spieler ${index + 1}`,
        color: PLAYER_COLORS[index],
        position: 0
      };
    });

    currentPlayerIndex = 0;
    visitedZones = new Set([0]);
    pendingZoneIntros = [];
    pendingCompletion = null;
    phase = "intro";

    els.setupView.hidden = true;
    els.gameView.hidden = false;
    els.restartButton.hidden = false;

    createTokens();
    renderAll();
    showZoneIntro(0, () => beginTurn());
  }

  function resetToSetup() {
    clearInterval(diceTimer);
    diceTimer = null;
    players = [];
    currentPlayerIndex = 0;
    phase = "setup";
    visitedZones = new Set();
    pendingZoneIntros = [];
    pendingCompletion = null;
    eventAction = null;

    els.tokensLayer.innerHTML = "";
    els.playerStrip.innerHTML = "";
    hideEvent();
    resetTaskPanel();

    els.gameView.hidden = true;
    els.setupView.hidden = false;
    els.restartButton.hidden = true;
  }

  function beginTurn() {
    phase = "awaitRoll";
    resetTaskPanel();
    els.rollButton.disabled = false;
    els.rollLabel.textContent = "Würfeln";
    els.gameHint.textContent = `${players[currentPlayerIndex].name} ist dran.`;
    renderAll();
  }

  function rollDice() {
    if (phase !== "awaitRoll") return;

    phase = "rolling";
    els.rollButton.disabled = true;
    els.rollLabel.textContent = "…";
    els.diceFace.classList.add("rolling");

    let ticks = 0;
    clearInterval(diceTimer);
    diceTimer = window.setInterval(() => {
      const temp = randomDie();
      els.diceFace.textContent = DICE_GLYPHS[temp - 1];
      ticks += 1;

      if (ticks >= 8) {
        clearInterval(diceTimer);
        diceTimer = null;
        const result = randomDie();
        finishRoll(result);
      }
    }, 80);
  }

  function finishRoll(result) {
    els.diceFace.classList.remove("rolling");
    els.diceFace.textContent = DICE_GLYPHS[result - 1];
    els.rollLabel.textContent = String(result);

    const taskKey = taskForRoll(result);
    const task = TASKS[taskKey];

    els.taskPlaceholder.hidden = true;
    els.taskCard.hidden = false;
    els.taskCard.dataset.task = taskKey;
    els.taskSymbol.textContent = task.symbol;
    els.rolledNumber.textContent = String(result);
    els.taskName.textContent = task.name;
    els.taskInstruction.textContent = task.instruction;

    els.gameHint.textContent = `${players[currentPlayerIndex].name}: ${task.instruction} Danach entscheidet ihr gemeinsam, ob die Aufgabe geschafft wurde.`;
    phase = "awaitResult";
  }

  async function resolveTask(success) {
    if (phase !== "awaitResult") return;
    phase = "resolving";
    setResultButtonsDisabled(true);

    const player = players[currentPlayerIndex];

    if (!success) {
      els.gameHint.textContent = `${player.name} bleibt stehen.`;
      await wait(650);
      endTurn();
      return;
    }

    const oldPosition = player.position;
    const intendedTarget = Math.min(oldPosition + 3, fields.length - 1);
    let finalTarget = intendedTarget;

    while (finalTarget < fields.length - 1 && isOccupiedByOther(finalTarget, player.id)) {
      finalTarget += 1;
    }

    const enteredZones = [];
    let lastZone = fields[oldPosition].zone;

    for (let next = oldPosition + 1; next <= finalTarget; next += 1) {
      player.position = next;
      const zone = fields[next].zone;
      if (zone !== lastZone) {
        if (!visitedZones.has(zone) && !enteredZones.includes(zone)) {
          enteredZones.push(zone);
        }
        lastZone = zone;
      }
      renderAll();
      pulseToken(player.id);
      await wait(300);
    }

    if (finalTarget > intendedTarget) {
      els.gameHint.textContent = "Das Zielfeld war besetzt – weiter zum nächsten freien Feld.";
      await wait(550);
    }

    enteredZones.forEach((zone) => visitedZones.add(zone));
    pendingZoneIntros = enteredZones.slice();

    const won = player.position >= fields.length - 1;
    pendingCompletion = { won, playerId: player.id };

    if (pendingZoneIntros.length > 0) {
      showNextPendingZone();
    } else {
      finishResolvedMove();
    }
  }

  function finishResolvedMove() {
    if (!pendingCompletion) return;
    const completion = pendingCompletion;
    pendingCompletion = null;

    if (completion.won) {
      showWinner(completion.playerId);
    } else {
      endTurn();
    }
  }

  function showNextPendingZone() {
    if (pendingZoneIntros.length === 0) {
      finishResolvedMove();
      return;
    }

    const zone = pendingZoneIntros.shift();
    showZoneIntro(zone, showNextPendingZone);
  }

  function endTurn() {
    phase = "switching";
    currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
    renderAll();

    const next = players[currentPlayerIndex];
    els.gameHint.textContent = `Jetzt ist ${next.name} dran.`;

    window.setTimeout(() => {
      beginTurn();
    }, 500);
  }

  function showZoneIntro(zoneIndex, after) {
    const zone = ZONES[zoneIndex];
    phase = "intro";
    els.eventIcon.textContent = zone.icon;
    els.eventKicker.textContent = `Bereich ${zone.number} von 5`;
    els.eventTitle.textContent = zone.card;
    els.eventText.textContent = `Nehmt die Infokarte „${zone.card}“ und lest den Text einmal gemeinsam laut vor.`;
    els.eventButton.textContent = "Gelesen – weiter";
    eventAction = () => {
      hideEvent();
      if (typeof after === "function") after();
    };
    els.eventOverlay.hidden = false;
    els.eventButton.focus();
  }

  function showWinner(playerId) {
    const player = players.find((item) => item.id === playerId);
    phase = "finished";
    els.eventIcon.textContent = "🏁";
    els.eventKicker.textContent = "Am Ziel";
    els.eventTitle.textContent = `${player.name} gewinnt!`;
    els.eventText.textContent = "Ihr habt den Weg vom Baum bis zum Brett gemeinsam durchgespielt.";
    els.eventButton.textContent = "Neue Runde";
    eventAction = () => resetToSetup();
    els.eventOverlay.hidden = false;
    els.eventButton.focus();
    renderAll();
  }

  function hideEvent() {
    els.eventOverlay.hidden = true;
  }

  function resetTaskPanel() {
    els.taskPlaceholder.hidden = false;
    els.taskCard.hidden = true;
    els.taskCard.dataset.task = "";
    els.taskPlaceholder.textContent = "Würfle. Die Zahl bestimmt eure Kartenart.";
    setResultButtonsDisabled(false);
    els.diceFace.textContent = "⚄";
  }

  function setResultButtonsDisabled(disabled) {
    els.successButton.disabled = disabled;
    els.failButton.disabled = disabled;
  }

  function createTokens() {
    els.tokensLayer.innerHTML = "";
    players.forEach((player) => {
      const token = document.createElement("div");
      token.className = "player-token";
      token.id = `token-${player.id}`;
      token.style.setProperty("--token-color", player.color);
      token.setAttribute("aria-label", player.name);
      token.textContent = initials(player.name);
      els.tokensLayer.appendChild(token);
    });
  }

  function renderAll() {
    renderTokens();
    renderPlayerStrip();
    renderTurnPanel();
  }

  function renderTokens() {
    const groups = new Map();
    players.forEach((player) => {
      if (!groups.has(player.position)) groups.set(player.position, []);
      groups.get(player.position).push(player);
    });

    groups.forEach((group, position) => {
      const offsets = tokenOffsets(group.length);
      group.forEach((player, index) => {
        const token = document.getElementById(`token-${player.id}`);
        if (!token) return;
        const field = fields[position];
        token.style.left = `${field.x}%`;
        token.style.top = `${field.y}%`;
        token.style.setProperty("--dx", `${offsets[index][0]}px`);
        token.style.setProperty("--dy", `${offsets[index][1]}px`);
        token.classList.toggle("active", player.id === players[currentPlayerIndex]?.id && phase !== "setup");
      });
    });
  }

  function renderPlayerStrip() {
    els.playerStrip.innerHTML = "";
    players.forEach((player, index) => {
      const chip = document.createElement("div");
      chip.className = "player-chip";
      if (index === currentPlayerIndex && phase !== "finished") chip.classList.add("active");
      chip.style.setProperty("--chip-color", player.color);

      const mini = document.createElement("span");
      mini.className = "mini-token";
      mini.textContent = initials(player.name);

      const textWrap = document.createElement("span");
      textWrap.className = "chip-text";
      textWrap.textContent = player.name;

      const position = document.createElement("span");
      position.className = "chip-position";
      position.textContent = `· ${player.position + 1}`;

      chip.append(mini, textWrap, position);
      els.playerStrip.appendChild(chip);
    });
  }

  function renderTurnPanel() {
    if (players.length === 0) return;
    const player = players[currentPlayerIndex];
    const field = fields[player.position];

    els.turnToken.textContent = initials(player.name);
    els.turnToken.style.background = player.color;
    els.currentPlayerName.textContent = player.name;
    els.turnLocation.textContent = `Bereich ${ZONES[field.zone].number} – ${ZONES[field.zone].name} · Feld ${player.position + 1}`;
  }

  function pulseToken(playerId) {
    const token = document.getElementById(`token-${playerId}`);
    if (!token) return;
    token.classList.add("moving");
    window.setTimeout(() => token.classList.remove("moving"), 170);
  }

  function isOccupiedByOther(position, playerId) {
    return players.some((player) => player.id !== playerId && player.position === position);
  }

  function taskForRoll(value) {
    if (value === 1 || value === 6) return "malen";
    if (value === 2 || value === 5) return "quiz";
    return "pantomime";
  }

  function randomDie() {
    return Math.floor(Math.random() * 6) + 1;
  }

  function initials(name) {
    const parts = name.trim().split(/\s+/).filter(Boolean);
    if (parts.length === 0) return "?";
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }

  function tokenOffsets(count) {
    const patterns = {
      1: [[0, 0]],
      2: [[-8, 0], [8, 0]],
      3: [[-8, 6], [8, 6], [0, -8]],
      4: [[-8, -8], [8, -8], [-8, 8], [8, 8]],
      5: [[-10, -7], [10, -7], [-10, 9], [10, 9], [0, 0]]
    };
    return patterns[count] || patterns[1];
  }

  function wait(ms) {
    return new Promise((resolve) => window.setTimeout(resolve, ms));
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }
})();
