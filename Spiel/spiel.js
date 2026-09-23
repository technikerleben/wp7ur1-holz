(() => {
  "use strict";

  const ZONES = [
    "Wald",
    "Baumfällung",
    "Transport",
    "Sägewerk",
    "Baumarkt"
  ];

  const FIELDS_PER_ZONE = 8;

  // Jedes Element enthält eine Position in Prozent des Spielfeldes.
  // Die x-Koordinaten werden bewusst aus fünf exakt 20 % breiten
  // Abschnitten erzeugt. So bleiben Hintergrund, Bereichserkennung
  // und Spiellogik sauber voneinander getrennt.
  const yPatterns = [
    [78, 65, 50, 35, 23, 34, 50, 66],
    [72, 57, 42, 28, 20, 32, 49, 66],
    [73, 59, 44, 31, 24, 36, 52, 68],
    [74, 59, 44, 29, 21, 33, 49, 65],
    [72, 57, 42, 29, 22, 35, 51, 67]
  ];

  const fields = [];

  for (let zone = 0; zone < 5; zone += 1) {
    const zoneStart = zone * 20;
    const localX = [2.1, 4.35, 6.65, 8.95, 11.25, 13.55, 15.85, 18.15];

    for (let local = 0; local < FIELDS_PER_ZONE; local += 1) {
      fields.push({
        index: fields.length,
        zone,
        x: zoneStart + localX[local],
        y: yPatterns[zone][local]
      });
    }
  }

  const board = document.getElementById("board");
  const fieldsLayer = document.getElementById("fields");
  const trackSvg = document.getElementById("trackSvg");
  const trackLine = document.getElementById("trackLine");
  const token = document.getElementById("testToken");
  const nextButton = document.getElementById("nextButton");
  const resetButton = document.getElementById("resetButton");
  const fieldInfo = document.getElementById("fieldInfo");
  const zoneInfo = document.getElementById("zoneInfo");
  const statusText = document.getElementById("statusText");

  if (!board || !fieldsLayer || !trackSvg || !trackLine || !token) return;

  // Zweite Linie als helle Wegfläche unter der dunklen Kontur.
  const underLine = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
  underLine.setAttribute("id", "trackLineUnder");
  trackSvg.insertBefore(underLine, trackLine);

  const points = fields.map((field) => `${field.x},${field.y}`).join(" ");
  underLine.setAttribute("points", points);
  trackLine.setAttribute("points", points);

  fields.forEach((field) => {
    const el = document.createElement("span");
    el.className = "field";
    if (field.index % FIELDS_PER_ZONE === 0) el.classList.add("section-start");
    el.style.left = `${field.x}%`;
    el.style.top = `${field.y}%`;
    el.dataset.field = String(field.index + 1);
    fieldsLayer.appendChild(el);
  });

  let position = 0;

  function renderPosition(animate = false) {
    const field = fields[position];

    token.style.left = `${field.x}%`;
    token.style.top = `${field.y}%`;

    if (animate) {
      token.classList.add("moving");
      window.setTimeout(() => token.classList.remove("moving"), 180);
    }

    fieldInfo.textContent = `Feld ${position + 1} von ${fields.length}`;
    zoneInfo.textContent = ZONES[field.zone];
    statusText.textContent = `Bereich: ${ZONES[field.zone]}`;

    nextButton.disabled = position >= fields.length - 1;
  }

  nextButton.addEventListener("click", () => {
    if (position < fields.length - 1) {
      position += 1;
      renderPosition(true);
    }
  });

  resetButton.addEventListener("click", () => {
    position = 0;
    renderPosition(false);
  });

  renderPosition(false);
})();
