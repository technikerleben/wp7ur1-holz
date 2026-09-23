from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from pypdf import PdfReader, PdfWriter

OUT = Path(__file__).resolve().parent

AREAS = [
    {
        "number": 1,
        "name": "Wald",
        "info_title": "Der Wald",
        "info": (
            "Ein Wald ist ein großer Ort mit vielen Bäumen. Bäume haben Blätter oder "
            "Nadeln und bestehen aus verschiedenen Teilen. Die Rinde ist außen und "
            "schützt den Baum. Unter der Rinde ist das Splintholz, das Wasser von den "
            "Wurzeln bis zu den Blättern bringt. Ganz innen ist das Kernholz. Das Kernholz "
            "ist hart und gibt dem Baum Stabilität. Bäume sind sehr wichtig. Sie machen "
            "Sauerstoff, den wir zum Atmen brauchen. Außerdem bieten sie vielen Tieren "
            "ein Zuhause. Der Wald schützt den Boden und hält ihn feucht. Wir müssen auf "
            "den Wald gut aufpassen, damit er gesund bleibt."
        ),
        "malen": [
            "Male einen Baum mit Rinde, Splintholz und Kernholz.",
            "Zeichne ein Eichhörnchen, das auf einem Baum sitzt.",
            "Male einen Wald mit vielen Bäumen und Tieren.",
            "Zeichne die Blätter eines Laubbaumes.",
            "Male einen Baum im Herbst, bei dem die Blätter herunterfallen.",
        ],
        "quiz": [
            ("Was macht die Rinde eines Baumes?", "Sie schützt den Baum."),
            ("Was transportiert das Splintholz im Baum?", "Wasser und Nährstoffe."),
            ("Warum ist Kernholz wichtig für den Baum?", "Es macht den Baum stabil."),
            ("Was brauchen Bäume, um zu wachsen?", "Wasser, Sonne und Nährstoffe."),
            ("Warum sind Wälder wichtig für die Umwelt?", "Sie machen Sauerstoff und bieten Tieren ein Zuhause."),
        ],
        "pantomime": [
            "Stelle pantomimisch dar, wie ein Baum im Wind schwankt.",
            "Imitiere das langsame Wachsen eines Baumes.",
            "Zeige pantomimisch, wie ein Eichhörnchen auf einem Baum herumklettert.",
            "Stelle dar, wie ein Vogel auf einem Ast landet.",
            "Zeige pantomimisch, wie Blätter vom Baum im Herbst zu Boden fallen.",
        ],
    },
    {
        "number": 2,
        "name": "Baumfällung",
        "info_title": "Baumfällung",
        "info": (
            "Wenn ein Baum groß genug ist, kann er gefällt werden. Früher wurden Bäume "
            "mit einer Axt gefällt. Heute benutzt man meistens eine Motorsäge. Nach dem "
            "Fällen liegt der Baum auf dem Boden. Dann werden die Äste entfernt. Dieser "
            "Vorgang heißt Entasten. Danach wird die Rinde abgeschält. Das ist wichtig, "
            "damit das Holz gut trocknen kann. Sobald der Baum vorbereitet ist, kann er "
            "zum Sägewerk gebracht werden. Es ist wichtig, dass der Baumstamm sauber ist, "
            "bevor er verarbeitet wird. Die Maschinen im Sägewerk schneiden den Baum später "
            "in Bretter."
        ),
        "malen": [
            "Zeichne eine Motorsäge, die einen Baum durchschneidet.",
            "Male einen Baum, der gerade gefällt wird.",
            "Zeichne einen gefällten Baum, der entastet wird.",
            "Male die Rinde, die von einem Baum entfernt wird.",
            "Zeichne den Baumstamm ohne Äste und Rinde.",
        ],
        "quiz": [
            ("Mit welchem Werkzeug wurden Bäume früher gefällt?", "Mit einer Axt."),
            ("Welches Werkzeug wird heute meistens zum Fällen eines Baumes benutzt?", "Motorsäge."),
            ("Was wird nach dem Fällen des Baumes entfernt?", "Die Äste."),
            ("Warum wird die Rinde vom Baumstamm abgeschält?", "Damit das Holz gut trocknen kann."),
            ("Wie nennt man das Entfernen der Äste nach dem Fällen?", "Entasten."),
        ],
        "pantomime": [
            "Stelle pantomimisch dar, wie du einen Baum mit einer Motorsäge fällst.",
            "Zeige pantomimisch, wie du die Äste von einem gefällten Baum entfernst.",
            "Imitiere das Abschälen der Rinde von einem Baumstamm.",
            "Stelle pantomimisch dar, wie ein Baum langsam umfällt.",
            "Imitiere das Geräusch einer Motorsäge beim Fällen eines Baumes.",
        ],
    },
    {
        "number": 3,
        "name": "Transport",
        "info_title": "Transport",
        "info": (
            "Nachdem der Baum gefällt wurde, muss der Baumstamm ins Sägewerk gebracht werden. "
            "Früher haben Menschen und Tiere die Baumstämme transportiert. Heute benutzt man "
            "große Maschinen und LKWs dafür. Diese Maschinen können sehr schwere Baumstämme "
            "bewegen. Der Transport muss schnell passieren, damit das Holz nicht beschädigt wird. "
            "Im Sägewerk wird der Baumstamm dann weiterverarbeitet. Der Stamm wird dort in Bretter "
            "geschnitten, die dann getrocknet werden. Ein sauberer und schneller Transport ist "
            "wichtig, damit das Holz gut verarbeitet werden kann."
        ),
        "malen": [
            "Zeichne einen LKW, der Baumstämme transportiert.",
            "Male einen Baumstamm, der auf den LKW geladen wird.",
            "Zeichne einen großen Wald mit einem LKW, der Baumstämme abholt.",
            "Male das Sägewerk, in das der LKW die Stämme bringt.",
            "Zeichne eine Maschine, die Baumstämme transportiert.",
        ],
        "quiz": [
            ("Mit welchem Fahrzeug werden Baumstämme heute oft transportiert?", "Mit einem LKW."),
            ("Warum muss der Baumstamm schnell ins Sägewerk gebracht werden?", "Damit das Holz nicht beschädigt wird."),
            ("Was passiert mit dem Baumstamm im Sägewerk?", "Er wird in Bretter geschnitten."),
            ("Wofür braucht man Maschinen beim Transport von Baumstämmen?", "Um die schweren Stämme zu bewegen."),
            ("Wohin wird der Baumstamm nach dem Fällen gebracht?", "Ins Sägewerk."),
        ],
        "pantomime": [
            "Zeige pantomimisch, wie du einen Baumstamm auf einen LKW lädst.",
            "Imitiere einen LKW, der Baumstämme zum Sägewerk transportiert.",
            "Stelle pantomimisch dar, wie du einen schweren Baumstamm bewegst.",
            "Zeige, wie du einen Baumstamm mit einer Maschine auflädst.",
            "Imitiere, wie der LKW den Wald verlässt und das Sägewerk erreicht.",
        ],
    },
    {
        "number": 4,
        "name": "Sägewerk",
        "info_title": "Im Sägewerk",
        "info": (
            "Im Sägewerk wird der Baumstamm in Bretter geschnitten. Dafür benutzt man große "
            "Maschinen, wie zum Beispiel die Blockbandsäge. Diese Maschinen schneiden den "
            "Baumstamm in viele dünne Bretter. Nachdem die Bretter geschnitten wurden, müssen "
            "sie getrocknet werden. Das ist wichtig, damit das Holz stabil und haltbar bleibt. "
            "Wenn das Holz noch zu feucht ist, kann es sich verziehen oder brechen. Nach dem "
            "Trocknen sind die Bretter bereit, um weiterverarbeitet oder verkauft zu werden. "
            "Der Prozess im Sägewerk ist ein wichtiger Schritt, um aus einem Baum nutzbare "
            "Bretter zu machen."
        ),
        "malen": [
            "Zeichne eine große Maschine, die einen Baumstamm in Bretter schneidet.",
            "Male den Stapel von frisch geschnittenen Brettern.",
            "Zeichne das Sägewerk mit den Maschinen, die das Holz schneiden.",
            "Male den Prozess der Holztrocknung, indem Bretter zum Trocknen gestapelt werden.",
            "Zeichne einen Baumstamm, der gerade in die Blockbandsäge kommt.",
        ],
        "quiz": [
            ("Mit welcher Maschine werden Baumstämme im Sägewerk in Bretter geschnitten?", "Mit der Blockbandsäge."),
            ("Warum müssen Bretter nach dem Sägen getrocknet werden?", "Damit das Holz stabil bleibt und sich nicht verzieht."),
            ("Was passiert, wenn Holz zu feucht bleibt?", "Es kann sich verziehen oder brechen."),
            ("Was wird im Sägewerk aus einem Baumstamm gemacht?", "Der Baumstamm wird in Bretter geschnitten."),
            ("Was ist der nächste Schritt nach dem Schneiden der Bretter im Sägewerk?", "Die Bretter müssen getrocknet werden."),
        ],
        "pantomime": [
            "Stelle pantomimisch dar, wie du einen Baumstamm in Bretter sägst.",
            "Imitiere das Geräusch einer Blockbandsäge, die einen Baumstamm schneidet.",
            "Zeige pantomimisch, wie Bretter aufgestapelt und zum Trocknen ausgelegt werden.",
            "Stelle dar, wie du ein Brett untersuchst, ob es gerade und trocken ist.",
            "Imitiere, wie ein Baumstamm in eine Maschine geschoben wird, um gesägt zu werden.",
        ],
    },
    {
        "number": 5,
        "name": "Baumarkt",
        "info_title": "Der Baumarkt",
        "info": (
            "Nachdem die Bretter im Sägewerk getrocknet wurden, werden sie in den Baumarkt gebracht. "
            "Im Baumarkt können die Bretter gekauft werden. Viele Menschen nutzen das Holz, um Möbel "
            "oder Häuser zu bauen. Vollholz ist besonders beliebt, weil es stabil und langlebig ist. "
            "In den Baumärkten gibt es viele verschiedene Arten von Holz, wie Eiche, Buche oder Kiefer. "
            "Man kann sich das Holz im Baumarkt aussuchen und direkt mitnehmen. Bevor das Holz verkauft "
            "wird, wird es geprüft, damit es eine gute Qualität hat. Der Baumarkt ist der letzte Schritt "
            "im Weg vom Baum zum fertigen Holzprodukt."
        ),
        "malen": [
            "Zeichne einen Stapel Bretter im Baumarkt.",
            "Male verschiedene Holzarten, die im Baumarkt verkauft werden, zum Beispiel Eiche oder Kiefer.",
            "Zeichne einen Menschen, der im Baumarkt Holz kauft.",
            "Male ein Möbelstück, das aus Holz gebaut wurde.",
            "Zeichne den Baumarkt, in dem das Holz verkauft wird.",
        ],
        "quiz": [
            ("Wohin werden die Bretter nach dem Sägewerk gebracht?", "In den Baumarkt."),
            ("Wofür nutzen viele Menschen das Holz aus dem Baumarkt?", "Um Möbel oder Häuser zu bauen."),
            ("Warum ist Vollholz im Baumarkt besonders beliebt?", "Weil es stabil und langlebig ist."),
            ("Welche Holzarten werden oft im Baumarkt verkauft?", "Eiche, Buche, Kiefer."),
            ("Was wird vor dem Verkauf des Holzes im Baumarkt geprüft?", "Die Qualität des Holzes."),
        ],
        "pantomime": [
            "Stelle pantomimisch dar, wie du ein Brett im Baumarkt aussuchst.",
            "Zeige pantomimisch, wie du Bretter in den Einkaufswagen legst.",
            "Imitiere, wie du im Baumarkt verschiedene Holzarten betrachtest.",
            "Stelle dar, wie du ein Brett auf Qualität überprüfst.",
            "Imitiere, wie du Bretter aus dem Baumarkt nach Hause trägst.",
        ],
    },
]

TYPE_META = {
    "malen": ("Malaufgabe", colors.HexColor("#C94038"), colors.HexColor("#FFF5F4")),
    "quiz": ("Quizfrage", colors.HexColor("#E2B929"), colors.HexColor("#FFFBEA")),
    "pantomime": ("Pantomime", colors.HexColor("#2C72AE"), colors.HexColor("#F1F8FE")),
}

PAGE_W, PAGE_H = A4
MARGIN = 12 * mm

styles = getSampleStyleSheet()
BODY = ParagraphStyle(
    "Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.5,
    leading=14, textColor=colors.HexColor("#222222"), spaceAfter=0
)
BODY_SMALL = ParagraphStyle(
    "BodySmall", parent=BODY, fontSize=9.4, leading=12.2
)
TITLE = ParagraphStyle(
    "Title", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17,
    leading=20, textColor=colors.HexColor("#173126"), spaceAfter=4 * mm
)
CENTER = ParagraphStyle(
    "Center", parent=BODY, alignment=TA_CENTER, fontName="Helvetica-Bold"
)
CARD_TEXT = ParagraphStyle(
    "CardText", parent=BODY, fontSize=11.2, leading=14.4, alignment=TA_CENTER
)
CARD_LABEL = ParagraphStyle(
    "CardLabel", parent=BODY, fontSize=8.5, leading=10, alignment=TA_CENTER,
    textColor=colors.HexColor("#555555")
)

def area_label(area):
    return f"Bereich {area['number']}: {area['name']}"

def make_info_pdf(path):
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN
    )
    story = []
    card_h = (PAGE_H - 2 * MARGIN - 7 * mm) / 2
    for idx, area in enumerate(AREAS):
        content = [
            Paragraph(area_label(area), ParagraphStyle(
                "InfoNum", parent=BODY, fontName="Helvetica-Bold",
                fontSize=10, textColor=colors.HexColor("#66736C")
            )),
            Spacer(1, 1.5 * mm),
            Paragraph(area["info_title"], TITLE),
            Paragraph("Vom Baum zum Brett", ParagraphStyle(
                "InfoSub", parent=BODY, fontName="Helvetica-Bold",
                fontSize=9.5, textColor=colors.HexColor("#1F6A45")
            )),
            Spacer(1, 4 * mm),
            Paragraph(area["info"], BODY),
        ]
        table = Table([[content]], colWidths=[PAGE_W - 2 * MARGIN], rowHeights=[card_h])
        table.setStyle(TableStyle([
            ("BOX", (0,0), (-1,-1), 1.2, colors.HexColor("#8B7A61")),
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FCFAF4")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("LEFTPADDING", (0,0), (-1,-1), 10 * mm),
            ("RIGHTPADDING", (0,0), (-1,-1), 10 * mm),
            ("TOPPADDING", (0,0), (-1,-1), 9 * mm),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8 * mm),
        ]))
        story.append(table)
        if idx % 2 == 0:
            story.append(Spacer(1, 7 * mm))
        else:
            story.append(PageBreak())

    rules = [
        Paragraph("So spielt ihr", TITLE),
        Spacer(1, 2 * mm),
        Table([
            ["1 oder 6", "rote Karte - Malaufgabe"],
            ["2 oder 5", "gelbe Karte - Quizfrage"],
            ["3 oder 4", "blaue Karte - Pantomime"],
            ["Geschafft", "3 Felder vor"],
            ["Nicht geschafft", "stehenbleiben"],
            ["Neuer Bereich", "Infokarte gemeinsam laut lesen"],
        ], colWidths=[38 * mm, 115 * mm], style=[
            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
            ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
            ("FONTSIZE", (0,0), (-1,-1), 10.5),
            ("LEADING", (0,0), (-1,-1), 13),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#D4D9D5")),
            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F3F5F3")),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]),
        Spacer(1, 7 * mm),
        Paragraph(
            "Das iPad ist nur der Spielleiter.<br/>"
            "Aufgaben, Lösungen und Texte bleiben auf dem Tisch.",
            ParagraphStyle("RulesNote", parent=BODY, alignment=TA_CENTER,
                           fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                           textColor=colors.HexColor("#1F6A45"))
        ),
        Spacer(1, 4 * mm),
        Paragraph("Vom Baum zum Brett", CENTER),
    ]
    table = Table([[rules]], colWidths=[PAGE_W - 2 * MARGIN], rowHeights=[card_h])
    table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 1.2, colors.HexColor("#8B7A61")),
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#FCFAF4")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 10 * mm),
        ("RIGHTPADDING", (0,0), (-1,-1), 10 * mm),
        ("TOPPADDING", (0,0), (-1,-1), 9 * mm),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8 * mm),
    ]))
    story.append(table)
    doc.build(story)

def draw_wrapped(c, text, x, y, width, max_lines=5, font="Helvetica-Bold", size=11.2, leading=14):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else line + " " + word
        if stringWidth(trial, font, size) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines[-1] and not lines[-1].endswith("…"):
            lines[-1] = lines[-1].rstrip(".") + "…"
    block_h = len(lines) * leading
    yy = y + block_h / 2 - leading
    c.setFont(font, size)
    c.setFillColor(colors.HexColor("#222222"))
    for line in lines:
        c.drawCentredString(x, yy, line)
        yy -= leading

def make_task_pdf(path):
    c = canvas.Canvas(str(path), pagesize=A4)
    cols, rows = 2, 3
    gap = 5 * mm
    card_w = (PAGE_W - 2 * MARGIN - gap) / 2
    card_h = (PAGE_H - 2 * MARGIN - 2 * gap) / 3

    for area in AREAS:
        for key in ("malen", "quiz", "pantomime"):
            title, accent, bg = TYPE_META[key]
            tasks = area[key]
            if key == "quiz":
                tasks = [q for q, _ in tasks]
            cards = list(tasks) + [None]

            for i, task in enumerate(cards):
                row = i // cols
                col = i % cols
                x = MARGIN + col * (card_w + gap)
                y = PAGE_H - MARGIN - (row + 1) * card_h - row * gap

                c.setFillColor(bg)
                c.setStrokeColor(accent)
                c.setLineWidth(1.5)
                c.roundRect(x, y, card_w, card_h, 4 * mm, fill=1, stroke=1)

                c.setFillColor(accent)
                c.roundRect(x, y + card_h - 16 * mm, card_w, 16 * mm, 4 * mm, fill=1, stroke=0)
                c.rect(x, y + card_h - 16 * mm, card_w, 8 * mm, fill=1, stroke=0)

                c.setFillColor(colors.white if key != "quiz" else colors.HexColor("#2C2500"))
                c.setFont("Helvetica-Bold", 10.5)
                c.drawString(x + 5 * mm, y + card_h - 10.3 * mm, title)

                c.setFillColor(colors.HexColor("#555555"))
                c.setFont("Helvetica-Bold", 8.3)
                c.drawRightString(x + card_w - 5 * mm, y + card_h - 10.3 * mm, area_label(area))

                if task is not None:
                    draw_wrapped(
                        c, task, x + card_w / 2, y + card_h / 2 - 3 * mm,
                        card_w - 18 * mm, max_lines=6, size=11.0, leading=14
                    )
                    c.setFillColor(colors.HexColor("#666666"))
                    c.setFont("Helvetica", 8)
                    footer = f"{i + 1}   ·   Vom Baum zum Brett"
                    if key == "quiz":
                        footer = f"{i + 1}   ·   Lösung auf der Lösungsübersicht"
                    c.drawCentredString(x + card_w / 2, y + 7 * mm, footer)
                else:
                    c.setFillColor(accent)
                    c.setFont("Helvetica-Bold", 18)
                    c.drawCentredString(x + card_w / 2, y + card_h / 2 + 5 * mm, title.upper())
                    c.setFillColor(colors.HexColor("#444444"))
                    c.setFont("Helvetica-Bold", 11)
                    c.drawCentredString(x + card_w / 2, y + card_h / 2 - 4 * mm, area_label(area))
                    c.setFont("Helvetica", 9)
                    c.drawCentredString(x + card_w / 2, y + card_h / 2 - 11 * mm, "5 Karten")
                    c.setFont("Helvetica", 7.5)
                    c.setFillColor(colors.HexColor("#777777"))
                    c.drawCentredString(x + card_w / 2, y + 7 * mm, "Trennkarte / Deckkarte")

            c.showPage()
    c.save()

def solution_block(area):
    rows = []
    for i, (q, a) in enumerate(area["quiz"], start=1):
        rows.append([
            Paragraph(f"<b>{i}</b>", BODY_SMALL),
            Paragraph(f"<b>{q}</b><br/>Antwort: {a}", BODY_SMALL),
        ])
    t = Table(rows, colWidths=[10 * mm, 78 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LINEBELOW", (0,0), (-1,-2), 0.35, colors.HexColor("#D5DAD6")),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (0,0), (-1,-1), 3),
    ]))
    return KeepTogether([
        Paragraph(f"Quiz-Lösungen · Bereich {area['number']}", ParagraphStyle(
            "SolutionTitle", parent=TITLE, fontSize=14.5, leading=17, spaceAfter=2 * mm
        )),
        Paragraph(area["name"], ParagraphStyle(
            "SolutionArea", parent=BODY, fontName="Helvetica-Bold",
            fontSize=10, textColor=colors.HexColor("#1F6A45"), spaceAfter=3 * mm
        )),
        t,
    ])

def make_solution_pdf(path):
    doc = SimpleDocTemplate(
        str(path), pagesize=A4, rightMargin=MARGIN, leftMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN
    )
    story = []
    for i, area in enumerate(AREAS):
        story.append(solution_block(area))
        if i in (1, 3):
            story.append(PageBreak())
        elif i != len(AREAS) - 1:
            story.append(Spacer(1, 8 * mm))
    doc.build(story)

def merge_pdfs(paths, output):
    writer = PdfWriter()
    for path in paths:
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)
    with open(output, "wb") as f:
        writer.write(f)

def main():
    info = OUT / "Infokarten_Vom_Baum_zum_Brett.pdf"
    tasks = OUT / "Aufgabenkarten_Vom_Baum_zum_Brett.pdf"
    solutions = OUT / "Quizloesungen_Vom_Baum_zum_Brett.pdf"
    full = OUT / "Druckset_Vom_Baum_zum_Brett.pdf"

    make_info_pdf(info)
    make_task_pdf(tasks)
    make_solution_pdf(solutions)
    merge_pdfs([info, tasks, solutions], full)

    print("Erstellt:")
    for p in (full, info, tasks, solutions):
        print(f"- {p.name}")

if __name__ == "__main__":
    main()
