from guide_lib import *
from uml import Diagram

g = Guide("L8-DeepModeling-Questions.pdf", "MDD - Lecture 8: Deep Modeling - Exam question bank",
          "MDD Lecture 8 - Exam Questions")
T = "See the table below."


def p(name, pot):
    """Potency as superscript in paragraph text: p('Car', 2) -> Car^2."""
    return f"{name}<super>{pot}</super>"


def vbar(dg, keys, parent, y):
    """Shared-target generalization: children (keys) to parent box, horizontal bar at height y."""
    xs = [dg.pt(k, "top")[0] for k in keys]
    for k, x in zip(keys, xs):
        dg.line([dg.pt(k, "top"), (x, y)])
    px = dg.pt(parent, "bottom")[0]
    dg.line([(min(xs + [px]), y), (max(xs + [px]), y)])
    dg.line([(px, y), dg.pt(parent, "bottom")], head="hollow")


# ---------------------------------------------------------------- diagrams
def account_deep():
    dg = Diagram(170 * mm, 215)
    dg.box("at", 170, 200, "AccountType^2", ["TaxCode^2 = TX00^1", "TypeIntroductionDate^1"], w=150)
    dg.level(158, "")
    dg.box("acc", 205, 150, "Account^0", ["balance^1"], w=80)
    dg.box("ca", 25, 92, "CheckingAccount^1:AccountType", ["TypeIntroductionDate^0 = 11/6/2003", "TaxCode^1 = TX34^0"],
           w=190)
    dg.box("sa", 265, 92, "SavingsAccount^1:AccountType", ["TypeIntroductionDate^0 = 1/1/2000", "TaxCode^1 = TX54^0"],
           w=190)
    vbar(dg, ["ca", "sa"], "acc", 106)
    dg.text(250, 109, "AccountType (generalization set)")
    dg.level(46, "")
    dg.box("c7", 25, 38, "CA776^0:CheckingAccount", ["TaxCode^0 = TX34", "balance = 2000"], w=190)
    dg.box("s3", 265, 38, "SA342^0:SavingsAccount", ["balance = 500", "TaxCode^0 = TX54"], w=190)
    return dg.drawing


def sheet8_q1():
    dg = Diagram(170 * mm, 200)
    dg.level(197, "O0")
    dg.box("lp", 10, 180, "LeafPattern^1", w=85)
    dg.box("ts", 195, 180, "TreeSpecies^2", w=95)
    dg.box("ga", 370, 180, "GeographicArea^2", w=105)
    dg.line([dg.pt("lp", "right"), dg.pt("ts", "left")])
    dg.text(98, 173, "1"); dg.text(186, 173, "1"); dg.text(120, 162, "leafPattern")
    dg.line([dg.pt("ts", "right"), dg.pt("ga", "left")])
    dg.text(294, 173, "*"); dg.text(356, 173, "1..*"); dg.text(298, 162, "generalLocations")
    dg.level(148, "O1")
    dg.box("tree", 205, 135, "Tree^1", w=75)
    dg.box("al", 345, 135, "actualLocation^1:GeographicArea", w=135)
    dg.line([dg.pt("tree", "right"), dg.pt("al", "left")])
    dg.text(284, 128, "*"); dg.text(330, 128, "1"); dg.text(292, 118, "actualLocation")
    xs = [5, 125, 245, 365]
    sp = ["SugarMaple", "Apricot", "AmericanElm", "Saguaro"]
    leaf = ["Monolayered", "lanceolate", "ovate-oblong", "spines"]
    for n, x in zip(sp, xs):
        dg.box(n, x, 85, n + "^1:TreeSpecies", w=112)
    vbar(dg, sp, "tree", 100)
    for n, l, x in zip(sp, leaf, xs):
        dg.box(l, x, 35, l + "^0:LeafPattern", w=112)
        dg.line([dg.pt(n, "bottom"), dg.pt(l, "top")])
    return dg.drawing


def sheet8_q2():
    dg = Diagram(170 * mm, 372)
    dg.level(370, "O0")
    dg.box("vc", 160, 358, "VehicleCategory^3", ["!launchDate^2 : String", "!constructionDate^3 : String"], w=160)
    dg.level(312, "O1")
    dg.box("ac", 175, 302, "!AbstractCategory^0", ["price^2 : Integer"], w=130)
    dg.box("tr", 60, 250, "Truck^2:VehicleCategory", ["!launchDate^1 : String", "constructionDate^2 : String"], w=160)
    dg.box("car", 260, 250, "Car^2:VehicleCategory", ["!launchDate^1 : String", "!constructionDate^2 : String"],
           w=160)
    vbar(dg, ["tr", "car"], "ac", 262)
    dg.level(203, "O2")
    dg.box("veh", 200, 194, "!Vehicle^0", ["colour^1 : String"], w=80)
    dg.box("fe", 5, 142, "Ferrari^1:Car", ["!launchDate^0 = Dec 95", "price^1 = 1000000^0", "!constructionDate^1 : String",
                                           "!colour^1 = Red^0"], w=150)
    dg.box("vw", 165, 142, "VWGolf^1:Car", ["!launchDate^0 = March 69", "price^1 = 23000^0",
                                            "!constructionDate^1 : String"], w=150)
    dg.box("ff", 325, 142, "FordFiesta^1:Car", ["!launchDate^0 = June 74", "price^1 = 18000^0",
                                                "!constructionDate^1 : String"], w=150)
    vbar(dg, ["fe", "vw", "ff"], "veh", 154)
    dg.level(66, "O3")
    dg.box("f6", 5, 56, "F64646^0:Ferrari", ["!price^0 = 1000000", "!constructionDate^0 = Jan 05", "!colour^0 = Red"],
           w=150)
    dg.box("v2", 165, 56, "VW2324^0:VWGolf", ["!price^0 = 23000", "!constructionDate^0 = Dec 05", "!colour^0 = Blue"],
           w=150)
    dg.box("f3", 325, 56, "F3434^0:FordFiesta", ["!price^0 = 18000", "!constructionDate^0 = Oct 09",
                                                 "!colour^0 = Black"], w=150)
    return dg.drawing


def sheet8_q3():
    dg = Diagram(170 * mm, 232)
    dg.level(230, "O0")
    dg.box("hp", 155, 220, "!HighProfileProfession^2", ["pay^2 : Integer", "typicalRateOfPay^1 : Integer"], w=170)
    dg.level(173, "O1")
    dg.box("pe", 200, 164, "!Person^0", ["age^1 : Integer"], w=80)
    dg.box("ac", 5, 112, "!Actor^1:HighProfileProfession", ["pay^1 : Integer", "typicalRateOfPay^0 = 500000"], w=150)
    dg.box("po", 165, 112, "!Politician^1:HighProfileProfession", ["!pay^1 : Integer", "!typicalRateOfPay^0 = 200000"],
           w=150)
    dg.box("as", 325, 112, "!Astronaut^1:HighProfileProfession", ["pay^1 : Integer", "typicalRateOfPay^0 = 65000"],
           w=150)
    vbar(dg, ["ac", "po", "as"], "pe", 124)
    dg.level(64, "O2")
    dg.box("th", 5, 54, "!TomHanks^0:Actor", ["pay^0 = 800000", "age^0 = 56"], w=150)
    dg.box("rr", 165, 54, "!RonaldReagan^0:Politician", ["pay^0 = 0", "age^0 = 102"], w=150)
    dg.box("na", 325, 54, "!NeilArmstrong^0:Astronaut", ["pay^0 = 0", "age^0 = 82"], w=150)
    return dg.drawing


# ---------------------------------------------------------------- intro
g.p("Lecture 8: Deep Modeling", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "slides 1-21 and Exercise Sheet 8.", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "Deep modeling (multi-level modeling) is the answer to a problem from Lectures 6-7: <b>where do domain metatypes "
    "such as powertypes go</b> in a strict level architecture? Expect: <b>define</b> strict metamodeling, clabject, "
    "linguistic vs ontological classification, potency/durability/mutability; <b>read and complete deep models</b> "
    "with potencies (Sheet 8 is exactly that).",
    "In the diagrams, superscripts are potencies: " + p("Car", 2) + " is a clabject with potency 2; "
    + p("price", 1) + " = 1000000<super>0</super> is an attribute with durability 1 whose value has mutability 0. "
    "<font color='#B42318'>Red</font> marks what the tutorial solution added.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "Classic OMG architecture: <b>M3</b> meta-metamodel (MOF), <b>M2</b> metamodel (UML), <b>M1</b> model, <b>M0</b> "
    "user objects. <b>Strict metamodeling</b>: every element is an instance of exactly one element one level up, and "
    "every other relationship stays within one level.",
    "Problem: a domain type of types (Breed, a powertype) has no proper place: Breed, Poodle and Fido would need three "
    "<b>domain</b> levels inside M1.",
    "<b>Multi-level modeling</b> separates two orthogonal classifications: <b>linguistic</b> (every model element is an "
    "instance of the language concept <b>Clabject</b>) and <b>ontological</b> (Fido instanceOf Poodle instanceOf Breed). "
    "Strictness holds in each dimension.",
    "A <b>clabject</b> (class + object) has both a <b>type facet</b> and an <b>instance facet</b>: Poodle has "
    "catalogId = \"0815\" (as an object of Breed) and age : Integer (as a class of Fido).",
    "<b>Deep instantiation</b> uses <b>potency</b> (non-negative integer): an instance has a potency one lower than its "
    "type. Three kinds: <b>clabject potency</b> (levels of instances), <b>durability</b> (levels an attribute "
    "survives), <b>mutability</b> (levels a value may still change). <b>Mutability must not exceed durability.</b>",
    "Potency 0 on a clabject = no instances = <b>abstract class</b> (with subclasses) or a plain object.",
    "<b>LML</b> (Level-agnostic Modeling Language) and the Eclipse tool <b>Melanee</b> support this; connections and "
    "generalizations are first-class.",
]))

g.p("Cheat sheet: potency", "h1")
g.add(grid([
    ["Kind", "Attached to", "Meaning", "Example"],
    ["<b>Potency</b>", "clabject", "over how many levels it may have instances", p("VehicleCategory", 3) +
     ": instances down to O3"],
    ["<b>Durability</b> (feature potency)", "attribute / method", "over how many levels it is present in instances",
     p("launchDate", 2) + " at O0: present at O1, O2, not O3"],
    ["<b>Mutability</b> (value potency)", "attribute value", "over how many levels it may be changed from the default",
     "Red<super>0</super>: fixed, instances cannot change it"],
], [32 * mm, 26 * mm, 56 * mm, 56 * mm]))
g.add(Spacer(1, 4))
g.add(grid([
    ["Rule", "Consequence"],
    ["instance potency = type potency - 1", p("Car", 2) + " : VehicleCategory<super>3</super>; "
     + p("Ferrari", 1) + " : Car; " + p("F64646", 0) + " : Ferrari"],
    ["feature durability drops by 1 per instantiation", p("pay", 2) + " in HighProfileProfession, " + p("pay", 1) +
     " in Actor, " + p("pay", 0) + " = 800000 in TomHanks"],
    ["mutability &lt;= durability", p("price", 3) + " = 0<super>4</super> is <b>invalid</b> (slide 19)"],
    ["potency 0 on a clabject", "no instances: an object, or an <b>abstract</b> class (Account<super>0</super>, "
     "Person<super>0</super>)"],
    ["potency and level are independent", "Account<super>0</super> sits on the middle level, Person<super>0</super> on O1"],
], [55 * mm, 115 * mm]))
g.add(PageBreak())

# ---------------------------------------------------------------- A
g.sec("A. Classic level architectures and strict metamodeling")
g.qa("HIGH", "Describe the UML 1.x four-layer model infrastructure with an example for each layer.", T, "slide 2",
     short="UML 1.x four layers M3-M0 with descriptions and examples.",
     extra=[grid([
         ["Layer", "Description", "Example"],
         ["<b>M3</b> meta-metamodel", "infrastructure for a metamodeling architecture; defines the language for "
                                      "specifying metamodels", "MetaClass, MetaAttribute, MetaOperation"],
         ["<b>M2</b> metamodel", "an instance of a meta-metamodel; defines the language for specifying a model",
          "Class, Attribute, Operation, Component"],
         ["<b>M1</b> model", "an instance of a metamodel; defines a language to describe an information domain",
          "StockShare, askPrice, sellLimitOrder, StockQuoteServer"],
         ["<b>M0</b> user objects (user data)", "an instance of a model; defines a specific information domain",
          "&lt;Acme_Software_Share_98789&gt;, 654.56, sell_limit_order, &lt;Stock_Quote_Svr_32123&gt;"],
     ], [35 * mm, 75 * mm, 60 * mm]), Spacer(1, 4),
         Paragraph("Link to Lecture 6: metalanguage (MOF) = M3, language = M2, PIM = M1.", S["small"])])

g.qa("HIGH", "Explain the UML 2.x infrastructure figure (slide 3). What question does it leave open?",
     bullets([
         "<b>M0</b>: the real-world elements (subject of the model), e.g. <b>aVideo</b>, a run-time instance.",
         "<b>M1</b>: the model representation of <b>types and instances</b>: class <b>Video</b> (+title : String) and an "
         "object <b>:Video</b> (title = \"2001: A Space Odyssey\"), related by «snapshot».",
         "<b>M2</b>: the <b>linguistic types</b> of the M1 elements: Attribute, Class, Instance (Instance has a "
         "classifier Class).",
         "<b>M3</b>: the meta-metamodel (MOF) with Class.",
     ]) + "<br/>Every element is «instanceOf» an element one level up. Note that M1 already holds both a type "
     "and an instance, so domain classification (\":Video is a Video\") happens <b>inside</b> M1, not across levels. "
     "The highlighted arrow from UML's Class to MOF's Class is a <b>generalization across levels</b>.<br/><b>Open "
     "question (the slide's punchline):</b> how are <b>domain meta types such as powertypes</b> modeled, and on which "
     "level do they go? Breed (a type of Poodle) would need a level above Poodle, but both are domain types in M1.",
     "slide 3", short="UML 2.x infrastructure figure; the open question about powertypes.")

g.qa("HIGH", "State the classic definition of strict metamodeling and its three consequences. <i>(Learn the "
     "definition.)</i>",
     "\"In an n-level modeling architecture M<sub>0</sub>, M<sub>1</sub> ... M<sub>n-1</sub>, <b>every element of an "
     "M<sub>m</sub> level model must be an instance-of exactly one element of an M<sub>m+1</sub> level model</b>, for "
     "all m &lt; n-1, and <b>any relationship other than the instance-of relationship between two elements X and Y "
     "implies that level(X) = level(Y)</b>.\"<br/>Consequences:<br/>" + bullets([
         "every element has <b>exactly one type</b>, except the elements in the top level",
         "the <b>instance-of relationship defines the levels</b>",
         "model elements are allocated to levels according to their <b>position in the hierarchy of instance-of "
         "relationships</b>",
     ]), "slide 4", short="Strict metamodeling: definition and three consequences.")

g.qa("MED", "Does the UML 2.x figure (slide 3) satisfy strict metamodeling? Argue.",
     bullets([
         "The «instanceOf» arrows between levels are fine: each element has one type one level up.",
         "The <b>generalization</b> from UML::Class (M2) to MOF::Class (M3) is a non-instance-of relationship <b>across "
         "levels</b>, which the definition forbids (level(X) must equal level(Y)).",
         "Within M1, \":Video\" is ontologically an instance of \"Video\" although both sit on the same level; strict "
         "metamodeling only counts the <b>linguistic</b> instance-of, so this domain classification has no proper "
         "place. That is the motivation for separating linguistic and ontological levels.",
     ]) + "<i>(Argument is mine, based on the slide-4 definition.)</i>", "slides 3-4 (reasoning)",
     short="Does slide 3 satisfy strict metamodeling? (cross-level generalization, :Video).")

# ---------------------------------------------------------------- B
g.sec("B. Multi-level modeling and clabjects")
g.qa("HIGH", "What are linguistic and ontological classification? Explain the orthogonal classification architecture "
     "(slide 5).",
     "Multi-level modeling uses <b>two distinct forms of classification</b> in different, <b>orthogonal</b> "
     "dimensions, with <b>strict (meta)modeling in each dimension</b>:<br/>" + bullets([
         "<b>Linguistic</b> classification: what kind of <b>language element</b> something is. Levels L0 (language "
         "definition: <b>Clabject</b>), L1 (the user model), L2 (the real world). ProductType, Video and "
         "2001aSpaceOdyssey are all <b>linguistic instances of Clabject</b>.",
         "<b>Ontological</b> classification: <b>domain</b> classification <b>inside L1</b>, in levels O0, O1, O2: "
         "2001aSpaceOdyssey (director = \"Stanley Kubric\") instanceOf <b>Video</b> (director : String) instanceOf "
         "<b>ProductType</b>.",
         "L2 holds the real-world things the model elements represent (the concepts and the actual cassette).",
     ]) + "<br/>So the user can have <b>as many ontological levels as the domain needs</b>, while the language "
     "definition stays fixed and simple.", "slide 5", short="Linguistic vs ontological classification; orthogonal "
     "classification architecture.")

g.qa("MED", "What is the difference between the tool developer's view and the modeler's view (slide 6)?",
     bullets([
         "<b>Tool developer's view</b>: the <b>linguistic</b> levels are vertical (linguistic metamodel on top, the user "
         "model with Breed, Poodle, Fido and Dog in one layer, the real world below). The ontological instance-of "
         "arrows run <b>horizontally</b> inside the model layer.",
         "<b>Modeler's view</b>: the same picture <b>rotated by 90 degrees</b>: now the <b>ontological</b> levels are "
         "vertical (Breed above Poodle above Fido), which is how a domain modeler thinks; the linguistic metamodel is "
         "on the side.",
     ]) + "<br/>Same model, two viewpoints: the tool cares about the language, the modeler about the domain.",
     "slide 6", short="Tool developer's view vs modeler's view (rotated 90 degrees).")

g.qa("HIGH", "Is an element in the middle level (e.g. Poodle) a type or an instance? What follows for modeling "
     "languages?",
     "<b>It is both.</b> Poodle is an <b>instance</b> of Breed and a <b>type</b> of Fido.<br/>Consequences (slide 7):"
     "<br/>" + bullets([
         "there should be <b>as many logical levels as needed</b>, not just objects, classes and metaclasses",
         "but structural classifiers should be <b>unified</b>: recognise the <b>instance and type facets</b> of model "
         "elements, and treat the differences as special cases",
     ]) + "<br/>That unified element is the <b>clabject</b>.", "slide 7", short="Middle-level element: type or instance? "
     "Consequences.")

g.qa("HIGH", "What is a clabject? Explain its type/instance duality with Breed, Poodle and Fido.",
     "A <b>clabject</b> (<b>cla</b>ss + o<b>bject</b>) is a model element with two facets:<br/>" + bullets([
         "<b>Type (class) view</b>: attribute types and method types, e.g. Poodle's <b>age : Integer</b>, which its "
         "instances (Fido) must fill.",
         "<b>Instance (object) view</b>: attribute values and method instances, e.g. Poodle's <b>catalogId = "
         "\"0815\"</b>, which fills the attribute declared by its type Breed (catalogId : String).",
     ]) + "<br/>Chain: Breed (catalogId : String) to Poodle (catalogId = \"0815\"; age : Integer) to Fido : Poodle "
     "(age = 5).", "slide 8", short="Clabject; type/instance duality (Breed, Poodle, Fido).")

g.qa("HIGH", "Explain \"power types clarified\" (slide 9): how do Breed, Dog, Poodle and Collie relate?",
     bullets([
         "Ontological levels: <b>O2</b> Breed (catalogId : String); <b>O1</b> Dog (age : Integer), Poodle : Breed "
         "(catalogId = \"4711\", age : Integer), Collie : Breed (catalogId = \"0815\", age : Integer); <b>O0</b> Fido : "
         "Poodle (age = 7), Lassie : Collie (age = 5).",
         "Poodle and Collie are <b>instances of Breed</b> (one level up) <b>and subclasses of Dog</b> (same level). "
         "Breed is therefore the <b>powertype</b> of Dog, shown by the «powertype» arrow from Dog to Breed.",
         "Fido and Lassie are instances of Poodle/Collie and hence (indirectly) Dogs.",
     ]) + "<br/>Point: in a multi-level model the powertype simply sits <b>one ontological level above</b> the class it "
     "partitions, which UML's two-level model could not express cleanly (Lecture 7).", "slide 9",
     short="Power types clarified: Breed / Dog / Poodle / Collie / Fido levels.")

# ---------------------------------------------------------------- C
g.sec("C. Melanee and LML")
g.qa("LOW", "What is Melanee? Name its features.",
     "An <b>Eclipse plugin</b> (\"the deep-modeling domain-specific language workbench\") supporting:" + bullets([
         "multi-level modeling and clean, strict metamodeling",
         "a general-purpose UML-like modeling language (LML) and domain-specific languages: graphical, text-based, "
         "form-based, tabular",
         "fully embedded in <b>EMF</b>, so usable with <b>OCL, ATL, QVT</b>, ...",
         "real-time (meta) modeling, emendation support, support for traditional modeling technologies",
     ]), "slide 10", short="Melanee features.")

g.qa("HIGH", "What is LML, and how does it differ from UML?",
     bullets([
         "<b>Level-Agnostic Modeling Language</b>: a <b>general-purpose concrete syntax</b> for deep models.",
         "Keeps the <b>look and feel</b> of mainstream information modeling languages (UML, ERA, ...).",
         "<b>Uniform concepts across all ontological levels</b>: the same notation on every level.",
         "<b>Unifies classes and objects into clabjects</b>.",
     ]) + "<br/>In UML, Person (class) and Mike : Person (object) are linguistic instances of <b>different</b> "
     "metaclasses (Class vs InstanceSpecification); in LML both are linguistic instances of <b>Clabject</b>, on "
     "different ontological levels of a \"Person Deep Model\".", "slide 11", short="LML: purpose and difference to UML.")

g.qa("HIGH", "How does LML represent associations, links and association classes? What extra power does it have?",
     bullets([
         "Associations and links are one unified concept: <b>connections</b>.",
         "<b>Connections are clabjects</b>: they can have <b>attributes</b> and take part in <b>generalizations</b>; "
         "drawn in an <b>exploded</b> form (a hexagon, e.g. isEmployedBy between Person/employee and Company/employer "
         "0..1) or a compact <b>\"dotted\"</b> form.",
         "Because connections have attributes, they <b>automatically play the role of association classes</b> (Job "
         "with salary between Person * and Company 1..*).",
         "Connections can have <b>more than two participants</b> (Team, Player and Year in PlayedInYear), where UML "
         "needs the diamond notation for n-ary associations.",
     ]), "slides 12-13", short="LML connections; association classes; n-ary connections.")

g.qa("MED", "How does LML treat inheritance and generalization-set constraints?",
     bullets([
         "Inheritance relationships are <b>first-class citizens</b> (can also be shown in an exploded or "
         "\"visually insignificant\" form).",
         "The <b>name of the relationship usually identifies the discriminant</b>: Person is split by <b>Gender</b> "
         "(MalePerson, FemalePerson) and by <b>EmploymentStatus</b> (Employee).",
         "Constraints such as <b>disjoint</b> and <b>complete</b> are supported as <b>linguistic attributes</b> of the "
         "generalization.",
     ]) + "<br/>Link: discriminant and complete/disjoint are exactly the generalization-set ideas from Lecture 7 and "
     "Sheet 7 Q4.", "slide 14; L7 slides 16-20", short="LML inheritance: discriminant, disjoint/complete.")

g.qa("HIGH", "How are stereotypes and powertypes modeled in LML compared with UML?",
     "<b>Stereotypes</b> (slide 15): UML needs a profile, " + c("«Stereotype» Clock") + " extending "
     + c("«Metaclass» Class") + ", and a stereotyped element " + c("«Clock» AlarmClock") + " with "
     "tagged values. In LML the stereotype is just a clabject <b>Clock</b> on the upper level and <b>AlarmClock : "
     "Clock</b> is its ordinary instance below, with the tags as normal attribute values: <b>stereotyping is supported "
     "by metamodeling</b>.<br/><b>Powertypes</b> (slide 16): full, real-time metamodeling lets powertypes be modeled "
     "<b>naturally</b>: they are <b>ontological metaclasses whose instances are also subclasses</b>. AccountType sits on "
     "the upper level; CheckingAccount : AccountType and SavingsAccount : AccountType are its instances <b>and</b> "
     "subclasses of Account (generalization set named AccountType). No special powertype notation is needed.",
     "slides 15-16", short="Stereotypes and powertypes in LML vs UML.")

# ---------------------------------------------------------------- D
g.sec("D. Deep characterization, deep instantiation and potency")
g.qa("HIGH", "What is deep characterization, and why can't traditional (UML) classification express it?",
     bullets([
         "Usually a type only describes or governs its <b>direct</b> instances.",
         "Sometimes we want to constrain the properties of the <b>instances of an instance</b>: e.g. <b>every instance of "
         "a breed instance has an age</b> (Breed should say that Fido-like objects have an age).",
         "Such <b>transitive influences</b> cannot be expressed directly with traditional classification.",
         "In UML you must resort to workarounds: <b>constraints</b> (OCL), <b>powertypes</b>, <b>stereotypes</b>, ...",
     ]), "slide 17", short="Deep characterization; why UML needs workarounds.")

g.qa("HIGH", "What is deep instantiation? State its rules.",
     bullets([
         "A <b>simple mechanism supporting deep characterization</b>, more concise and powerful than the UML approaches.",
         "Feature properties are specified exactly with the notion of <b>potency</b>.",
         "It gives a simple but precise definition of instance-of over <b>multiple classification levels</b>:",
         "&nbsp;&nbsp;potency takes <b>non-negative integer</b> values;",
         "&nbsp;&nbsp;an <b>instance of a type always has a potency one lower than the type</b>.",
         "The <b>potency and the level of a clabject do not have to be the same</b>.",
     ]) + "<br/>Example: Breed<super>2</super> with age<super>2</super> : Integer. Poodle<super>1</super> : Breed then "
     "has age<super>1</super> : Integer (a type facet), and Fido<super>0</super> : Poodle has age<super>0</super> = 5 "
     "(a value). That is exactly \"every instance of a breed instance has an age\".",
     "slide 18", short="Deep instantiation: definition and rules; Breed/Poodle/Fido with potency.")

g.qa("HIGH", "Name and explain the three forms of potency, and the rule that relates two of them.",
     "Potency is a non-negative integer attached to <b>clabjects</b>, <b>features</b> (ontological attributes and "
     "methods) and <b>values</b>; it defines their \"power\" with respect to classification:<br/>" + bullets([
         "<b>Clabject potency</b>: over <b>how many levels it may have instances</b>.",
         "<b>Feature potency = durability</b>: over how many levels the feature is <b>expected to be present</b> in "
         "instances of the clabject.",
         "<b>Value potency = mutability</b>: over how many levels the value <b>may be changed from the default</b>.",
     ]) + "<br/><b>Rule: an attribute's mutability must be no greater than its durability.</b> (A value cannot remain "
     "changeable on levels where the attribute no longer exists.)", "slide 19",
     short="Three forms of potency; mutability <= durability.")

g.qa("HIGH", "Why is the crossed-out clabject on slide 19 (" + p("Breed", 2) + " with " + p("price", 3) +
     " : Integer = 0<super>4</super>) invalid?",
     "The value 0 has <b>mutability 4</b> but the attribute price has <b>durability 3</b>: mutability may never exceed "
     "durability, so the model is invalid. <i>(Also suspicious, though not stated on the slide: durability 3 on a "
     "clabject of potency 2. Its instances only reach two levels down, so a third level of price can never be "
     "used.)</i> A valid version would be e.g. " + p("price", 2) + " : Integer = 0<super>1</super>.",
     "slide 19", short="Why Breed^2 with price^3 = 0^4 is invalid.")

g.qa("HIGH", "Which UML concepts can potency express? Give the encoding for each.", T, "slide 20 (encodings: reasoning)",
     short="UML concepts expressed with potency (attribute, slot, static, abstract, default, tag).",
     extra=[grid([
         ["UML concept", "Potency encoding", "Example from the slides/tutorial"],
         ["attribute (in a class)", "feature with durability 1", p("balance", 1) + " in Account"],
         ["slot (value in an object)", "feature with durability 0 and a value", "balance = 2000 in CA776"],
         ["static / class-level variable", "durability 0 value <b>on the class itself</b>, declared one level up with "
          "durability 1", "TypeIntroductionDate<super>0</super> = 11/6/2003 on CheckingAccount"],
         ["abstract class", "clabject potency 0 with subclasses", "Account<super>0</super>, Vehicle<super>0</super>, "
                                                                   "Person<super>0</super>"],
         ["default value", "value with mutability &gt;= 1 (instances may change it)", "TaxCode<super>2</super> = "
                                                                                       "TX00<super>1</super>"],
         ["constant / frozen value", "value with mutability 0", "colour<super>1</super> = Red<super>0</super> in "
                                                                "Ferrari"],
         ["tags / tagged values", "attribute of the type (stereotype-like clabject) and its value in the instance",
          "Clock / AlarmClock : Clock (slide 15)"],
     ], [38 * mm, 70 * mm, 62 * mm]), Spacer(1, 4),
         Paragraph("Slide 20 lists the concepts (attributes/slots, tags/tagged values, static variables, abstract "
                   "classes, default values) and adds that potency also models more complex behaviour: "
                   "<b>durability</b> and <b>mutability</b>. The encodings are my explanation.", S["small"])])

g.qa("HIGH", "Explain every potency in the deep version of the account powertype example (slide 21).",
     "Diagram below (redrawn). Reading it top-down:<br/>" + bullets([
         p("AccountType", 2) + ": its instances (CheckingAccount, SavingsAccount) have instances themselves (CA776, "
         "SA342), so potency 2.",
         p("TaxCode", 2) + " = TX00<super>1</super>: present for two levels (account types and accounts); default TX00 "
         "that may be changed <b>one</b> level down.",
         "TypeIntroductionDate<super>1</super>: only the account <b>types</b> get a value (TypeIntroductionDate<super>0"
         "</super> = 11/6/2003 on CheckingAccount): a <b>class-level (static) variable</b>.",
         p("Account", 0) + ": <b>abstract</b>, no direct instances; " + p("balance", 1) + " gives every concrete account "
         "a balance (balance = 2000 in CA776).",
         p("CheckingAccount", 1) + " : AccountType: an instance of AccountType <b>and</b> a subclass of Account (the "
         "generalization set is named AccountType). " + p("TaxCode", 1) + " = TX34<super>0</super> fixes the tax code "
         "for all checking accounts.",
         p("CA776", 0) + " : CheckingAccount: an object; TaxCode<super>0</super> = TX34 (cannot differ, mutability 0), "
         "balance = 2000.",
     ]), "slide 21", short="Explain all potencies in the deep account example.", extra=[account_deep()])

# ---------------------------------------------------------------- E tutorial
g.sec("E. Tutorial: Exercise Sheet 8")
g.p("All three exercises: read the potencies, then fix or add them. Diagrams show the sample solution; "
    "<font color='#B42318'>red</font> = what the solution adds or changes.", "small")

g.qa("HIGH", "1. Model the Tree Species powertype example (UML specification, Lecture 7 slide 22) as a deep model.",
     "<b>Sample solution</b> (diagram below):<br/>" + bullets([
         "<b>O0</b>: " + p("TreeSpecies", 2) + " (its instances are species, whose instances are trees) with "
         "connections to " + p("LeafPattern", 1) + " (leafPattern, 1 : 1) and " + p("GeographicArea", 2) + " "
         "(generalLocations, * : 1..*).",
         "<b>O1</b>: " + p("Tree", 1) + " is the general class; the species " + p("SugarMaple", 1) + ", "
         + p("Apricot", 1) + ", " + p("AmericanElm", 1) + ", " + p("Saguaro", 1) + " are <b>instances of TreeSpecies "
         "and subclasses of Tree</b>, exactly the powertype pattern. Each species is linked to its leaf pattern "
         "(" + p("Monolayered", 0) + ", " + p("lanceolate", 0) + ", " + p("ovate-oblong", 0) + ", " + p("spines", 0) +
         ", all instances of LeafPattern).",
         "Tree has an " + p("actualLocation", 1) + " : GeographicArea, so each individual tree (O2, not drawn, potency 0) "
         "has an actual location.",
     ]) + "<br/>Compare: UML powertype (L7 slide 22), stereotype workaround (Sheet 7 Q3), deep model (here). Only the "
     "deep model makes the species ordinary objects <b>and</b> classes at the same time, on a proper level.<br/>"
     + careful("the sample solution writes \"generalLoactions\" (typo) and gives actualLocation the multiplicity 1..*, "
               "while the original model says every tree has exactly <b>1</b> actual location. Use 1."),
     "Exercise Sheet 8, Q1 (sample solution)", tut="8, Q1", short="Tree Species powertype as a deep model.",
     extra=[sheet8_q1()])

g.qa("HIGH", "2. Complete the vehicle model: (a) AbstractCategory and Vehicle are abstract; (b) O3 clabjects have no "
     "launchDate; (c) a Ferrari's colour must be Red and cannot be changed; (d) add constructionDate and price where "
     "necessary.",
     "<b>Sample solution</b> (diagram below), item by item:<br/>" + bullets([
         "<b>(a) abstract = potency 0</b>: " + p("AbstractCategory", 0) + " and " + p("Vehicle", 0) + ". They have "
         "subclasses but no direct instances.",
         "<b>(b)</b> " + p("launchDate", 2) + " on " + p("VehicleCategory", 3) + ": it lives in Truck/Car ("
         + p("launchDate", 1) + ") and gets a value in Ferrari, VWGolf, FordFiesta (" + p("launchDate", 0) + " = Dec "
         "95, ...), so <b>it is gone at O3</b>. Durability 2 = two levels below O0.",
         "<b>(c)</b> in Ferrari: " + p("colour", 1) + " : String = Red<super>0</super>. Durability 1 means every "
         "Ferrari object at O3 has a colour; <b>mutability 0</b> means it cannot change from Red "
         "(F64646 : colour<super>0</super> = Red).",
         "<b>(d)</b> " + p("constructionDate", 3) + " on VehicleCategory, " + p("constructionDate", 2) + " in Truck and "
         "Car, " + p("constructionDate", 1) + " in the car models, and a value at O3 (" + p("constructionDate", 0) +
         " = Jan 05). <b>price</b>: " + p("price", 2) + " on AbstractCategory is inherited by Car; the models give "
         "price<super>1</super> = 1000000<super>0</super>, so every O3 object gets " + p("price", 0) + " = 1000000, "
         "fixed.",
     ]) + "<br/>Check the clabject potencies: VehicleCategory<super>3</super>, Car<super>2</super>, Ferrari<super>1"
     "</super>, F64646<super>0</super>: each instance is exactly one lower. " +
     careful("the sample solution leaves FordFiesta's constructionDate without a durability; it must be "
             + p("constructionDate", 1) + " like in the other models, otherwise F3434 would have no construction date."),
     "Exercise Sheet 8, Q2 (sample solution)", tut="8, Q2",
     short="Vehicle deep model: abstract (potency 0), launchDate, fixed colour, constructionDate/price.",
     extra=[sheet8_q2()])

g.qa("HIGH", "3. Complete the profession model: (a) O2 clabjects cannot have instances; (b) Person is abstract; "
     "(c) add the missing clabject at O1.",
     "<b>Sample solution</b> (diagram below):<br/>" + bullets([
         "<b>(a)</b> TomHanks, RonaldReagan, NeilArmstrong get <b>potency 0</b> (no instances); consequently Actor, "
         "Astronaut and the new clabject at O1 have potency 1, and " + p("HighProfileProfession", 2) + " at O0.",
         "<b>(b)</b> " + p("Person", 0) + ": abstract, but its " + p("age", 1) + " is inherited by the professions "
         "and filled at O2 (" + p("age", 0) + " = 56).",
         "<b>(c)</b> RonaldReagan at O2 is typed by a profession that is missing at O1. Add "
         "<b>Politician</b><super>1</super> : HighProfileProfession with " + p("pay", 1) + " : Integer and "
         + p("typicalRateOfPay", 0) + " = a value (the solution uses 200000), as a subclass of Person.",
     ]) + "<br/>Durabilities: " + p("pay", 2) + " (declared at O0, a value at O2) and " + p("typicalRateOfPay", 1) +
     " (a value already at O1: a class-level value per profession, like a static variable).<br/>" +
     careful("the sample solution names the new clabject <b>Leader</b> and retypes RonaldReagan as \":Leader\", but the "
             "exercise types him \":Politician\". Use <b>Politician</b> so the given O2 model stays consistent "
             "(either is fine if you state it)."),
     "Exercise Sheet 8, Q3 (sample solution)", tut="8, Q3", short="Profession deep model: potencies, abstract Person, "
     "missing Politician.", extra=[sheet8_q3()])

# ---------------------------------------------------------------- F practice
g.sec("F. Practice")
g.p("My own exercises in the style of the slides and Sheet 8.", "small")

g.qa("HIGH", "Given " + p("Breed", 2) + " with " + p("catalogId", 1) + " : String and " + p("age", 2) +
     " : Integer, and Poodle : Breed, Fido : Poodle. Which potencies do Poodle and Fido have, and which attributes "
     "(with durability) appear in each?", T, "slides 8, 18-19 (exercise)",
     short="Trace potencies: Breed^2 / Poodle / Fido with catalogId^1 and age^2.",
     extra=[grid([
         ["Clabject", "Potency", "Attributes"],
         ["Breed", "2", p("catalogId", 1) + " : String, " + p("age", 2) + " : Integer (types)"],
         ["Poodle : Breed", "1", p("catalogId", 0) + " = \"0815\" (a value: instance facet); " + p("age", 1) +
          " : Integer (still a type: type facet)"],
         ["Fido : Poodle", "0", p("age", 0) + " = 5. <b>No catalogId</b>: its durability ran out at Poodle."],
     ], [35 * mm, 20 * mm, 115 * mm])])

g.qa("HIGH", "Which of these are invalid, and why?",
     bullets([
         "(a) " + p("Car", 2) + " : VehicleCategory<super>3</super> : <b>valid</b> (one lower).",
         "(b) " + p("Ferrari", 2) + " : Car<super>2</super> : <b>invalid</b>, an instance must be exactly one lower (1).",
         "(c) " + p("X", 0) + " : Y<super>0</super> : <b>invalid</b>, a potency-0 clabject has no instances.",
         "(d) " + p("price", 1) + " = 5<super>2</super> : <b>invalid</b>, mutability 2 exceeds durability 1.",
         "(e) " + p("Account", 0) + " on the middle level with subclasses: <b>valid</b>, potency and level are "
         "independent; this is an abstract class.",
         "(f) " + p("pay", 2) + " in a clabject of potency 1: <b>suspicious</b>; the attribute should not outlive the "
         "instances (my reading; not explicitly on the slides).",
     ]), "slides 18-19 (exercise)", short="Spot invalid potencies (6 cases).")

g.qa("HIGH", "Compare three ways to model a powertype: UML powertype notation, a stereotype, and a deep model.", T,
     "L7 slides 21-22, Sheet 7 Q3, L8 slides 9, 16, 21, Sheet 8 Q1 (comparison: mine)",
     short="Powertype three ways: UML, stereotype, deep model.",
     extra=[grid([
         ["", "UML powertype (L7)", "Stereotype (Sheet 7)", "Deep model (L8, Sheet 8)"],
         ["How", "class TreeSpecies + association + generalization set labelled \": Tree Species\"",
          "«stereotype» TreeSpecies extends Class; species classes stereotyped",
          "TreeSpecies<super>2</super> one level up; species are its instances and subclasses of Tree"],
         ["Species as objects?", "only implicitly (by the label)", "no, they are classes with tagged values",
          "<b>yes</b>, clabjects: object and class"],
         ["Strict levels?", "no: type and type-of-type on M1", "mixes language level and domain", "<b>yes</b>, "
                                                                                                 "ontological levels"],
         ["Deep characterization", "needs extra OCL", "needs extra OCL", "<b>potency</b> does it directly"],
     ], [30 * mm, 47 * mm, 45 * mm, 48 * mm])])

g.qa("MED", "Model in a deep model: a product type (e.g. Smartphone) defines a list price for all its products; each "
     "product (e.g. Pixel 9) has a release year; each physical item has a serial number. The list price is fixed per "
     "product.",
     "Three ontological levels:<br/>" + bullets([
         "O0: " + p("ProductType", 2) + " with " + p("releaseYear", 1) + " : Integer, " + p("listPrice", 1) +
         " : Real, " + p("serialNumber", 2) + " : String.",
         "O1: " + p("Pixel9", 1) + " : ProductType with releaseYear<super>0</super> = 2024, listPrice<super>0</super> = "
         "799, " + p("serialNumber", 1) + " : String.",
         "O2: " + p("item4711", 0) + " : Pixel9 with serialNumber<super>0</super> = \"A-123\".",
     ]) + "<br/>Durability 1 puts listPrice and releaseYear on the products only (class-level values); durability 2 puts "
     "serialNumber on the items. <i>(My own exercise; the slides use the same structure for ProductType / Video / "
     "2001aSpaceOdyssey.)</i>", "slides 5, 18-21 (exercise)", short="Model ProductType / product / item as a deep "
     "model.")

# ---------------------------------------------------------------- G errata
g.sec("G. Slide and solution details to be aware of")
g.qa("LOW", "Which details are inconsistent?",
     bullets([
         "<b>Level numbering:</b> slides 5 and 9 put the <b>most abstract</b> level at O2 and objects at O0; Sheet 8 "
         "puts the most abstract level at <b>O0</b> and objects at O2/O3. Use the numbering of the diagram you are "
         "given. Potency, not the level number, decides instantiation.",
         "<b>Slides 8 vs 9:</b> Poodle has catalogId \"0815\" on slide 8 but \"4711\" on slide 9 (where Collie has "
         "\"0815\").",
         "<b>Slide 15:</b> the LML values look swapped (startOperation : Operation = True, POSIXCompliant : Boolean = "
         "Start).",
         "<b>Slides 16 vs 21:</b> UML side {disjoint, incomplete}, LML side {complete; disjoint}.",
         "<b>Typos:</b> \"conection\", \"particpate\" (slide 12), \"EmploymentStaus\" (slide 14), \"Stanley Kubric\" "
         "(slide 5).",
         "<b>Sheet 8 solution:</b> \"generalLoactions\", actualLocation 1..* instead of 1, FordFiesta constructionDate "
         "without durability, Leader instead of Politician (see section E).",
     ]), "slides 5, 8, 9, 12, 14, 15, 16, 21; Exercise Sheet 8", short="Slide/solution inconsistencies.")

g.self_test()
g.build()
