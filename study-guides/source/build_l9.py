from guide_lib import *
from uml import Diagram

g = Guide("L9-PAMoLa-Questions.pdf", "MDD - Lecture 9: PAMoLa and Endogenous OWL Overlays - Exam question bank",
          "MDD Lecture 9 - Exam Questions")
T = "See the table below."


def p(name, pot):
    """Potency as superscript in paragraph text."""
    return f"{name}<super>{pot}</super>"


def vbar(dg, keys, parent, y):
    xs = [dg.pt(k, "top")[0] for k in keys]
    for k, x in zip(keys, xs):
        dg.line([dg.pt(k, "top"), (x, y)])
    px = dg.pt(parent, "bottom")[0]
    dg.line([(min(xs + [px]), y), (max(xs + [px]), y)])
    dg.line([(px, y), dg.pt(parent, "bottom")], head="hollow")


# ---------------------------------------------------------------- diagrams
def family_model():
    """Slide 7: the family model in LML."""
    dg = Diagram(170 * mm, 205)
    dg.level(203, "O0")
    dg.box("pt", 205, 192, "PersonType^2", w=90)
    dg.level(165, "O1")
    dg.box("pe", 210, 140, "Person^0", w=80)
    dg.line([(225, 140), (225, 153), (255, 153), (255, 140)])
    dg.text(262, 147, "hasParent 0..2 / hasChild *")
    dg.box("mp", 40, 92, "MalePerson^1 : PersonType", w=135)
    dg.box("fp", 315, 92, "FemalePerson^1 : PersonType", w=140)
    vbar(dg, ["mp", "fp"], "pe", 112)
    dg.text(200, 104, "{complete, disjoint}  (CA1 'Male-Female')")
    # hasFather: MalePerson (father end) <- Person ; hasMother : FemalePerson
    dg.line([dg.pt("mp", "left"), (12, dg.pt("mp", "left")[1]), (12, 133), (210, 133)])
    dg.text(16, 122, "hasFather {subsetOf hasParent} 0..1", size=6.8)
    dg.line([dg.pt("fp", "right"), (470, dg.pt("fp", "right")[1]), (470, 133), (290, 133)])
    dg.text(330, 122, "hasMother {subsetOf hasParent} 0..1", size=6.8)
    dg.level(58, "O2")
    dg.box("gp", 40, 38, "GrantPlinth^0 : MalePerson", w=135)
    dg.box("mr", 315, 38, "MrPlinth^0 : MalePerson", w=135)
    dg.line([dg.pt("gp", "right"), dg.pt("mr", "left")], label="hasFather", label_at=(225, 31))
    return dg.drawing


def powertype_model():
    """Slide 13: partitioning powertype with MixedPerson."""
    dg = Diagram(170 * mm, 185)
    dg.level(183, "O0")
    dg.box("pt", 205, 176, "PersonType^2", w=90)
    dg.level(150, "O1")
    dg.box("pe", 210, 138, "Person^0", w=80)
    dg.line([dg.pt("pe", "top"), dg.pt("pt", "bottom")], head="open", label="partitions", label_at=(255, 143))
    dg.box("mp", 60, 92, "MalePerson^1 : PersonType", w=135)
    dg.box("fp", 290, 92, "FemalePerson^1 : PersonType", w=140)
    vbar(dg, ["mp", "fp"], "pe", 110)
    dg.box("mx", 205, 32, "MixedPerson^1", w=90)
    xm, xf = dg.pt("mp", "bottom")[0], dg.pt("fp", "bottom")[0]
    dg.line([dg.pt("mx", "top", 0.3), (232, 52), (xm, 52), dg.pt("mp", "bottom")], head="hollow")
    dg.line([dg.pt("mx", "top", 0.7), (268, 52), (xf, 52)])
    dg.line([(xf, 52), dg.pt("fp", "bottom")], head="hollow")
    return dg.drawing


# ---------------------------------------------------------------- intro
g.p("Lecture 9: PAMoLa and Endogenous OWL Overlays", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "the 16 slides of the ECMFA 2026 talk <i>Supporting OWL-Style Reasoning over UML-Style Models via Endogenous OWL "
    "Overlays</i> (Gupta, Sadeghi, Ojha, Atkinson). There is no exercise sheet for this lecture.", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON[:2] + [HOW_TO_USE_COMMON[3]] + [
    "The file is a <b>slide deck</b> (the conference talk), not the full paper. Every answer below is taken from the "
    "slides and cites the slide number. Where an answer needs standard OWL/RDF knowledge that the slides only show "
    "(e.g. what owl:disjointWith means), it is tagged [STRETCH] or says so.",
    "This is a <b>research lecture by the course's own group</b> (Atkinson). It reuses the course concepts: clabjects, "
    "potency, LML and the orthogonal classification architecture (L8), powertypes and {complete, disjoint} "
    "generalization sets (L7), OCL snapshot checking (L2-L4), M-levels and transformations (L5-L6). Expect "
    "<b>explain</b> questions (what problem, why, what are the steps) and possibly <b>apply</b> questions: given a "
    "small model, what does the reasoner infer?",
    "Pages 2-3 are cheat sheets. Section J lists slide errors.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "<b>UML</b> is compact and well supported by tools, but its <b>reasoning support is modest</b>: tools rarely derive "
    "implied facts or expose contradictions, and OCL mostly checks constraints over a <b>snapshot</b>. <b>OWL</b> is "
    "built for <b>inference</b> (subclass closure, instance classification, property-hierarchy closure) and "
    "consistency/unsatisfiability diagnostics, but is a poor notation for engineering diagrams.",
    "<b>Goal:</b> OWL-style reasoning over UML-style diagrams.",
    "The usual bridge is <b>transformation-based</b> (e.g. ODM): an M2-level transformation turns the UML model into "
    "an OWL ontology. Three problems: (1) it creates a <b>new artefact that must be maintained</b>, (2) <b>multiple "
    "ontological levels</b> are not naturally supported (is MalePerson TBox or ABox?), (3) the <b>semantics of common "
    "modeling idioms</b> (e.g. a partitioning powertype = disjointness) are lost.",
    "<b>PAMoLa</b> (Poly-Aligned Modeling Language): a <b>graph-based modelling substrate</b>, self-describing, "
    "level-agnostic, homoiconic, with a fixed set of node and edge types. One model, several views: LML diagram, RDF "
    "Turtle, HUTN text.",
    "<b>Endogenous OWL overlay:</b> the model is read as facts (base graph G_base); <b>overlay derivation rules</b> "
    "(kernel + optional modules) compute OWL facts (overlay graph G_owl) from it; an <b>OWL reasoner</b> returns "
    "entailments and diagnostics; the modeler updates the model; repeat. No separately synchronised OWL file.",
    "Four demo scenarios: <b>role ends and subproperties</b>, <b>role classes and domain-based typing</b>, <b>property "
    "chaining</b>, <b>partitioning powertypes</b>. Tools: <b>Nemo</b> (rules) + <b>HermiT</b> (OWL reasoner).",
]))

g.p("Cheat sheet 1: UML vs OWL (slide 2)", "h1")
g.add(grid([
    ["", "UML", "OWL"],
    ["Strength", "compact, familiar, mature tooling; the default for authoring and communicating domain structure",
     "built for inference: subclass closure, instance classification, property-hierarchy closure"],
    ["Weakness", "modest reasoning: tools rarely derive implied facts or expose contradictions; OCL checks constraints "
     "over a snapshot, not entailment or classification", "poor notation for compact, engineering-oriented diagrams"],
    ["Checking", "constraint violated or not in this snapshot", "consistency and unsatisfiability diagnostics under a "
     "precise model-theoretic semantics"],
], [22 * mm, 74 * mm, 74 * mm]))

g.p("Cheat sheet 2: OWL/RDF vocabulary used on the slides", "h1")
g.p("Meanings are standard OWL/RDF(S); the slides use the terms without defining them.", "small")
g.add(grid([
    ["Term", "Meaning", "Slide example"],
    ["TBox / ABox", "terminology (classes, properties, axioms) / assertions about individuals", "Person, hasFather "
     "/ GrantPlinth, MrPlinth"],
    ["rdf:type", "individual is an instance of a class", "GrantPlinth rdf:type Person"],
    ["rdfs:subClassOf", "every instance of the subclass is an instance of the superclass", "MalePerson subClassOf "
     "Person"],
    ["rdfs:subPropertyOf", "every pair linked by the sub-property is linked by the super-property", "hasFather "
     "subPropertyOf hasParent"],
    ["rdfs:domain / range", "subject / object of the property is typed with that class", "P3_MotherEnd range Mother"],
    ["owl:inverseOf", "x P y iff y Q x", "Child inverseOf Parent"],
    ["owl:propertyChainAxiom", "P1 followed by P2 implies the chained property", "hasGrandparent = (hasParent "
     "hasParent)"],
    ["owl:disjointWith", "no individual is in both classes", "MalePerson disjointWith FemalePerson"],
    ["unsatisfiable class", "a class that cannot have any instance (equivalent to owl:Nothing)", "MixedPerson"],
], [33 * mm, 72 * mm, 65 * mm]))

g.p("Cheat sheet 3: the overlay workflow (slide 9)", "h1")
g.add(code_block("""1 BASE GRAPH      PAMoLa G_base   typed triple / fact view of the snapshot
2 OVERLAY RULES   rule fragment Rk  kernel plus optional modules
3 OVERLAY FACTS   G_owl           execute Rk to compute the overlay graph
4 REASON          OWL reasoner    entailments + diagnostics
  -> extend / update the model manually, then run again"""))

g.p("Cheat sheet 4: the four scenarios (slides 10-13)", "h1")
g.add(grid([
    ["Scenario", "UML-style idiom in the model", "Overlay produces", "Reasoner infers"],
    ["1 Role ends and subproperties", "hasFather {subsetOf hasParent}; GrantPlinth hasFather MrPlinth",
     "hasFather subPropertyOf hasParent; MalePerson subClassOf Person; types", "GrantPlinth hasParent MrPlinth"],
    ["2 Role classes, domain-based typing", "«role» Mother subclass of Person; unnamed end to Mother; GrantPlinth "
     "-Mother- MrsPlinth : Person", "P3_MotherEnd subPropertyOf Parent, domain Person, range Mother; Child "
     "inverseOf Parent", "MrsPlinth type Mother; GrantPlinth Parent MrsPlinth; MrsPlinth Child GrantPlinth"],
    ["3 Property chaining", "hasGrandparent with chain (hasParent hasParent); two hasParent links",
     "the hasParent assertions (+ the chain axiom)", "GrantPlinth hasGrandparent oldMrPlinth"],
    ["4 Partitioning powertypes", "PersonType<super>2</super> partitions Person; MixedPerson subclass of Male- and "
     "FemalePerson", "Person partitionedBy PersonType; MalePerson disjointWith FemalePerson; MixedPerson subClassOf "
     "both", "diagnostic: MixedPerson is unsatisfiable"],
], [30 * mm, 48 * mm, 50 * mm, 42 * mm]))
g.add(PageBreak())

# ---------------------------------------------------------------- A
g.sec("A. The problem: UML models vs OWL knowledge graphs")
g.qa("HIGH", "What is the goal of the PAMoLa / endogenous overlay work, and why is it needed?",
     "<b>Goal: provide OWL-style reasoning over UML-style diagrams.</b> UML is the default for authoring and "
     "communicating domain structure (compact, familiar, mature tools), but its reasoning support is modest: tools "
     "rarely derive implied facts or expose contradictions, and OCL mostly checks constraints over a snapshot. OWL "
     "offers exactly that reasoning (inference + diagnostics) but is a poor notation for engineering diagrams. The "
     "work wants the notation of UML <b>and</b> the reasoning of OWL.", "slide 2",
     short="Goal of the work and why it is needed.")

g.qa("HIGH", "Name three kinds of inference OWL is built for, and the two kinds of diagnostics.",
     "Inference: <b>subclass closure</b>, <b>instance classification</b>, <b>property-hierarchy closure</b>. "
     "Diagnostics: <b>consistency</b> and <b>unsatisfiability</b>, under a precise model-theoretic semantics.",
     "slide 2", short="Three OWL inference kinds + two diagnostics.")

g.qa("HIGH", "Contrast what OCL does with what an OWL reasoner does.",
     "OCL (Lectures 2-4) evaluates constraints over a <b>snapshot</b> (one object diagram): an invariant is true or "
     "false for the objects that are there. It does not derive new facts. An OWL reasoner computes <b>entailments</b> "
     "(facts that follow from the model, e.g. GrantPlinth hasParent MrPlinth from hasFather + subPropertyOf) and "
     "<b>classifies</b> instances and classes, and it reports inconsistent or unsatisfiable parts (e.g. a class that "
     "can never have instances).", "slide 2; L2-L4 (OCL)", short="OCL snapshot checking vs OWL entailment.")

g.qa("MED", "Why not simply model everything in OWL from the start?",
     "Because OWL is a <b>poor notation for compact, engineering-oriented diagrams</b>: the slide shows the same family "
     "model as a UML class/object diagram and as an OWL graph of rdfs:domain, rdfs:range, rdfs:subClassOf and rdf:type "
     "edges, which is much harder to read and author. UML also has the mature tooling.", "slide 2",
     short="Why not model in OWL directly?")

g.qa("LOW", "Which example domain runs through the whole talk?",
     "A <b>family history</b> model (after Stevens &amp; Stevens 2008, a family history knowledge base in OWL 2): "
     "Person, MalePerson, FemalePerson, hasFather, hasMother, hasParent, and the individuals GrantPlinth, MrPlinth, "
     "MrsPlinth, oldMrPlinth.", "slides 2, 7, 10-13", short="Running example of the talk.")

# ---------------------------------------------------------------- B
g.sec("B. Transformation-based bridging and its three problems")
g.qa("HIGH", "Explain transformation-based bridging (e.g. ODM) using the M-levels.",
     bullets([
         "At <b>M2</b> a <b>transformation definition</b> maps UML metaclasses to ODM/OWL metaclasses: UML "
         "<b>Class</b> -&gt; OWL <b>Class</b>, <b>Association</b> -&gt; <b>ObjectProperty</b>, "
         "<b>InstanceSpecification</b> -&gt; <b>Individual</b>. Both metamodels are instances of MOF Class (M3).",
         "At <b>M1</b> the <b>transformation execution</b> turns the UML model (Person, MalePerson, hasFather, "
         "GrantPlinth : MalePerson, ...) into an OWL ontology: classes and properties go to the <b>TBox</b>, instance "
         "specifications to the <b>ABox</b>.",
         "M0 holds the real GrantPlinth and MrPlinth.",
     ]) + "<br/>It is the same idea as an ATL transformation (L5): rules written against two metamodels, run on a "
     "model.", "slide 3; L5, L6", short="Transformation-based bridging (ODM) across M-levels.")

g.qa("HIGH", "State the three problems of transformation-based bridging that the talk identifies.",
     "(1) <b>A new maintenance-requiring artefact is created</b>: the generated OWL ontology is a second model that "
     "must be kept in sync with the UML model. (2) <b>Multiple ontological levels are not naturally supported</b>. "
     "(3) <b>The semantics of common modeling idioms/patterns are not supported</b> (e.g. a partitioning powertype).",
     "slides 3, 4, 5", short="Three problems of transformation-based bridging.")

g.qa("HIGH", "Explain the multiple-levels problem with the PersonType / MalePerson / GrantPlinth example.",
     "In a three-level model, " + p("PersonType", 2) + " sits at O0, Person and " + p("MalePerson", 1) +
     " : PersonType at O1, and GrantPlinth : MalePerson at O2. MalePerson is a <b>clabject</b>: it is a class (of "
     "GrantPlinth) <b>and</b> an instance (of PersonType). OWL has a two-way split: TBox (classes) and ABox "
     "(individuals). So the middle level is \"<b>TBox and/or ABox?</b>\": a classic UML-to-OWL transformation has no "
     "natural place for it.", "slide 4; L8 (clabjects)", short="Multiple-levels problem (TBox or ABox?).")

g.qa("HIGH", "Explain the modeling-idioms problem using the partition example.",
     "In the model, PersonType <b>partitions</b> Person into MalePerson and FemalePerson (a powertype whose instances "
     "are disjoint subclasses, L7). The intended meaning includes that MalePerson and FemalePerson are "
     "<b>disjoint</b>, i.e. OWL <b>disjointWith</b>. A naive class-to-class transformation only produces subClassOf "
     "and type triples, so this meaning is lost: <b>the semantics of the idiom is not supported</b>.",
     "slide 5; L7 (powertypes, generalization sets)", short="Modeling-idioms problem (partition = disjointness).")

# ---------------------------------------------------------------- C
g.sec("C. PAMoLa: the modelling substrate")
g.qa("HIGH", "What is PAMoLa? List its properties as given on the slide.",
     "<b>P</b>oly-<b>A</b>ligned <b>Mo</b>deling <b>La</b>nguage: <b>a graph-based modelling substrate for "
     "representing model content</b>. Properties:" + bullets([
         "self-describing", "level-agnostic", "homoiconic", "fixed set of nodes", "fixed set of edges",
         "each node can have a maximum of one of its allowed edges",
         "there can only be a maximum of one edge between any given pair of nodes",
     ]), "slide 6", short="What is PAMoLa + its listed properties.")

g.qa("MED", "Explain \"level-agnostic\" and \"homoiconic\" in this context.",
     "<b>Level-agnostic</b>: the same node types are used on every ontological level, so PersonType, Person and "
     "GrantPlinth are all Clabjects; the level comes from the type relationships and potency, not from different "
     "language concepts (same idea as LML in L8). <b>Homoiconic</b>: the model's content and its description use "
     "the same representation (the graph), so the model can be read and processed as data, e.g. as the facts the "
     "overlay rules run over. <i>(The slide lists the terms; these explanations follow L8 and the fact view on "
     "slide 8.)</i>", "slides 6, 8; L8", short="Level-agnostic and homoiconic.")

g.qa("MED", "Sketch the main concepts of the PAMoLa metamodel (slide 6).", T, "slide 6",
     short="Main concepts of the PAMoLa metamodel.",
     extra=[grid([
         ["Concept", "Specialises", "Key properties / meaning"],
         ["<b>Ordium</b>", "root", "hasName, hasFQN, hasPID, hasNote, hasCustodian (owner), follows, hasLinguisticType"],
         ["<b>Clabject</b>", "ImmanentOrdium", "hasPotency (default 0), hasDeclaredType; subclasses <b>Entity</b> "
          "(class/object) and <b>Relationship</b> (association/link, hasAssociationName)"],
         ["<b>Mediation</b>", "ImmanentOrdium", "hasRelatum (the clabject it points to); subclasses <b>Intercalation"
          "</b> (generalization end, isGeneralisation) and <b>Participation</b> (association end: hasRoleName, "
          "hasLowerBound, hasUpperBound, isOrdered, isUnique, isNavigableTo)"],
         ["<b>Categorisation</b>", "ImmanentOrdium", "a generalization set: isComplete, isDisjoint"],
         ["<b>Moment</b>", "ImmanentOrdium", "hasDurability, hasMutability; subclasses <b>Attribute</b> (hasDataType, "
          "hasValue) and <b>Method</b>"],
         ["<b>Marker</b>", "TranscendentOrdium", "hasTag, refersTo: e.g. tag subsetOf, role, partitions"],
         ["Literal, DataValue, DataType, Artifact", "TranscendentOrdium", "values and external artefacts"],
         ["Operation, Action, Atom, ...", "BehaviouralOrdium", "behaviour (not used in the scenarios)"],
     ], [38 * mm, 32 * mm, 100 * mm])])

g.qa("HIGH", "Which L8 concepts reappear in PAMoLa's metamodel?",
     bullets([
         "<b>Clabject</b> with <b>hasPotency</b>: the type/instance duality and deep instantiation from L8.",
         "<b>Moment</b> with <b>hasDurability</b> and <b>hasMutability</b>: the two attribute potencies of L8.",
         "<b>Categorisation</b> with isComplete / isDisjoint: the UML generalization-set constraints (L7).",
         "The <b>orthogonal classification architecture</b>: linguistic types (Entity, Participation, ...) vs "
         "ontological types (hasDeclaredType).",
     ]), "slides 6-8; L7, L8", short="L7/L8 concepts in the PAMoLa metamodel.")

g.qa("HIGH", "A PAMoLa model has multiple views. Name them.",
     "(1) <b>LML</b> (Level-agnostic Modeling Language) diagram with clabjects and potency; (2) <b>RDF Turtle</b> "
     "format (triples such as :EN2 :hasName \"PersonType\" ; :hasPotency 2); (3) <b>HUTN</b> (Human-Usable Textual "
     "Notation), a nested textual form. All are views of the same model.", "slide 7",
     short="The three views of a PAMoLa model.")

g.qa("MED", "Read the family model (slide 7, redrawn below). Give the potencies and explain them.",
     bullets([
         p("PersonType", 2) + " (O0): its instances (MalePerson, FemalePerson) are themselves types, which have "
         "instances (GrantPlinth): two levels of instances.",
         p("MalePerson", 1) + ", " + p("FemalePerson", 1) + " : PersonType (O1): instances of PersonType with one "
         "level of instances left.",
         p("Person", 0) + " (O1): no direct instances; it is the abstract superclass, as in L8 (Account<super>0"
         "</super>).",
         p("GrantPlinth", 0) + ", " + p("MrPlinth", 0) + " : MalePerson (O2): plain objects.",
     ]) + "<br/>The generalization set Male-Female (CA1) is complete and disjoint; hasFather and hasMother are marked "
     "{subsetOf hasParent}.", "slide 7; L8 (potency)", short="Potencies in the family model.",
     extra=[family_model()])

g.qa("MED", "In the HUTN of slide 7, how is the generalization Person &lt;- MalePerson, FemalePerson stored?",
     "As a <b>Categorisation</b> CA1 \"Male-Female\" with isComplete True, isDisjoint True, which owns three "
     "<b>Intercalations</b>: IC1 with isGeneralisation True and relatum EN3 (Person, the general end); IC2 and IC3 "
     "with isGeneralisation False and relata EN4 (MalePerson) and EN5 (FemalePerson). So a generalization is not one "
     "edge but a node (the set) with one end per participating class.", "slide 7",
     short="How a generalization is stored in PAMoLa (HUTN).")

g.qa("MED", "How is {subsetOf hasParent} on the hasFather end stored?",
     "As a <b>Marker</b> MK owned by the participation PA3 (role name hasFather) with hasTag subsetOf and refersTo "
     "PA1 (the end with role name hasParent). Markers are how PAMoLa records such idioms so that rules can give them "
     "meaning later.", "slide 7", short="How {subsetOf} is stored (Marker).")

# ---------------------------------------------------------------- D
g.sec("D. Orthogonal classification architecture and the fact view")
g.qa("HIGH", "Slide 8 shows the family model as facts. What does the fact view look like and why is it useful?",
     "Every model element becomes facts over the PAMoLa vocabulary, e.g." + ocl("""
Entity(Person).  Entity(MalePerson).  Categorisation(C1).
Intercalation(I1).  hasCustodian(I1, C1).  isGeneralisation(I1, False).
hasRelatum(I1, MalePerson).  isGeneralisation(I2, True).
hasRelatum(I2, Person).
Entity(GrantPlinth).  hasDeclaredType(GrantPlinth, MalePerson).
Relationship(R3).  hasDeclaredType(R3, R2).  Participation(P5).
hasCustodian(P5, R3).  hasRelatum(P5, MrPlinth).  hasRoleName(P5, hasFather).""") +
     "<br/>The facts describe the model in its <b>linguistic</b> terms (Entity, Participation, ...) while "
     "hasDeclaredType carries the <b>ontological</b> classification. Because it is plain data, rules can run over it "
     "(the base graph G_base).", "slide 8; L8 (orthogonal classification)", short="The fact view of a model.")

g.qa("HIGH", "Explain the rules on slide 8 that derive type and subClassOf, and derive the facts for the example.",
     ocl("""subClassOf(X, Y) :- hasSubUnit(S, X), hasCustodian(S, C),
                    hasCustodian(G, C), hasSuperUnit(G, Y).
subClassOf(X, Y) :- subClassOf(X, Z), subClassOf(Z, Y).
type(X, Y) :- hasDeclaredType(X, Y), Y != undefined.
type(X, Y) :- hasDeclaredType(X, Z), Z != undefined, subClassOf(Z, Y).""") +
     "<br/>Datalog style: head <b>:-</b> body, comma = and. Generalization ends in the same categorisation C link a "
     "sub and a super unit, so <b>subClassOf(MalePerson, Person)</b>. subClassOf is transitive. An element is of its "
     "declared type and of every superclass: <b>type(GrantPlinth, MalePerson)</b> and <b>type(GrantPlinth, Person)"
     "</b>.", "slide 8 (rules 2a, 2b, 3a, 3b)", short="Slide 8 rules for type and subClassOf, applied.")

g.qa("MED", "How is the model mapped onto the OWL TBox / ABox and the OWL vocabulary (slide 8)?",
     "The slide shows the mapping as a figure: entities used as types become OWL <b>Classes</b> and role ends of "
     "type-level associations become <b>Object Properties</b> (TBox; cf. rule 13 on slide 10: ObjectProperty(O) :- "
     "typeLevelParticipation(P), inducedProperty(P, O)); instances and links become ABox assertions. The model relationships map to OWL as: classification -&gt; "
     "<b>type</b>, generalization -&gt; <b>subClassOf</b>, {subsetOf} between ends -&gt; <b>subPropertyOf</b>. "
     "Unlike ODM, the mapping is not a transformation into a separate file but rules over the same model.",
     "slide 8", short="Mapping onto TBox/ABox (slide 8).")

# ---------------------------------------------------------------- E
g.sec("E. Endogenous overlays and the workflow")
g.qa("HIGH", "What is an endogenous OWL overlay? Contrast it with transformation-based bridging.",
     "The OWL facts are <b>derived by rules from the model itself</b> (the overlay graph G_owl sits on top of the "
     "base graph G_base) instead of being produced as a separate ontology by a transformation. Differences:" +
     bullets([
         "<b>No separate synchronised OWL artefact</b> to maintain: the model stays the <b>single source of truth"
         "</b>; the overlay can be recomputed at any time.",
         "The rules read PAMoLa's level-agnostic graph, so <b>multiple levels</b> (clabjects) can be handled.",
         "Rule modules give <b>idioms their meaning</b> (subsetOf -&gt; subPropertyOf, partitions -&gt; disjointWith).",
         "It is <b>lightweight and traceable</b>: every OWL fact comes from a rule applied to named model facts.",
     ]), "slides 3, 9, 14, 15", short="Endogenous overlay vs transformation-based bridging.")

g.qa("HIGH", "Describe the four-step execution workflow.",
     "(1) <b>Base graph</b>: the PAMoLa model G_base as a typed triple/fact view of the snapshot. (2) <b>Overlay "
     "rules</b>: choose a rule fragment R_k = <b>kernel plus optional modules</b>. (3) <b>Overlay facts</b>: execute "
     "R_k to compute the overlay graph G_owl. (4) <b>Reason</b>: an OWL reasoner returns <b>entailments and "
     "diagnostics</b>. Then the modeler <b>extends/updates the model manually</b> (e.g. adds an inferred link) and "
     "the loop starts again.", "slide 9", short="The four-step workflow.")

g.qa("MED", "Why is the model update after reasoning manual, and what happens when the rules run again?",
     "The reasoner's results are <b>suggestions</b> about the model; the modeler decides which to add, so the model "
     "remains the authoritative source. In scenario 1 the modeler adds the inferred hasParent link between "
     "GrantPlinth and MrPlinth to the model; running the overlay rules again then produces the <b>additionally "
     "generated assertion</b> GrantPlinth hasParent MrPlinth directly from the model.", "slides 9, 10, 12",
     short="Why the model update is manual.")

g.qa("MED", "Which tools were used, and for what?",
     "<b>Nemo</b> for rule-based reasoning (executing the overlay derivation rules) and <b>HermiT</b> for "
     "ontology-based reasoning (the OWL reasoner).", "slide 14", short="Tools used (Nemo, HermiT).")

# ---------------------------------------------------------------- F
g.sec("F. The four scenarios")
g.qa("HIGH", "Scenario 1 (role ends and subproperties). Model: hasFather {subsetOf hasParent}, GrantPlinth : "
     "MalePerson hasFather MrPlinth : MalePerson. What do the overlay rules generate and what does the reasoner infer?",
     "<b>Overlay assertions:</b> GrantPlinth rdf:type Person; MrPlinth rdf:type MalePerson; <b>hasFather "
     "rdfs:subPropertyOf hasParent</b>; GrantPlinth hasFather MrPlinth; MalePerson rdfs:subClassOf Person; hasParent "
     "rdf:type owl:ObjectProperty.<br/><b>Reasoner infers:</b> GrantPlinth <b>hasParent</b> MrPlinth "
     "(sub-property: every hasFather pair is a hasParent pair). After the modeler adds the link, the rules "
     "generate it as an assertion as well.", "slide 10", short="Scenario 1: role ends and subproperties.")

g.qa("MED", "Which overlay rule produces hasFather subPropertyOf hasParent? Read it.",
     ocl("""subPropertyOf(X, Y) :- Participation(P), Participation(Q),
    hasRoleName(P, X), Marker(M), hasCustodian(M, P),
    hasTag(M, subsetOf), refersTo(M, Q), hasRoleName(Q, Y).""") +
     "<br/>If end P (role name X) owns a marker with tag subsetOf that refers to end Q (role name Y), then X is a "
     "sub-property of Y. With P = PA3 (hasFather) and Q = PA1 (hasParent) this gives subPropertyOf(hasFather, "
     "hasParent).", "slide 10 (rule 1a); slide 7", short="Rule 1a (subsetOf -> subPropertyOf).")

g.qa("MED", "Rules 2, 3 and 4a on slide 10 derive subClassOf. Read them and apply them to the family model.",
     ocl("""generalises(C, Y)   :- Intercalation(I), hasCustodian(I, C),
                       isGeneralisation(I, True),  hasRelatum(I, Y).
specialisesIn(C, X) :- Intercalation(I), hasCustodian(I, C),
                       isGeneralisation(I, False), hasRelatum(I, X).
subClassOf(X, Y)    :- generalises(C, Y), specialisesIn(C, X).""") +
     "<br/>Categorisation CA1 generalises Person (IC1) and specialises in MalePerson (IC2) and FemalePerson (IC3), "
     "so subClassOf(MalePerson, Person) and subClassOf(FemalePerson, Person).", "slide 10 (rules 2, 3, 4a); slide 7",
     short="Rules 2/3/4a (generalization -> subClassOf), applied.")

g.qa("HIGH", "Scenario 2 (role classes, domain-based typing). Person has a Parent/Child self-association; «role» "
     "Mother is a subclass of Person; an unnamed end leads from Person (Child) to Mother; at O2, GrantPlinth : Person "
     "is linked to MrsPlinth : Person via the end Mother. What is generated and inferred?",
     "<b>Overlay assertions:</b> P3_MotherEnd subPropertyOf Parent; GrantPlinth P3_MotherEnd MrsPlinth; "
     "P3_MotherEnd domain Person; P3_MotherEnd <b>range Mother</b>; Child <b>inverseOf</b> Parent.<br/>"
     "<b>Reasoner infers:</b> MrsPlinth rdf:type <b>Mother</b> (from the range: she is classified although she was "
     "declared only as a Person), GrantPlinth Parent MrsPlinth (sub-property), MrsPlinth Child GrantPlinth "
     "(inverse).<br/>The unnamed role end gets a generated name (P3_MotherEnd) from the role class (rules 14-15b).",
     "slide 11", short="Scenario 2: role classes and domain-based typing.")

g.qa("MED", "In scenario 2, why does the overlay say P3_MotherEnd subPropertyOf Parent (rule 1b)?",
     ocl("""subPropertyOf(X, Y) :- inducedProperty(P, X), inducedProperty(Q, Y),
    sameNavigationFamily(P, Q), domain(X, D), domain(Y, D),
    range(X, A), range(Y, B), subClassOf(A, B), X != Y.""") +
     "<br/>Both properties start from the same class (domain Person, same navigation family), and the range of "
     "P3_MotherEnd (Mother) is a subclass of the range of Parent (Person). So the Mother end is a special Parent end. "
     "This is derived from structure, not from an explicit {subsetOf} marker.", "slide 11 (rules 1b, 16-19)",
     short="Rule 1b (structural subPropertyOf).")

g.qa("HIGH", "Scenario 3 (property chaining). Person has hasParent and hasGrandparent with hasGrandparent "
     "owl:propertyChainAxiom (hasParent hasParent). GrantPlinth hasParent MrPlinth, MrPlinth hasParent oldMrPlinth. "
     "What is inferred?",
     "The overlay generates GrantPlinth hasParent MrPlinth and MrPlinth hasParent oldMrPlinth; together with the chain "
     "axiom (model facts + overlay axiom) the reasoner infers <b>GrantPlinth hasGrandparent oldMrPlinth</b>. After "
     "the modeler adds the hasGrandparent link, the rules generate it as an additional assertion.", "slide 12",
     short="Scenario 3: property chaining.")

g.qa("HIGH", "Scenario 4 (partitioning powertypes, figure below). What does the overlay produce and what is the "
     "diagnostic? Explain it.",
     "<b>Overlay:</b> MalePerson, FemalePerson and MixedPerson rdf:type PersonType; Person partitionedBy PersonType; "
     "MalePerson <b>disjointWith</b> FemalePerson (both directions); MixedPerson subClassOf MalePerson and subClassOf "
     "FemalePerson.<br/><b>Diagnostic:</b> MixedPerson is a subclass of the intersection of MalePerson and "
     "FemalePerson, which is empty because they are disjoint, so <b>MixedPerson is unsatisfiable</b> (equivalent to "
     "owl:Nothing): it can never have an instance. The model contains a design error that plain UML tools would not "
     "report.", "slide 13; L7 (partition = complete + disjoint)",
     short="Scenario 4: partitioning powertypes and the diagnostic.", extra=[powertype_model()])

g.qa("MED", "Read the partition rules of scenario 4.",
     ocl("""partitionedBy(Base, PT) :- Categorisation(C), Marker(M),
    hasCustodian(M, C), hasTag(M, partitions), refersTo(M, PT),
    Intercalation(I), hasCustodian(I, C), isGeneralisation(I, True),
    hasRelatum(I, Base), isDisjoint(C, True), isComplete(C, True).
subClassOf(X, Base) :- partitionedBy(Base, PT), hasDeclaredType(X, PT).
type(X, PT)         :- partitionedBy(Base, PT), subClassOf(X, Base), X != Base.""") +
     "<br/>A complete and disjoint generalization set marked \"partitions PT\" makes Base partitioned by PT; every "
     "instance of PT is a subclass of Base; every proper subclass of Base is typed as an instance of PT (that is why "
     "MixedPerson rdf:type PersonType appears). Rule 23 then derives disjointWith between the specific classes of the "
     "partition.", "slide 13 (rules 22, 4c, 5d, 23)", short="Partition rules 22/4c/5d/23.")

g.qa("STRETCH", "Apply the approach yourself: add hasMother {subsetOf hasParent} and a link GrantPlinth hasMother "
     "MrsPlinth : FemalePerson to the family model. What would the overlay produce and the reasoner infer?",
     "Rule 1a gives <b>hasMother subPropertyOf hasParent</b>; rules 2-4a give FemalePerson subClassOf Person; rule 5 "
     "gives MrsPlinth type FemalePerson and type Person. The reasoner infers <b>GrantPlinth hasParent MrsPlinth</b>. "
     "If MrsPlinth were also declared a MalePerson, the disjointness from the partition would make the model "
     "<b>inconsistent</b> (an individual in two disjoint classes). <i>(My own exercise, same pattern as slides 10 "
     "and 13.)</i>", "slides 7, 10, 13 (exercise)", short="Own exercise: hasMother {subsetOf hasParent}.")

# ---------------------------------------------------------------- G
g.sec("G. Evaluation, conclusion, limitations")
g.qa("HIGH", "Summarise the evaluation.",
     bullets([
         "Validated on <b>four representative scenarios</b>.",
         "Tools <b>Nemo + HermiT</b> for rule-based and ontology-based reasoning.",
         "<b>No separate synchronised OWL artefact</b> required.",
         "<b>Successful inference and diagnostic generation</b> (new knowledge inferred, inconsistencies identified).",
     ]), "slide 14", short="Evaluation (four points).")

g.qa("MED", "What future directions does the conclusion name?",
     "The same authoritative model should feed other targets: <b>projections</b> (SQL, GraphQL, SysML views "
     "generated from one model), <b>rules and materialisation</b> (rule execution over fact views, derived results "
     "folded back) and <b>multi-level reach</b> (reasoning and overlays across classification levels, not one). "
     "Overall claim: a lightweight, traceable bridge between UML-style modeling and OWL reasoning that keeps the "
     "original model as the <b>single source of truth</b>.", "slide 15", short="Conclusion and future scope.")

g.qa("STRETCH", "Name limitations of the work as presented.",
     bullets([
         "Validation is by <b>four demonstration scenarios</b>, not a larger case study or performance measurement.",
         "Feeding inferences back into the model is a <b>manual</b> step.",
         "Multi-level reasoning is still listed as <b>future scope</b> (\"across classification levels, not one\"), so "
         "the level problem of slide 4 is only partly addressed.",
         "Each idiom needs its own <b>rule module</b>; idioms without rules get no OWL meaning.",
     ]) + "<i>(My reading of slides 9, 14, 15; the slides do not have a limitations section.)</i>",
     "slides 9, 14, 15", short="Limitations (own reading).")

# ---------------------------------------------------------------- H
g.sec("H. Connections to earlier lectures")
g.qa("HIGH", "Relate this lecture to L8 (deep modeling).",
     "The multiple-levels problem (slide 4) is the L8 problem: <b>Breed/Poodle/Fido</b> = <b>PersonType/MalePerson/"
     "GrantPlinth</b>. PAMoLa uses L8's answers: <b>clabjects</b> with <b>potency</b> (PersonType<super>2</super>), "
     "attribute <b>durability/mutability</b> (Moment), the <b>LML</b> notation, and the <b>orthogonal "
     "classification architecture</b> (linguistic types such as Entity vs ontological hasDeclaredType).",
     "slides 4, 6-8; L8", short="Connection to L8 deep modeling.")

g.qa("HIGH", "Relate this lecture to L7 (powertypes and generalization sets).",
     "PersonType is a <b>powertype</b> of Person: its instances (MalePerson, FemalePerson) are subclasses of Person. "
     "The generalization set is <b>{complete, disjoint}</b>, i.e. a <b>partition</b>. In UML these are just "
     "annotations; the overlay turns <b>disjoint</b> into owl:disjointWith so the reasoner can detect MixedPerson as "
     "unsatisfiable.", "slides 5, 7, 13; L7", short="Connection to L7 powertypes.")

g.qa("MED", "Relate this lecture to OCL (L2-L4) and to transformations (L5-L6).",
     "<b>OCL</b>: could express a check like \"no object is both a MalePerson and a FemalePerson\" for a given "
     "snapshot, but would not detect that the <b>class</b> MixedPerson can never have instances, and would not derive "
     "hasParent from hasFather. <b>Transformations</b>: ODM bridging is an M2-level model transformation like ATL "
     "(L5), with the MDA drawback that the generated model is a second artefact (L6). The overlay replaces it by "
     "rules over the same model.", "slides 2, 3; L2-L6", short="Connection to OCL and transformations.")

# ---------------------------------------------------------------- J
g.sec("J. Slide details to be aware of")
g.qa("LOW", "Which details on the slides are inconsistent or misprinted?",
     bullets([
         "<b>Page numbers</b>: most slides say x/15, slide 8 says 8/18 and slide 15 says 15/18; the file has 16 pages.",
         "<b>Person's potency</b>: Person<super>0</super> on slides 7, 10, 13, but Person<super>1</super> on slides "
         "11 and 12.",
         "<b>Rule 5c</b> on slide 10 reads type(X, Y) :- type(X, T), type(T, Y). Read literally, in the slide 7 model "
         "(MalePerson : PersonType) it would make GrantPlinth an instance of PersonType, the type of its type, which "
         "the strict ontological levels of L8 rule out. None of the generated assertions on the slides shows such a "
         "fact, so do not quote it as a general principle.",
         "<b>Typos</b>: \"RDF Turte Format\" (slide 7), \"rdf:subclassOf\" and \"TBOx\" (slide 5), and \"Additionally "
         "Generatsd Assertion\" (slide 12).",
         "The file name says \"ECMFA paper\", but it contains the <b>talk slides</b>, not the paper text.",
     ]), "slides 5, 7, 8, 10-13, 15", short="Slide inconsistencies.")

g.self_test()
g.build()
