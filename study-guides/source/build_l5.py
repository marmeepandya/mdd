from guide_lib import *

g = Guide("L5-ATL-Questions.pdf", "MDD - Lecture 5: ATL - Exam question bank", "MDD Lecture 5 - Exam Questions")
T = "See the table below."

g.p("Lecture 5: ATL (ATLAS Transformation Language)", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "slides 1-26 and Exercise Sheet 5.", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "ATL is where the course turns into <b>model transformations</b> (the PIM-to-PSM arrow from Lecture 1). Expect "
    "<b>theory</b> (rule kinds, source/target patterns, determinism, refining mode) and <b>writing a small "
    "transformation</b> for two given metamodels, exactly like Exercise Sheet 5.",
    "ATL expressions are OCL, so everything from Lectures 2-3 (navigation, collect, sum, iterate, oclIsUndefined) is "
    "reused here.",
    "Page 2 is a cheat sheet with the complete Families2Persons transformation: learn to write it from memory.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "ATL is a <b>model transformation language</b>: a module turns a <b>source model</b> (conforming to a source "
    "metamodel) into a <b>target model</b> (conforming to a target metamodel). The transformation is itself a model "
    "conforming to the ATL metamodel.",
    "<b>Hybrid</b>: declarative <b>matched rules</b> (recommended) plus an imperative part (<b>called rules</b>, "
    "<b>action blocks</b>). Expressions are <b>OCL</b>.",
    "<b>Source models are read-only, target models are write-only.</b> So rule order and binding order do not "
    "matter and execution stays <b>deterministic</b>.",
    "A rule has a <b>source pattern</b> (" + c("from") + ": typed elements plus an optional <b>guard</b>) and a "
    "<b>target pattern</b> (" + c("to") + ": target elements plus <b>bindings</b> " + c("prop <- expr") + ").",
    "Declarative rule kinds: <b>standard</b> (once per match), <b>lazy</b> (each time it is called), <b>unique "
    "lazy</b> (at most once per match, only if called).",
    "<b>Helpers</b> are ATL's methods: " + c("helper context T def: name(params) : Type = expr;") + ".",
    "<b>Refining mode</b> copies everything not matched automatically: " + c("create OUT : MMA refining IN : MMA;"),
]))

g.add(PageBreak())
g.p("Cheat sheet 1: the complete Families2Persons transformation", "h1")
g.add(code_block("""
module Families2Persons;
create OUT : Persons from IN : Families;

helper context Families!Member def: isFemale() : Boolean =
  if not self.familyMother.oclIsUndefined() then true
  else
    if not self.familyDaughter.oclIsUndefined() then true
    else false
    endif
  endif;

helper context Families!Member def: familyName : String =
  if not self.familyFather.oclIsUndefined() then self.familyFather.lastName
  else
    if not self.familyMother.oclIsUndefined() then self.familyMother.lastName
    else
      if not self.familySon.oclIsUndefined() then self.familySon.lastName
      else self.familyDaughter.lastName
      endif
    endif
  endif;

rule Member2Male {
  from s : Families!Member (not s.isFemale())
  to   t : Persons!Male (
         fullName <- 'Mr. ' + s.firstName + ' ' + s.familyName
       )
}

rule Member2Female {
  from s : Families!Member (s.isFemale())
  to   t : Persons!Female (
         fullName <- 'Mrs. ' + s.firstName + ' ' + s.familyName
       )
}
"""))
g.p("The slide writes " + c("'Mr.'") + " without the trailing space; see section I.", "small")
g.add(Spacer(1, 6))
g.p("Cheat sheet 2: ATL syntax", "h1")
g.add(grid([
    ["Syntax", "Meaning"],
    [c("module Name;"), "names the transformation module"],
    [c("create OUT : MMt from IN : MMs;"), "target model OUT conforms to MMt, source model IN conforms to MMs"],
    [c("create OUT : MMA refining IN : MMA;"), "refining mode: unmatched elements are copied automatically"],
    [c("Families!Member"), "class Member of metamodel Families (metamodel!Class)"],
    [c("from s : MM!C (guard)"), "source pattern: element type plus optional Boolean guard"],
    [c("to t : MM!D ( p <- expr, ... )"), "target pattern with bindings (comma-separated)"],
    [c("helper context MM!C def: h(x : T) : R = expr;"), "operation helper (called as " + c("s.h(x)") + ")"],
    [c("helper context MM!C def: h : R = expr;"), "attribute helper, no parameters (used as " + c("s.h") + ")"],
    [c("lazy rule R { from ... to ... }"), "applied only when called, once per call"],
    [c("unique lazy rule R { ... }"), "applied at most once per match, only when called"],
    [c("thisModule.R(e)"), "call a lazy rule (or reach module-level helpers) from an expression"],
    [c("'a' + 'b'"), "string concatenation in ATL (OCL would use " + c("concat") + ")"],
    [c("x.oclIsUndefined()"), "test whether an optional (0..1) reference is empty"],
], [72 * mm, 98 * mm]))

g.add(PageBreak())

g.sec("A. What ATL is")
g.qa("MED", "What is ATL, who developed it, and where does it come from?",
     bullets([
         "A <b>model transformation language (MTL)</b>, originally developed by the <b>INRIA</b>-supported modeling group "
         "at the <b>University of Nantes</b> (formerly the ATLAS group, now <b>AtlanMod</b>); maintained by AtlanMod and "
         "<b>OBEO</b>.",
         "Developed as a submission to the <b>OMG's QVT</b> (Query/View/Transformation) Request For Proposals.",
         "Part of <b>AMMA</b> (ATLAS Model Management Architecture).",
         "Released under the <b>Eclipse Public License</b>; an <b>M2M</b> component inside the <b>Eclipse Modeling "
         "Project (EMP)</b>.",
     ]) + "<br/>In use at over 100 sites (teaching, research, industry); a library of more than 40 scenarios / 100 "
     "transformations exists.", "slides 2-3", short="What ATL is; origin (Nantes, INRIA, QVT, AMMA, Eclipse).")

g.qa("HIGH", "What are the characteristics of ATL? What is the difference between declarative and imperative?",
     bullets([
         "<b>Simple declarative syntax</b>: builds on the <b>syntax and principles of OCL</b>; simple problems are solved "
         "simply.",
         "<b>Advanced features</b>: lazy rules, refining mode, rule inheritance, ...; many complex problems can still be "
         "handled declaratively.",
         "<b>Imperative part</b>: makes it possible to handle <b>any</b> problem.",
     ]) + "<br/><b>Declarative</b> describes <b>what</b> should happen; <b>imperative</b> describes <b>how</b> it happens.",
     "slide 4", short="ATL characteristics; declarative vs imperative.")

g.sec("B. The big picture")
g.qa("HIGH", "Explain the big picture of an ATL transformation (slides 5-6). Draw it.",
     bullets([
         "A <b>source model M<sub>s</sub></b> conforms to (is an instance of) a <b>source metamodel MM<sub>s</sub></b>; "
         "a <b>target model M<sub>t</sub></b> conforms to a <b>target metamodel MM<sub>t</sub></b>.",
         "The transformation <b>MMa2MMb.atl</b> is itself a model conforming to the <b>ATL metamodel</b>; it refers to "
         "MM<sub>s</sub> and MM<sub>t</sub>.",
         "MM<sub>s</sub>, ATL and MM<sub>t</sub> all conform to the <b>metametamodel (MOF)</b>.",
         "Executing the transformation turns M<sub>s</sub> into M<sub>t</sub>.",
     ]) + "<br/><b>Slide 6 example:</b> MM<sub>s</sub> has classes Green and Red, MM<sub>t</sub> has Blue and Pink. The "
     "transformation has rules <b>R2B</b> (Red to Blue) and <b>G2P</b> (Green to Pink). Each red element of "
     "M<sub>s</sub> becomes a blue one in M<sub>t</sub>, each green one a pink one. Rules are instances of the ATL class "
     "Rule; Green/Red/Rule are all instances of the metametamodel's Class.",
     "slides 5-6", short="Big picture: models, metamodels, ATL, MOF (slides 5-6).")

g.qa("HIGH", "Explain the EMF picture of Families2Persons (slide 17) with its levels M3, M2, M1.",
     T, "slide 17", short="M3/M2/M1 levels of Families2Persons (EMF picture).",
     extra=[grid([
         ["Level", "Elements", "Conforms to (C2)"],
         ["<b>M3</b> (metametamodel)", "Ecore.ecore", "itself"],
         ["<b>M2</b> (metamodels)", "Families.ecore, ATL.ecore, Persons.ecore", "Ecore.ecore"],
         ["<b>M1</b> (models)", "sample-Families.ecore, Families2Persons.atl, sample-Persons.ecore",
          "their M2 metamodel (Families, ATL, Persons)"],
     ], [40 * mm, 80 * mm, 50 * mm]), Spacer(1, 4),
         Paragraph("<b>C2</b> = \"conforms to\". The arrow sample-Families to sample-Persons is the execution of "
                   "Families2Persons.atl. In EMF the metametamodel is <b>Ecore</b> (the counterpart of MOF on slide 5).",
                   S["a"])])

g.sec("C. Source and target models, rules")
g.qa("HIGH", "What does \"source models are read-only, target models are write-only\" mean, and why does ATL do it?",
     bullets([
         "<b>Source models are read-only</b>: they can only be navigated, not modified.",
         "<b>Target models are write-only</b>: they cannot be navigated (you cannot read what was already produced).",
     ]) + "<br/><b>Why:</b> so that the declarative rules stay <b>deterministic</b> regardless of execution order: a rule "
     "cannot change a match (source is unchanged), and one binding cannot change the value of another (targets are not "
     "navigable). See also section D.", "slides 7, 13", short="Source read-only / target write-only, and why.")

g.qa("HIGH", "What are the declarative and imperative parts of ATL? Which style is recommended?",
     bullets([
         "<b>Declarative:</b> <b>matched rules</b> with <b>automatic traceability support</b>, and the side-effect free "
         "navigation/query language <b>OCL 2.0</b>.",
         "<b>Imperative:</b> <b>called rules</b> and <b>action blocks</b>.",
         "<b>Recommended style: declarative.</b>",
     ]) + "<br/><i>Traceability (explanation beyond the slide):</i> ATL remembers which target element each matched rule "
     "created for which source element. When a binding assigns a <b>source</b> element to a target reference, ATL "
     "automatically uses the <b>corresponding target</b> element instead.", "slide 7",
     short="Declarative vs imperative parts of ATL; recommended style.")

g.qa("HIGH", "What does a declarative rule specify, and what is an imperative rule?",
     "<b>Declarative rule</b>:<br/>" + bullets([
         "a <b>source pattern</b> to be <b>matched</b> in the source models",
         "a <b>target pattern</b> to be <b>created</b> in the target models for each match during rule application",
     ]) + "<br/><b>Imperative rule</b>: basically a <b>procedure</b>:<br/>" + bullets([
         "it is <b>called by its name</b> and may take <b>arguments</b>",
         "it can contain a <b>declarative target pattern</b>, an <b>action block</b> (a sequence of statements), or "
         "<b>both</b>",
     ]), "slide 8", short="Declarative rule vs imperative rule.")

g.qa("HIGH", "What does applying a declarative rule mean? Name and explain the three kinds of declarative rules.",
     "Applying a rule means <b>creating the specified target elements</b> and <b>initialising their properties</b>.",
     "slide 9; Exercise Sheet 5", short="Three kinds of declarative rules (standard, lazy, unique lazy).",
     extra=[grid([
         ["Kind", "Applied ...", "Notes"],
         ["<b>Standard</b> (matched)", "<b>once for each match</b>, automatically",
          "a given set of elements may only be matched by <b>one</b> standard rule"],
         ["<b>Lazy</b>", "<b>as many times</b> for each match <b>as it is referred to</b> from other rules (possibly "
                         "never)", "each call creates new target elements; called with " + c("thisModule.R(x)")],
         ["<b>Unique lazy</b>", "<b>at most once</b> for each match, and <b>only if referred to</b>",
          "repeated calls with the same element return the same target"],
     ], [32 * mm, 70 * mm, 68 * mm])])

g.qa("HIGH", "What is the source pattern, and what is a match?",
     "The source pattern consists of:<br/>" + bullets([
         "a <b>labelled set of types</b> from the <b>source metamodel</b> (e.g. " + c("s : Families!Member") + ")",
         "a <b>guard</b> (Boolean expression) used to <b>filter matches</b> (e.g. " + c("(not s.isFemale())") + ")",
     ]) + "<br/>A <b>match</b> is a set of source elements that are <b>instances of the types</b> in the pattern (<b>one "
     "element per type</b>) and that <b>satisfy the guard</b>.", "slide 11", short="Source pattern; what a match is.")

g.qa("HIGH", "What is the target pattern, and how is it applied?",
     "The target pattern consists of:<br/>" + bullets([
         "a <b>labelled set of types</b> from the <b>target metamodel</b>",
         "for each, a set of <b>bindings</b> that initialise properties using an expression (" +
         c("fullName <- ...") + ")",
     ]) + "<br/>For each match it is applied by:<br/>" + bullets([
         "<b>creating</b> elements in the target model (<b>one for each type</b> of the target pattern)",
         "<b>initialising</b> them by executing the bindings: <b>first evaluating</b> the value, <b>then assigning</b> it "
         "to the property",
     ]), "slide 12", short="Target pattern; how it is applied (create, then bind).")

g.qa("HIGH", "In which order are declarative rules executed? How can execution still be deterministic?",
     "Declarative rules <b>free the developer from specifying execution order</b>: the order in which <b>rules are "
     "matched and applied</b> and the order in which <b>bindings are applied</b> are <b>not specified</b>.<br/>"
     "Execution stays <b>deterministic</b> because:<br/>" + bullets([
         "a rule <b>cannot change the source models</b>, so it cannot change a match",
         "<b>target elements are not navigable</b>, so executing one binding cannot change the value of another",
     ]) + "<br/>That is also why the output on slide 16 lists the persons in a different order than the families on "
     "slide 15.", "slide 13", short="Execution order of declarative rules; why deterministic.")

g.sec("D. Helpers")
g.qa("HIGH", "What are helpers? Name their parts using the doubleX example.",
     "Helpers are the ATL equivalent of <b>Java methods</b>: auxiliary functions that compute a result needed in a "
     "rule and can be called from different points of a transformation.<br/>" +
     ocl("helper context Integer def : doubleX(x : Integer) : Integer = x * 2;") + "<br/>" + bullets([
         "<b>name</b>: " + c("doubleX"),
         "<b>context type</b>: " + c("Integer") + " (the type it is called on)",
         "<b>optional parameters</b>: " + c("(x : Integer)"),
         "<b>return type</b>: " + c("Integer"),
         "<b>ATL expression</b> (body) giving the <b>return value</b>: " + c("x * 2"),
     ]), "slides 10, 20", short="Helpers: purpose and the five parts (doubleX).")

g.qa("HIGH", "Explain the helper " + c("isFemale()") + ".",
     ocl("helper context Families!Member def: isFemale() : Boolean =\n"
         "  if not self.familyMother.oclIsUndefined() then true\n"
         "  else if not self.familyDaughter.oclIsUndefined() then true\n       else false endif\n  endif;") +
     "<br/>A Member is female if it is the <b>mother</b> of a family (" + c("familyMother") + " is set) or a "
     "<b>daughter</b> (" + c("familyDaughter") + " is set). Each opposite end is " + c("0..1") + ", so "
     + c("oclIsUndefined()") + " tests whether the member plays that role. Shorter equivalent: "
     + c("not self.familyMother.oclIsUndefined() or not self.familyDaughter.oclIsUndefined()") + ".",
     "slide 20", short="Explain helper isFemale().")

g.qa("HIGH", "Why is the helper " + c("familyName") + " needed, and how does it work?",
     "The family name is <b>not stored in Member</b>, only in Family (" + c("lastName") + "). The helper <b>navigates "
     "from the member to its family</b> through whichever role it plays: father, else mother, else son, else daughter, "
     "and returns that family's " + c("lastName") + ".<br/>It is written <b>without parentheses</b> (" +
     c("def: familyName : String") + "), i.e. an <b>attribute helper</b> with no parameters, used as " +
     c("s.familyName") + "; " + c("isFemale()") + " is an <b>operation helper</b>, used as " + c("s.isFemale()") + ".",
     "slide 21", short="Helper familyName: why and how; attribute vs operation helper.")

g.sec("E. The Families2Persons example")
g.qa("HIGH", "Describe the Families and Persons metamodels and what the transformation should do.",
     bullets([
         "<b>Families</b>: " + c("Family(lastName : String)") + " with four composition associations to "
         + c("Member(firstName : String)") + ": " + c("father") + " (1), " + c("mother") + " (1), " + c("sons") + " (*), "
         + c("daughters") + " (*). Opposite roles: " + c("familyFather, familyMother, familySon, familyDaughter") +
         " (each 0..1).",
         "<b>Persons</b>: abstract " + c("Person(fullName : String)") + " with subclasses " + c("Male") + " and "
         + c("Female") + ".",
         "<b>Goal:</b> every member becomes a Male or Female person whose fullName is title + first name + family name, "
         "e.g. Family March (Jim, Cindy, Brandon, Brenda) becomes Mr. Jim March, Mrs. Cindy March, Mr. Brandon March, "
         "Mrs. Brenda March.",
     ]), "slides 14-16, 18", short="Families and Persons metamodels; goal of the transformation.")

g.qa("HIGH", "Write the header section of Families2Persons and explain it.",
     ocl("module Families2Persons;\ncreate OUT : Persons from IN : Families;") +
     "<br/>The header <b>names the transformation module</b> and the <b>variables for the source and target models</b> "
     "(" + c("IN") + ", " + c("OUT") + "), together with their <b>metamodels acting as types</b> (" + c("Families") +
     ", " + c("Persons") + ").", "slide 19", short="Header section of Families2Persons.")

g.qa("HIGH", "Write the two rules Member2Male and Member2Female and explain them.",
     ocl("rule Member2Male {\n  from s : Families!Member (not s.isFemale())\n"
         "  to   t : Persons!Male (\n         fullName <- 'Mr. ' + s.firstName + ' ' + s.familyName\n       )\n}\n\n"
         "rule Member2Female {\n  from s : Families!Member (s.isFemale())\n"
         "  to   t : Persons!Female (\n         fullName <- 'Mrs. ' + s.firstName + ' ' + s.familyName\n       )\n}") +
     "<br/>Both match " + c("Member") + "; the <b>guards are complementary</b>, so every member is matched by exactly "
     "one standard rule (which slide 9 requires). Each match creates one Male or Female and binds " + c("fullName") +
     ". " + c("+") + " concatenates strings in ATL.", "slide 22", short="Write Member2Male and Member2Female.")

g.qa("MED", "Summarise the transformation as on the overview slide.",
     bullets([
         c("Family.lastName") + " + " + c("Member.firstName") + " (via helper familyName) give " + c("Person.fullName") + ".",
         "Each " + c("Member") + " becomes " + c("Female") + " if " + c("isFemale()") + ", else " + c("Male") + ".",
     ]), "slide 23", short="Overview of Families2Persons (slide 23).")

g.qa("HIGH", "What is the output of Families2Persons for Family Sailor (father Peter, mother Jackie, sons David and "
     "Dylan, daughter Kelly)? In which order?",
     "Five persons: <b>Male</b> \"Mr. Peter Sailor\", \"Mr. David Sailor\", \"Mr. Dylan Sailor\"; <b>Female</b> \"Mrs. "
     "Jackie Sailor\", \"Mrs. Kelly Sailor\". The <b>order is not specified</b> (slide 16 lists them mixed with the "
     "March family), because rule execution order is not defined.", "slides 15-16",
     short="Output for Family Sailor; order.")

g.sec("F. Refining mode and tool support")
g.qa("HIGH", "What is refining mode, why is it needed, and what is its syntax?",
     bullets([
         "For transformations that <b>only modify a small part of a model</b>.",
         "Since source models are read-only, the target must be created <b>from scratch</b>; writing <b>copy rules</b> "
         "for every unchanged element works but is <b>not elegant</b>.",
         "In refining mode the ATL engine <b>automatically copies unmatched elements</b>; the developer <b>only "
         "specifies what changes</b>.",
         "ATL semantics is respected: <b>sources are still read-only</b>. An optimised engine may modify in place but "
         "only <b>commits the changes at the end</b>.",
     ]) + "<br/>Syntax: replace " + c("from") + " by " + c("refining") + ":<br/>" +
     ocl("module A2A;\ncreate OUT : MMA refining IN : MMA;") +
     "<br/>Source and target use the <b>same metamodel</b> (MMA).", "slide 25", short="Refining mode: why, how, syntax.")

g.qa("LOW", "What tool support exists for ATL?",
     bullets([
         "<b>Execution engine</b>: ATL-to-bytecode compiler and a virtual machine.",
         "<b>IDE</b>: editor with syntax highlighting and outline, execution support with launch configurations, "
         "source-level debugger.",
         "<b>Documentation</b>: starter's guide, user manual, installation guide (eclipse.org/atl).",
     ]), "slides 24, 26", short="ATL tool support.")

g.sec("G. Tutorial: Exercise Sheet 5")
g.p("Sheet 5, Q1: Book to Publication", "h1")
g.p("Source metamodel <b>Book</b>: " + c("Book(title : String)") + " composed of " + c("Chapter(nbPages : Integer, "
    "title : String)") + " (role " + c("chapter") + "). Target metamodel <b>Publication</b>: " +
    c("Publication(title : String, nbPages : Integer)") + ". Example: Book \"Bible\" with chapters of 2, 1 and 2 pages "
    "becomes Publication \"Bible\" with 5 pages.", "body")

g.qa("HIGH", "Write a transformation from Book to Publication, using a helper to calculate the number of pages. "
     "Write at least one version with iterate.",
     "<b>Official:</b><br/>" +
     ocl("module Book2Publication;\ncreate OUT : Publication from IN : Book;\n\n"
         "helper context Book!Book def: getSumPages() : Integer =\n"
         "  self.chapter->collect(c | c.nbPages)->sum();\n\n"
         "rule Book2Publication {\n  from b : Book!Book\n  to out : Publication!Publication (\n"
         "       title   <- b.title,\n       nbPages <- b.getSumPages()\n     )\n}") +
     "<br/><b>Official iterate version of the helper:</b><br/>" +
     ocl("helper context Book!Book def: getSumPages() : Integer =\n"
         "  self.chapter->collect(c | c.nbPages)\n              ->iterate(pages; acc : Integer = 0 | acc + pages);") +
     "<br/>Also correct (iterate directly over the chapters): " +
     c("self.chapter->iterate(c; acc : Integer = 0 | acc + c.nbPages)") + ". Shortest: " +
     c("self.chapter.nbPages->sum()") + ".<br/>Only Book is matched; chapters produce no target elements, they are "
     "only read by the helper.", "Exercise Sheet 5, Q1 (sample solution)", tut="5, Q1",
     short="Write Book2Publication with a helper (sum and iterate versions).")

g.p("Sheet 5, Q2: PortA to PortB (lazy rules)", "h1")
g.p("Source <b>PortA</b> metamodel: " + c("BlockA") + " composes " + c("PortA(name : String)") + " via two references, "
    + c("inputPort") + " and " + c("outputPort") + ". Target <b>PortB</b> metamodel: " + c("BlockB") + " composes "
    + c("InPortB") + " (" + c("inputPort") + ") and " + c("OutPortB") + " (" + c("outputPort") + "), both subclasses of "
    + c("PortB(name : String)") + ". Example: block X with input port P1 and output ports P1, P2 becomes block X with "
    "InPortB P1 and OutPortB P1, P2.", "body")

g.qa("HIGH", "Write the transformation PortA2PortB that splits a block's ports into input and output ports, using "
     "lazy rules.",
     "<b>Official:</b><br/>" +
     ocl("module PortA2PortB;\ncreate OUT : PortB from IN : PortA;\n\n"
         "rule BlockA2BlockB {\n  from blockA : PortA!BlockA\n  to   blockB : PortB!BlockB (\n"
         "         inPort  <- blockA.inputPort->collect(e | thisModule.PortA2InPortB(e)),\n"
         "         outPort <- blockA.outputPort->collect(e | thisModule.PortA2OutPortB(e))\n       )\n}\n\n"
         "lazy rule PortA2InPortB {\n  from s : PortA!PortA\n  to   t : PortB!InPortB ( name <- s.name )\n}\n\n"
         "lazy rule PortA2OutPortB {\n  from s : PortA!PortA\n  to   t : PortB!OutPortB ( name <- s.name )\n}") +
     "<br/>" + careful("the target metamodel calls the references " + c("inputPort") + " and " + c("outputPort") +
                       "; the official solution binds " + c("inPort") + "/" + c("outPort") + ". Use the names from the "
                       "metamodel: " + c("inputPort <- ...") + ", " + c("outputPort <- ...") + "."),
     "Exercise Sheet 5, Q2 (sample solution)", tut="5, Q2", short="Write PortA2PortB with two lazy rules.")

g.qa("HIGH", "Why are lazy rules the natural choice in PortA2PortB? What does " + c("thisModule") + " do?",
     bullets([
         "The <b>same source type</b> (PortA) must become <b>two different target types</b> depending on <b>which "
         "reference</b> it sits in (inputPort or outputPort). A standard rule matches on the element alone and cannot "
         "see that context, and slide 9 allows only <b>one standard rule</b> per match.",
         "In the example, P1 appears both as an input and as an output port and becomes both an InPortB and an "
         "OutPortB. A lazy rule creates a <b>new element each time it is called</b>, so calling both rules works.",
         "The block rule decides the role: it calls " + c("PortA2InPortB") + " for every element of "
         + c("inputPort") + " and " + c("PortA2OutPortB") + " for every element of " + c("outputPort") + " (via "
         + c("collect") + ").",
         c("thisModule") + " refers to the <b>ATL module itself</b>; through it you reach the module's helpers, "
         "lazy rules and module-level attributes (the hint on the sheet).",
     ]) + "<br/><i>Lazy vs unique lazy:</i> with " + c("unique lazy") + ", a port referenced twice in the same role "
     "would give one target element instead of two.", "slide 9; Exercise Sheet 5", tut="5, Q2",
     short="Why lazy rules in PortA2PortB; what thisModule is.")

g.sec("H. Practice")
g.p("My own exercises in the style of the slides and Sheet 5.", "small")

g.qa("HIGH", "Write the header of a transformation that turns a UML model (metamodel " + c("UML") + ") into a Java "
     "model (metamodel " + c("Java") + "), and the header for a refinement of a UML model.",
     ocl("module UML2Java;\ncreate OUT : Java from IN : UML;\n\nmodule UMLRefactor;\ncreate OUT : UML refining IN : UML;"),
     "slides 19, 25", short="Write headers: UML2Java and a UML refinement.")

g.qa("HIGH", "Write a helper on " + c("Families!Family") + " that returns the number of members, and a rule that "
     "turns only fathers into Male persons.",
     ocl("helper context Families!Family def: memberCount : Integer =\n"
         "  2 + self.sons->size() + self.daughters->size();\n\n"
         "rule Father2Male {\n  from s : Families!Member (not s.familyFather.oclIsUndefined())\n"
         "  to   t : Persons!Male (\n         fullName <- 'Mr. ' + s.firstName + ' ' + s.familyName\n       )\n}") +
     "<br/>2 because father and mother are both mandatory (multiplicity 1). The guard selects members that play the "
     "father role.", "slides 18-22 (exercise)", short="Write helper memberCount and a rule for fathers only.")

g.qa("HIGH", "Write Book2Publication so that only books with more than 100 pages are transformed, and the publication "
     "title is the book title in upper case.",
     ocl("rule Book2Publication {\n  from b : Book!Book (b.getSumPages() > 100)\n"
         "  to   p : Publication!Publication (\n         title   <- b.title.toUpper(),\n"
         "         nbPages <- b.getSumPages()\n       )\n}") +
     "<br/>The guard filters matches; the helper from Sheet 5 is reused in both the guard and a binding.",
     "slide 11 + Exercise Sheet 5 (exercise)", short="Book2Publication with a guard (> 100 pages) and toUpper.")

g.qa("HIGH", "Which kind of rule fits each situation?", T, "slides 8-9 (exercise)",
     short="Pick standard / lazy / unique lazy / called rule for 4 situations.",
     extra=[grid([
         ["Situation", "Rule kind"],
         ["Every Member must become a Person, automatically.", "<b>standard</b> (matched) rule"],
         ["A Port must become an InPortB or an OutPortB depending on the reference it is in; the same port may be "
          "needed in both roles.", "<b>lazy</b> rules, called from the Block rule"],
         ["Several classes reference the same Address; it should be converted once, but only if someone uses it.",
          "<b>unique lazy</b> rule"],
         ["Create one extra summary element at the end, with step-by-step statements.",
          "<b>called rule</b> with an action block (imperative)"],
     ], [120 * mm, 50 * mm])])

g.qa("MED", "Two standard rules both match " + c("Families!Member") + " without guards. What is the problem, and how "
     "does the slide's transformation avoid it?",
     "Slide 9: <b>a given set of elements may only be matched by one standard rule</b>. Two unguarded rules would both "
     "match every member, which is an error. Member2Male and Member2Female avoid it with <b>complementary guards</b> "
     + c("(not s.isFemale())") + " / " + c("(s.isFemale())") + ", so each member matches exactly one rule.",
     "slides 9, 22", short="Two standard rules matching the same element: problem and fix.")

g.qa("MED", "Can a binding read an attribute of an element already created in the target model? Why (not)?",
     "<b>No.</b> Target models are <b>write-only</b> (not navigable). Bindings may only read the <b>source</b> model "
     "(and helpers on it). This keeps the result independent of the unspecified order in which rules and bindings are "
     "executed. Compute what you need from the source instead, e.g. with a helper.", "slides 7, 13",
     short="Can a binding read the target model? Why not?")

g.qa("MED", "ATL vs OCL: what is different when you write expressions in ATL?",
     bullets([
         "Types are qualified with the metamodel: " + c("Families!Member") + " (OCL just " + c("Member") + ").",
         "Strings are concatenated with " + c("+") + " (OCL: " + c("concat") + ").",
         "Values are assigned with bindings " + c("prop <- expr") + " inside a target pattern; OCL has no assignment.",
         "Helpers (" + c("helper context ... def: ...;") + ") play the role of OCL's " + c("def") + "; they end with "
         + c(";") + ".",
         "Everything else (navigation, " + c("->collect/select/sum/iterate") + ", " + c("if-then-else-endif") + ", "
         + c("oclIsUndefined()") + ") is plain OCL.",
     ]), "slides 4, 7, 10, 19-22", short="ATL vs OCL syntax differences.")

g.sec("I. Slide details to be aware of")
g.qa("LOW", "Which details on the slides are inconsistent?",
     bullets([
         "<b>Slide 22:</b> " + c("'Mr.' + s.firstName") + " gives \"Mr.Jim March\" (no space), but slide 16 shows "
         "\"Mr. Jim March\". Write " + c("'Mr. '") + " / " + c("'Mrs. '") + " with a trailing space.",
         "<b>Slide 19:</b> the text says IN/OUT with metamodels \"Persons\" and \"Families\"; the code is "
         + c("create OUT : Persons from IN : Families") + " (OUT is Persons, IN is Families).",
         "<b>Sheet 5, Q2 solution:</b> binds " + c("inPort/outPort") + " although the metamodel names are "
         + c("inputPort/outputPort") + ".",
     ]), "slides 16, 19, 22; Exercise Sheet 5", short="Slide/solution inconsistencies.")

g.self_test()
g.build()
