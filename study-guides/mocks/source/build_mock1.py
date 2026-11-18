"""MDD Mock Exam 1: questions PDF + solutions PDF.

Run:  python build_mock1.py   (needs reportlab; reuses ../../source/guide_lib.py and uml.py)
Output: ../MDD-Mock-1.pdf and ../MDD-Mock-1-Solutions.pdf
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "source")))

from guide_lib import *  # noqa: E402,F401
from guide_lib import ANS_BG  # noqa: E402
import uml  # noqa: E402
from uml import Diagram, draw_text  # noqa: E402
from reportlab.graphics.shapes import Rect, Line, Polygon  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, ".."))
G, H = "«", "»"
RED = colors.HexColor("#B42318")
EXAM = colors.HexColor("#0E6E9C")


# ---------------------------------------------------------------- small helpers
import re


def sup(text):
    """'Genre^3' -> Genre with superscript 3, for paragraph text."""
    return re.sub(r"\^(\d)", r"<super>\1</super>", text)


def sgrid(rows, widths):
    return grid([[sup(str(x)) for x in r] for r in rows], widths)

def box3(dg, key, x, y, name, attrs, ops, w, size=7.5):
    """UML class box with three compartments (name / attributes / operations). (x, y) = top-left."""
    lh = size + 3
    hh = lh + 4
    ah = (lh * len(attrs) + 4) if attrs else 6
    oh = (lh * len(ops) + 4) if ops else 6
    h = hh + ah + oh
    d = dg.d
    d.add(Rect(x, y - h, w, h, fillColor=uml.FILL, strokeColor=uml.INK, strokeWidth=0.8))
    d.add(Line(x, y - hh, x + w, y - hh, strokeColor=uml.INK, strokeWidth=0.6))
    d.add(Line(x, y - hh - ah, x + w, y - hh - ah, strokeColor=uml.INK, strokeWidth=0.6))
    draw_text(d, x + w / 2, y - 3 - lh + 2, name, "Helvetica-Bold", size, uml.INK, anchor="middle")
    for i, t in enumerate(attrs):
        draw_text(d, x + 4, y - hh - lh * (i + 1) + 1, t, "Helvetica", size, uml.INK)
    for i, t in enumerate(ops):
        draw_text(d, x + 4, y - hh - ah - lh * (i + 1) + 1, t, "Helvetica", size, uml.INK)
    dg.boxes[key] = (x, y - h, w, h)


def diamond(dg, x, y, direction):
    """Filled composition diamond with its tip at (x, y), pointing towards direction 'left'|'right'|'up'|'down'."""
    L, W = 10, 4
    dx, dy = {"left": (1, 0), "right": (-1, 0), "up": (0, -1), "down": (0, 1)}[direction]
    px, py = -dy, dx
    pts = [x, y, x + dx * L / 2 + px * W, y + dy * L / 2 + py * W, x + dx * L, y + dy * L,
           x + dx * L / 2 - px * W, y + dy * L / 2 - py * W]
    dg.d.add(Polygon(pts, fillColor=uml.INK, strokeColor=uml.INK, strokeWidth=0.6))


def frame(dg, x, y, w, h, label):
    """Package frame with a tab (top-left at x, y)."""
    tw = uml.text_width(label, "Helvetica-Bold", 7.5) + 12
    dg.d.add(Rect(x, y - 13, tw, 13, fillColor=colors.white, strokeColor=uml.INK, strokeWidth=0.7))
    dg.d.add(Rect(x, y - 13 - h, w, h, fillColor=None, strokeColor=uml.INK, strokeWidth=0.7))
    draw_text(dg.d, x + 6, y - 10, label, "Helvetica-Bold", 7.5, uml.INK)


def bar_gen(dg, children, parent, y):
    """Shared-target generalization: children -> parent with a horizontal bar at height y (children below)."""
    xs = [dg.pt(k, "top")[0] for k in children]
    for k, x in zip(children, xs):
        dg.line([dg.pt(k, "top"), (x, y)])
    px = dg.pt(parent, "bottom")[0]
    dg.line([(min(xs + [px]), y), (max(xs + [px]), y)])
    dg.line([(px, y), dg.pt(parent, "bottom")], head="hollow")


def bar_gen_up(dg, children, parent, y):
    """Shared-target generalization where the parent is to the side at the same level: bar below all boxes."""
    xs = [dg.pt(k, "bottom")[0] for k in children]
    for k, x in zip(children, xs):
        dg.line([dg.pt(k, "bottom"), (x, y)])
    px = dg.pt(parent, "bottom")[0]
    dg.line([(min(xs + [px]), y), (max(xs + [px]), y)])
    dg.line([(px, y), dg.pt(parent, "bottom")], head="hollow")


# ---------------------------------------------------------------- diagrams
def library_diagram():
    dg = Diagram(170 * mm, 250)
    box3(dg, "lib", 10, 240, "Library", ["name : String", "maxLoansPerMember : Integer"],
         ["overdueMembers(today : Integer) : Set(Member)"], w=180)
    box3(dg, "book", 320, 240, "Book", ["title : String", "isbn : String", "year : Integer",
                                         "/availableCopies : Integer"], [], w=150)
    box3(dg, "mem", 10, 150, "Member", ["memberId : Integer", "name : String", "age : Integer"],
         ["borrow(c : Copy) : Loan"], w=118)
    box3(dg, "loan", 188, 150, "Loan", ["start : Integer", "due : Integer", "returned : Boolean", "fee : Real"],
         ["extend(days : Integer)"], w=108)
    box3(dg, "copy", 345, 130, "Copy", ["copyNo : Integer", "damaged : Boolean", "/onLoan : Boolean"], [], w=130)
    box3(dg, "stu", 10, 45, "StudentMember", ["university : String"], [], w=118)
    sz = 6.8
    # Library - Book
    dg.line([(190, 214), (320, 214)])
    dg.text(194, 217, "1", sz); dg.text(194, 205, "library", sz)
    dg.text(312, 217, "*", sz); dg.text(296, 205, "books", sz)
    # Library - Member
    dg.line([(45, dg.pt("lib", "bottom")[1]), (45, 150)])
    dg.text(49, dg.pt("lib", "bottom")[1] - 9, "1  library", sz)
    dg.text(49, 154, "*  members", sz)
    # Book - Copy
    dg.line([(410, dg.pt("book", "bottom")[1]), (410, 130)])
    dg.text(414, dg.pt("book", "bottom")[1] - 9, "1  book", sz)
    dg.text(414, 134, "1..*  copies", sz)
    # Member - Loan
    dg.line([(128, 115), (188, 115)])
    dg.text(131, 118, "1", sz); dg.text(131, 106, "member", sz)
    dg.text(181, 118, "*", sz); dg.text(166, 106, "loans", sz)
    # Loan - Copy
    dg.line([(296, 112), (345, 112)])
    dg.text(299, 115, "*", sz); dg.text(299, 103, "loans", sz)
    dg.text(338, 115, "1", sz); dg.text(326, 103, "copy", sz)
    # StudentMember -> Member
    dg.line([(69, 45), dg.pt("mem", "bottom")], head="hollow")
    return dg.drawing


def kitchen_menu_diagram():
    dg = Diagram(170 * mm, 205)
    sz = 6.8
    frame(dg, 2, 200, 255, 172, "Kitchen (source)")
    box3(dg, "rec", 70, 175, "Recipe", ["name : String", "vegetarian : Boolean"], [], w=110)
    box3(dg, "step", 12, 85, "Step", ["number : Integer", "minutes : Integer", "text : String"], [], w=100)
    box3(dg, "ing", 140, 85, "Ingredient", ["name : String", "grams : Integer"], [], w=105)
    # Recipe <>- Step
    rx, ry = 100, dg.pt("rec", "bottom")[1]
    diamond(dg, rx, ry, "up")
    dg.line([(rx, ry - 10), (rx, 100), (62, 100), (62, 85)])
    dg.text(66, 88, "steps  *", sz)
    # Recipe <>- Ingredient
    rx2 = 150
    diamond(dg, rx2, ry, "up")
    dg.line([(rx2, ry - 10), (rx2, 100), (192, 100), (192, 85)])
    dg.text(196, 88, "ingredients  *", sz)
    dg.text(154, ry - 22, "recipe  1", sz)

    frame(dg, 272, 200, 208, 172, "Menu (target)")
    box3(dg, "dish", 300, 175, "Dish", ["title : String", "totalMinutes : Integer", "speed : String"], [], w=120)
    box3(dg, "comp", 300, 85, "Component", ["name : String", "grams : Integer"], [], w=120)
    dx, dy = 360, dg.pt("dish", "bottom")[1]
    diamond(dg, dx, dy, "up")
    dg.line([(dx, dy - 10), (dx, 85)])
    dg.text(364, 88, "components  *", sz)
    return dg.drawing


def deep_skeleton(solution=False):
    dg = Diagram(170 * mm, 300)
    s = solution
    dg.level(297, "O0")
    dg.box("genre", 170, 285, "Genre^3" if s else "Genre",
           ["shelfColour^1 : String", "loanPeriodDays^2 : Integer"] if s else
           ["shelfColour : String", "loanPeriodDays : Integer"], w=140)
    dg.level(240, "O1")
    dg.box("book", 20, 228, "Book^0" if s else "Book",
           ["title^1 : String", "copyNo^2 : Integer"] if s else ["title : String", "copyNo : Integer"], w=110)
    dg.box("sf", 175, 228, "ScienceFiction^2:Genre" if s else "ScienceFiction:Genre",
           ["shelfColour^0 = 'blue'", "loanPeriodDays^1 = 28^0"] if s else
           ["shelfColour = 'blue'", "loanPeriodDays = 28"], w=145)
    kids = ["sf"]
    if s:
        dg.box("crime", 340, 228, "!Crime^2:Genre", ["!shelfColour^0 = 'red'", "!loanPeriodDays^1 = 14^0"], w=135)
        kids.append("crime")
    bar_gen_up(dg, kids, "book", 178)
    dg.level(168, "O2")
    dg.box("dune", 150, 156, "Dune^1:ScienceFiction" if s else "Dune:ScienceFiction",
           ["title^0 = 'Dune'", "loanPeriodDays^0 = 28", "!copyNo^1 : Integer"] if s else
           ["title = 'Dune'", "loanPeriodDays = 28"], w=145)
    dg.box("tbs", 320, 156, "TheBigSleep^1:Crime" if s else "TheBigSleep:Crime",
           ["title^0 = 'The Big Sleep'", "loanPeriodDays^0 = 14", "!copyNo^1 : Integer"] if s else
           ["title = 'The Big Sleep'", "loanPeriodDays = 14"], w=150)
    dg.level(92, "O3")
    dg.box("d3", 150, 80, "dune3^0:Dune" if s else "dune3:Dune", ["copyNo^0 = 3"] if s else ["copyNo = 3"], w=145)
    if s:
        dg.text(330, 60, "red = added by the solution", 7, RED)
    return dg.drawing


def profile_solution():
    dg = Diagram(170 * mm, 150)
    frame(dg, 2, 145, 300, 125, G + "profile" + H + " Persistence")
    dg.box("pers", 15, 115, [G + "stereotype" + H, "Persistent"], ["tableName : String", "cached : Boolean"], w=110)
    dg.box("cls", 190, 115, [G + "metaclass" + H, "Class"], w=95)
    dg.line([dg.pt("pers", "right", 0.6), (190, dg.pt("pers", "right", 0.6)[1])], head="filled")
    dg.box("rem", 15, 45, [G + "stereotype" + H, "Remote"], w=110)
    dg.box("itf", 190, 45, [G + "metaclass" + H, "Interface"], w=95)
    yy = dg.pt("rem", "right")[1]
    dg.line([dg.pt("rem", "right"), (190, yy)], head="filled")
    dg.text(135, yy + 4, "{required}", 7, RED, "Helvetica-Bold")
    dg.text(320, 135, "(b) applied:", 7.5, uml.INK, "Helvetica-Bold")
    dg.box("loan", 320, 120, [G + "Persistent" + H, "Loan"], w=80)
    dg.note("n", 320, 70, [G + "Persistent" + H, "tableName = 'LOANS'", "cached = false"])
    dg.line([dg.pt("loan", "bottom"), (360, 70)], dashed=True)
    return dg.drawing


def powertype_solution():
    dg = Diagram(170 * mm, 160)
    dg.box("book", 60, 150, "Book", ["title : String", "isbn : String"], w=110)
    dg.box("genre", 320, 150, "Genre", ["shelfColour : String", "loanPeriodDays : Integer"], w=140)
    y = dg.pt("book", "right")[1]
    dg.line([dg.pt("book", "right"), (320, y)])
    dg.text(174, y + 3, "*", 6.8); dg.text(174, y - 9, "books", 6.8)
    dg.text(312, y + 3, "1", 6.8); dg.text(292, y - 9, "genre", 6.8)
    dg.box("sf", 10, 55, "ScienceFiction", ["techLevel : Integer"], w=100)
    dg.box("cr", 140, 55, "Crime", ["detective : String"], w=100)
    bar_gen(dg, ["sf", "cr"], "book", 85)
    dg.text(200, 89, ": Genre      {disjoint, incomplete}", 7.2, uml.INK, "Helvetica-Bold")
    return dg.drawing


# ---------------------------------------------------------------- layout primitives
def subq(label, text, pts):
    t = Table([[Paragraph(f"<b>{label}</b>&nbsp; {text}", S["a"]),
                Paragraph(f'<font color="#0E6E9C"><b>({pts} pt)</b></font>', S["a"])]],
              colWidths=[150 * mm, 20 * mm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def task(title, pts):
    return Paragraph(f"{title} <font color='#0E6E9C'>({pts} points)</font>", S["h1"])


def solbox(label, pts, answer, grading, src):
    head = Paragraph(f"<b>{label}</b> <font color='#0E6E9C'>({pts} pt)</font>", S["q"])
    body = answer
    if grading:
        body += f'<br/><font color="#B54708"><b>Grading:</b></font> {grading}'
    body += f'<br/><font size="8" color="#5A6270">Source: {src}</font>'
    box = Table([[Paragraph(body, S["a"])]], colWidths=[CW])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ANS_BG), ("LINEBEFORE", (0, 0), (0, -1), 2.5, TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return KeepTogether([head, Spacer(1, 3), box, Spacer(1, 9)])


POINTS = [("1", "Foundations: models, MDA, metamodeling levels", "L1, L6", 10),
          ("2", "OCL on a library model", "L2, L3, L4; Sheets 1-4", 35),
          ("3", "ATL transformation Kitchen2Menu", "L5; Sheets 5-6", 15),
          ("4", "Profiles, generalization sets, powertypes", "L7; Sheet 7", 15),
          ("5", "Deep modeling", "L8; Sheet 8", 15)]


def points_table():
    rows = [["Task", "Topic", "Lectures / sheets", "Points"]]
    rows += [[a, b, c_, str(d)] for a, b, c_, d in POINTS]
    rows += [["", "<b>Total</b>", "", "<b>90</b>"]]
    return grid(rows, [14 * mm, 90 * mm, 46 * mm, 20 * mm])


# ================================================================ QUESTIONS
q = Guide("x.pdf", "MDD - Mock Exam 1 - Questions", "MDD Mock Exam 1")
q.out = os.path.join(OUT, "MDD-Mock-1.pdf")
q.p("MDD Mock Exam 1", "title")
q.p("Model-Driven Development, University of Mannheim, HWS 2026. Practice exam built from Lectures 1-8 and "
    "Exercise Sheets 1-8.", "sub")
q.add(Spacer(1, 8))
q.p("Instructions", "h1")
q.p(bullets([
    "<b>Time: 90 minutes. Total: 90 points</b> (about one point per minute). Closed book; write by hand on paper.",
    "The real exam format has not been announced yet, so this mock mixes short theory questions with writing OCL, "
    "ATL and diagrams, the style of the exercise sheets (Sheet 6 even gives exam-style points).",
    "OCL: always write the <b>context</b> line, use role names from the diagram, single quotes for strings, "
    "<font face='Courier'>.</font> for attributes/navigation and <font face='Courier'>-&gt;</font> for collection "
    "operations.",
    "ATL: write complete modules, rules and helpers in the syntax from Lecture 5.",
    "Diagrams: draw them neatly; label stereotypes, potencies, multiplicities and role names.",
    "Do the whole mock timed before you open the solutions file.",
]))
q.add(Spacer(1, 6), points_table())

# ---- Task 1
q.add(PageBreak(), task("Task 1: Foundations", 10))
q.add(subq("(a)", "Give Stachowiak's definition of a model and name and explain its <b>three aspects</b>. Illustrate "
               "each aspect with a class diagram of a library lending system.", 3))
q.add(subq("(b)", "Three models of the same library lending system are described below. Classify each as "
               "<b>CIM, PIM or PSM</b> and justify each answer in one sentence.<br/>"
               "(i) Boxes Member, Book and Loan with associations and a note \"Members borrow books at the counter; "
               "late returns cost a fee.\" No attribute types, no operations.<br/>"
               "(ii) Classes Member, Copy and Loan with typed attributes and the operations "
               + c("borrow(c : Copy) : Loan") + " and " + c("extend(days : Integer)") + "; no technology is "
               "mentioned.<br/>"
               "(iii) A class " + c(G + "JavaBean" + H + " LoanBean") + " with an attribute of type "
               + c("java.util.ArrayList") + " and a class " + c(G + "WebService" + H + " LendingService") + ".", 3))
q.add(subq("(c)", "Assign each element to its level <b>M3, M2, M1 or M0</b> of the OMG architecture: "
               "(1) MOF, (2) the UML metaclass Class, (3) the class Member of the library model, "
               "(4) the attribute declaration " + c("age : Integer") + " of class Member, "
               "(5) the member Ann who is registered in the running system, (6) Ecore, "
               "(7) the ATL metamodel, (8) the transformation file " + c("Library2Catalog.atl") + ".", 4))

# ---- Task 2
q.add(PageBreak(), task("Task 2: OCL on a library model", 35))
q.p("All OCL in this task refers to the class diagram below. A library has members and books; every book has one or "
    "more physical copies. A loan links one member with one copy. Days are counted as integers (day numbers). "
    "Derived attributes are marked with /.")
q.add(library_diagram(), Spacer(1, 6))
q.p("Role names: " + c("Library.members, Member.library, Library.books, Book.library, Book.copies, Copy.book, "
                       "Member.loans, Loan.member, Loan.copy, Copy.loans") + ".", "small")
q.add(Spacer(1, 4))
q.add(subq("(a)", "Explain the idea of <b>Design by Contract</b> using the operation " + c("Member::borrow") +
               ": whose rights and whose obligations do its pre- and postconditions specify? If "
               + c("borrow") + " is called for a damaged copy and the precondition requires an undamaged copy, "
               "who has broken the contract?", 2))
q.add(subq("(b)", "Write an invariant: within a library, no two members have the same " + c("memberId") + ".", 2))
q.add(subq("(c)", "Write an invariant: a member never has more open (not yet returned) loans than the "
               + c("maxLoansPerMember") + " of the member's library.", 3))
q.add(subq("(d)", "Write initial values: a new loan is not returned and its fee is 0.", 2))
q.add(subq("(e)", "Define the derived attribute " + c("onLoan") + " of Copy: a copy is on loan if it has a loan "
               "that has not been returned.", 3))
q.add(subq("(f)", "Define the derived attribute " + c("availableCopies") + " of Book: the number of its copies that "
               "are neither damaged nor on loan.", 3))
q.add(subq("(g)", "Use OCL to add an <b>operation</b> " + c("borrowedTitles()") + " to Member that returns the titles "
               "of all books the member has ever borrowed, each title only once.", 3))
q.add(subq("(h)", "Specify the result of the query operation " + c("Library::overdueMembers(today : Integer)")
               + ": all members of the library who have at least one loan that is not returned and whose due day "
                 "is before " + c("today") + ".", 3))
q.add(subq("(i)", "Write the pre- and postconditions of " + c("Member::borrow(c : Copy) : Loan") + ". A member may "
               "borrow a copy only if the copy is neither damaged nor on loan, the member has fewer open loans than "
               "the library's limit, and the copy belongs to a book of the member's own library. Afterwards a "
               "<b>new</b> loan exists that is returned by the operation, links this member with " + c("c") +
               ", is not returned, and the member has exactly this one loan more than before.", 5))
k_rows = [["Loan", "copy", "book of the copy", "returned", "due"],
          ["L1", "c1", "Dune", "true", "10"], ["L2", "c2", "Dune", "false", "20"],
          ["L3", "c5", "Emma", "false", "30"]]
q.add(KeepTogether([
    subq("(j)", "Ann is a " + c("StudentMember") + " (age 22) with exactly the three loans below. Evaluate each "
                "expression in " + c("context Member") + " with " + c("self") + " = Ann. " + c("u") + " is an "
                "undefined Boolean expression.", 5),
    Spacer(1, 3), grid(k_rows, [20 * mm, 20 * mm, 40 * mm, 25 * mm, 20 * mm]), Spacer(1, 4),
    code_block("(1) loans.copy.book.title\n"
               "(2) loans.copy.book->asSet()->size()\n"
               "(3) loans->select(not returned).due->sum()\n"
               "(4) self.oclIsTypeOf(Member)      and separately      self.oclIsKindOf(Member)\n"
               "(5) age >= 18 or u                and separately      age >= 18 and u")]))
q.add(Spacer(1, 4))
q.add(KeepTogether([
    subq("(k)", "Each constraint below is wrong. Say what is wrong and give a corrected version.", 4),
    Spacer(1, 3),
    code_block("-- (1) intended: a damaged copy is never on loan\n"
               "context Book\n"
               "inv: copies.damaged = true implies copies.onLoan = false\n\n"
               "-- (2) intended: extend moves the due day back by the given number of days\n"
               "context Loan::extend(days : Integer)\n"
               "post: due = due + days")]))

# ---- Task 3
q.add(PageBreak(), task("Task 3: ATL transformation", 15))
q.p("The source metamodel <b>Kitchen</b> describes recipes; the target metamodel <b>Menu</b> describes dishes on a "
    "restaurant menu. Black diamonds are compositions. An Ingredient belongs to exactly one recipe "
    "(reference " + c("recipe") + ").")
q.add(kitchen_menu_diagram(), Spacer(1, 6))
q.p("Write a transformation <b>Kitchen2Menu</b>. Only <b>vegetarian</b> recipes become dishes. A dish gets the "
    "recipe's name as title, the sum of the minutes of all steps as " + c("totalMinutes") + ", " + c("speed") +
    " = 'quick' if it takes at most 30 minutes and 'slow' otherwise, and one Component (same name and grams) "
    "for every ingredient of the recipe. Steps produce no target elements.")
q.add(subq("(a)", "Write the header of the module.", 2))
q.add(subq("(b)", "Write a helper " + c("totalMinutes()") + " on Recipe that computes the total minutes of its steps. "
               "Use <b>iterate</b>.", 3))
q.add(subq("(c)", "Write the matched rule " + c("Recipe2Dish") + ".", 4))
q.add(subq("(d)", "Write the matched rule " + c("Ingredient2Component") + ". Make sure no Component is created "
               "that does not belong to a dish.", 2))
q.add(subq("(e)", "(1) In " + c("Recipe2Dish") + " you can bind " + c("components") + " to the recipe's "
               "<i>source</i> ingredients. Why does the target model still contain Components, not Ingredients? "
               "(2) Suppose the Kitchen metamodel is changed so that several recipes may share the same Ingredient "
               "element, but every Dish must still get its own Component objects. Which kind of rule do you use "
               "for ingredients, how is it invoked, and why would a standard rule or a unique lazy rule not work?",
          4))

# ---- Task 4
q.add(PageBreak(), task("Task 4: Profiles, generalization sets and powertypes", 15))
q.add(subq("(a)", "Draw a profile <b>Persistence</b> with two stereotypes: " + c("Persistent") + " extends the "
               "metaclass Class and has the tags " + c("tableName : String") + " and " + c("cached : Boolean") +
               "; " + c("Remote") + " extends the metaclass Interface, and <b>every</b> interface must carry it.", 3))
q.add(subq("(b)", "Draw the class Loan stereotyped with " + c("Persistent") + ", with table name 'LOANS' and "
               "cached false.", 2))
q.add(subq("(c)", "What exactly does the constraint on the Remote extension in (a) mean for a model? Why is a "
               "profile called a <i>lightweight</i> extension, compared with the metamodeling approach?", 2))
gs_rows = [["#", "General class", "Generalization set (subclasses)"],
           ["1", "Vehicle", "Car, Bicycle, Truck"],
           ["2", "Loan", "OpenLoan, ReturnedLoan"],
           ["3", "Person", "Author, Reader"],
           ["4", "LibraryUser", "Member, Staff (staff can also register as members)"]]
q.add(KeepTogether([
    subq("(d)", "For each generalization set state whether it is complete or incomplete and disjoint or "
                "overlapping, with a one-sentence justification. State your assumption where the domain is "
                "ambiguous.", 4),
    Spacer(1, 3), grid(gs_rows, [10 * mm, 40 * mm, 120 * mm])]))
q.add(Spacer(1, 4))
q.add(subq("(e)", "Every book of the library belongs to exactly one <b>Genre</b>, e.g. ScienceFiction or Crime. A "
               "genre has a shelf colour and a loan period in days that apply to all of its books. Every book has a "
               "title and an ISBN. ScienceFiction and Crime are also subclasses of Book with their own features "
               "(ScienceFiction: " + c("techLevel : Integer") + "; Crime: " + c("detective : String") + "). "
               "Draw a UML class diagram that models Genre as a <b>powertype</b>, including the "
               "generalization-set constraints you choose, and explain in one sentence why Genre is a powertype.",
          4))

# ---- Task 5
q.add(PageBreak(), task("Task 5: Deep modeling", 15))
q.add(subq("(a)", "What is a <b>clabject</b>? Explain its two facets using an element of the model in (c).", 2))
q.add(subq("(b)", "State the classic definition of <b>strict metamodeling</b>. Then explain why Genre, "
               "ScienceFiction and Dune (a book of genre ScienceFiction) cannot be placed cleanly in the UML "
               "M0-M3 architecture.", 3))
q.p("The deep model below has the most abstract level at the top (O0) and physical book copies at O3. Potencies "
    "are missing.")
q.add(deep_skeleton(False), Spacer(1, 4))
q.add(subq("(c)", "Complete the model by adding all clabject potencies, attribute durabilities and, where needed, "
               "value mutabilities, so that: (1) Book is abstract; (2) every genre has its own shelf colour, but "
               "books and copies have none; (3) the loan period is set per genre, every book of the genre has that "
               "loan period and cannot change it, and copies have no loan period; (4) every book has a title, but "
               "copies do not; (5) every copy has a copy number. (6) TheBigSleep is typed by the genre Crime, "
               "which is missing: add it (shelf colour 'red', loan period 14).", 6))
q.add(subq("(d)", "Valid or invalid? Justify briefly. (1) " + sup("Thriller^2 : Genre^3") + "; "
               "(2) " + sup("dune7^1 : Dune^1") + "; (3) an attribute " + sup("fee^1 : Real = 2^2") + "; "
               "(4) " + sup("Book^0") + " on level O1 with subclasses ScienceFiction and Crime. (Superscripts are "
               "potencies.)", 2))
q.add(subq("(e)", "Give two advantages of the deep model in (c) over the UML powertype model of Task 4(e).", 2))
q.p("<i>End of the exam.</i>", "small")
q.build()

# ================================================================ SOLUTIONS
s = Guide("x.pdf", "MDD - Mock Exam 1 - Solutions", "MDD Mock Exam 1 - Solutions")
s.out = os.path.join(OUT, "MDD-Mock-1-Solutions.pdf")
s.p("MDD Mock Exam 1: Solutions", "title")
s.p("Model answers, grading notes and the slide or exercise source for every sub-task. Mark your own attempt "
    "strictly: a missing context line or a wrong arrow costs points in a real exam too.", "sub")
s.add(Spacer(1, 8), points_table(), Spacer(1, 6))
s.p("How to use this", "h1")
s.p(bullets([
    "Mark every sub-task with the grading note, then add up your points. 45 of 90 is a reasonable pass target.",
    "For each lost point write the topic on your error list and redo that question type from the study guide "
    "of the lecture named in the source line.",
    "Where several OCL/ATL versions are given, all of them earn full marks.",
]))

# ---- Task 1
s.add(PageBreak(), task("Task 1: Foundations", 10))
s.add(solbox("1(a)", 3,
    "\"A formal representation of entities and relationships in the real world (abstraction) with a certain "
    "correspondence (homomorphism) for a certain purpose (pragmatics).\"<br/>"
    "&bull; <b>Reduction (abstraction):</b> a model does not contain all attributes of the original; details "
    "irrelevant to the purpose are left out. <i>Library:</i> the class diagram has no cover colour or shelf "
    "dust.<br/>"
    "&bull; <b>Projection (homomorphism):</b> every model element represents something real, and statements about "
    "the model must hold for the original. <i>Library:</i> every Loan object corresponds to a real loan; if the "
    "model says a loan has one copy, a real loan is of one copy.<br/>"
    "&bull; <b>Pragmatics (purpose):</b> the model can replace the original for specific questions only. "
    "<i>Library:</i> built to implement lending, it answers \"who has which copy\", not \"where is the fire exit\".",
    "1 pt per aspect: correct name plus meaning. The example is needed for the full point.",
    "L1 slide 9 (Stachowiak)"))
s.add(solbox("1(b)", 3,
    "(i) <b>CIM</b>: describes the environment and the domain in the domain's own terms; the system's structure "
    "and processing are not decided yet.<br/>"
    "(ii) <b>PIM</b>: defines how the system works (typed attributes, operations) but nothing about a platform; "
    "it would stay the same on Java, .NET, ...<br/>"
    "(iii) <b>PSM</b>: adds platform details: platform stereotypes from a profile (" + c(G + "JavaBean" + H) + ", "
    + c(G + "WebService" + H) + ") and Java library types.",
    "0.5 pt label + 0.5 pt justification each.",
    "Sheet 1 Q2 (sample solution); L6 slide 3 (three viewpoints); L7 slides 3-10 (profiles in the PSM)"))
s.add(solbox("1(c)", 4,
    "See the table below.", "0.5 pt per element.",
    "L6 slide 12 and Q15 of the L6 guide; L8 slide 2; L5 slides 5, 17"))
s.add(grid([["Element", "Level", "Why"],
            ["(1) MOF", "M3", "meta-metamodel: the language for defining metamodels"],
            ["(2) UML metaclass Class", "M2", "part of the UML metamodel"],
            ["(3) class Member", "M1", "element of a user model"],
            ["(4) " + c("age : Integer") + " in Member", "M1", "also part of the model (an instance of the "
                                                                  "metaclass Attribute)"],
            ["(5) Ann at runtime", "M0", "user object, an instance of Member"],
            ["(6) Ecore", "M3", "EMF's counterpart of MOF; conforms to itself"],
            ["(7) ATL metamodel", "M2", "the language in which transformations are written"],
            ["(8) " + c("Library2Catalog.atl"), "M1", "a transformation is itself a model that conforms to the ATL "
                                                        "metamodel (L5 slide 17)"]],
           [48 * mm, 15 * mm, 107 * mm]), Spacer(1, 10))

# ---- Task 2
s.add(PageBreak(), task("Task 2: OCL on a library model", 35))
s.add(solbox("2(a)", 2,
    "Design by Contract comes from a legal contract: both parties accept obligations and gain rights. For "
    + c("borrow") + ": the <b>precondition</b> specifies the <b>rights</b> of the object offering the service (it "
    "only has to work if the copy is fine, the limit is not reached, ...), which are the caller's obligations. The "
    "<b>postcondition</b> specifies the provider's <b>obligations</b> (a new loan exists ...), which are the "
    "caller's rights. Calling " + c("borrow") + " with a damaged copy violates the precondition, so the "
    "<b>caller</b> broke the contract; the member object owes nothing. (Invariants must hold whenever no "
    "operation is executing; during " + c("borrow") + " they may be violated temporarily.)",
    "1 pt pre = rights / post = obligations of the provider; 1 pt caller is at fault.",
    "L2 slides 4-8; Sheet 1 Q1"))
s.add(solbox("2(b)", 2,
    ocl("context Library\ninv uniqueIds: members->isUnique(memberId)") + "<br/>Equivalent:<br/>" +
    ocl("context Library\ninv: members->forAll(m1, m2 | m1 <> m2 implies m1.memberId <> m2.memberId)"),
    "1 pt context + navigation " + c("members") + ", 1 pt isUnique / forAll. " + c("Member::allInstances()") +
    " gives only 1 pt (it is unique over all libraries, not within one).",
    "L2 slide 18 (isUnique); L3 slides 29, 42; Sheet 1 Q3(a)"))
s.add(solbox("2(c)", 3,
    ocl("context Member\ninv maxOpen:\n  loans->select(l | not l.returned)->size() <= library.maxLoansPerMember") +
    "<br/>Also fine: " + c("loans->reject(returned)->size()") + ". " + c("library") + " has multiplicity 1, so "
    + c("library.maxLoansPerMember") + " is a single Integer.",
    "1 pt context, 1 pt select/reject of open loans, 1 pt size compared with the limit.",
    "L3 slides 39-40; Sheet 2 Q2(b)-(c)"))
s.add(solbox("2(d)", 2,
    ocl("context Loan::returned : Boolean\ninit: false\n\ncontext Loan::fee : Real\ninit: 0"),
    "1 pt each. The context of an init is the attribute (Class::attribute), not the class. "
    + c("derive") + " instead of " + c("init") + " is wrong: the value may change later.",
    "L3 slide 18; Sheet 3 Q1(b), Q2(c)"))
s.add(solbox("2(e)", 3,
    ocl("context Copy::onLoan : Boolean\nderive: loans->exists(l | not l.returned)") +
    "<br/>Also fine: " + c("loans->select(not returned)->notEmpty()") + " or " +
    c("loans->select(not returned)->size() > 0") + ".",
    "1 pt context Copy::onLoan with derive, 1 pt navigation " + c("loans") + ", 1 pt exists/select on not "
    "returned. " + c("loans.returned = false") + " gets 0 for the last point (Bag compared with Boolean).",
    "L3 slides 18, 43; Sheet 2 Q2(a)"))
s.add(solbox("2(f)", 3,
    ocl("context Book::availableCopies : Integer\n"
        "derive: copies->select(c | not c.damaged and not c.onLoan)->size()") +
    "<br/>Also fine: " + c("copies->reject(c | c.damaged or c.onLoan)->size()") + " (De Morgan).",
    "1 pt context/derive, 1 pt correct condition (and of both negations), 1 pt ->size().",
    "L3 slides 39-40, 43 (De Morgan); Sheet 2 Q2(c)"))
s.add(solbox("2(g)", 3,
    ocl("context Member\ndef: borrowedTitles() : Set(String) =\n  loans.copy.book.title->asSet()") +
    "<br/>" + c("loans.copy.book.title") + " navigates over several associations, so it is a <b>Bag</b> (a title "
    "borrowed twice appears twice); " + c("asSet()") + " removes the duplicates. Equivalent: "
    + c("loans->collect(l | l.copy.book.title)->asSet()") + ".",
    "1 pt def with parentheses and return type Set(String) (it is an operation), 1 pt navigation, 1 pt asSet().",
    "L3 slides 20, 41; L2 (Set vs Bag rule); Sheet 2 Q2(d), Sheet 3 Q1(d)"))
s.add(solbox("2(h)", 3,
    ocl("context Library::overdueMembers(today : Integer) : Set(Member)\n"
        "body: members->select(m | m.loans->exists(l | not l.returned and l.due < today))") +
    "<br/>" + c("post: result = members->select(...)") + " is also accepted (L3 slide 23 style).",
    "1 pt body with the operation as context, 1 pt select over members, 1 pt nested exists with both "
    "conditions.",
    "L3 slide 19 (body); L4 Sheet 4 Q1(c) (select inside select)"))
s.add(solbox("2(i)", 5,
    ocl("context Member::borrow(c : Copy) : Loan\n"
        "pre : not c.damaged and not c.onLoan\n"
        "pre : loans->select(not returned)->size() < library.maxLoansPerMember\n"
        "pre : c.book.library = self.library\n"
        "post: result.oclIsNew()\n"
        "post: result.member = self and result.copy = c and not result.returned\n"
        "post: loans = loans@pre->including(result)") +
    "<br/>Instead of the last line, " + c("loans->size() = loans@pre->size() + 1 and loans->includes(result)") +
    " is fine. Note the strict " + c("<") + " in the second precondition: after the loan is added the "
    "invariant of (c) still holds.",
    "2 pt preconditions (copy state, limit with &lt;, same library; -0.5 per missing condition). 3 pt "
    "postconditions: oclIsNew (1), links/values via result (1), @pre comparison (1).",
    "L3 slides 22 (@pre), 23 (result), 30 (oclIsNew); Sheet 1 Q3(d)-(e); Sheet 3 Q1(e)"))
s.add(solbox("2(j)", 5,
    "(1) " + c("Bag{'Dune', 'Dune', 'Emma'}") + " (order irrelevant; a Set is wrong).<br/>"
    "(2) <b>2</b>: the books are Dune, Dune, Emma; asSet keeps Dune and Emma.<br/>"
    "(3) <b>50</b>: the open loans are L2 and L3, due 20 + 30.<br/>"
    "(4) " + c("oclIsTypeOf(Member)") + " = <b>false</b> (exact type is StudentMember); "
    + c("oclIsKindOf(Member)") + " = <b>true</b> (StudentMember is a subtype).<br/>"
    "(5) " + c("age >= 18 or u") + " = <b>true</b> (true or undefined is true); " + c("age >= 18 and u") +
    " = <b>undefined</b> (only false and undefined is false).",
    "1 pt per line; in (4) and (5) both values are needed for the point.",
    "L2 navigation rule; L3 slides 27 (oclIsKindOf/TypeOf), 28 (undefined), 41 (collect gives Bag); "
    "Sheet 3 Q2(e)"))
s.add(solbox("2(k)", 4,
    "(1) " + c("copies.damaged") + " is a Bag of Booleans (one per copy) and cannot be compared with "
    + c("true") + "; the same for " + c("copies.onLoan") + ". It also loses the link between one copy's two "
    "values. Correct:<br/>" +
    ocl("context Book\ninv: copies->forAll(c | c.damaged implies not c.onLoan)") +
    "<br/>or simply " + c("context Copy inv: damaged implies not onLoan") + ".<br/>"
    "(2) In a postcondition " + c("due") + " means the value <i>after</i> the operation, so " +
    c("due = due + days") + " is only true for " + c("days = 0") + ". The old value needs @pre:<br/>" +
    ocl("context Loan::extend(days : Integer)\npost: due = due@pre + days"),
    "1 pt diagnosis + 1 pt correction each.",
    "L3 slides 22, 41-42; L3 guide Q43(e); Sheet 2 Q3(b) (the same Bag mistake is in its sample solution)"))

# ---- Task 3
s.add(PageBreak(), task("Task 3: ATL transformation", 15))
s.p("Complete module (the parts are graded separately below):")
s.add(code_block(
    "module Kitchen2Menu;\n"
    "create OUT : Menu from IN : Kitchen;\n\n"
    "helper context Kitchen!Recipe def: totalMinutes() : Integer =\n"
    "  self.steps->iterate(s; acc : Integer = 0 | acc + s.minutes);\n\n"
    "rule Recipe2Dish {\n"
    "  from\n"
    "    r : Kitchen!Recipe (r.vegetarian)\n"
    "  to\n"
    "    d : Menu!Dish (\n"
    "      title <- r.name,\n"
    "      totalMinutes <- r.totalMinutes(),\n"
    "      speed <- if r.totalMinutes() <= 30 then 'quick' else 'slow' endif,\n"
    "      components <- r.ingredients\n"
    "    )\n"
    "}\n\n"
    "rule Ingredient2Component {\n"
    "  from\n"
    "    i : Kitchen!Ingredient (i.recipe.vegetarian)\n"
    "  to\n"
    "    c : Menu!Component (\n"
    "      name <- i.name,\n"
    "      grams <- i.grams\n"
    "    )\n"
    "}"), Spacer(1, 8))
s.add(solbox("3(a)", 2,
    ocl("module Kitchen2Menu;\ncreate OUT : Menu from IN : Kitchen;"),
    "1 pt module line, 1 pt create line with OUT/target and IN/source the right way round.",
    "L5 slide 19; Sheet 6 Q1(a)"))
s.add(solbox("3(b)", 3,
    ocl("helper context Kitchen!Recipe def: totalMinutes() : Integer =\n"
        "  self.steps->iterate(s; acc : Integer = 0 | acc + s.minutes);") +
    "<br/>Also accepted (iterate over the collected values, as in the Sheet 5 solution): "
    + c("self.steps->collect(s | s.minutes)->iterate(m; acc : Integer = 0 | acc + m)") + ". Without iterate ("
    + c("self.steps.minutes->sum()") + ") at most 2 pt.",
    "1 pt helper header (context with metamodel!Class, def, return type, ;), 2 pt correct iterate "
    "(accumulator type and start value 0, update).",
    "L5 slides 10, 20; L3 slides 44-45 (iterate); Sheet 5 Q1"))
s.add(solbox("3(c)", 4,
    "See the module above. Points: source pattern with guard " + c("(r.vegetarian)") + " (1); " +
    c("title") + " and " + c("totalMinutes") + " bindings (1); " + c("speed") + " with if-then-else-endif (1); "
    + c("components <- r.ingredients") + " (1).",
    "Bindings use " + c("<-") + " and are separated by commas; a missing guard costs the first point.",
    "L5 slides 11-12, 22; Sheet 6 Q1(b)"))
s.add(solbox("3(d)", 2,
    ocl("rule Ingredient2Component {\n  from\n    i : Kitchen!Ingredient (i.recipe.vegetarian)\n  to\n"
        "    c : Menu!Component (\n      name <- i.name,\n      grams <- i.grams\n    )\n}") +
    "<br/>The guard is needed because a standard rule fires for <b>every</b> match: without it, the ingredients "
    "of non-vegetarian recipes would become Components that no Dish refers to.",
    "1 pt rule with bindings, 1 pt guard " + c("i.recipe.vegetarian") + ".",
    "L5 slides 9, 11"))
s.add(solbox("3(e)", 4,
    "(1) <b>Traceability / automatic resolution.</b> Matched rules record which target element was created for "
    "which source element. When a binding assigns source elements (" + c("r.ingredients") + ") to a target "
    "reference, ATL replaces them with the target elements created for them by a matched rule, here the "
    "Components from " + c("Ingredient2Component") + ". (We could not navigate to the Components ourselves: target "
    "models are write-only.)<br/>"
    "(2) A <b>lazy rule</b>, called explicitly from the dish rule:<br/>" +
    ocl("components <- r.ingredients->collect(i | thisModule.Ingredient2Component(i))") +
    "<br/>A lazy rule creates new target elements <b>each time</b> it is called, so a shared ingredient gives a "
    "separate Component in every dish. A standard rule fires only once per match (one Component, shared by all "
    "dishes); a unique lazy rule is also applied at most once per match and returns the same Component on every "
    "call. (With the lazy rule the guard of (d) disappears: it is only called for vegetarian recipes.)",
    "(1) 2 pt: traceability/resolution + the rule for Ingredient is what makes it work. "
    "(2) 1 pt lazy rule with thisModule call, 1 pt why not standard / unique lazy.",
    "L5 slides 7, 9, 13; Sheet 5 Q2 (lazy rules, thisModule)"))

# ---- Task 4
s.add(PageBreak(), task("Task 4: Profiles, generalization sets and powertypes", 15))
s.p("Model answer for (a) and (b):")
s.add(profile_solution(), Spacer(1, 6))
s.add(solbox("4(a)", 3,
    "Profile package " + c(G + "profile" + H + " Persistence") + " with two " + c(G + "stereotype" + H) +
    " boxes. Persistent lists its tags (tag definitions) " + c("tableName : String") + " and "
    + c("cached : Boolean") + " as attributes. Each stereotype is connected to its " + c(G + "metaclass" + H) +
    " box by an <b>extension</b>: a solid line with a <b>filled</b> arrowhead at the metaclass (not a hollow "
    "generalization triangle). The Remote extension carries " + c("{required}") + ".",
    "1 pt stereotypes with tags, 1 pt extensions with filled arrowheads to the right metaclasses, 1 pt "
    "{required} on Remote (and the profile package).",
    "L7 slides 3-7, 11 (EJB profile: {required}); Sheet 7 Q1"))
s.add(solbox("4(b)", 2,
    "Class box " + c(G + "Persistent" + H + " Loan") + " and a note attached with a dashed line: "
    + c(G + "Persistent" + H + " tableName = 'LOANS', cached = false") + ". Alternative (storage view, slide "
    "10): Loan linked to an instance " + c(":Persistent") + " holding the two values.",
    "1 pt stereotype on the class, 1 pt tagged values in a note grouped under the stereotype.",
    "L7 slides 9-10; Sheet 7 Q2"))
s.add(solbox("4(c)", 2,
    "<b>{required}</b>: every instance of the metaclass Interface in a model that applies the profile must carry "
    "the stereotype Remote; there can be no interface without it (an optional extension could be applied or "
    "removed at will).<br/><b>Lightweight</b>: a profile only extends existing metaclasses logically through "
    "stereotypes; it cannot change the metamodel, so any UML tool that supports profiles can use it. The "
    "heavyweight metamodeling approach adds a real new metaclass (e.g. a subclass of Class) and so changes the "
    "language.",
    "1 pt each.", "L7 slides 3-7"))
s.add(solbox("4(d)", 4,
    "See the table below.",
    "0.5 pt per dimension, but only with a reason (state the assumption in 2 and 4).",
    "L7 slides 16-20; Sheet 7 Q4-Q5"))
s.add(grid([["#", "Answer", "Justification"],
            ["1", "incomplete, disjoint", "other vehicles exist (motorbike, bus); a vehicle is not both a car and "
                                         "a truck"],
            ["2", "complete, disjoint", "at any moment a loan is either open or returned, never both and never "
                                       "neither (if loans can be cancelled: incomplete)"],
            ["3", "incomplete, overlapping", "most persons are neither authors nor readers in the model; an author "
                                            "can also be a reader"],
            ["4", "complete, overlapping", "assuming only members and staff use the library; a staff member may "
                                          "also be a member"]],
           [8 * mm, 40 * mm, 122 * mm]), Spacer(1, 10))
s.p("Model answer for (e):")
s.add(powertype_solution(), Spacer(1, 6))
s.add(solbox("4(e)", 4,
    "Genre is a <b>powertype</b> of Book because its instances (ScienceFiction, Crime, ...) are subclasses of "
    "Book: ScienceFiction is at the same time an object of Genre (with shelfColour and loanPeriodDays stored "
    "once for the whole genre) and a class of books (with its own feature techLevel). Constraints "
    + c("{disjoint, incomplete}") + ": a book has exactly one genre, and more genres exist than the two modelled.",
    "1 pt Book and Genre with the attributes in the right class (genre data in Genre, not in Book); 1 pt "
    "association Book * - 1 Genre; 1 pt generalization set labelled " + c(": Genre") + " with constraints; "
    "1 pt explanation (instances of Genre are subclasses of Book).",
    "L7 slides 21-24 (Tree Species, Account Type, Vehicle Type)"))

# ---- Task 5
s.add(PageBreak(), task("Task 5: Deep modeling", 15))
s.add(solbox("5(a)", 2,
    "A <b>clabject</b> (class + object) is a model element that is a class and an object at the same time. "
    "Its <b>instance facet</b> holds values for the attributes declared by its type; its <b>type facet</b> "
    "declares attributes that its own instances must fill. Example: ScienceFiction is an instance of Genre "
    "(shelfColour = 'blue', loanPeriodDays = 28) and a type of Dune (it passes on title and copyNo).",
    "1 pt definition with both facets, 1 pt correct example.", "L8 slides 7-8"))
s.add(solbox("5(b)", 3,
    "\"In an n-level modeling architecture M0, M1 ... Mn-1, every element of an Mm level model must be an "
    "instance-of exactly one element of an Mm+1 level model, for all m &lt; n-1, and any relationship other than "
    "the instance-of relationship between two elements X and Y implies that level(X) = level(Y).\"<br/>"
    "Problem: Genre, ScienceFiction and Dune are all domain model elements, so in UML they all sit on M1 (classes "
    "and objects are both on M1). But Dune is an instance of ScienceFiction, which is an instance of Genre: two "
    "domain instance-of relationships inside one level, which the linguistic level structure cannot express. "
    "ScienceFiction would be both an instance (of Genre) and a class (of Dune). Deep modeling solves this by "
    "separating <b>linguistic</b> classification (everything is a Clabject) from <b>ontological</b> "
    "classification (O0-O3), with strictness in each dimension.",
    "1.5 pt definition (exactly one type one level up + other relationships stay within a level); 1.5 pt "
    "problem (domain type-of-type inside M1).",
    "L8 slides 3-6"))
s.p("Model answer for (c) (red = added):")
s.add(deep_skeleton(True), Spacer(1, 4))
s.add(solbox("5(c)", 6,
    "See the table below.",
    "2 pt clabject potencies (all five correct, -0.5 per error); 3 pt attributes (shelfColour, loanPeriodDays "
    "with mutability 0, title and copyNo); 1 pt Crime with potency 2, its values and the generalization to "
    "Book.",
    "L8 slides 18-21; Sheet 8 Q2 (Ferrari colour<super>1</super> = Red<super>0</super>) and Q3 (missing clabject)"))
s.add(sgrid([["Element", "Potency", "Why"],
            ["Genre", "3", "its instances (genres, O1) have instances (books, O2) which have instances (copies, O3)"],
            ["Book", "0", "abstract: only subclasses, no direct instances (req. 1); potency 0 on O1 is fine"],
            ["ScienceFiction, Crime", "2", "instances of Genre: one lower than 3"],
            ["Dune, TheBigSleep", "1", "instances of a genre: one lower again; their instances are copies"],
            ["dune3", "0", "a plain object"],
            ["Genre: shelfColour^1", "durability 1", "a value per genre (shelfColour^0 = 'blue'); books and "
                                                     "copies have none (req. 2)"],
            ["Genre: loanPeriodDays^2", "durability 2", "declared for genres, value at book level, absent at "
                                                        "copies"],
            ["ScienceFiction: loanPeriodDays^1 = 28^0", "mutability 0", "every book of the genre has 28 and may not "
                                                                       "change it (req. 3); Dune: "
                                                                       "loanPeriodDays^0 = 28"],
            ["Book: title^1", "durability 1", "Dune: title^0 = 'Dune'; copies have no title (req. 4)"],
            ["Book: copyNo^2", "durability 2", "inherited by ScienceFiction, copyNo^1 : Integer in Dune, "
                                               "copyNo^0 = 3 in dune3 (req. 5)"]],
           [55 * mm, 25 * mm, 90 * mm]), Spacer(1, 10))
s.add(solbox("5(d)", 2,
    "(1) <b>valid</b>: 2 = 3 - 1. (2) <b>invalid</b>: an instance of a potency-1 clabject must have potency 0. "
    "(3) <b>invalid</b>: mutability 2 exceeds durability 1. (4) <b>valid</b>: potency 0 with subclasses = "
    "abstract class; potency and level are independent.",
    "0.5 pt each, only with the reason.", "L8 slides 18-20; L8 guide Q25"))
s.add(solbox("5(e)", 2,
    "&bull; Genres are real <b>clabjects</b>: ScienceFiction is an ordinary object of Genre and a class of books "
    "on a proper ontological level, so the model is strict in both dimensions (UML keeps type and type-of-type on "
    "M1 and needs a special " + c(": Genre") + " label).<br/>"
    "&bull; <b>Deep characterization</b> with potency: Genre can directly say that books have a fixed loan period "
    "and copies a copy number (durability/mutability), which in UML needs extra OCL constraints.<br/>"
    "&bull; One uniform notation (LML) on all levels; no special powertype notation needed.",
    "1 pt per advantage, any two.", "L8 slides 9, 15-17, 21; L8 guide Q26"))
s.build()
