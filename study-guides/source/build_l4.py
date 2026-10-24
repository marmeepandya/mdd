from guide_lib import *

g = Guide("L4-OCLModeling-Questions.pdf", "MDD - Lecture 4: Modeling with OCL - Exam question bank",
          "MDD Lecture 4 - Exam Questions")
T = "See the table below."

g.p("Lecture 4: Modeling with OCL", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "slides 1-14 and Exercise Sheet 4.", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "This lecture is about <b>using</b> OCL when modelling. Expect \"explain the rule\" questions (Liskov: what may be "
    "strengthened or weakened?) and \"apply it\" questions (state diagram to pre/post, simplify a diagram, fix a cycle).",
    "Sheet 4 (section F) adds <b>nested collections</b> (authors with articles) and <b>recursive structures</b> (all "
    "ancestors via " + c("closure") + "). Both are typical exam material.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "OCL can live in a <b>separate text</b> (with " + c("context") + ") or in a <b>note box</b> attached to the model "
    "element; the attachment defines the context.",
    "State diagrams map onto OCL: <b>events</b> are <b>operation calls</b>, <b>guards</b> are <b>preconditions</b>, "
    "<b>resulting states</b> give <b>postconditions</b> (" + c("oclInState") + ").",
    "<b>Liskov Substitution Principle:</b> a subclass instance must work wherever the superclass is expected, so: "
    "<b>invariants</b> only <b>strengthened</b>; <b>preconditions</b> only <b>weakened</b>; <b>postconditions</b> only "
    "<b>strengthened</b>.",
    "Constraints can <b>simplify diagrams</b>: one association plus an invariant instead of parallel specialised "
    "associations or whole subclass hierarchies.",
    "<b>Association cycles</b> are ambiguous; an invariant rules out unwanted object structures.",
    "Recursive associations (parent/child): " + c("self->closure(parent)") + " collects all ancestors.",
]))

g.p("Cheat sheet", "h1")
g.add(grid([
    ["Inheritance rule", "Subclass may ...", "Memory hook"],
    ["Invariant", "<b>strengthen</b>, never weaken", "keeps every promise about its state"],
    ["Precondition", "<b>weaken</b>, never strengthen", "<b>demand no more</b>"],
    ["Postcondition", "<b>strengthen</b>, never weaken", "<b>promise no less</b>"],
], [35 * mm, 55 * mm, 80 * mm]))
g.add(Spacer(1, 6))
g.add(grid([
    ["State diagram element", "OCL counterpart"],
    ["event, e.g. " + c("fill(amount)"), "operation call: context " + c("Bottle::fill(amount : Integer)")],
    ["guard, e.g. " + c("[amount < capacity]"), "part of the <b>precondition</b>"],
    ["source state", c("pre: self.oclInState(empty)")],
    ["target state", c("post: self.oclInState(partiallyFilled)") + " (plus new attribute values)"],
], [55 * mm, 115 * mm]))
g.add(PageBreak())

g.sec("A. OCL inside class diagrams")
g.qa("MED", "What are the two ways to attach OCL constraints to a UML model?",
     bullets([
         "In a <b>separate textual document</b>, with the context written explicitly:<br/>" +
         ocl("context Microwave\ninv: self.temperature > 0"),
         "On the class diagram as a <b>note box</b>; the <b>context is defined by connecting the box</b> (dashed line) "
         "<b>to the model element</b>.",
     ]) + "<br/>The same holds for <b>pre- and postconditions</b>: a note attached to an <b>operation</b> makes that "
     "operation the context.", "slides 2-3", short="Text vs note box; how the context is defined.")

g.qa("MED", "Write the Microwave constraints from slide 3 as text, and explain " + c("State::on") + ".",
     ocl("context Microwave\ninv: self.temperature > 0\n\ncontext Microwave::turnOn()\npost: status = State::on\n\n"
         "context Microwave::turnOff()\npost: status = State::off") +
     "<br/>" + c("State") + " is an <b>enumeration</b> (on, off); a literal is written " + c("EnumName::literal") + ".",
     "slide 3", short="Microwave constraints as text; State::on.")

g.sec("B. State diagrams and pre/postconditions")
g.qa("HIGH", "How do operation pre- and postconditions relate to state diagrams?",
     "They can capture <b>much of the information in statechart diagrams</b>:<br/>" + bullets([
         "<b>events</b> often correspond to <b>operation calls</b>",
         "<b>guards</b> on transitions are essentially <b>preconditions</b>",
         "<b>resulting states</b> contain the information for <b>postconditions</b>"]), "slide 4",
     short="How state diagrams map to pre/post.")

g.qa("HIGH", "Describe the Bottle state diagram (slide 5).",
     "Bottle: " + c("capacity, contents : Integer") + "; " + c("fill(amount : Integer)") + ", " + c("cap()") +
     "; 0..1 Cap.<br/>" + bullets([
         "Start in <b>empty</b>.",
         "empty to <b>partially filled</b>: " + c("fill(amount) [amount < capacity]"),
         "empty to <b>filled</b>: " + c("fill(amount) [amount >= capacity]"),
         "partially filled to itself: " + c("fill(amount) [contents + amount < capacity]"),
         "partially filled to filled: " + c("fill(amount) [contents + amount >= capacity]"),
         "filled to <b>capped</b>: " + c("cap()") + "; then the final state.",
     ]) + "<br/>No fill from filled or capped, so filling a full or capped bottle is not allowed.",
     "slide 5", short="Describe the Bottle state diagram.")

g.qa("HIGH", "Write and explain the pre- and postcondition of " + c("Bottle::fill") + " (slide 6).",
     ocl("context Bottle::fill(amount : Integer)\n"
         "pre : self.oclInState(empty) or self.oclInState(partiallyFilled) and amount > 0\n"
         "post: (contents@pre + amount < capacity and\n       self.oclInState(partiallyFilled) and\n"
         "       contents = contents@pre + amount)\n      or\n      (contents@pre + amount >= capacity and\n"
         "       self.oclInState(filled) and\n       contents = capacity)") + "<br/>" + bullets([
         "<b>Pre:</b> empty or partially filled, and amount positive.",
         "<b>Post 1:</b> still below capacity: partially filled, contents grew by exactly amount.",
         "<b>Post 2:</b> otherwise: filled, contents = capacity (extra is lost).",
         c("contents@pre") + " is needed because the condition is about the value <b>before</b> filling. When empty, "
         + c("contents@pre = 0") + ", so this also covers the guards from the empty state.",
     ]) + "<br/>" + careful("the precondition has an operator-precedence problem: see section G."),
     "slide 6", short="Pre/post of Bottle::fill (both cases, why @pre).")

g.qa("MED", "What does " + c("oclInState") + " do, and where do the states come from?",
     c("o.oclInState(s)") + " (an OclAny operation, Lecture 3) is true if o is currently in state s of <b>its class's "
     "state machine</b>. The state names come from the UML state diagram.", "slide 6; L3 slide 26",
     short="oclInState; where state names come from.")

g.sec("C. Constraints and inheritance (Liskov)")
g.qa("HIGH", "State the Liskov Substitution Principle and what it means for contracts.",
     bullets(["<b>Wherever an instance of a class is expected, one can always substitute an instance of any of its "
              "subclasses.</b>",
              "So <b>an instance of a subclass must fulfil all the contracts defined for that class</b>."]),
     "slide 7", short="Liskov Substitution Principle.")

g.qa("HIGH", "What is the rule for invariants under inheritance? Explain the Stove example.",
     "Invariants of a class must be <b>at least as strong as those of its superclasses</b>: inherited, and may be "
     "<b>strengthened</b> but <b>not weakened</b>.<br/>" +
     ocl("context Stove\ninv maxTemp: temperature <= 200\n\ncontext ElectricStove\ninv maxTemp: temperature <= 100") +
     "<br/>ElectricStove's invariant is <b>stronger</b> (at most 100 implies at most 200), so this is allowed.",
     "slides 7-8", short="Invariants under inheritance; Stove example.")

g.qa("HIGH", "What are the rules for pre- and postconditions of redefined operations, and why?",
     bullets(["A <b>precondition may be weakened, but not strengthened</b>.",
              "A <b>postcondition may be strengthened, but not weakened</b>."]) +
     "<br/><b>Why:</b> a client that thinks it holds a Stove only guarantees the Stove's precondition, so the subclass may "
     "not demand more; and it relies on the Stove's postcondition, so the subclass must deliver at least that. "
     "Hook: <b>demand no more, promise no less</b>.", "slide 9", short="Pre/post rules for redefined operations.")

g.qa("HIGH", "Check the slide-9 example: are both redefinitions legal?",
     ocl("context Stove::open()\npre : status = StoveState::off and temperature < 100\npost: isOpen\n\n"
         "context ElectricStove::open()\npre : status = StoveState::off\npost: status = StoveState::off and isOpen") +
     "<br/>" + bullets(["<b>Pre weakened (legal):</b> drops " + c("temperature < 100") + ".",
                        "<b>Post strengthened (legal):</b> promises " + c("isOpen") + " <b>and</b> status off."]),
     "slide 9", short="Check Stove/ElectricStove open().")

g.sec("D. Simplifying visual models")
g.qa("MED", "Why use constraints to simplify visual models? Describe the problem in the guitar example.",
     "When modelling you must judge <b>how much information to show and how much to leave out</b>; the appropriate use "
     "of constraints can <b>significantly simplify visual models</b>. Slide 10 needs extra specialised associations "
     "(ElectricGuitar-MetalString, ClassicGuitar-PlasticString) next to the general Guitar-GuitarString association: "
     "many lines, hard to read.", "slide 10", short="Why simplify with constraints; the guitar problem.")

g.qa("HIGH", "Give the three simplified guitar models and their OCL constraints.",
     "<b>Version 1</b>: keep both hierarchies, one association " + c("strings") + ":<br/>" +
     ocl("context ClassicGuitar\ninv: strings->forAll(s | s.oclIsTypeOf(PlasticString))\n"
         "context ElectricGuitar\ninv: strings->forAll(s | s.oclIsTypeOf(MetalString))") +
     "<br/><b>Version 2</b>: string subclasses become " + c("type : StringType") + " (plastic/metal):<br/>" +
     ocl("context ClassicGuitar\ninv: strings->forAll(type = StringType::plastic)\n"
         "context ElectricGuitar\ninv: strings->forAll(type = StringType::metal)") +
     "<br/><b>Version 3</b>: both hierarchies become enumerations:<br/>" +
     ocl("context Guitar\ninv: type = GuitarType::classic implies\n       string->forAll(type = StringType::plastic)\n"
         "context Guitar\ninv: type = GuitarType::electric implies\n       string->forAll(type = StringType::metal)"),
     "slides 11-13", short="The three simplified guitar models with OCL.")

g.qa("MED", "When would you choose subclasses (version 1) and when enumerations (versions 2-3)?",
     bullets([
         "<b>Subclasses</b> when kinds differ in <b>attributes, associations or behaviour</b>.",
         "<b>Enumerations</b> when kinds differ <b>only by a label</b>: fewer classes and associations.",
         "Trade-off: meaning moves from the picture into OCL text; version 3 needs " + c("implies") + ".",
     ]) + "<br/><i>(My own discussion.)</i>", "slides 10-13 (reasoning)", short="Subclasses vs enumerations.")

g.qa("MED", "In version 1, what changes if " + c("oclIsKindOf") + " is used instead of " + c("oclIsTypeOf") + "?",
     c("oclIsKindOf(PlasticString)") + " would also accept subclasses of PlasticString. With no further subclasses both "
     "mean the same; " + c("oclIsKindOf") + " is more robust if the hierarchy grows.", "slide 11; L3 slide 27",
     short="oclIsKindOf vs oclIsTypeOf in version 1.")

g.sec("E. Cycles in class models")
g.qa("HIGH", "Why are association cycles a problem? Explain the Person/House/Mortgage example.",
     "Whenever there is an <b>association cycle</b>, there is a <b>potential for ambiguity</b>; <b>invariants are often "
     "needed to rule out undesired meanings</b>.<br/>Person owns House (home, 0..*); Person has a Mortgage; the Mortgage "
     "has a House as <b>security</b>. The diagram allows a mortgage secured by <b>somebody else's</b> house. In the "
     "picture: M<sub>a</sub> links P1 to H<sub>x</sub>, which P1 owns (fine); M<sub>b</sub> links <b>P3</b> to "
     "H<sub>y</sub>, which <b>P2</b> owns (unwanted).<br/>" + ocl("context Person\ninv: self.mortgage.security.owner = self"),
     "slide 14", short="Why cycles are ambiguous; mortgage example; which instance is wrong.")

g.qa("MED", "Write a robust version of the slide-14 invariant for persons with several mortgages.",
     "If " + c("self.mortgage") + " is a Set, " + c("self.mortgage.security.owner") + " is a <b>Bag</b> and cannot equal "
     + c("self") + ".<br/>" + ocl("context Person\ninv: self.mortgage->forAll(m | m.security.owner = self)") +
     "<br/><i>(My own correction; the slide gives no multiplicity on mortgage.)</i>", "slide 14 (reasoning)",
     short="Robust (forAll) mortgage invariant.")

g.sec("F. Tutorial: Exercise Sheet 4")
g.p("Sheet 4, Q1: Conferences, authors, articles", "h1")
g.p("Model: <b>Conference</b> (goldAuthors : Integer) -- <b>Author</b> -- <b>Article</b> (citations : Integer). No role "
    "names or multiplicities are given, so navigate with lower-case class names: " + c("author") + ", " + c("article") +
    ", and assume many on each side.", "body")

g.qa("HIGH", "(a) An author can only take part in a conference if he/she published an article.",
     "<b>Official:</b><br/>" + ocl("context Conference\ninv: author.article->size() > 0") +
     "<br/>" + careful("this only says the conference's authors have <b>at least one article in total</b>; one author "
                       "with articles makes it true even if the others have none. Each author must be checked:") +
     "<br/>" + ocl("context Conference\ninv: author->forAll(a | a.article->notEmpty())\n\n"
                   "-- or, from the author's side\ncontext Author\ninv: conference->notEmpty() implies article->notEmpty()"),
     "Exercise Sheet 4, Q1(a)", tut="4, Q1(a)", short="Authors at a conference must have published (forAll per author).")

g.qa("HIGH", "(b) A \"gold author\" has an article with at least 100 citations. goldAuthors of a conference equals the "
     "number of gold authors.",
     "<b>Official:</b><br/>" +
     ocl("context Conference::goldAuthor : Integer\n"
         "derive: author->select(a | a.article.citation > 100)->asSet()->size()") +
     "<br/>" + careful("three problems: " + c("a.article.citation") + " is a <b>Bag</b> of numbers and cannot be compared "
                       "with 100; \"at least\" is " + c(">=") + "; and the names are " + c("goldAuthors") + "/" +
                       c("citations") + ". Correct:") + "<br/>" +
     ocl("context Conference\ninv: goldAuthors =\n     author->select(a | a.article->exists(citations >= 100))->size()") +
     "<br/>(A " + c("derive") + " on " + c("Conference::goldAuthors") + " with the same right-hand side is also fine. "
     + c("asSet()") + " is harmless but unnecessary, since " + c("author") + " is already a Set.)",
     "Exercise Sheet 4, Q1(b)", tut="4, Q1(b)", short="goldAuthors = authors with an article >= 100 citations.")

g.qa("HIGH", "(c) Now a gold author needs at least <b>two</b> articles with at least 100 citations.",
     "<b>Official:</b><br/>" +
     ocl("context Conference::goldAuthor : Integer\n"
         "derive: author->select(a | a.article->select(citation > 100)->size() >= 2)\n"
         "        ->asSet()->size()") +
     "<br/>The structure (a select <b>inside</b> a select) is right; fix " + c(">= 100") + " and the attribute names:<br/>"
     + ocl("context Conference\ninv: goldAuthors =\n"
           "     author->select(a | a.article->select(citations >= 100)->size() >= 2)\n           ->size()") +
     "<br/>Pattern to remember: <b>count the outer elements whose inner collection has at least k matches</b>.",
     "Exercise Sheet 4, Q1(c)", tut="4, Q1(c)", short="goldAuthors with at least two highly cited articles (nested select).")

g.p("Sheet 4, Q2: Transitive parent/child relationship", "h1")
g.p("Model: <b>Person</b> with a recursive association to itself, roles " + c("parent") + " and " + c("child") +
    " (both *), and operations " + c("getParents() : Set(Person)") + ", " + c("getChildren() : Set(Person)") +
    ". getParents should return <b>all direct and indirect</b> parents (parents, grandparents, ...).", "body")

g.qa("HIGH", "(a) Write OCL body constraints for getParents() and getChildren().",
     "<b>Official:</b><br/>" +
     ocl("context Person::getParents() : Set(Person)\nbody: self->closure(parent)->excluding(self)\n\n"
         "context Person::getChildren() : Set(Person)\nbody: self->closure(child)->excluding(self)") +
     "<br/>" + c("closure(expr)") + " is an iterator (OCL 2.3+, <b>not on the lecture slides</b>): it applies expr again "
     "and again (parents, their parents, ...) and collects every object reached, without duplicates. "
     + c("excluding(self)") + " makes sure the person is not in their own result.<br/>Without closure, using only lecture "
     "constructs (recursion through the operation itself):<br/>" +
     ocl("context Person::getParents() : Set(Person)\nbody: parent->union(parent.getParents())->asSet()") +
     "<br/>The recursive version terminates only if nobody is their own ancestor; " + c("closure") + " also handles "
     "cycles.", "Exercise Sheet 4, Q2(a)", tut="4, Q2(a)", short="body for getParents/getChildren (closure, or recursion).")

g.qa("HIGH", "(b) Simpson family: Abe and Mona are Homer's parents; Homer and Marge are the parents of Bart, Lisa and "
     "Maggie. What do these calls return?", "<b>Official answers</b> (plus a few extras to practise):",
     "Exercise Sheet 4, Q2(b)", tut="4, Q2(b)", short="Simpsons: evaluate getParents/getChildren.",
     extra=[grid([
         ["Call", "Result"],
         [c("Abe.getParents()"), "{}  (no parents in the model)"],
         [c("Abe.getChildren()"), "{Homer, Bart, Lisa, Maggie}"],
         [c("Maggie.getParents()"), "{Marge, Homer, Abe, Mona}"],
         [c("Maggie.getChildren()"), "{}"],
         [c("Homer.getChildren()"), "{Bart, Lisa, Maggie}"],
         [c("Homer.getParents()"), "{Abe, Mona}"],
         ["<i>extra:</i> " + c("Marge.getParents()"), "{}  (Marge's parents are not modelled)"],
         ["<i>extra:</i> " + c("Mona.getChildren()"), "{Homer, Bart, Lisa, Maggie}"],
         ["<i>extra:</i> " + c("Bart.getParents()"), "{Homer, Marge, Abe, Mona}"],
     ], [70 * mm, 100 * mm]), Spacer(1, 4),
         Paragraph("The results are <b>Sets</b>: order does not matter and nobody appears twice. (The sample solution "
                   "has typos such as \"Aba\" for Abe.)", S["small"])])

g.sec("G. Practice")
g.qa("HIGH", "Write pre/postconditions for " + c("Bottle::cap()") + ", using the state diagram.",
     ocl("context Bottle::cap()\npre : self.oclInState(filled)\npost: self.oclInState(capped)") +
     "<br/>Optionally " + c("and contents = contents@pre") + ". Note " + c("cap") + " (navigation to Cap, lower-case "
     "class name) vs " + c("cap()") + " (operation): parentheses tell them apart.", "slides 5-6",
     short="Pre/post for Bottle::cap().")

g.qa("HIGH", "A bottle has capacity 100. Trace each call: resulting state and contents.", T, "slides 5-6 (exercise)",
     short="Trace fill/cap calls on a bottle with capacity 100.",
     extra=[grid([
         ["Before", "Call", "After"],
         ["empty, 0", c("fill(40)"), "partiallyFilled, 40"],
         ["partiallyFilled, 40", c("fill(30)"), "partiallyFilled, 70"],
         ["partiallyFilled, 70", c("fill(50)"), "filled, 100"],
         ["empty, 0", c("fill(100)"), "filled, 100"],
         ["filled, 100", c("fill(10)"), "<b>precondition violated</b>"],
         ["filled, 100", c("cap()"), "capped"],
         ["partiallyFilled, 70", c("cap()"), "<b>not allowed</b> (only from filled)"],
     ], [45 * mm, 30 * mm, 95 * mm])])

g.qa("MED", "Write invariants that tie the Bottle's states to its contents.",
     ocl("context Bottle\ninv: contents >= 0 and contents <= capacity\ninv: self.oclInState(empty) implies contents = 0\n"
         "inv: self.oclInState(partiallyFilled) implies\n       contents > 0 and contents < capacity\n"
         "inv: self.oclInState(filled) implies contents = capacity"), "slides 5-6 (exercise)",
     short="Invariants linking Bottle states to contents.")

g.qa("HIGH", "Stove's " + c("open()") + " has " + c("pre: status = StoveState::off") + " and " + c("post: isOpen") +
     ". Which subclass redefinitions are legal?", T, "slides 7-9 (exercise)",
     short="Classify 5 subclass redefinitions (Liskov).",
     extra=[grid([
         ["Redefinition in the subclass", "Legal?", "Why"],
         [c("pre: true"), "yes", "weaker pre"],
         [c("pre: status = StoveState::off and temperature < 50"), "<b>no</b>", "stronger pre"],
         [c("post: isOpen and temperature < 100"), "yes", "stronger post"],
         [c("post: true"), "<b>no</b>", "weaker post"],
         ["invariant " + c("temperature <= 300") + " (Stove: " + c("<= 200") + ")", "<b>no</b>", "weaker invariant"],
     ], [85 * mm, 18 * mm, 67 * mm])])

g.qa("MED", "Classic guitars have exactly 6 strings: write it for version 1 and version 3.",
     ocl("context ClassicGuitar\ninv: strings->size() = 6\n\n"
         "context Guitar\ninv: type = GuitarType::classic implies string->size() = 6"), "slides 11, 13 (exercise)",
     short="Classic guitars have 6 strings (versions 1 and 3).")

g.qa("MED", "Using the Person model of Sheet 4: nobody is their own ancestor, and every person has at most two "
     "direct parents.",
     ocl("context Person\ninv: not self->closure(parent)->includes(self)\ninv: parent->size() <= 2") +
     "<br/>The first rules out cycles in the parent relation (another use of an invariant against an unwanted "
     "structure, as in section E). <i>(My own exercise.)</i>", "Exercise Sheet 4 + slide 14 (exercise)",
     short="Write: nobody is own ancestor; at most two parents.")

g.sec("H. Slide problems to be aware of")
g.qa("MED", "What is wrong with the precondition on slide 6, and how should it be written?",
     ocl("pre: self.oclInState(empty) or self.oclInState(partiallyFilled) and amount > 0") +
     "<br/>In OCL, " + c("and") + " binds <b>more strongly</b> than " + c("or") + ", so this reads as "
     + c("inEmpty or (inPartial and amount > 0)") + ": an empty bottle could be \"filled\" with 0 or a negative amount. "
     "Intended:<br/>" + ocl("pre: (self.oclInState(empty) or self.oclInState(partiallyFilled)) and amount > 0") +
     "<br/><i>(Precedence is OCL standard; writing the brackets is always safe.)</i>", "slide 6",
     short="Precedence problem in the slide-6 precondition.")

g.qa("LOW", "Which other slide details are inconsistent?",
     bullets([
         "<b>Slide 14:</b> the mortgage invariant only works with at most one mortgage per person; otherwise use forAll.",
         "<b>Slide 13:</b> changes to " + c("1..*") + " and role " + c("string") + " (instead of " + c("0..1") + " / "
         + c("strings") + "). Use what the diagram in front of you shows.",
     ]), "slides 13, 14", short="Other slide inconsistencies.")

g.self_test()
g.build()
