"""Build MDD Mock Exam 2 (questions + solutions).

Usage (from this folder):  python build_mock2.py
Needs: reportlab. Reuses the study-guide tooling in ../../source (guide_lib.py, uml.py).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "source")))

from guide_lib import *  # noqa: E402,F401
from guide_lib import ANS_BG, RULE, LONG_LINES  # noqa: E402
from uml import Diagram, RED  # noqa: E402
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.platypus import SimpleDocTemplate  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, ".."))
G, H = "«", "»"
GRADE_BG = colors.HexColor("#FFF6E5")


def fit(flow, maxw=CW - 20):
    """Scale a reportlab Drawing down so it fits inside a solution box."""
    if isinstance(flow, Drawing) and flow.width > maxw:
        f = maxw / flow.width
        flow.scale(f, f)
        flow.width, flow.height = flow.width * f, flow.height * f
    return flow


def sup(name, pot):
    return f"{name}<super>{pot}</super>"


# =====================================================================================================
# Diagrams
# =====================================================================================================
def diamond(dg, x, y, direction="down", filled=True):
    """Composition diamond with its tip at (x, y), pointing in `direction` (the body lies on the other side)."""
    s, w = 9, 4.5
    if direction == "down":
        pts = [x, y, x - w, y + s / 2, x, y + s, x + w, y + s / 2]
    elif direction == "up":
        pts = [x, y, x - w, y - s / 2, x, y - s, x + w, y - s / 2]
    elif direction == "right":
        pts = [x, y, x - s / 2, y + w, x - s, y, x - s / 2, y - w]
    else:  # left
        pts = [x, y, x + s / 2, y + w, x + s, y, x + s / 2, y - w]
    dg.d.add(Polygon(pts, fillColor=INK if filled else colors.white, strokeColor=INK, strokeWidth=0.7))


def ocl_model():
    """Task 2 class diagram: university course registration."""
    dg = Diagram(170 * mm, 200)
    dg.box("lec", 5, 185, "Lecturer", ["name : String"], w=90)
    dg.box("course", 170, 185, "Course", ["title : String", "ects : Integer", "capacity : Integer",
                                         "/freeSeats : Integer", "allPrerequisites() : Set(Course)"], w=150)
    dg.box("stud", 380, 185, "Student", ["name : String", "semester : Integer", "/ectsEarned : Integer",
                                         "enroll(c : Course)"], w=100)
    dg.box("enr", 295, 100, "Enrollment", ["grade : Real [0..1]", "/passed : Boolean"], w=110)
    # Student - Course with association class
    dg.line([(320, 160), (380, 160)])
    dg.text(323, 163, "course"); dg.text(323, 152, "*")
    dg.text(352, 163, "student"); dg.text(372, 152, "*")
    dg.line([(350, 160), (350, 100)], dashed=True)
    # Lecturer - Course
    dg.line([(95, 170), (170, 170)])
    dg.text(98, 173, "lecturer"); dg.text(98, 161, "1")
    dg.text(143, 173, "course"); dg.text(162, 161, "*")
    # recursive prerequisite association
    dg.line([(215, 114), (215, 80), (140, 80), (140, 130), (170, 130)])
    dg.text(88, 118, "prerequisite *")
    dg.text(219, 100, "followUp *")
    return dg.drawing


def atl_metamodels():
    dg = Diagram(170 * mm, 215)
    dg.text(5, 205, "Source metamodel: Curriculum", 8, color=INK, font="Helvetica-Bold")
    dg.text(265, 205, "Target metamodel: Catalogue", 8, color=INK, font="Helvetica-Bold")
    # source
    dg.box("prog", 40, 192, "Programme", ["name : String"], w=110)
    dg.box("mod", 40, 132, "Module", ["code : String", "title : String", "ects : Integer", "mandatory : Boolean"],
           w=110)
    dg.box("ses", 40, 45, "Session", ["weekday : String", "hours : Integer"], w=110)
    px = 95
    dg.line([(px, dg.pt("prog", "bottom")[1] - 9), (px, dg.pt("mod", "top")[1])])
    diamond(dg, px, dg.pt("prog", "bottom")[1], "up")
    dg.text(px + 4, 140, "modules"); dg.text(px - 12, 135, "*")
    dg.line([(px, dg.pt("mod", "bottom")[1] - 9), (px, dg.pt("ses", "top")[1])])
    diamond(dg, px, dg.pt("mod", "bottom")[1], "up")
    dg.text(px + 4, 53, "sessions"); dg.text(px - 12, 48, "*")
    # target
    dg.box("cat", 300, 192, "Catalogue", ["title : String"], w=120)
    dg.box("ent", 300, 132, "Entry", ["label : String", "credits : Integer", "weeklyHours : Integer"], w=120,
           italic=True)
    dg.text(425, 122, "{abstract}")
    dg.box("core", 255, 40, "CoreEntry", w=90)
    dg.box("elec", 375, 40, "ElectiveEntry", w=95)
    cx = 360
    dg.line([(cx, dg.pt("cat", "bottom")[1] - 9), (cx, dg.pt("ent", "top")[1])])
    diamond(dg, cx, dg.pt("cat", "bottom")[1], "up")
    dg.text(cx + 4, 140, "entries"); dg.text(cx - 12, 135, "*")
    bar = 62
    for k in ("core", "elec"):
        x = dg.pt(k, "top")[0]
        dg.line([dg.pt(k, "top"), (x, bar)])
    dg.line([(dg.pt("core", "top")[0], bar), (dg.pt("elec", "top")[0], bar)])
    dg.line([(cx, bar), dg.pt("ent", "bottom")], head="hollow")
    return dg.drawing


def approaches_solution():
    dg = Diagram(170 * mm, 190)
    dg.text(0, 182, "Metamodeling approach", 7.8, color=INK, font="Helvetica-Bold")
    dg.text(250, 182, "Profile approach", 7.8, color=INK, font="Helvetica-Bold")
    dg.d.add(Line(238, 0, 238, 186, strokeColor=RULE, strokeWidth=0.8))
    dg.text(0, 168, "metamodel level", 7)
    dg.text(0, 62, "model level", 7)
    # metamodeling: Entity generalizes Class
    dg.box("c1", 60, 165, [G + "metaclass" + H, "Class"], w=90)
    dg.box("e1", 60, 112, "Entity", ["table : String"], w=90)
    dg.line([dg.pt("e1", "top"), dg.pt("c1", "bottom")], head="hollow")
    dg.text(110, 120, "generalization", 6.8)
    dg.box("m1", 40, 50, "Enrollment : Entity", ["table = 'ENROLLMENTS'"], w=130)
    # profile: Entity extends Class
    dg.box("c2", 255, 165, [G + "metaclass" + H, "Class"], w=80)
    dg.box("e2", 375, 165, [G + "stereotype" + H, "Entity"], ["table : String"], w=95)
    dg.line([dg.pt("e2", "left", 0.62), dg.pt("c2", "right", 0.5)], head="filled")
    dg.text(338, 155, "extension", 6.8)
    dg.box("m2", 255, 75, [G + "Entity" + H, "Enrollment"], w=90)
    dg.text(350, 64, "representation", 6.8)
    dg.box("m3", 255, 32, "Enrollment : Class", w=95)
    dg.box("s3", 375, 38, ":Entity", ["table = 'ENROLLMENTS'"], w=110)
    dg.line([dg.pt("m3", "right"), dg.pt("s3", "left", 0.4)])
    dg.text(300, 4, "realisation (slides 6, 10)", 6.8)
    return dg.drawing


def stereotyped_solution():
    dg = Diagram(170 * mm, 170)
    dg.text(0, 162, "Notation 1: guillemets + note with tagged values", 7.5, color=INK, font="Helvetica-Bold")
    dg.box("e", 20, 140, [G + "Entity" + H, G + "Audited" + H, "Enrollment"], ["grade : Real [0..1]"], w=110)
    dg.note("n", 230, 150, [G + "Entity" + H, "table = 'ENROLLMENTS'", G + "Audited" + H, "auditor = 'Exam Office'",
                            "retentionYears = 10"])
    dg.line([dg.pt("e", "right"), dg.pt("n", "left")], dashed=True)
    dg.text(0, 66, "Notation 2: stored as instances of the stereotypes (slide 10)", 7.5, color=INK,
            font="Helvetica-Bold")
    dg.box("e2", 20, 50, "Enrollment", w=90)
    dg.box("i1", 200, 58, ":Entity", ["table = 'ENROLLMENTS'"], w=120)
    dg.box("i2", 340, 58, ":Audited", ["auditor = 'Exam Office'", "retentionYears = 10"], w=125)
    dg.line([dg.pt("e2", "right"), dg.pt("i1", "left")])
    dg.line([dg.pt("e2", "bottom"), (65, 6), (402, 6), dg.pt("i2", "bottom")])
    return dg.drawing


def powertype_solution():
    dg = Diagram(170 * mm, 150)
    dg.box("course", 40, 140, "Course", ["title : String", "term : String"], w=110)
    dg.box("fmt", 330, 140, "CourseFormat", ["maxParticipants : Integer", "examForm : String"], w=135)
    dg.line([dg.pt("course", "right", 0.6), dg.pt("fmt", "left", 0.6)])
    dg.text(155, 129, "classified course *")
    dg.text(270, 129, "format 1")
    xs = [5, 115, 225]
    names = ["Lecture", "Seminar", "ProjectCourse"]
    for n, x in zip(names, xs):
        dg.box(n, x, 30, n, w=95)
    bar = 70
    for n in names:
        x = dg.pt(n, "top")[0]
        dg.line([dg.pt(n, "top"), (x, bar)])
    dg.line([(dg.pt(names[0], "top")[0], bar), (dg.pt(names[-1], "top")[0], bar)])
    cx = dg.pt("course", "bottom")[0]
    dg.line([(cx, bar), dg.pt("course", "bottom")], head="hollow")
    dg.text(cx + 6, 84, ": CourseFormat", 7.4, color=RED, font="Helvetica-Bold")
    dg.text(cx + 6, 75, "{disjoint, incomplete}", 7.4, color=RED, font="Helvetica-Bold")
    return dg.drawing


def deep_model(blanks=True):
    """Task 5 deep model. blanks=True shows [a]..[f]; False shows the solution in red."""
    v = (lambda k, val: f"[{k}]") if blanks else (lambda k, val: str(val))
    r = "" if blanks else "!"
    dg = Diagram(170 * mm, 270)
    dg.level(268, "O0")
    dg.box("cf", 150, 260, r + "CourseFormat^" + v("a", 2),
           [r + "maxParticipants^" + v("b", 1) + " : Integer", r + "examForm^2 : String = 'written'^" + v("c", 1),
            "ects^2 : Integer"], w=185)
    dg.level(192, "O1")
    dg.box("co", 200, 186, r + "Course^" + v("d", 0), ["title^1 : String", "term^1 : String"], w=90, italic=False)
    dg.box("le", 30, 130, "Lecture^1:CourseFormat",
           ["maxParticipants^0 = 300", "examForm^1 = 'written'^0", r + "ects^" + v("e", 1) + " = 6^0"], w=165)
    dg.box("se", 285, 130, "Seminar^1:CourseFormat",
           ["maxParticipants^0 = 20", "examForm^1 = 'presentation'^0", "ects^1 = 4^0"], w=165)
    bar = 138
    for k in ("le", "se"):
        x = dg.pt(k, "top")[0]
        dg.line([dg.pt(k, "top"), (x, bar)])
    dg.line([(dg.pt("le", "top")[0], bar), (dg.pt("se", "top")[0], bar)])
    dg.line([(dg.pt("co", "bottom")[0], bar), dg.pt("co", "bottom")], head="hollow")
    dg.level(74, "O2")
    dg.box("mdd", 30, 66, r + "MDD2026^" + v("f", 0) + ":Lecture",
           ["title^0 = 'Model-Driven Dev.'", "term^0 = 'HWS 2026'", "examForm^0 = 'written'", "ects^0 = 6"], w=165)
    dg.box("ds", 285, 66, "DataSem^0:Seminar",
           ["title^0 = 'Data Seminar'", "term^0 = 'FSS 2027'", "examForm^0 = 'presentation'", "ects^0 = 4"], w=165)
    return dg.drawing


# =====================================================================================================
# Document helpers
# =====================================================================================================
S2 = {
    "task": ParagraphStyle("task", fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=TEAL,
                           spaceBefore=8, spaceAfter=4, keepWithNext=1),
    "sq": ParagraphStyle("sq", fontName="Helvetica", fontSize=10, leading=14, textColor=INK, leftIndent=16,
                         firstLineIndent=-16, spaceBefore=3, spaceAfter=3),
    "grade": ParagraphStyle("grade", fontName="Helvetica-Oblique", fontSize=8.5, leading=11.5, textColor=INK),
}


class Doc:
    def __init__(self, filename, footer, title):
        self.path = os.path.join(OUT, filename)
        self.footer, self.title = footer, title
        self.story = []

    def p(self, text, style="body"):
        st = S2.get(style) or S[style]
        self.story.append(Paragraph(text, st))

    def add(self, *f):
        self.story.extend(f)

    def task(self, n, title, pts):
        self.story.append(Paragraph(f"Task {n}: {title} &nbsp;<font color='#5A6270' size='10'>({pts} points)</font>",
                                    S2["task"]))

    def sq(self, label, text, pts):
        self.story.append(Paragraph(f"<b>({label})</b> {text} &nbsp;<font color='#B42318'><b>[{pts} P]</b></font>",
                                    S2["sq"]))

    def sol(self, label, pts, answer, grading, src, table=None):
        head = Paragraph(f"<b>({label})</b> <font color='#B42318'>[{pts} P]</font>", S["q"])
        rows = [[Paragraph(answer, S["a"])]]
        extras = table if isinstance(table, (list, tuple)) else ([table] if table is not None else [])
        for t in extras:
            rows.append([fit(t)])
        gi = len(rows)
        rows.append([Paragraph("<b>Grading:</b> " + grading, S2["grade"])])
        rows.append([Paragraph(f'<font size="8" color="#5A6270">Source: {src}</font>', S["a"])])
        box = Table(rows, colWidths=[CW])
        box.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), ANS_BG), ("BACKGROUND", (0, gi), (0, gi), GRADE_BG),
            ("LINEBEFORE", (0, 0), (0, -1), 2.5, TEAL),
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        self.story.append(KeepTogether([head, Spacer(1, 3), box, Spacer(1, 9)]))

    def build(self):
        label = self.footer

        def footer(canvas, doc):
            canvas.saveState()
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(MUTED)
            canvas.drawString(20 * mm, 12 * mm, label)
            canvas.drawRightString(190 * mm, 12 * mm, f"Page {doc.page}")
            canvas.restoreState()

        doc = SimpleDocTemplate(self.path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                                bottomMargin=20 * mm, title=self.title, author="Study guide")
        doc.build(self.story, onFirstPage=footer, onLaterPages=footer)
        print("wrote", self.path)
        for l in LONG_LINES:
            print("  LONG CODE LINE (may wrap):", len(l), l)
        LONG_LINES.clear()


TASKS = [(1, "MDA foundations and language definition", 10), (2, "OCL: course registration", 37),
         (3, "ATL: Curriculum to Catalogue", 15), (4, "Profiles, stereotypes and powertypes", 14),
         (5, "Deep modeling", 14)]
assert sum(t[2] for t in TASKS) == 90

# =====================================================================================================
# QUESTIONS
# =====================================================================================================
q = Doc("MDD-Mock-2.pdf", "MDD - Mock Exam 2 (HWS 2026) - questions", "MDD Mock Exam 2")
q.p("Model-Driven Development: Mock Exam 2", "title")
q.p("University of Mannheim, HWS 2026. Practice exam, 90 minutes, 90 points. Planned for <b>Sun 13 Dec, 08:30</b> "
    "(the real exam slot). Solutions are in <i>MDD-Mock-2-Solutions.pdf</i>.", "sub")
q.add(Spacer(1, 8))
q.p("Instructions", "h1")
q.p(bullets([
    "Work <b>closed book</b>, on paper, with a timer: about <b>one point per minute</b>. Write OCL and ATL by hand.",
    "The real exam format was not announced yet, so this mock mixes theory and writing. Compared with Mock 1 it is "
    "<b>slightly harder</b>: association classes, <b>iterate</b>, undefined values, <b>@pre</b>, def/let, ATL guards and "
    "refining mode, extension vs. generalization, multiple stereotypes, potency arithmetic.",
    "Use the exact names from the diagrams. Strings in single quotes. Where a task is ambiguous, state your assumption "
    "in one sentence.",
    "\"Briefly justify\" means one sentence per point.",
]))
q.add(Spacer(1, 4))
q.add(grid([["Task", "Topic", "Points", "Your score"]] +
           [[str(n), t, str(pts), ""] for n, t, pts in TASKS] + [["", "<b>Total</b>", "<b>90</b>", ""]],
           [15 * mm, 105 * mm, 20 * mm, 30 * mm]))
q.add(PageBreak())

# ---------------------------------------------------------------- Task 1
q.task(1, "MDA foundations and language definition", 10)
q.sq("a", "(i) Name the three primary goals of MDA and the principle through which MDA wants to reach them. "
     "(ii) In the MDA process, which artefacts does the <b>transformation tool</b> take as input and produce as output, "
     "and which role writes the <b>transformation definition</b>?", 3)
q.sq("b", "Formal languages are defined by four ingredients. Name all four, say in one sentence what each defines, "
     "and state <b>how the UML specification</b> defines each of them.", 4)
q.sq("c", "State the role of each of the following OMG standards in the MDA infrastructure (one sentence each): "
     "<b>MOF</b>, <b>QVT</b>, <b>XMI</b>.", 3)

# ---------------------------------------------------------------- Task 2
q.task(2, "OCL: course registration", 37)
q.p("A university uses the following class diagram. <b>Enrollment</b> is an <b>association class</b> between Student and "
    "Course. Its <font face='Courier'>grade</font> (German scale 1.0 to 5.0, at most 4.0 = passed) is <b>undefined</b> "
    "until the exam is graded. The recursive association gives each course its direct prerequisites. The derived "
    "attribute freeSeats is defined by:")
q.add(code_block("context Course::freeSeats : Integer\nderive: capacity - student->size()"))
q.add(Spacer(1, 4), ocl_model(), Spacer(1, 4))
q.sq("a", "Write an invariant (with a name) ensuring that a course never has more enrolled students than its capacity.", 2)
q.sq("b", "Define the derived attribute <font face='Courier'>passed</font> of Enrollment: an enrollment is passed if it "
     "has a grade and the grade is at most 4.0. Briefly justify why your expression is never undefined, even for "
     "enrollments that are not graded yet.", 3)
q.sq("c", "Define the derived attribute <font face='Courier'>ectsEarned</font> of Student: the sum of the ECTS of all "
     "courses the student has passed. A classmate writes "
     "<font face='Courier'>...course.ects-&gt;asSet()-&gt;sum()</font>. Why is that wrong? Give a concrete case.", 4)
q.sq("d", "Write <font face='Courier'>ectsEarned</font> again, this time using <b>only iterate</b> (no select, collect "
     "or sum). Write out the iterator and accumulator types.", 4)
q.sq("e", "Use <b>def</b> to add an operation <font face='Courier'>averageGrade() : Real</font> to Student: the average of "
     "all grades the student has received so far (ungraded enrollments are ignored); 0.0 if there is no grade yet. "
     "Use a <b>let</b> expression for the set of graded enrollments.", 3)
q.sq("f", "(i) Write a <b>body</b> expression for <font face='Courier'>allPrerequisites()</font>: all direct and indirect "
     "prerequisites of a course. (ii) Assume the body is <font face='Courier'>self-&gt;closure(prerequisite)"
     "-&gt;excluding(self)</font> (the Sheet 4 pattern). A colleague tries to forbid cyclic prerequisites with "
     "<font face='Courier'>context Course inv: not self.allPrerequisites()-&gt;includes(self)</font>. Explain why this "
     "does not work, and write a correct invariant.", 4)
q.sq("g", "Write the contract for <font face='Courier'>Student::enroll(c : Course)</font>.<br/>"
     "Preconditions: (1) the course has a free seat; (2) the student is not yet enrolled in c; (3) the student has "
     "passed every <b>direct</b> prerequisite of c.<br/>"
     "Postconditions: (4) c has been added to the student's courses and nothing else has changed in that set; "
     "(5) there is an enrollment for c that was created during the operation and has no grade yet; (6) c has one free "
     "seat less than before.", 6)
q.p("For (h), assume this object situation. Courses (ects, capacity): MDD (6, 2), ML (8, 40), DB (6, 30), SEM (4, 10). "
    "Prerequisites: SEM has the prerequisite MDD; no other prerequisites. Enrollments (student, course, grade): "
    "(Anna, MDD, 1.7), (Anna, ML, 5.0), (Anna, SEM, <i>no grade yet</i>), (Ben, MDD, 2.3), (Ben, DB, 1.3). "
    "anna, ben and mdd denote the objects. Use your definitions from (b) and (c).", "body")
q.sq("h", "Evaluate (result suffices, one point each):<br/>"
     "(1) <font face='Courier'>ben.enrollment.course.ects</font> &nbsp; "
     "(2) <font face='Courier'>ben.enrollment.course.ects-&gt;asSet()-&gt;sum()</font><br/>"
     "(3) <font face='Courier'>anna.ectsEarned</font> &nbsp; "
     "(4) <font face='Courier'>mdd.freeSeats</font><br/>"
     "(5) <font face='Courier'>anna.enrollment-&gt;exists(e | e.grade &gt; 4.0)</font> &nbsp; "
     "(6) <font face='Courier'>anna.enrollment-&gt;forAll(e | e.grade &lt;= 4.0)</font>", 6)
q.sq("i", "Each constraint below is syntactically valid but does not say what is intended. Name the problem and fix "
     "it. (1) Intended: enroll adds exactly one course. (2) Intended: every grade lies between 1.0 and 5.0. "
     "(3) Intended: a lecturer teaches at most 200 <b>different</b> students.", 3)
q.add(code_block("-- (1)\ncontext Student::enroll(c : Course)\npost: course->size() = course->size() + 1\n"
                 "-- (2)\ncontext Enrollment\ninv: grade >= 1.0 and grade <= 5.0\n"
                 "-- (3)\ncontext Lecturer\ninv: course.student->size() <= 200"), Spacer(1, 2))
q.sq("j", "ExchangeStudent is a subclass of Student. It redefines the precondition of enroll as shown below. "
     "(i) Is this redefinition allowed under the Liskov Substitution Principle? Justify. (ii) May ExchangeStudent "
     "add the extra postcondition <font face='Courier'>semester = semester@pre</font>? Justify.", 2)
q.add(code_block("context ExchangeStudent::enroll(c : Course)\npre: c.freeSeats > 0 and c.ects <= 6"))

# ---------------------------------------------------------------- Task 3
q.add(PageBreak())
q.task(3, "ATL: Curriculum to Catalogue", 15)
q.p("A curriculum model is to be transformed into a course catalogue. The two metamodels are:")
q.add(Spacer(1, 4), atl_metamodels(), Spacer(1, 4))
q.p("Requirements:")
q.p(bullets([
    "Every Programme becomes a Catalogue whose title is the programme's name and whose entries are the entries created "
    "for its modules.",
    "A <b>mandatory</b> module becomes a <b>CoreEntry</b>. A module that is not mandatory becomes an "
    "<b>ElectiveEntry</b>, but <b>only if it has at least one session</b>. Electives without sessions are not "
    "transformed at all.",
    "label = code + ' - ' + title (e.g. 'IE675 - Machine Learning'); credits = ects; weeklyHours = the sum of the "
    "hours of the module's sessions. Sessions are not transformed into elements of their own.",
]))
q.sq("a", "Write the header of the module <font face='Courier'>Curriculum2Catalogue</font>.", 1)
q.sq("b", "Write two helpers on Curriculum!Module: <font face='Courier'>totalHours</font> (computed with "
     "<b>iterate</b>) and <font face='Courier'>entryLabel</font>.", 3)
q.sq("c", "Write the rule for Programme.", 3)
q.sq("d", "Write the rule(s) for Module.", 4)
q.sq("e", "(i) Why must the source patterns of your Module rules not overlap? (1 P)<br/>"
     "(ii) A second transformation shall only change every module title to upper case and leave the rest of the "
     "curriculum model unchanged. Write its header, and explain why you do not need copy rules for Programme and "
     "Session. (2 P)<br/>"
     "(iii) Could a Module rule contain the binding <font face='Courier'>weeklyHours &lt;- e.credits * 2</font>, where e is "
     "the created target element? Why (not)? (1 P)", 4)

# ---------------------------------------------------------------- Task 4
q.task(4, "Profiles, stereotypes and powertypes", 14)
q.sq("a", "What is an <b>extension</b> in a UML profile, and how is it drawn? Why does a profile use extensions "
     "instead of simply adding a new subclass of the metaclass Class to the UML metamodel?", 2)
q.sq("b", "Slide 6 contrasts the <b>metamodeling approach</b> and the <b>profile approach</b>. Draw both for a "
     "new concept <b>Entity</b> with the property table : String: (i) on the metamodel level, (ii) on the model level "
     "for a class Enrollment with table = 'ENROLLMENTS'. Label which relationship is a generalization and which an "
     "extension.", 4)
q.sq("c", "A second stereotype <b>Audited</b> (tags auditor : String, retentionYears : Integer) extends both Class "
     "and Operation. May one stereotype extend two metaclasses, and may one class carry two stereotypes? Draw Enrollment "
     "with Entity and Audited applied and the tagged values table = 'ENROLLMENTS', auditor = 'Exam Office', "
     "retentionYears = 10. Then show the same information as it is <b>stored</b> (instances of the stereotypes).", 3)
q.sq("d", "Every course has a title and a term. Each course has exactly one format: Lecture, Seminar or "
     "ProjectCourse, modelled as subclasses of Course. A format has a maximum number of participants and an exam form, "
     "the same for all courses of that format. The university also has rare formats (e.g. excursions) that get no "
     "subclass.<br/>(i) Model this with a <b>powertype</b> CourseFormat, including the generalization-set constraints. "
     "(3 P)<br/>(ii) Student has the subclasses BachelorStudent, MasterStudent and ExchangeStudent. Every student is "
     "enrolled in a Bachelor or a Master programme; exchange students are also enrolled in one of them. State the "
     "constraints of this generalization set and justify. (2 P)", 5)

# ---------------------------------------------------------------- Task 5
q.task(5, "Deep modeling", 14)
q.sq("a", "(i) What is <b>deep characterization</b>, and why can traditional UML classification not express it "
     "directly? Name two UML workarounds. (ii) For MDD2026 (model below): give its <b>linguistic</b> type and its "
     "<b>ontological</b> type and level.", 3)
q.p("The following deep model describes the course formats of Task 4. Superscripts are potencies. "
    "Requirements: (R1) course formats have instances (Lecture, Seminar) whose instances are concrete courses; concrete "
    "courses have no instances. (R2) maxParticipants is set once per format. (R3) The default exam form 'written' may "
    "be changed by each format, but a concrete course must use the exam form of its format. (R4) Course is abstract. "
    "(R5) Every concrete course has ECTS, fixed by its format.")
q.add(Spacer(1, 2), deep_model(blanks=True), Spacer(1, 2))
q.sq("b", "The clabject Seminar has a type facet and an instance facet. List what belongs to each.", 2)
q.sq("c", "Fill in the potencies [a] to [f] so that the model meets R1 to R5. Briefly justify each.", 6)
q.sq("d", "Potency arithmetic, one sentence each.<br/>"
     "(1) CourseFormat additionally declares fee<super>1</super> : Integer. Does MDD2026 have a fee? Why (not)?<br/>"
     "(2) Concrete courses shall now be allowed to change the exam form of their format. Which potencies in the model "
     "must change, and to which values?<br/>"
     "(3) May a new clabject Tutorial<super>2</super> : CourseFormat be added on O1?", 3)
q.add(Spacer(1, 10))
q.p("<i>End of Mock Exam 2. Check your answers with MDD-Mock-2-Solutions.pdf and add every lost point to your "
    "mistake list.</i>")
q.build()

# =====================================================================================================
# SOLUTIONS
# =====================================================================================================
s = Doc("MDD-Mock-2-Solutions.pdf", "MDD - Mock Exam 2 (HWS 2026) - solutions", "MDD Mock Exam 2 - Solutions")
s.p("Mock Exam 2: Solutions", "title")
s.p("Model answers, grading notes and sources. Mark your paper strictly: a point needs the right idea <b>and</b> "
    "correct syntax/names. \"Source\" tells you where to re-learn a lost point.", "sub")
s.add(Spacer(1, 6))
s.add(grid([["Task", "Topic", "Points", "Main sources"],
            ["1", "MDA foundations, language definition", "10", "L1 slides 7-8, L6 slides 2-16"],
            ["2", "OCL with association class", "37", "L2, L3 (slides 12-45), L4 (Liskov, closure), Sheets 1-4"],
            ["3", "ATL", "15", "L5 slides 7-25, Sheets 5-6"],
            ["4", "Profiles, stereotypes, powertypes", "14", "L7 slides 3-24, Sheet 7"],
            ["5", "Deep modeling", "14", "L8 slides 5-21, Sheet 8"]],
           [15 * mm, 60 * mm, 18 * mm, 77 * mm]))
s.add(Spacer(1, 6))
s.p("<b>After marking:</b> every lost point goes on the mistake list in <i>study-plan.md</i>, with the source "
    "shown under each answer. Redo those sub-tasks three days later without looking.")

# ---------------------------------------------------------------- Task 1
s.task(1, "MDA foundations and language definition", 10)
s.sol("a", 3, bullets([
    "(i) <b>Portability, interoperability and reusability</b>, reached through <b>architectural separation of "
    "concerns</b>: the specification of the functionality (PIM) is separated from the details of how it is realised on "
    "a particular platform (PSM).",
    "(ii) The transformation tool takes the <b>PIM</b> and the <b>transformation definition</b> as input and produces the "
    "<b>PSM</b>. The transformation definition is written by the <b>transformation definition creator</b> (with a "
    "transformation definition editor, in a transformation definition language such as QVT); the PIM comes from the "
    "PIM analyst (model editor/validator), and the PSM creator uses the result.",
]), "(i) 1 P for the three goals, 0.5 P for separation of concerns. (ii) 1 P input/output, 0.5 P role.",
      "L6 slide 2 (goals); L1 slides 7-8 (MDA process, roles); L6 slide 4")
s.sol("b", 4,
      "Syntax and semantics, each with two parts. UML uses a metamodeling approach: less rigorous than a formal "
      "specification, but more intuitive and pragmatic.",
      "1 P per row: name + meaning + the UML technique. The classic trap: static semantics is OCL, not natural language.",
      "L6 slides 5-6",
      table=grid([
    ["Ingredient", "Defines", "In the UML specification"],
    ["Abstract syntax", "which constructs exist and how they are built from other constructs", "class diagrams "
     "(the metamodel)"],
    ["Concrete syntax", "how the constructs of the abstract syntax are visualized", "natural language"],
    ["Static semantics", "how instances of constructs must be connected to be meaningful (well-formedness)", "OCL"],
    ["Dynamic semantics", "the meaning of well-formed constructs in terms of their effect on the real world",
     "natural language (fUML formalises a subset)"],
], [32 * mm, 80 * mm, 50 * mm]))
s.sol("c", 3, bullets([
    "<b>MOF</b> (Meta-Object Facility): the <b>metalanguage</b> (M3) in which metamodels such as UML, CWM and MOF itself "
    "are defined; also a framework for repositories of metadata.",
    "<b>QVT</b> (MOF 2.0 Query/Views/Transformations): the <b>transformation definition language</b>, defined with MOF, "
    "in which transformation definitions (PIM to PSM) are written. ATL was a submission to the QVT RFP.",
    "<b>XMI</b>: the precise <b>MOF-to-XML mapping</b> used to serialise and interchange MOF-based models and metamodels "
    "between tools (XML documents validated against generated DTDs/schemas).",
]), "1 P each; the key word in bold is required.", "L6 slides 4, 9, 13-16; L5 slide 2")

# ---------------------------------------------------------------- Task 2
s.task(2, "OCL: course registration", 37)
s.p("Navigation facts used throughout: from Student, <font face='Courier'>self.enrollment</font> navigates <b>to</b> the "
    "association class (lower-case class name) and gives a Set(Enrollment); <font face='Courier'>e.course</font> "
    "navigates <b>from</b> the association class and gives a single object; navigating <b>over</b> it "
    "(<font face='Courier'>self.enrollment.course</font>, <font face='Courier'>course.student</font> from Lecturer) gives a "
    "<b>Bag</b>.")
s.sol("a", 2, ocl("context Course\ninv capacityLimit: self.student->size() <= self.capacity") +
      "<br/>Equivalent: <font face='Courier'>enrollment-&gt;size() &lt;= capacity</font> or "
      "<font face='Courier'>freeSeats &gt;= 0</font>.",
      "1 P context + name, 1 P expression. Using <font face='Courier'>.size()</font> instead of "
      "<font face='Courier'>-&gt;size()</font>: -0.5.", "L3 slide 12; Sheet 2 Q2(b)")
s.sol("b", 3, ocl("context Enrollment::passed : Boolean\nderive: not self.grade.oclIsUndefined() and self.grade <= 4.0") +
      "<br/>Why never undefined: for an ungraded enrollment, <font face='Courier'>grade &lt;= 4.0</font> is undefined, but "
      "the left operand is <b>false</b>, and <b>false and undefined = false</b> (one of the two exceptions to undefined "
      "propagation). For graded enrollments both parts are defined.",
      "1 P oclIsUndefined test, 1 P comparison/derive syntax, 1 P justification naming the "
      "false-and-undefined rule. <font face='Courier'>grade &lt;&gt; null</font> is not lecture OCL: -0.5.",
      "L3 slides 18, 28-29")
s.sol("c", 4, ocl("context Student::ectsEarned : Integer\nderive: self.enrollment->select(e | e.passed).course.ects->sum()") +
      "<br/><font face='Courier'>.course</font> after a Set(Enrollment) is a collect and gives a Bag(Course); "
      "<font face='Courier'>.ects</font> gives a <b>Bag(Integer)</b>. "
      "<br/><b>Why asSet() is wrong:</b> it removes duplicate <b>numbers</b>, not duplicate courses. Ben passed MDD (6) "
      "and DB (6): the Bag is {6, 6}, sum 12; after asSet() it is {6}, sum 6. The ECTS of one course would be lost.",
      "2 P expression (1 for the navigation to the association class, 1 for select + sum), 1 P \"duplicates of equal "
      "values are removed\", 1 P concrete example.", "L3 slides 12-13, 41 (collect gives a Bag); Sheet 1 Q3(b)")
s.sol("d", 4, ocl("context Student::ectsEarned : Integer\nderive: self.enrollment->iterate(e : Enrollment; acc : Integer = 0 |\n"
                  "          if e.passed then acc + e.course.ects else acc endif)") +
      "<br/>Start value 0; each passed enrollment adds its course's ECTS, others leave the accumulator unchanged. The "
      "else branch is mandatory.",
      "1 P iterator with type, 1 P accumulator with type and start value 0, 1 P if-then-else with else acc, 1 P "
      "e.course.ects (single object from the association class).", "L3 slides 7, 44-45; Sheet 5 Q1 (iterate)")
s.sol("e", 3, ocl("context Student\n"
                  "def: averageGrade() : Real =\n"
                  "  let graded : Set(Enrollment) =\n"
                  "        self.enrollment->reject(e | e.grade.oclIsUndefined())\n"
                  "  in if graded->isEmpty() then 0.0\n"
                  "     else graded.grade->sum() / graded->size()\n"
                  "     endif") +
      "<br/><font face='Courier'>graded.grade</font> is a Bag(Real), so equal grades all count. "
      "<font face='Courier'>/</font> always returns a Real.",
      "1 P def operation syntax (with parentheses), 1 P let ... in with the filter, 1 P guarded average. Using "
      "<font face='Courier'>passed</font> as the filter is wrong (failed grades also count): -1.",
      "L3 slides 8, 20-21, 28-29; Sheet 3 Q1(c)-(d)")
s.sol("f", 4, "(i)<br/>" + ocl("context Course::allPrerequisites() : Set(Course)\n"
                              "body: self->closure(prerequisite)->excluding(self)") +
      "<br/>(closure as in Sheet 4 Q2; the recursive alternative is also fine: "
      "<font face='Courier'>prerequisite-&gt;union(prerequisite.allPrerequisites())-&gt;asSet()</font>.)"
      "<br/>(ii) The body ends with <font face='Courier'>-&gt;excluding(self)</font>, so the result <b>never</b> "
      "contains self, and the colleague's invariant is always true: it forbids nothing. Correct:<br/>" +
      ocl("context Course\ninv noCycle: self.prerequisite->closure(prerequisite)->excludes(self)") +
      "<br/>Starting at the <b>direct</b> prerequisites, self is reached only via a path of length at least 1, i.e. a "
      "cycle. (This works whether or not closure counts its start elements.) With recursion only: "
      "<font face='Courier'>not prerequisite-&gt;exists(p | p = self or p.allPrerequisites()-&gt;includes(self))</font>; "
      "the recursive body only terminates on acyclic data, so closure is preferable.",
      "(i) 2 P. (ii) 1 P for \"always true because self was excluded\", 1 P correct invariant.",
      "Sheet 4 Q2(a); L4 guide Q27 (cycles); L3 slide 22")
s.sol("g", 6, ocl("context Student::enroll(c : Course)\n"
                  "pre seatFree:    c.freeSeats > 0\n"
                  "pre notEnrolled: self.course->excludes(c)\n"
                  "pre prereqsDone: c.prerequisite->forAll(p |\n"
                  "                   self.enrollment->exists(e | e.course = p and e.passed))\n"
                  "post: self.course = self.course@pre->including(c)\n"
                  "post: self.enrollment->exists(e | e.course = c and e.oclIsNew()\n"
                  "                                 and e.grade.oclIsUndefined())\n"
                  "post: c.freeSeats = c.freeSeats@pre - 1") +
      "<br/>(4) needs equality with <font face='Courier'>@pre-&gt;including(c)</font>; "
      "<font face='Courier'>course-&gt;includes(c)</font> alone does not say \"nothing else changed\". "
      "(2) may also be written <font face='Courier'>not self.course-&gt;includes(c)</font> (Sheet 1 Q3(e)).",
      "1 P per numbered condition. Missing @pre in (4) or (6): 0 for that line. In (3) the forAll/exists nesting "
      "must be right; checking only that some prerequisite is passed is 0.",
      "L3 slides 22, 30 (@pre, oclIsNew); L4 slide 4; Sheets 1 Q3(d)-(e), 3 Q1(e)")
s.sol("h", 6,
      "exists behaves like an <b>or</b> over the elements and forAll like an <b>and</b>, so the undefined SEM grade "
      "does not decide (5) and (6).",
      "1 P each. (1): \"Set{6}\" or \"{6, 6}\" without the Bag: 0.5. (5)/(6): \"undefined\" is the classic wrong answer.",
      "L3 slides 13, 28, 41-43",
      table=grid([
    ["#", "Result", "Why"],
    ["1", "Bag{6, 6}", "MDD and DB both have 6 ECTS; navigation over the association class gives a Bag"],
    ["2", "6", "asSet() gives Set{6}; compare ->sum() = 12"],
    ["3", "6", "MDD passed (1.7); ML failed (5.0); SEM ungraded, so passed = false"],
    ["4", "0", "capacity 2 - 2 enrolled students (Anna, Ben)"],
    ["5", "true", "ML has 5.0 &gt; 4.0; SEM gives undefined, but true or undefined = true"],
    ["6", "false", "ML gives false; SEM gives undefined, but false and undefined = false"],
], [10 * mm, 25 * mm, 125 * mm]))
s.sol("i", 3, bullets([
    "(1) <b>Missing @pre</b>: x = x + 1 is never true. Fix: <font face='Courier'>post: course-&gt;size() = "
    "course@pre-&gt;size() + 1</font>.",
    "(2) For <b>ungraded</b> enrollments grade is undefined, so the invariant is undefined (not true) and every new "
    "enrollment violates it. Fix: <font face='Courier'>inv: grade.oclIsUndefined() or (grade &gt;= 1.0 and grade &lt;= "
    "5.0)</font> (true or undefined = true).",
    "(3) <font face='Courier'>course.student</font> is a <b>Bag</b>: a student attending two of the lecturer's courses "
    "is counted twice. Fix: <font face='Courier'>course.student-&gt;asSet()-&gt;size() &lt;= 200</font>.",
]), "1 P per item: 0.5 diagnosis, 0.5 fix.", "L3 slides 13, 22, 28; Sheet 3 Q1(e), Q2(g)")
s.sol("j", 2, bullets([
    "(i) <b>Not allowed.</b> Preconditions may only be <b>weakened</b> (demand no more). A client holding a Student "
    "reference may legally call enroll for an 8-ECTS course with a free seat; the ExchangeStudent version rejects that "
    "call, so the original precondition does not imply the new one.",
    "(ii) <b>Allowed.</b> Postconditions may be <b>strengthened</b> (promise no less); an extra guarantee never breaks "
    "a client of Student.",
]), "1 P each, only with the reason.", "L4 slides 7-9 (Liskov, Stove example)")

# ---------------------------------------------------------------- Task 3
s.add(PageBreak())
s.task(3, "ATL: Curriculum to Catalogue", 15)
s.p("Complete transformation (parts a-d):")
s.add(code_block(
    "module Curriculum2Catalogue;\n"
    "create OUT : Catalogue from IN : Curriculum;\n\n"
    "helper context Curriculum!Module def: totalHours : Integer =\n"
    "  self.sessions->iterate(s; acc : Integer = 0 | acc + s.hours);\n\n"
    "helper context Curriculum!Module def: entryLabel : String =\n"
    "  self.code + ' - ' + self.title;\n\n"
    "rule Programme2Catalogue {\n"
    "  from\n"
    "    p : Curriculum!Programme\n"
    "  to\n"
    "    c : Catalogue!Catalogue (\n"
    "      title   <- p.name,\n"
    "      entries <- p.modules->select(m | m.mandatory or m.sessions->notEmpty())\n"
    "    )\n"
    "}\n\n"
    "rule Module2CoreEntry {\n"
    "  from\n"
    "    m : Curriculum!Module (m.mandatory)\n"
    "  to\n"
    "    e : Catalogue!CoreEntry (\n"
    "      label       <- m.entryLabel,\n"
    "      credits     <- m.ects,\n"
    "      weeklyHours <- m.totalHours\n"
    "    )\n"
    "}\n\n"
    "rule Module2ElectiveEntry {\n"
    "  from\n"
    "    m : Curriculum!Module (not m.mandatory and m.sessions->notEmpty())\n"
    "  to\n"
    "    e : Catalogue!ElectiveEntry (\n"
    "      label       <- m.entryLabel,\n"
    "      credits     <- m.ects,\n"
    "      weeklyHours <- m.totalHours\n"
    "    )\n"
    "}"))
s.add(Spacer(1, 6))
s.sol("a", 1, ocl("module Curriculum2Catalogue;\ncreate OUT : Catalogue from IN : Curriculum;"),
      "0.5 module line, 0.5 create line with OUT/IN in the right order (target first).", "L5 slide 19; Sheet 6 Q1(a)")
s.sol("b", 3, "See above. <font face='Courier'>totalHours</font> and <font face='Courier'>entryLabel</font> are "
      "<b>attribute helpers</b> (no parameters, used as <font face='Courier'>m.totalHours</font>); operation helpers with "
      "<font face='Courier'>()</font> are equally fine. Strings are concatenated with <font face='Courier'>+</font> in "
      "ATL. A module without sessions gets totalHours = 0 (the start value).",
      "totalHours 2 P (iterate with accumulator type and start value 0, correct context "
      "<font face='Courier'>Curriculum!Module</font>), entryLabel 1 P. Using sum() instead of iterate: max 1 P.",
      "L5 slides 10, 20-21; Sheet 5 Q1")
s.sol("c", 3, "Rule Programme2Catalogue above. The entries binding yields Curriculum!Module elements although the "
      "reference is typed Entry: matched rules have <b>automatic traceability</b> (slide 7), so each matched module is "
      "<b>resolved</b> to the CoreEntry/ElectiveEntry created for it. Electives without sessions are matched by no rule "
      "and could not be resolved, so the select keeps exactly the matched modules.",
      "1 P source/target pattern with metamodel!class, 1 P title binding, 1 P entries binding <b>with</b> the filter. "
      "Without the filter: 0.5 for entries.", "L5 slides 11-12; Sheet 6 Q1(b)")
s.sol("d", 4, "Rules Module2CoreEntry and Module2ElectiveEntry above. Two standard rules with <b>complementary "
      "guards</b> (like Member2Male/Member2Female). Modules that are neither mandatory nor have sessions match no "
      "rule, so they are not transformed. No rule for Session: its data is only read by the helper (like Chapter in "
      "Sheet 5).",
      "1 P each guard, 1 P bindings (label, credits, weeklyHours), 1 P correct target classes CoreEntry/ElectiveEntry "
      "(Entry is abstract and cannot be instantiated).", "L5 slides 9, 11-12, 22; Sheet 5 Q1")
s.sol("e", 4, bullets([
    "(i) A given source element may be matched by <b>only one standard rule</b> (slide 9). If a mandatory module also "
    "satisfied the elective guard, two rules would match it, which is an error.",
    "(ii) Use <b>refining mode</b>:<br/>" + ocl("module UpperTitles;\ncreate OUT : Curriculum refining IN : Curriculum;") +
    "<br/>plus one rule for Module with <font face='Courier'>title &lt;- m.title.toUpper()</font>. In refining mode the "
    "engine <b>automatically copies all unmatched elements</b>; the developer only specifies what changes. Source and "
    "target use the same metamodel, and the source stays read-only (an optimised engine may work in place but commits "
    "only at the end).",
    "(iii) <b>No.</b> Target models are <b>write-only</b> and cannot be navigated (slides 7, 13); bindings may only "
    "read source elements and helpers. Use <font face='Courier'>m.ects * 2</font> instead.",
]), "(i) 1 P, (ii) 1 P header with <font face='Courier'>refining</font> and the same metamodel on both sides, "
      "1 P explanation, (iii) 1 P.", "L5 slides 7, 9, 13, 25")

# ---------------------------------------------------------------- Task 4
s.add(PageBreak())
s.task(4, "Profiles, stereotypes and powertypes", 14)
s.sol("a", 2, bullets([
    "An extension indicates that the properties of a <b>metaclass are extended through a stereotype</b>. It is a kind "
    "of <b>association with the effect of specialization</b>, drawn as a solid line with a <b>filled</b> arrowhead "
    "pointing at the «metaclass».",
    "Profiles are a <b>lightweight</b> mechanism: they <b>do not allow existing metamodels to be modified</b> (not a "
    "first-class extension). A stereotype is only a limited metaclass that is always used together with the metaclass "
    "it extends.",
]), "1 P definition + notation, 1 P \"metamodel cannot be modified / lightweight\".", "L7 slides 3-6")
s.sol("b", 4, bullets([
    "<b>Metamodeling approach</b>: Entity becomes a real new metaclass, a <b>subclass</b> of Class (generalization, "
    "hollow triangle) with the attribute table. On the model level Enrollment is an <b>instance of Entity</b>: "
    "Enrollment : Entity (table = 'ENROLLMENTS'). This modifies the metamodel.",
    "<b>Profile approach</b>: Entity is a «stereotype» connected to «metaclass» Class by an <b>extension</b> (solid "
    "line, filled arrowhead); the logical specialization is only simulated. On the model level Enrollment stays an "
    "instance of Class and is shown as «Entity» Enrollment; it is realised as Enrollment : Class plus an instance "
    ":Entity that stores table = 'ENROLLMENTS'.",
]), "Per approach: 1 P metamodel level (correct arrow type), 1 P model level. Mixing up the hollow triangle and the "
      "filled arrowhead costs the point.", "L7 slides 4-6, 10", table=approaches_solution())
s.sol("c", 3, "<b>Yes and yes</b>: a single stereotype can extend more than one base class, and a base class can have "
      "more than one stereotype (slide 9). Model answer below. Both stereotypes are listed in guillemets (or as one list «Entity, Audited»); "
      "the tagged values are shown in a note attached with a dashed line, grouped by stereotype. In storage, they are "
      "attributes of <b>instances</b> of the stereotypes linked to the class.",
      "1 P yes/yes with both stereotypes applied, 1 P note with all three values grouped correctly, 1 P instance "
      "(storage) view.",
      "L7 slides 9-10; Sheet 7 Q2", table=stereotyped_solution())
s.sol("d", 5, bullets([
    "(i) Course (title, term) with subclasses Lecture, Seminar, ProjectCourse. The powertype <b>CourseFormat</b> "
    "(maxParticipants, examForm) is associated with Course (classified course * to format 1); the generalization set "
    "is labelled <b>: CourseFormat</b>. Constraints <b>{disjoint, incomplete}</b>: each course has exactly one format "
    "(disjoint), and rare formats such as excursions exist without a subclass (incomplete). Lecture, Seminar and "
    "ProjectCourse are <b>instances</b> of CourseFormat (carrying the per-format values) and <b>subclasses</b> of "
    "Course.",
    "(ii) <b>{complete, overlapping}</b>: complete because every student is a Bachelor or Master student (so at least "
    "one subclass); overlapping because an exchange student is also a Bachelor or Master student.",
]) + "<br/>Powertype diagram (i):",
      "(i) 1 P powertype class with the per-format attributes and the association, 1 P \": CourseFormat\" label on the "
      "generalization set, 1 P {disjoint, incomplete}. (ii) 1 P per dimension, only with the reason.",
      "L7 slides 16-24; Sheet 7 Q3-Q5", table=powertype_solution())

# ---------------------------------------------------------------- Task 5
s.add(PageBreak())
s.task(5, "Deep modeling", 14)
s.sol("a", 3, bullets([
    "(i) Usually a type only describes or governs its <b>direct</b> instances. Deep characterization means placing "
    "constraints on the properties of the <b>instances of its instances</b> (e.g. CourseFormat wants every concrete "
    "course to have a term). Traditional (two-level) classification cannot express such transitive influences "
    "directly; UML must resort to <b>constraints (OCL), powertypes or stereotypes</b>.",
    "(ii) <b>Linguistic</b> type: <b>Clabject</b> (the LML language element, like every element of the model). "
    "<b>Ontological</b> type: <b>Lecture</b>, on level <b>O2</b> (and, indirectly, a Course).",
]), "(i) 1 P definition, 0.5 P why not, 0.5 P two workarounds. (ii) 0.5 P each type (level included).",
      "L8 slides 5-6, 11, 17")
s.sol("b", 2, bullets([
    "<b>Instance facet</b> (Seminar as an object of CourseFormat): the values maxParticipants = 20, examForm = "
    "'presentation', ects = 4.",
    "<b>Type facet</b> (Seminar as a class of DataSem): the attributes its instances must fill: examForm<super>1</super> "
    ": String, ects<super>1</super> : Integer, plus title<super>1</super> and term<super>1</super> inherited from "
    "Course.",
]), "1 P per facet with correct examples. Listing ects only in one facet: 0.5 (it is in both: value and type).",
      "L8 slides 7-9")
s.sol("c", 6,
      "[a] = <b>2</b>, [b] = <b>1</b>, [c] = <b>1</b>, [d] = <b>0</b>, [e] = <b>1</b>, [f] = <b>0</b>. Reasons in the "
      "table, then the completed diagram (red = filled in).",
      "1 P per blank, only with a reason that names the rule (potency drops by 1 per instantiation, durability, "
      "mutability &lt;= durability, potency 0 = abstract).", "L8 slides 18-21; Sheet 8 Q2-Q3",
      table=[grid([
    ["Blank", "Value", "Reason"],
    ["[a] CourseFormat", "2", "R1: instances (O1) that have instances (O2)"],
    ["[b] maxParticipants", "1", "R2: present one level down only (value at O1, gone at O2)"],
    ["[c] 'written'", "1", "R3: the default may be changed one level down (by the formats), not by courses; "
                           "mutability 1 &lt;= durability 2"],
    ["[d] Course", "0", "R4: abstract = no instances; potency and level are independent"],
    ["[e] ects at Lecture", "1", "declared ects<super>2</super> at O0, minus 1 per instantiation; value 6<super>0</super> "
                                 "cannot change (R5)"],
    ["[f] MDD2026", "0", "R1: concrete courses have no instances; = Lecture's potency 1 minus 1"],
], [35 * mm, 15 * mm, 110 * mm]), deep_model(blanks=False)])
s.sol("d", 3, bullets([
    "(1) <b>No.</b> Durability 1 means the attribute is present only <b>one level</b> below: Lecture and Seminar get "
    "fee<super>0</super> = a value (a class-level value per format); at O2 it is gone.",
    "(2) In Lecture and Seminar the values need mutability 1: examForm<super>1</super> = "
    "'written'<super>1</super> / 'presentation'<super>1</super>. Then at O0 the default needs mutability 2: "
    "'written'<super>2</super>, which is allowed because durability is 2 (mutability &lt;= durability).",
    "(3) <b>No.</b> An instance always has a potency <b>one lower</b> than its type: an instance of "
    "CourseFormat<super>2</super> must have potency 1.",
]), "1 P each, only with the rule.", "L8 slides 18-19; Sheet 8 Q2-Q3")
s.build()
