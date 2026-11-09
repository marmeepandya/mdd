"""Tiny UML-ish diagram helper for the study guides (reportlab graphics).

Coordinates are in points, origin bottom-left. Text supports potency superscripts: "Car^2:VehicleCategory"
draws "2" raised and small. Box text lines starting with '*' are drawn bold.
"""
import math
import re
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, PolyLine
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors

INK = colors.HexColor("#1F2328")
MUTED = colors.HexColor("#5A6270")
RED = colors.HexColor("#B42318")
FILL = colors.HexColor("#F6F8FA")
LEVEL = colors.HexColor("#8C959F")

_SUP = re.compile(r"\^(\S+?)(?=$|[\s:=,)])")


def _segments(text):
    """Split 'Car^2:Vehicle' into [('Car', False), ('2', True), (':Vehicle', False)]."""
    out, pos = [], 0
    for m in _SUP.finditer(text):
        out.append((text[pos:m.start()], False))
        out.append((m.group(1), True))
        pos = m.end()
    out.append((text[pos:], False))
    return [(t, sup) for t, sup in out if t]


def text_width(text, font="Helvetica", size=7.5):
    return sum(stringWidth(t, font, size * (0.75 if sup else 1)) for t, sup in _segments(text))


def draw_text(d, x, y, text, font="Helvetica", size=7.5, color=INK, anchor="start"):
    w = text_width(text, font, size)
    if anchor == "middle":
        x -= w / 2
    for t, sup in _segments(text):
        s = size * (0.75 if sup else 1)
        d.add(String(x, y + (size * 0.4 if sup else 0), t, fontName=font, fontSize=s, fillColor=color))
        x += stringWidth(t, font, s)


class Diagram:
    def __init__(self, width, height):
        self.d = Drawing(width, height)
        self.boxes = {}

    def box(self, key, x, y, header, attrs=(), w=None, size=7.5, color=INK, italic=False):
        """header: str or list of str (e.g. ['<<stereotype>>', 'Clock']). (x, y) = top-left corner."""
        hdr = [header] if isinstance(header, str) else list(header)
        lines = list(attrs)
        hfont = "Helvetica-BoldOblique" if italic else "Helvetica-Bold"
        need = max([text_width(h.lstrip("!"), hfont, size) for h in hdr] + [text_width(a, "Helvetica", size) for a in lines] + [20])
        w = w or need + 10
        lh = size + 3
        hh = lh * len(hdr) + 4
        ah = (lh * len(lines) + 4) if lines else 6
        h = hh + ah
        self.d.add(Rect(x, y - h, w, h, fillColor=FILL, strokeColor=color, strokeWidth=0.8))
        self.d.add(Line(x, y - hh, x + w, y - hh, strokeColor=color, strokeWidth=0.6))
        for i, t in enumerate(hdr):
            c = RED if t.startswith("!") else color
            t = t.lstrip("!")
            f = "Helvetica" if t.startswith("«") else hfont
            draw_text(self.d, x + w / 2, y - 3 - lh * (i + 1) + 2, t, f, size, c, anchor="middle")
        for i, t in enumerate(lines):
            c = RED if t.startswith("!") else color
            draw_text(self.d, x + 4, y - hh - lh * (i + 1) + 1, t.lstrip("!"), "Helvetica", size, c)
        self.boxes[key] = (x, y - h, w, h)
        return self.boxes[key]

    # anchor points on a box
    def pt(self, key, side, frac=0.5):
        x, y, w, h = self.boxes[key]
        return {"top": (x + w * frac, y + h), "bottom": (x + w * frac, y),
                "left": (x, y + h * frac), "right": (x + w, y + h * frac)}[side]

    def _head(self, x1, y1, x2, y2, kind):
        ang = math.atan2(y2 - y1, x2 - x1)
        s, a = 7, 0.42
        p = [x2, y2, x2 - s * math.cos(ang - a), y2 - s * math.sin(ang - a),
             x2 - s * math.cos(ang + a), y2 - s * math.sin(ang + a)]
        if kind == "filled":
            self.d.add(Polygon(p, fillColor=INK, strokeColor=INK, strokeWidth=0.6))
        elif kind == "hollow":
            self.d.add(Polygon(p, fillColor=colors.white, strokeColor=INK, strokeWidth=0.8))
        elif kind == "open":
            self.d.add(PolyLine([p[2], p[3], x2, y2, p[4], p[5]], strokeColor=INK, strokeWidth=0.8))

    def line(self, pts, head=None, dashed=False, label=None, label_at=None, size=6.8):
        """pts: list of (x, y); head drawn at the last point: 'filled' | 'hollow' | 'open' | None."""
        flat = [v for p in pts for v in p]
        self.d.add(PolyLine(flat, strokeColor=INK, strokeWidth=0.8, strokeDashArray=[3, 2] if dashed else None))
        if head:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            self._head(x1, y1, x2, y2, head)
        if label:
            lx, ly = label_at or ((pts[0][0] + pts[-1][0]) / 2 + 3, (pts[0][1] + pts[-1][1]) / 2 + 3)
            draw_text(self.d, lx, ly, label, "Helvetica-Oblique", size, MUTED)

    def text(self, x, y, t, size=7, color=MUTED, font="Helvetica-Oblique"):
        draw_text(self.d, x, y, t, font, size, color)

    def level(self, y, label, x0=0, x1=None):
        x1 = x1 or self.d.width
        self.d.add(Line(x0, y, x1, y, strokeColor=LEVEL, strokeWidth=0.6, strokeDashArray=[4, 3]))
        draw_text(self.d, x0 + 1, y - 9, label, "Helvetica-Bold", 8, LEVEL)

    def note(self, key, x, y, lines, size=7.2):
        w = max(text_width(t, "Helvetica", size) for t in lines) + 12
        lh = size + 3
        h = lh * len(lines) + 6
        f = 7
        self.d.add(Polygon([x, y - h, x + w, y - h, x + w, y - f, x + w - f, y, x, y],
                           fillColor=colors.HexColor("#FFFBEA"), strokeColor=INK, strokeWidth=0.7))
        for i, t in enumerate(lines):
            draw_text(self.d, x + 5, y - 3 - lh * (i + 1) + 2, t, "Helvetica", size, INK)
        self.boxes[key] = (x, y - h, w, h)

    @property
    def drawing(self):
        return self.d
