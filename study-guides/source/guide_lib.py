"""Shared builder for the MDD exam question PDFs.

Usage (from this folder):  python build_all.py
Needs: reportlab  (pip install reportlab)
"""
import os
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TEAL = colors.HexColor("#00695C")
INK = colors.HexColor("#1F2328")
MUTED = colors.HexColor("#5A6270")
RULE = colors.HexColor("#D0D7DE")
ANS_BG = colors.HexColor("#F3F7F6")
TUT_BG = colors.HexColor("#EEF6FB")
TUT_LINE = colors.HexColor("#0E6E9C")
CODE_BG = colors.HexColor("#EEF1F4")
PRI = {"HIGH": "#B42318", "MED": "#B54708", "LOW": "#475467", "STRETCH": "#6941C6", "TUT": "#0E6E9C"}

base = dict(fontName="Helvetica", fontSize=10, leading=14, textColor=INK)
S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=22, leading=27, textColor=TEAL),
    "sub": ParagraphStyle("sub", **{**base, "textColor": MUTED, "fontSize": 10.5}),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=TEAL,
                         spaceBefore=10, spaceAfter=6, keepWithNext=1),
    "q": ParagraphStyle("q", fontName="Helvetica-Bold", fontSize=10.5, leading=14.5, textColor=INK),
    "a": ParagraphStyle("a", **base),
    "small": ParagraphStyle("small", **{**base, "fontSize": 8.5, "leading": 11, "textColor": MUTED}),
    "body": ParagraphStyle("body", **base, spaceAfter=4),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=9.5, leading=13, textColor=INK),
}

CW = 170 * mm  # content width


def bullets(items):
    return "<br/>".join(f"&bull;&nbsp;{i}" for i in items)


def c(s):
    """Inline code."""
    return f'<font face="Courier">{escape(s)}</font>'


LONG_LINES = []


def ocl(src):
    """Multi-line code as markup for use inside an answer paragraph."""
    for l in src.strip("\n").split("\n"):
        if len(l) > 80:
            LONG_LINES.append(l)
    lines = [escape(l).replace("  ", "&nbsp;&nbsp;") for l in src.strip("\n").split("\n")]
    return '<font face="Courier" size="9.5">' + "<br/>".join(lines) + "</font>"


def careful(text):
    """A highlighted warning inside an answer."""
    return f'<font color="#B42318"><b>Careful:</b></font> {text}'


def code_block(src):
    t = Table([[Paragraph(ocl(src), S["code"])]], colWidths=[CW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def grid(data, widths, header=True):
    t = Table([[Paragraph(str(x), S["a"]) for x in row] for row in data], colWidths=widths,
              repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.5, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0EFEC"))]
    t.setStyle(TableStyle(st))
    return t


class Guide:
    def __init__(self, filename, footer_label, title):
        self.out = os.path.join(OUT_DIR, filename)
        self.footer_label, self.title = footer_label, title
        self.story, self.pending, self.n, self.questions = [], [], 0, []

    def p(self, text, style="body"):
        para = Paragraph(text, S[style])
        if self.pending:
            # keep a section heading together with its intro note
            self.pending.append(para)
        else:
            self.story.append(para)

    def add(self, *flow):
        self.story.extend(flow)

    def sec(self, title):
        self.pending.append(Paragraph(title, S["h1"]))

    def qa(self, prio, question, answer, src, extra=(), short=None, tut=None):
        """prio: HIGH/MED/LOW/STRETCH. tut: e.g. 'Sheet 3, 1(e)' marks a tutorial question."""
        self.n += 1
        self.questions.append((f"[Tut. {tut}] " if tut else "") + (short or question))
        tag = f'<font color="{PRI[prio]}" size="8"><b>[{prio}]</b></font>'
        if tut:
            tag += f' <font color="{PRI["TUT"]}" size="8"><b>[TUTORIAL {escape(tut)}]</b></font>'
        q = Paragraph(f"Q{self.n}. {question} &nbsp;{tag}", S["q"])
        a = Paragraph(answer + f'<br/><font size="8" color="#5A6270">Source: {src}</font>', S["a"])
        box = Table([[a]], colWidths=[CW])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), TUT_BG if tut else ANS_BG),
            ("LINEBEFORE", (0, 0), (0, -1), 2.5, TUT_LINE if tut else TEAL),
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]))
        parts = [*self.pending, q, Spacer(1, 4), box]
        if extra:
            parts += [Spacer(1, 6), *extra]
        parts.append(Spacer(1, 10))
        self.pending = []
        self.story.append(KeepTogether(parts))

    def self_test(self):
        self.story.append(PageBreak())
        self.story.append(Paragraph("Self-test: questions only", S["h1"]))
        self.p("Answer each one on paper without looking, then check against the answers above. "
               "Tick the ones you got fully right; repeat the rest in two days. Tutorial questions are marked "
               "[Tut.]: these are the best predictor of exam style.")
        rows = [["#", "Question", "OK?"]] + [[str(i + 1), q, ""] for i, q in enumerate(self.questions)]
        self.story.append(grid(rows, [10 * mm, 145 * mm, 15 * mm]))

    def build(self):
        label = self.footer_label

        def footer(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(MUTED)
            canvas.drawString(20 * mm, 12 * mm, label)
            canvas.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
            canvas.restoreState()

        doc = SimpleDocTemplate(self.out, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                                bottomMargin=20 * mm, title=self.title, author="Study guide")
        doc.build(self.story, onFirstPage=footer, onLaterPages=footer)
        print("wrote", self.out)
        for l in LONG_LINES:
            print("  LONG CODE LINE (may wrap):", len(l), l)
        LONG_LINES.clear()


HOW_TO_USE_COMMON = [
    "Cover the answer box, say or write your answer, then check. Recalling beats re-reading.",
    "<b>[HIGH]</b> = core, learn it. <b>[MED]</b> = likely as part of a bigger question. <b>[LOW]</b> = background. "
    "<b>[STRETCH]</b> = beyond this lecture's slides.",
    "<b>Blue boxes marked [TUTORIAL]</b> are the exercise-sheet questions with the official sample solution. "
    "Where the sample solution is wrong or sloppy, the box shows <b>both</b> the official answer and a corrected "
    "one, marked <font color='#B42318'><b>Careful</b></font>. Learn the corrected version, but know what the "
    "official one looks like.",
    "The last page has every question without answers for self-testing.",
]

__all__ = ["Guide", "S", "bullets", "c", "ocl", "careful", "code_block", "grid", "mm", "Paragraph", "Spacer",
           "PageBreak", "KeepTogether", "CW", "HOW_TO_USE_COMMON", "Table", "TableStyle", "colors", "INK",
           "MUTED", "TEAL"]
