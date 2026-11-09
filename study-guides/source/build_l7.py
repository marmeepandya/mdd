from guide_lib import *
from uml import Diagram

G = "\u00ab"; H = "\u00bb"


def sheet7_q1():
    dg = Diagram(170 * mm, 112)
    dg.box("cls", 20, 95, [G + "metaclass" + H, "Class"], w=90)
    dg.box("comp", 250, 105, [G + "stereotype" + H, "Component"], ["language : String"], w=140)
    dg.box("test", 250, 50, [G + "stereotype" + H, "Test"], ["tester : String", "testprocedure : String"], w=140)
    dg.line([dg.pt("comp", "left"), dg.pt("cls", "right", 0.7)], head="filled")
    cx = dg.pt("cls", "bottom")[0]
    dg.line([dg.pt("test", "left"), (cx, dg.pt("test", "left")[1]), dg.pt("cls", "bottom")], head="filled")
    dg.text(125, 101, "extension (filled arrowhead)")
    return dg.drawing


def sheet7_q2():
    dg = Diagram(170 * mm, 82)
    dg.box("crm", 30, 65, [G + "Test" + H, G + "Component" + H, "CRM"], w=100)
    dg.note("n", 230, 78, [G + "Component" + H, "language = 'Java'", G + "Test" + H, "tester = 'Gate'",
                           "testprocedure = 'Black Box'"])
    dg.line([dg.pt("crm", "right"), dg.pt("n", "left")], dashed=True)
    return dg.drawing


def sheet7_q3():
    dg = Diagram(170 * mm, 205)
    dg.text(0, 196, "Diagram 1: profile", 7.5, color=INK, font="Helvetica-Bold")
    dg.box("cls", 10, 180, [G + "metaclass" + H, "Class"], w=80)
    dg.box("ts", 160, 180, [G + "stereotype" + H, "TreeSpecies"], w=100)
    dg.box("lp", 360, 192, "LeafPattern", w=105)
    dg.box("gl", 360, 150, "GeographicLocation", w=105)
    dg.line([dg.pt("ts", "left"), dg.pt("cls", "right")], head="filled")
    y1, y2 = dg.pt("ts", "right", 0.75)[1], dg.pt("ts", "right", 0.25)[1]
    dg.line([dg.pt("ts", "right", 0.75), (330, y1), (330, dg.pt("lp", "left")[1]), dg.pt("lp", "left")],
            label="leaf pattern", label_at=(266, y1 + 3))
    dg.line([dg.pt("ts", "right", 0.25), (340, y2), (340, dg.pt("gl", "left")[1]), dg.pt("gl", "left")],
            label="general locations", label_at=(266, y2 - 9))
    dg.text(0, 118, "Diagram 2: model", 7.5, color=INK, font="Helvetica-Bold")
    dg.box("tree", 160, 105, "Tree", w=60)
    dg.box("gl2", 330, 105, "GeographicLocation", w=105)
    dg.line([dg.pt("tree", "right"), dg.pt("gl2", "left")], label="actual location",
            label_at=(240, dg.pt("tree", "right")[1] + 3))
    xs = [10, 125, 240, 355]
    for n, x in zip(["SugarMaple", "Apricot", "AmericanElm", "Saguaro"], xs):
        dg.box(n, x, 30, [G + "TreeSpecies" + H, n], w=100)
    bar = 55
    dg.line([(dg.pt("tree", "bottom")[0], bar), dg.pt("tree", "bottom")], head="hollow")
    dg.line([(xs[0] + 50, bar), (xs[-1] + 50, bar)])
    for x in xs:
        dg.line([(x + 50, 30), (x + 50, bar)])
    return dg.drawing


g = Guide("L7-StereotypesPowertypes-Questions.pdf", "MDD - Lecture 7: Stereotypes and Powertypes - Exam question bank",
          "MDD Lecture 7 - Exam Questions")
T = "See the table below."

g.p("Lecture 7: Stereotypes and Powertypes", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "slides 1-24 and Exercise Sheet 7 (the PSM of Exercise Sheet 1 also uses stereotypes and is linked here).", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "Two topics: <b>profiles/stereotypes</b> (how UML is customised for a platform or domain, the \"lightweight\" "
    "alternative to a new metamodel) and <b>generalization sets and powertypes</b> (how to classify classes).",
    "Likely question types: define profile / extension / stereotype / tagged value; <b>metamodeling approach vs profile "
    "approach</b>; optional vs required extension; <b>read or draw a profile</b> (EJB example); the four generalization-set "
    "constraints and their combinations; <b>identify the powertype</b> in a model and explain it.",
    "Exercise Sheet 7 (section E) asks you to <b>draw</b> profiles, stereotyped classes with tagged values, and a "
    "powertype expressed with a stereotype, and to <b>classify generalization sets</b>. Practise drawing them on paper.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "<b>Platforms</b> come in three granularities: generic (object, batch, dataflow), technology-specific (CORBA, "
    "J2EE), vendor-specific (Orbix, WebSphere, ...).",
    "A <b>profile</b> is a <b>lightweight</b> way to define a DSL by <b>extending</b> existing metaclasses; it cannot "
    "modify the metamodel (not a first-class extension mechanism).",
    "A <b>stereotype</b> extends a metaclass via an <b>extension</b> (an association with the effect of specialization; "
    "filled arrowhead). Its properties are <b>tags</b>; their values on a model element are <b>tagged values</b>.",
    "Extensions are <b>optional</b> (may apply) or <b>{required}</b> (every instance must carry the stereotype).",
    "<b>Generalization sets</b>: <b>disjoint/overlapping</b> (can an instance be in several subclasses?) and "
    "<b>complete/incomplete</b> (must every instance be in some subclass?).",
    "A <b>powertype</b> is a class whose <b>instances are subclasses</b> of another class (Tree Species: Apricot, "
    "Saguaro, ... are both its instances and subclasses of Tree).",
]))

g.p("Cheat sheet: notation", "h1")
g.add(grid([
    ["Notation", "Meaning"],
    ["«stereotype» Clock, filled arrowhead to «metaclass» Class", "extension: Clock extends "
     "metaclass Class (optional)"],
    ["same, with " + c("{required}") + " on the arrow", "required extension: every Class must be a Clock"],
    ["«Clock» StopWatch, or a clock icon, or both", "a class StopWatch with stereotype Clock applied"],
    ["«Creator, Clock» StopWatch", "several stereotypes applied to one element"],
    ["note: «Clock» OSVersion = \"3.32\" ...", "tagged values of the applied stereotype"],
    ["«profile» EJB (package)", "a profile: a package of stereotypes, constraints, enumerations"],
    [c("{disjoint, complete}") + " at a generalization", "generalization-set constraints"],
    [c(": PowerTypeName") + " at a generalization set", "the subclasses are instances of this powertype"],
], [80 * mm, 90 * mm]))
g.add(PageBreak())

g.sec("A. Platforms in MDA")
g.qa("MED", "Give examples of platforms in MDA at the three levels of granularity.", T, "slide 2",
     short="Generic, technology-specific and vendor-specific platform types.",
     extra=[grid([
         ["Level", "Platform", "Description"],
         ["<b>Generic</b>", "Object platform", "objects with interfaces; requests for services via operation invocations"],
         ["", "Batch platform", "independent programs, each running to completion before the next starts"],
         ["", "Dataflow platform", "streams of data flowing between processing nodes"],
         ["<b>Technology-specific</b>", "CORBA", "object platform for remote invocation and event styles"],
         ["", "CORBA Components", "object platform with a \"components and containers\" style"],
         ["", "J2EE", "Java-based object platform with a \"components and containers\" style"],
         ["<b>Vendor-specific</b>", "CORBA: Iona Orbix, Borland VisiBroker, ...", "concrete products"],
         ["", "J2EE: BEA WebLogic Server, IBM WebSphere, ...", "concrete products"],
     ], [40 * mm, 53 * mm, 77 * mm]), Spacer(1, 4),
         Paragraph("Why it matters: \"platform-independent\" is relative. A PIM can be independent of the vendor but "
                   "specific to a generic platform type (L1/Sheet 1: \"a certain degree of platform independence\").",
                   S["small"])])

g.sec("B. Profiles, extensions and stereotypes")
g.qa("HIGH", "What is a profile? What can and can't it do?",
     bullets([
         "Provides a <b>\"lightweight\" way of defining new domain-specific languages</b> as <b>extensions</b> of the "
         "concepts in existing metamodels.",
         "Allows the <b>metaclasses of an existing metamodel to be specialized (logically)</b> with additional "
         "information for a specific purpose.",
         "Defined in the <b>Infrastructure Library</b> (package Profiles, which depends on Core; Lecture 6).",
         "<b>Not a first-class extension mechanism</b>: profiles <b>do not allow existing metamodels to be modified</b>.",
         "Essentially a lightweight way of adapting an existing metamodel with constructs specific to a particular "
         "<b>domain, platform, or method</b>.",
     ]), "slide 3", short="What a profile is; what it can and cannot do.")

g.qa("HIGH", "Compare the \"heavyweight\" metamodeling approach with the \"lightweight\" profile approach.", T,
     "slides 3, 6 (comparison: reasoning)", short="Metamodeling (heavyweight) vs profile (lightweight) approach.",
     extra=[grid([
         ["", "Metamodeling approach", "Profile approach"],
         ["How", "define new metaclasses, e.g. " + c("Clock") + " as a <b>real subclass</b> of metaclass " + c("Class"),
          "define a <b>stereotype</b> " + c("Clock") + " that <b>extends</b> metaclass " + c("Class")],
         ["Metamodel", "<b>changed</b> (first-class extension)", "<b>unchanged</b>; only logically specialised"],
         ["Model level", c("MyClock : Clock") + " (an instance of the new metaclass)",
          "shown as «clock» MyClock; realised as " + c("MyClock : Class") + " linked to " +
          c("Clock : Stereotype")],
         ["Tools", "need a new language/tool", "any UML tool that supports profiles works"],
         ["Expressiveness", "full freedom", "limited: only add to existing metaclasses"],
     ], [32 * mm, 69 * mm, 69 * mm])])

g.qa("HIGH", "What is an extension? Explain required and non-required extensions.",
     bullets([
         "An extension indicates that the <b>properties of a metaclass are extended through a stereotype</b>.",
         "It is a <b>kind of association with the effect of specialization</b>: one end is an ordinary property tying "
         "the extension to the <b>class</b>; the other end ties it to the <b>stereotype</b> that extends the class.",
         "<b>Required</b> (" + c("{required}") + "): an instance of the stereotype must <b>always</b> be linked to an "
         "instance of the extended metaclass, so <b>every</b> instance of the metaclass <b>must</b> carry the stereotype. "
         "No unstereotyped instances are allowed.",
         "<b>Non-required (optional)</b>: an instance of the metaclass <b>can</b> be stereotyped but need not be; the "
         "stereotype can be linked at will and later <b>deleted at will</b>.",
     ]), "slides 4, 7", short="Extension; required vs optional extension.")

g.qa("HIGH", "What is a stereotype? What are tags (tag definitions) and tagged values?",
     bullets([
         "A stereotype <b>defines how an existing metaclass is extended</b>, which enables <b>platform- or domain-specific "
         "terminology or notation</b> beyond the base metaclass.",
         "Like a class, it may have <b>properties</b>, called <b>tag definitions</b> or <b>tags</b> (e.g. Clock: "
         + c("OSVersion, startOperation, POSIXCompliant") + ").",
         "When applied to a model element, the property values are called <b>tagged values</b> (e.g. "
         + c('OSVersion = "3.32"') + ").",
         "A stereotype is a <b>limited kind of metaclass</b>: it <b>cannot be used by itself</b>, only together with a "
         "metaclass it extends.",
         "Each stereotype may extend <b>one or more</b> classes through extensions, <b>as part of a profile</b>.",
     ]), "slide 5", short="Stereotype; tag definitions vs tagged values.")

g.qa("HIGH", "How is the extension relationship drawn, and how is the logical specialization Clock-of-Class simulated "
     "by a profile?",
     "At metamodel level, a <b>specialization</b> " + c("Clock") + " to " + c("Class") + " (hollow triangle) is simulated "
     "in a profile by an <b>extension</b>: " + c("«stereotype» Clock") + " with a line ending in a <b>filled "
     "(black) arrowhead</b> pointing to " + c("«metaclass» Class") + ".<br/>At model level:" + bullets([
         "metamodeling approach: " + c("MyClock : Clock"),
         "profile approach, representation: a class box " + c("«clock» MyClock"),
         "profile approach, realisation: " + c("MyClock : Class") + " linked to an instance " + c("Clock : Stereotype"),
     ]), "slide 6", short="Extension notation; how a profile simulates specialization (three model-level views).")

g.qa("MED", "How can stereotyped classes be represented? How are several stereotypes shown?",
     bullets([
         "With the <b>guillemet notation</b> in a regular class box (" + c("«Clock» StopWatch") + "), with a "
         "<b>domain-specific icon</b>, or a <b>mixture</b> of both.",
         "A stereotype can extend <b>more than one</b> metaclass (Clock extends Component and Class), and a class can have "
         "<b>more than one</b> stereotype.",
         "Several stereotypes: list them in one guillemet pair (" + c("«Creator, Clock» StopWatch") +
         ") or as separate icons.",
     ]), "slides 8-9", short="Representing stereotyped classes; multiple stereotypes.")

g.qa("HIGH", "How are tagged values represented and stored?",
     "<b>Shown</b> in a <b>note attached to the stereotyped class</b>, grouped per stereotype:<br/>" +
     ocl('«Clock»\nOSVersion = "3.32"\nstartOperation = "Click"\nPOSIXCompliant = True') +
     "<br/><b>Stored</b> as <b>attributes of the stereotype instances</b>: StopWatch is linked to an instance "
     + c(":Clock") + " holding these values (and to " + c(":Creator") + " for the second stereotype). This is the profile "
     "realisation from slide 6.", "slide 10", short="Representing and storing tagged values.")

g.qa("HIGH", "Explain the EJB profile (slide 11).",
     "A package " + c("«profile» EJB") + " containing:<br/>" + bullets([
         c("«stereotype» Bean") + " (abstract, italic) extends <b>Component</b> with " + c("{required}") +
         ": in this profile every Component must be a Bean.",
         c("Entity") + " and " + c("Session") + " are stereotypes <b>specialising</b> Bean; Session has a tag "
         + c("state : StateKind") + ", where " + c("«enumeration» StateKind") + " is stateless | stateful.",
         c("«stereotype» JAR") + " extends <b>Artifact</b>; " + c("Remote") + " and " + c("Home") + " extend "
         "<b>«metaclass» Interface</b>.",
         "Constraints as notes: <b>\"A component cannot be generalized or specialized.\"</b> and <b>\"A Bean must "
         "realize exactly one Home interface.\"</b>",
     ]) + "<br/>Point: a profile bundles <b>stereotypes, tags, enumerations and constraints</b> for one platform. "
     "Stereotypes can themselves be generalised (Bean to Entity/Session).", "slide 11", short="Explain the EJB profile.")

g.qa("MED", "The PSM in Exercise Sheet 1 uses " + c("<<JavaBean>>") + " and " + c("<<WebService>>") + ". How does that "
     "relate to profiles?",
     "Those are <b>stereotypes from a platform profile</b> (Java/web services). Applying them turns PIM classes "
     "(Robot, Arm, ...) into platform-specific classes (NaoRobot, ...) <b>without changing the UML metamodel</b>. The "
     "notes on that PSM (Java SE 1.7, LinkedList, serializable = true) work like <b>tagged values</b>. This is the "
     "typical MDA use of profiles: <b>the PSM language is UML plus a platform profile</b>.",
     "slides 3-10; Exercise Sheet 1, Q2", tut="1, Q2 (related)", short="Stereotypes in the Sheet 1 robot PSM.")

g.qa("MED", "What is the UML standard profile? Give examples.",
     "The UML <b>superstructure contains a set of predefined standard stereotypes</b>.", "slides 12-13",
     short="Standard profile: examples and what they apply to.",
     extra=[grid([
         ["Stereotype", "Applies to", "Meaning"],
         ["«Auxiliary»", "Class", "supports a more central («Focus») class, typically implementing "
                                            "secondary logic or control flow"],
         ["«BuildComponent»", "Component", "elements collected for system-level development (compilation, "
                                                     "versioning)"],
         ["«Create»", "Usage", "the client classifier creates instances of the supplier"],
         ["«Create»", "BehavioralFeature", "the feature creates an instance of its classifier"],
         ["«Derive»", "Abstraction", "the client can be computed from the supplier (may still be implemented, "
                                               "e.g. for efficiency)"],
         ["others (slide 12)", "", "Usage: Call, Instantiate, Responsibility, Send; BehavioralFeature: Destroy; Model: "
                                   "Metamodel, SystemModel; Class: Focus, Metaclass, ImplementationClass, Type, Utility"],
     ], [35 * mm, 40 * mm, 95 * mm])])

g.qa("LOW", "Name some published UML profiles.",
     "<b>OMG:</b> UML profiles for <b>CORBA</b>, <b>EDOC</b>, <b>EAI</b>, <b>MARTE</b> (real-time embedded systems), "
     "<b>QoS and Fault Tolerance</b>, and <b>SysML</b> (a UML extension). <b>ISO/IEC JTC1 SC7:</b> UML profile for "
     "<b>RM-ODP</b>.", "slide 14", short="Published UML profiles.")

g.qa("HIGH", "Practice: define a profile for a simple web platform with stereotypes " + c("Page") + " (extends Class, "
     "tag " + c("url : String") + ") and " + c("Controller") + " (extends Class). Why can't \"every class is a Page or a "
     "Controller\" be expressed by making both extensions {required}?",
     "Profile: " + c("«profile» Web") + " with " + c("«stereotype» Page") + " (tag " +
     c("url : String") + ") and " + c("«stereotype» Controller") + ", each with an extension (filled "
     "arrowhead) to " + c("«metaclass» Class") + ". Applied: " + c("«Page» Login") + " with tagged "
     "value " + c('url = "/login"') + ".<br/><b>Problem:</b> a required extension means <b>every</b> Class must carry "
     "<b>that</b> stereotype. Two required extensions would force every class to be both a Page <b>and</b> a "
     "Controller. \"Each class is one of the two\" cannot be said with {required}; it needs a <b>constraint</b> (e.g. in "
     "OCL), like the EJB profile's note constraints. <i>(My own exercise.)</i>", "slides 4-7, 11 (exercise)",
     short="Practice: design a small profile; why two required extensions fail.")

g.sec("C. Generalization and generalization sets")
g.qa("MED", "What is generalization (inheritance)? Which notations exist?",
     bullets([
         "A <b>taxonomic relationship</b> between a more general and a more specific class.",
         "Each instance of the specific class is also an <b>indirect instance</b> of the general class, so the specific "
         "class <b>inherits the features</b> of the general class.",
         "A generalization relates a specific class to a more general one and is <b>owned by the specific class</b>.",
         "Notation: <b>separate target</b> (one arrow per subclass) or <b>shared target</b> (arrows merged into one "
         "triangle).",
     ]), "slide 15", short="Generalization; ownership; separate vs shared target notation.")

g.qa("HIGH", "What is a generalization set? Define overlapping, disjoint, complete and incomplete.",
     "A <b>generalization set</b> is a set of generalization relationships describing <b>how a general class "
     "(superclass) may be partitioned</b>.", "slide 16", short="Generalization set; the four constraints.",
     extra=[grid([
         ["Constraint", "Meaning", "Question it answers"],
         ["<b>overlapping</b>", "instances of the general class <b>may</b> be instances of <b>more than one</b> specific class",
          "Can one object be in several subclasses?  Yes"],
         ["<b>disjoint</b>", "instances <b>may not</b> be instances of more than one specific class", "... No"],
         ["<b>complete</b>", "instances <b>must</b> be instances of <b>at least one</b> specific class",
          "Is every object in some subclass?  Yes"],
         ["<b>incomplete</b>", "instances <b>do not have to</b> be instances of any specific class", "... No"],
     ], [28 * mm, 82 * mm, 60 * mm])])

g.qa("HIGH", "Explain the four common combinations and give an example of each.", T,
     "slides 17-20 (examples for overlapping: mine)", short="The four combinations with examples.",
     extra=[grid([
         ["Combination", "Meaning", "Example"],
         [c("{complete, disjoint}"), "subclasses cover all instances, no common instances",
          "Person: MalePerson / FemalePerson (slide 20)"],
         [c("{incomplete, disjoint}"), "do not cover all instances, no common instances",
          "Fruit: Pear / Apple (other fruits exist); Apple: Golden Delicious / Cox / Macintosh (slide 18)"],
         [c("{complete, overlapping}"), "cover all instances, some common instances",
          "UniversityMember: Student / Employee (everyone is at least one; a working student is both)"],
         [c("{incomplete, overlapping}"), "do not cover all, some common instances",
          "Person: Musician / Athlete (many persons are neither, some are both)"],
     ], [40 * mm, 60 * mm, 70 * mm]), Spacer(1, 4),
         Paragraph("On slide 20 <b>Person</b> is in <i>italics</i>, i.e. <b>abstract</b>: no direct Person instances "
                   "exist, which fits {complete}. On slide 17 ({disjoint} only) Person is not italic.", S["small"])])

g.qa("HIGH", "Express {disjoint} and {complete} for Person / MalePerson / FemalePerson as OCL invariants.",
     ocl("-- complete: every person is in at least one subclass\ncontext Person\n"
         "inv complete: self.oclIsKindOf(MalePerson) or self.oclIsKindOf(FemalePerson)\n\n"
         "-- disjoint: no person is in both subclasses\ncontext Person\n"
         "inv disjoint: not (self.oclIsKindOf(MalePerson) and\n                   self.oclIsKindOf(FemalePerson))") +
     "<br/>" + c("oclIsKindOf") + " (Lecture 3) is the right operation: it is true for the class and its subclasses. "
     "This shows that generalization-set constraints are shorthand for OCL constraints, just like multiplicities "
     "(Lecture 2, slide 15). <i>(My own exercise linking to the OCL lectures.)</i>", "slides 16-20; L3 slide 27",
     short="Write {complete} and {disjoint} as OCL invariants.")

g.sec("D. Powertypes")
g.qa("HIGH", "What is a power type? Where does the name come from?",
     bullets([
         "A <b>power type is a class whose instances are subclasses of another class</b>; power types are therefore "
         "<b>metaclasses whose instances are also classes</b>.",
         "<b>X is a power type of Y if the instances of X are subclasses of Y.</b>",
         "Motivated by the <b>power set</b>: for a set S, the power set is the set of all subsets of S. A power set is a "
         "<b>set of sets</b>, just as a power type is a <b>type of types</b>.",
     ]) + "<br/>Notation (slide 21): the generalization set from the General Classifier to its specific classifiers is "
     "labelled " + c(": powertype classifier-1") + "; the powertype class is associated with the general classifier. One "
     "general classifier can have <b>several</b> powertypes, each partitioning it differently.",
     "slide 21", short="Power type: definition, power-set origin, notation.")

g.qa("HIGH", "Explain the Tree Species example (slide 22), including the instance picture.",
     bullets([
         "<b>Tree</b> has subclasses <b>Sugar Maple, Apricot, American Elm, Saguaro</b> with " +
         c("{disjoint, incomplete}") + " (other species exist; no tree is two species).",
         "<b>Tree Species</b> is the <b>powertype</b> of Tree: its instances <b>are</b> those subclasses. Every Tree "
         "has exactly one tree species (association tree * to 1 tree species).",
         "Properties of the <b>species</b> (shared by all trees of that kind): <b>general locations</b> (*) and <b>leaf "
         "pattern</b> (1). Property of an <b>individual tree</b>: its <b>actual location</b> (1).",
     ]) + "<br/><b>Instance picture</b> (right): at the top, Tree Species is a class. In the middle, Apricot and Saguaro "
     "are <b>instances</b> (dots) of Tree Species and at the same time <b>subsets</b> of the instances of Tree. At the "
     "bottom, individual trees (dots) lie inside the sets Saguaro and Apricot within Tree. So <b>Apricot is an object "
     "(of Tree Species) and a class (of trees)</b>.", "slide 22", short="Explain the Tree Species powertype example.")

g.qa("HIGH", "Why use a powertype instead of just subclasses or just an attribute?",
     bullets([
         "With <b>subclasses only</b>, you cannot attach data to the species itself (leaf pattern, general "
         "locations); you would have to repeat it in every tree or hard-code it in each subclass.",
         "With <b>an attribute/association only</b> (Tree to TreeSpecies), you lose the subclasses, so species-specific "
         "attributes or behaviour cannot be modelled.",
         "A powertype gives <b>both</b>: Apricot is a <b>subclass</b> of Tree (own features, inheritance) <b>and</b> an "
         "<b>object</b> of TreeSpecies (it has its own attribute values).",
     ]) + "<br/>This dual class/object nature is the starting point of <b>multi-level modeling</b> (PAMoLa, listed in "
     "the course overview in Lecture 1). <i>(Explanation is mine.)</i>", "slides 21-22 (reasoning)",
     short="Why powertypes (vs only subclasses or only an attribute).")

g.qa("HIGH", "Identify the powertype, the partitioned class and the subclasses in each slide example.", T,
     "slides 23-24", short="Identify powertype / general class / subclasses in 4 examples.",
     extra=[grid([
         ["General class (role)", "Powertype (role)", "Subclasses = instances of the powertype"],
         ["Disease Occurrence (classified disease, *)", "Disease Classification (disease classifier, 1)",
          "Chicken Pox, Measles"],
         ["Installed Telephone Service (installed service, *)", "Telephone Service Category (service category, 1)",
          "Call Waiting, Call Transferring"],
         ["Account (account, *)", "Account Type (account classifier, 1)", "Checking Account, Savings Account"],
         ["Vehicle (classified vehicle, *)", "Vehicle Type (vehicle category, 1)", "Truck, Car"],
     ], [60 * mm, 60 * mm, 50 * mm]), Spacer(1, 4),
         Paragraph("All four use " + c("{disjoint, incomplete}") + " and the label " + c(": <PowerType>") + ". Pattern: "
                   "<b>each X is classified by exactly one XType; the subclasses of X are instances of XType.</b>",
                   S["small"])])

g.qa("HIGH", "Practice: model cars and car models with a powertype. A car has a serial number and a colour; a car model "
     "(e.g. VW Golf, BMW 3) has a list price and a top speed.",
     bullets([
         "General class <b>Car</b> (serialNumber, colour) with subclasses <b>VWGolf</b>, <b>BMW3</b>, ... and " +
         c("{disjoint, incomplete}") + ".",
         "Powertype <b>CarModel</b> (listPrice, topSpeed), associated with Car: car " + c("*") + " to model " + c("1") +
         "; the generalization set is labelled " + c(": CarModel") + ".",
         "VWGolf is a <b>subclass</b> of Car (each Golf has its own serial number and colour) and an <b>instance</b> of "
         "CarModel (listPrice and topSpeed are stored once for all Golfs).",
     ]) + "<br/><i>(My own exercise.)</i>", "slides 21-24 (exercise)", short="Practice: Car / CarModel powertype.")

g.qa("MED", "Is a powertype the same as a stereotype? Compare.",
     bullets([
         "Both have something to do with <b>classes as instances</b>, but at different levels.",
         "A <b>stereotype</b> extends a <b>UML metaclass</b> (M2, e.g. Class); stereotyped model elements are still "
         "ordinary classes with extra tagged values. It customises the <b>modeling language</b>.",
         "A <b>powertype</b> is a <b>domain class</b> (M1) whose instances are other domain classes (Tree Species). It "
         "models <b>domain categories</b>, not language extensions.",
     ]) + "<br/><i>(Comparison is mine.)</i>", "slides 5, 21 (reasoning)", short="Powertype vs stereotype.")

g.sec("E. Tutorial: Exercise Sheet 7")
g.p("Legend for the diagrams: <b>filled</b> black arrowhead = <b>extension</b> (stereotype to metaclass); "
    "<b>hollow</b> triangle = generalization; dashed line = note attachment.", "small")

g.qa("HIGH", "1. Draw a diagram defining two extensions of the base Class with the stereotypes (a) Component (tag "
     + c("language : String") + ") and (b) Test (tags " + c("tester : String") + ", " + c("testprocedure : String") + ").",
     "Model answer drawn below.<br/>" + bullets([
         "Three boxes: " + c("«metaclass» Class") + " and two " + c("«stereotype»") + " boxes.",
         "Each stereotype has its tags as <b>attributes</b> (tag definitions).",
         "Each stereotype is connected to Class by an <b>extension</b>: solid line, <b>filled</b> arrowhead at the "
         "metaclass. Not a hollow generalization triangle.",
         "No " + c("{required}") + ": nothing says every class must carry the stereotype, so both extensions are "
         "<b>optional</b>.",
     ]), "slides 4-7, 9; Exercise Sheet 7, Q1 (sample solution)", tut="7, Q1",
     short="Draw extensions: stereotypes Component and Test extend Class.", extra=[sheet7_q1()])

g.qa("HIGH", "2. Draw a class CRM stereotyped by Component and Test, with tagged values Java, 'Gate' and 'Black Box' for "
     "language, tester and testprocedure.",
     "Model answer drawn below.<br/>" + bullets([
         "Both stereotypes on the class: two guillemet lines, or one list " + c("«Component, Test» CRM") +
         " (slide 9).",
         "The <b>tagged values</b> go in a <b>note</b> attached with a dashed line, <b>grouped by stereotype</b> "
         "(slide 10).",
         "Alternative (storage view, slide 10): CRM linked to an instance " + c(":Component") + " (language = 'Java') "
         "and an instance " + c(":Test") + " (tester = 'Gate', testprocedure = 'Black Box').",
     ]) + "<br/>" + careful("the sample solution writes 'Gates' and 'Black-Box'; the question says 'Gate' and "
                            "'Black Box'. Copy the values exactly as asked."),
     "slides 9-10; Exercise Sheet 7, Q2 (sample solution)", tut="7, Q2",
     short="Draw CRM with stereotypes Component and Test and its tagged values.", extra=[sheet7_q2()])

g.qa("HIGH", "3. Draw two diagrams capturing the Tree Species powertype example (slide 22) using stereotypes.",
     "<b>Diagram 1, the profile:</b> the powertype becomes a <b>stereotype</b> that extends Class; the species-level "
     "properties become associations/tags of the stereotype.<br/>"
     "<b>Diagram 2, the model:</b> Tree with its actual location; each species is a subclass of Tree "
     "<b>stereotyped</b> " + c("\u00abTreeSpecies\u00bb") + ". Both diagrams are drawn below.<br/>"
     "<b>Why it works:</b> a stereotype is a kind of metaclass (slide 5), so \"SugarMaple is a TreeSpecies\" is "
     "expressed by stereotyping the <b>class</b> SugarMaple. Its leaf pattern and general locations become its "
     "<b>tagged values</b>. <b>Limitation:</b> the species are no longer ordinary objects of a domain class, and the "
     "stereotype mixes language level and domain level. This is exactly the problem <b>deep modeling</b> (Lecture 8, "
     "Sheet 8 Q1) solves.", "slides 5, 21-22; Exercise Sheet 7, Q3 (sample solution)", tut="7, Q3",
     short="Draw the Tree Species powertype with a stereotype (profile + model).", extra=[sheet7_q3()])

g.qa("HIGH", "4. Describe the principle of generalization sets. What are they used for?",
     "<b>Official answer:</b> a generalization set is a set of generalization relationships that <b>group together</b> "
     "generalizations from a given class and <b>specialize the class with respect to a certain property or "
     "perspective</b>, called the <b>discriminant</b>.<br/>" + bullets([
         "<b>Complete</b>: every instance of the specialized (general) class is an instance of <b>at least one</b> "
         "subclass in the set.",
         "<b>Disjoint</b>: no (indirect) instance of the general class is an instance of <b>more than one</b> subclass; "
         "each instance is in <b>at most one</b> subclass.",
         "(Opposites: <b>incomplete</b> and <b>overlapping</b>; see section C.)",
     ]) + "<br/><b>Used for:</b> stating precisely how a class is partitioned. One class can have <b>several</b> "
     "generalization sets with different discriminants, e.g. Person by <i>gender</i> {complete, disjoint} and by "
     "<i>employmentStatus</i> (Lecture 8, slide 14). The name of the set usually names the discriminant.",
     "slide 16; Exercise Sheet 7, Q4 (sample solution); L8 slide 14", tut="7, Q4",
     short="Principle of generalization sets (discriminant, complete, disjoint).")

g.qa("HIGH", "5. For each example, state whether the generalization set is complete/incomplete and "
     "disjoint/overlapping.", "<b>Official answers</b>, with the reason that earns the marks:",
     "Exercise Sheet 7, Q5 (sample solution)", tut="7, Q5",
     short="Classify 4 generalization sets (Sportsman, Employee, Shape, Patient).",
     extra=[grid([
         ["General class: subclasses", "Answer", "Reason"],
         ["Sportsman: Squashplayer, Tennisplayer", "<b>incomplete, overlapping</b>",
          "more sports exist than squash and tennis; one person can play both"],
         ["Employee: Placement Student, Casual Employee, Fulltime Employee, Consultant", "<b>complete, overlapping</b>",
          "complete <b>under the assumption</b> that these are all job categories; a consultant can also be a "
          "fulltime employee"],
         ["Shape: Polygon, Ellipse, Spline", "<b>incomplete, disjoint</b>",
          "more shapes exist; a shape is not two of these at once"],
         ["Patient: Out-patient, In-patient", "<b>complete, disjoint</b>",
          "every patient is treated either as an in-patient or as an out-patient, not both"],
     ], [55 * mm, 35 * mm, 80 * mm]), Spacer(1, 4),
         Paragraph("Exam tip: always give <b>both</b> dimensions and <b>one sentence of reasoning</b>, and state your "
                   "assumption where the domain is ambiguous (the official Employee answer does exactly this). "
                   "Patient is only disjoint <i>at a given moment</i>: the same person can be an in-patient now and an "
                   "out-patient later.", S["small"])])

g.sec("F. Slide details to be aware of")
g.qa("LOW", "Which slide details are inconsistent?",
     bullets([
         "<b>Slide 10:</b> the stereotype Creator defines " + c("author, date") + " (slide 9) but the tagged values say "
         + c("Name, Date") + "; the last row reads " + c('Date = "04-04-20" = True') + " (copy-paste slip).",
         "<b>Slide 5:</b> \"how an existing metaclass has be extended\" means \"has to be / is\" extended.",
         "<b>Slide 2:</b> \"flow of streams data\" means the flow of streams of data.",
     ]), "slides 2, 5, 9, 10", short="Slide typos/inconsistencies.")

g.self_test()
g.build()
