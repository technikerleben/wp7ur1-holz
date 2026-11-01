window.HOLZ_VORBEREITUNG = [
  {
    "title": "Vom Baum zum Brett",
    "scope": "A1 und A2",
    "questions": [
      {
        "type": "choice",
        "prompt": "Welche Aufgaben passen zum Stamm?",
        "options": [
          "Die Borke schützt den Stamm.",
          "Das Kambium ermöglicht Dickenwachstum.",
          "Das Mark nimmt Wasser aus dem Boden auf."
        ],
        "correct": [
          0,
          1
        ],
        "explanation": "Die Borke schützt außen. Das Kambium bildet neue Zellen. Wasser aus dem Boden nehmen die Wurzeln auf.",
        "sheet": "A1.1",
        "multi": true
      },
      {
        "type": "fill",
        "prompt": "Ergänze die Fachbegriffe.",
        "fields": [
          {
            "label": "Transportiert Zucker aus den Blättern:",
            "answers": [
              "Bast"
            ]
          },
          {
            "label": "Leitet im Stamm Wasser zu den Blättern:",
            "answers": [
              "Splintholz"
            ]
          }
        ],
        "explanation": "Bast transportiert Zucker. Im Splintholz wird Wasser nach oben geleitet.",
        "sheet": "A1.1"
      },
      {
        "type": "choice",
        "prompt": "Ein Modell zeigt 14 vollständige Jahresringe. Einer davon ist besonders schmal. Welche Aussage passt?",
        "options": [
          "Der Baum war an dieser Schnittstelle ungefähr 14 Jahre alt; der schmale Ring zeigt wenig Dickenzuwachs.",
          "Der Baum war 28 Jahre alt.",
          "Der schmale Ring beweist eindeutig einen kalten Winter."
        ],
        "correct": [
          0
        ],
        "explanation": "Ein vollständiger Jahresring steht für ein Jahr. Ein schmaler Ring zeigt wenig Dickenzuwachs; die genaue Ursache lässt sich daraus allein nicht ablesen.",
        "sheet": "A2.1 / A2.2",
        "multi": false
      }
    ],
    "retries": [
      {
        "type": "choice",
        "prompt": "Welche Aussage über das Kambium stimmt?",
        "options": [
          "Es liegt in der Stammmitte und zählt die Jahre.",
          "Es bildet neue Zellen für das Dickenwachstum.",
          "Es ist die äußere Schutzschicht."
        ],
        "correct": [
          1
        ],
        "explanation": "Das Kambium ist die Wachstumsschicht. Die äußere Schutzschicht heißt Borke.",
        "sheet": "A1.1",
        "multi": false
      },
      {
        "type": "fill",
        "prompt": "Ergänze nur das fehlende Wort.",
        "fields": [
          {
            "label": "Zucker wird im Stamm durch den … transportiert.",
            "answers": [
              "Bast"
            ]
          }
        ],
        "explanation": "Der Bast transportiert Zucker aus den Blättern zu anderen Teilen des Baums.",
        "sheet": "A1.1"
      },
      {
        "type": "choice",
        "prompt": "Ein Ring ist breiter als der vorherige. Was kannst du daraus ableiten?",
        "options": [
          "Der Stamm hat in diesem Jahr stärker in die Dicke zugelegt.",
          "Die Ursache war sicher mehr Licht.",
          "Der Baum hat in diesem Jahr sein Alter verdoppelt."
        ],
        "correct": [
          0
        ],
        "explanation": "Die Ringbreite zeigt den Dickenzuwachs. Für eine sichere Erklärung der Ursache brauchst du weitere Informationen.",
        "sheet": "A2.2",
        "multi": false
      }
    ]
  },
  {
    "title": "Produktionsweg und Schnittplan",
    "scope": "A3 und A4",
    "questions": [
      {
        "type": "order",
        "prompt": "Nummeriere den Weg vom Baum zum Brett mit 1 bis 6. Nutze jede Zahl einmal.",
        "fields": [
          {
            "label": "Transport",
            "answers": [
              "3"
            ]
          },
          {
            "label": "Schnittholz",
            "answers": [
              "6"
            ]
          },
          {
            "label": "Fällen",
            "answers": [
              "2"
            ]
          },
          {
            "label": "Einschnitt",
            "answers": [
              "5"
            ]
          },
          {
            "label": "Baum",
            "answers": [
              "1"
            ]
          },
          {
            "label": "Sägewerk",
            "answers": [
              "4"
            ]
          }
        ],
        "explanation": "Die Reihenfolge lautet: Baum → Fällen → Transport → Sägewerk → Einschnitt → Schnittholz.",
        "sheet": "A3.1"
      },
      {
        "type": "choice",
        "prompt": "Du brauchst mindestens 14 cm breite Bretter. Plan P liefert 16 cm breite Bretter bei 59 % Ausbeute. Plan Q liefert 10 cm breite Bretter bei 73 % Ausbeute. Zusammenleimen ist nicht erlaubt. Welcher Plan passt?",
        "options": [
          "Plan Q wegen der höheren Ausbeute.",
          "Beide Pläne.",
          "Plan P wegen der passenden Brettbreite."
        ],
        "correct": [
          2
        ],
        "explanation": "Die Mindestbreite muss erfüllt sein. Die höhere Ausbeute von Q hilft hier nicht, weil seine Bretter zu schmal sind.",
        "sheet": "A4.1 / A4.2",
        "multi": false
      },
      {
        "type": "choice",
        "prompt": "Welche Aussagen zum Schnittplan stimmen?",
        "options": [
          "Jeder Sägeschnitt erzeugt Späne.",
          "Mehr Bretter bedeuten immer mehr Ausbeute.",
          "Die gewünschten Brettmaße gehören zur Entscheidung."
        ],
        "correct": [
          0,
          2
        ],
        "explanation": "Die Schnittbreite kostet Material. Bretterzahl und nutzbarer Holzanteil sind unterschiedliche Größen. Ein Plan muss auch die geforderten Maße liefern.",
        "sheet": "A4.2",
        "multi": true
      }
    ],
    "retries": [
      {
        "type": "order",
        "prompt": "Ordne noch einmal. Trage nur Zahlen ein.",
        "fields": [
          {
            "label": "Baum",
            "answers": [
              "1"
            ]
          },
          {
            "label": "Transport",
            "answers": [
              "3"
            ]
          },
          {
            "label": "Fällen",
            "answers": [
              "2"
            ]
          },
          {
            "label": "Schnittholz",
            "answers": [
              "6"
            ]
          },
          {
            "label": "Sägewerk",
            "answers": [
              "4"
            ]
          },
          {
            "label": "Einschnitt",
            "answers": [
              "5"
            ]
          }
        ],
        "explanation": "Vor dem Transport wird gefällt. Im Sägewerk entstehen beim Einschnitt die Bretter.",
        "sheet": "A3.1"
      },
      {
        "type": "choice",
        "prompt": "Gefordert sind 20 cm Brettbreite. Plan L liefert 21 cm, Plan M nur 18 cm. Du darfst nichts zusammenleimen. Welcher Plan erfüllt die Breite?",
        "options": [
          "Plan L.",
          "Plan M.",
          "Keiner."
        ],
        "correct": [
          0
        ],
        "explanation": "21 cm erfüllen die Mindestbreite von 20 cm. 18 cm reichen nicht.",
        "sheet": "A4.2",
        "multi": false
      },
      {
        "type": "fill",
        "prompt": "Ergänze das Wort.",
        "fields": [
          {
            "label": "Durch die Schnittbreite des Sägeblatts entstehen …",
            "answers": [
              "Späne",
              "Sägespäne",
              "Sägemehl"
            ]
          }
        ],
        "explanation": "Material in der Schnittfuge wird zu Spänen und bleibt nicht als Brett erhalten.",
        "sheet": "A4.2"
      }
    ]
  },
  {
    "title": "Das Prüflabor",
    "scope": "A5 und A6",
    "questions": [
      {
        "type": "choice",
        "prompt": "Gleich große, ähnlich trockene Proben werden mit derselben Münze bei gleichem Druck geprüft: K wiegt 80 g und zeigt eine tiefe Spur. L wiegt 70 g und zeigt eine flache Spur. Welche Probe ist in diesem Test härter?",
        "options": [
          "K, weil sie schwerer ist.",
          "L, weil die Spur flacher ist.",
          "Beide sind gleich hart."
        ],
        "correct": [
          1
        ],
        "explanation": "Die flachere Spur bei gleichem Druck spricht für höhere Härte. Die Masse allein entscheidet das nicht.",
        "sheet": "A5.1",
        "multi": false
      },
      {
        "type": "choice",
        "prompt": "Welche Bedingungen helfen beim fairen Vergleich der Masse?",
        "options": [
          "Vergleichbares Volumen.",
          "Ähnlicher Wassergehalt.",
          "Eine Probe vor dem Wiegen wässern und die andere trocken lassen."
        ],
        "correct": [
          0,
          1
        ],
        "explanation": "Größe und Wassergehalt beeinflussen die Masse. Für diesen Vergleich sollen beide Bedingungen möglichst gleich sein.",
        "sheet": "A5.1",
        "multi": true
      },
      {
        "type": "fill",
        "prompt": "Verbinde Beobachtung, Eigenschaft und Verwendung.",
        "fields": [
          {
            "label": "Bei gleichem Druck kaum eine Spur: Das Holz ist im Vergleich eher …",
            "answers": [
              "hart",
              "härter"
            ]
          },
          {
            "label": "Das ist günstig für eine oft belastete …",
            "answers": [
              "Oberfläche",
              "Tischoberfläche",
              "Arbeitsfläche"
            ]
          }
        ],
        "explanation": "Die kleine Druckspur ist die Beobachtung. Hohe Härte ist die abgeleitete Eigenschaft. Sie ist zum Beispiel für eine belastete Oberfläche günstig.",
        "sheet": "A6.1"
      }
    ],
    "retries": [
      {
        "type": "choice",
        "prompt": "Bei gleichem Münzdruck hat M eine deutliche und N kaum eine Spur. Welche Probe ist eher weich?",
        "options": [
          "M.",
          "N.",
          "Die mit der größeren Masse, unabhängig von der Spur."
        ],
        "correct": [
          0
        ],
        "explanation": "Die deutlichere Spur spricht in diesem Vergleich für weicheres Holz.",
        "sheet": "A5.1",
        "multi": false
      },
      {
        "type": "choice",
        "prompt": "Eine Probe ist doppelt so groß wie die andere. Was folgt aus ihrer größeren Masse?",
        "options": [
          "Sie ist sicher härter.",
          "Sie muss aus einer anderen Holzart bestehen.",
          "Die größere Masse kann am größeren Volumen liegen."
        ],
        "correct": [
          2
        ],
        "explanation": "Mehr Volumen kann mehr Masse bedeuten. Daraus allein folgt keine höhere Härte.",
        "sheet": "A5.1",
        "multi": false
      },
      {
        "type": "choice",
        "prompt": "Welche Aussage verbindet Beobachtung und Eigenschaft sinnvoll?",
        "options": [
          "Das Holz ist braun, also ist es sicher am härtesten.",
          "Die Spur ist bei gleichem Druck flach, also ist die Probe im Vergleich eher hart.",
          "Die Probe ist lang, also nimmt sie kein Wasser auf."
        ],
        "correct": [
          1
        ],
        "explanation": "Eine Eigenschaft muss zur beobachteten Prüfung passen. Farbe allein belegt keine Härte.",
        "sheet": "A6.1",
        "multi": false
      }
    ]
  },
  {
    "title": "Holz und Wasser · Holzfehler",
    "scope": "A7 und A8",
    "questions": [
      {
        "type": "fill",
        "prompt": "Dieselbe Probe wiegt vor dem Trocknen 110 g und danach 94 g. Ihre Breite sinkt von 51 auf 50 mm. Ergänze.",
        "fields": [
          {
            "label": "Beim Trocknen gibt sie … ab.",
            "answers": [
              "Wasser",
              "Feuchtigkeit"
            ]
          },
          {
            "label": "Das Kleinerwerden heißt …",
            "answers": [
              "Schwinden"
            ]
          }
        ],
        "explanation": "Wasserabgabe erklärt die kleinere Masse. Die kleinere Breite zeigt Schwinden.",
        "sheet": "A7.1 / A7.2"
      },
      {
        "type": "choice",
        "prompt": "Eine Holztür nimmt bei feuchter Luft Wasser auf und wird breiter. Wie heißt das?",
        "options": [
          "Schwinden.",
          "Quellen.",
          "Einschnitt."
        ],
        "correct": [
          1
        ],
        "explanation": "Wasseraufnahme in die Zellwände kann Holz größer werden lassen. Das heißt Quellen.",
        "sheet": "A7.2",
        "multi": false
      },
      {
        "type": "order",
        "prompt": "Ordne zu: 1 = Ast, 2 = Riss, 3 = Verwerfen. Trage nur die Zahlen ein.",
        "fields": [
          {
            "label": "Das Brett ist verdreht und liegt nicht eben.",
            "answers": [
              "3"
            ]
          },
          {
            "label": "Eine dunkle Stelle zeigt einen früheren Zweigansatz.",
            "answers": [
              "1"
            ]
          },
          {
            "label": "Ein offener Spalt verläuft entlang der Fasern.",
            "answers": [
              "2"
            ]
          }
        ],
        "explanation": "Eine Formänderung heißt Verwerfen. Ein früherer Zweigansatz ist ein Ast. Der offene Spalt ist ein Riss.",
        "sheet": "A8.1"
      }
    ],
    "retries": [
      {
        "type": "fill",
        "prompt": "Ergänze das passende Wort.",
        "fields": [
          {
            "label": "Beim Trocknen wird ein Brett schmaler. Es …",
            "answers": [
              "schwindet"
            ]
          }
        ],
        "explanation": "Schwinden bedeutet: Die Maße werden durch Wasserabgabe aus den Zellwänden kleiner.",
        "sheet": "A7.2"
      },
      {
        "type": "fill",
        "prompt": "Ergänze das passende Wort.",
        "fields": [
          {
            "label": "Holz nimmt Wasser in die Zellwände auf und wird größer. Es …",
            "answers": [
              "quillt"
            ]
          }
        ],
        "explanation": "Quellen bezeichnet die Vergrößerung bei Wasseraufnahme in die Zellwände.",
        "sheet": "A7.2"
      },
      {
        "type": "choice",
        "prompt": "Genau an der geplanten Schraubstelle ist ein Riss. Welche Entscheidung passt?",
        "options": [
          "Den Riss ignorieren.",
          "Die Schraubstelle verlegen oder ein anderes geeignetes Brett nehmen.",
          "Das Brett anmalen; dann ist der Riss behoben."
        ],
        "correct": [
          1
        ],
        "explanation": "Ein Riss an der Schraubstelle kann die Verbindung schwächen. Entscheidend sind seine Lage und die geplante Nutzung.",
        "sheet": "A8.2",
        "multi": false
      }
    ]
  }
];
