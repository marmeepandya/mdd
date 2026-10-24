import math
from guide_lib import *
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon

g = Guide("L1-Introduction-Questions.pdf", "MDD - Lecture 1: Introduction - Exam question bank",
          "MDD Lecture 1 - Exam Questions")


def mda_diagram():
    d = Drawing(170 * mm, 66 * mm)
    W = 170 * mm

    def box(x, y, w, h, label, fill, fg=INK):
        d.add(Rect(x, y, w, h, fillColor=fill, strokeColor=TEAL, strokeWidth=0.8, rx=3, ry=3))
        lines = label.split("\n")
        for i, ln in enumerate(lines):
            d.add(String(x + w / 2, y + h / 2 + (len(lines) / 2 - i - 0.75) * 10, ln,
                         fontName="Helvetica-Bold", fontSize=8, fillColor=fg, textAnchor="middle"))

    def arrow(x1, y1, x2, y2, label=None):
        d.add(Line(x1, y1, x2, y2, strokeColor=INK, strokeWidth=1))
        ang = math.atan2(y2 - y1, x2 - x1)
        a, s = 0.45, 6
        d.add(Polygon([x2, y2, x2 - s * math.cos(ang - a), y2 - s * math.sin(ang - a),
                       x2 - s * math.cos(ang + a), y2 - s * math.sin(ang + a)], fillColor=INK, strokeColor=INK))
        if label:
            d.add(String((x1 + x2) / 2 + 4, (y1 + y2) / 2 + 3, label, fontName="Helvetica-Oblique",
                         fontSize=7.5, fillColor=MUTED))

    green = colors.HexColor("#DFF3E4")
    grey = colors.HexColor("#E6E8EB")
    box(0, 140, 90, 26, "PIM analyst\n(role)", colors.white)
    box(0, 92, 90, 30, "Model editor /\nvalidator (tool)", grey)
    box(W - 125, 140, 125, 26, "Transformation definition\ncreator (role)", colors.white)
    box(W / 2 - 60, 140, 120, 26, "Transf. definition\neditor (tool)", grey)
    box(W / 2 - 60, 92, 120, 26, "Transformation\ndefinition (artifact)", grey)
    box(0, 32, 90, 28, "PIM\n(artifact)", green)
    box(W / 2 - 60, 32, 120, 28, "Transformation\ntool", TEAL, colors.white)
    box(W - 90, 32, 90, 28, "PSM\n(artifact)", green)
    box(W / 2 - 50, 0, 100, 18, "PSM creator (role)", colors.white)
    d.add(String(W / 2 + 6, 21, "uses", fontName="Helvetica-Oblique", fontSize=7.5, fillColor=MUTED))
    arrow(45, 140, 45, 122, "uses")
    arrow(45, 92, 45, 60, "produces")
    arrow(W - 125, 153, W / 2 + 60, 153, "uses")
    arrow(W / 2, 140, W / 2, 118, "output")
    arrow(W / 2, 92, W / 2, 60, "input")
    arrow(90, 45, W / 2 - 60, 45, "input")
    arrow(W / 2 + 60, 45, W - 90, 45, "output")
    arrow(W / 2, 18, W / 2, 32)
    return d


g.p("Lecture 1: Introduction", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, "
    "built from slides 1-13 and Exercise Sheet 1 (Q2).", "sub")
g.add(Spacer(1, 10))
g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "Lecture 1 is short and sets up vocabulary (model, PIM, PSM, transformation) that every later lecture uses. "
    "The tutorial adds the <b>CIM</b>, which is <b>not on the slides</b> but was asked in Exercise Sheet 1, so "
    "treat it as exam material.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "Software is intangible information, so developers always work on a <b>representation</b> of it.",
    "Representations got more abstract over time: machine code, assembler, structured languages, OO languages, "
    "and now <b>modeling languages</b> (UML, DSLs). Each level is made executable by automatic translation to the level "
    "below (assembler, compiler, preprocessor).",
    "Enterprise systems (distributed, heterogeneous, many platforms) make hand-programming every platform impractical.",
    "<b>MDA</b> (the OMG's vision): developers build a <b>Platform Independent Model (PIM)</b>, and tools "
    "<b>automatically translate</b> it into <b>Platform Specific Models (PSMs)</b>. Before the PIM there can be a "
    "<b>Computation Independent Model (CIM)</b>: the domain model (from the tutorial).",
    "A <b>model</b> (Stachowiak) has three aspects: <b>reduction</b> (abstraction), <b>projection</b> "
    "(homomorphism), <b>pragmatics</b> (purpose).",
    "<b>UML</b> is a family of general-purpose modeling languages, <b>not a process</b>.",
]))
g.add(PageBreak())

g.sec("A. How software is represented")
g.qa("MED", "Why do software developers always work with a <i>representation</i> of software?",
     "Computer-based systems consist of hardware and software. Hardware is solid and tangible; software is "
     "<b>invisible and intangible: it is information</b>. Developers cannot touch software directly, so they create "
     "a <b>software representation</b> (program text, and with MDD, models), which is then turned into running software. "
     "The history of software engineering is largely a history of better representations.",
     "slide 2", short="Why developers work on a representation of software.")

g.qa("HIGH", "Describe the evolution of software representation approaches. For each level give examples and its "
     "core concepts.", "See the table below. Practise filling it in from memory.", "slides 3-5",
     short="Representation levels table (level, examples, concepts), incl. the modeling level.",
     extra=[grid([
         ["Level", "Examples", "Concepts"],
         ["Machine code", "PDP-11", "instructions, registers, memory locations"],
         ["Assembler languages", "PDP-11 Assembler", "abstract instructions, registers, memory locations"],
         ["High-level, structured", "FORTRAN, COBOL, C, Algol", "variables, procedures, control statements, types"],
         ["High-level, object-oriented", "Eiffel, C++, Java, C#", "classes, objects, instance variables, methods"],
         ["Modeling languages", "UML, DSLs", "metamodeling, transformations"],
     ], [45 * mm, 50 * mm, 75 * mm]), Spacer(1, 4),
         Paragraph("<b>Key point:</b> each step raises the abstraction level, moving concepts away from the machine and "
                   "closer to the problem. Modeling languages are the <i>next</i> level (the '?' row on slide 3).",
                   S["a"])])

g.qa("HIGH", "How does a representation on a higher level become executable? Name the translators between the levels.",
     "Through <b>automatic translation into the level below</b>:<br/>" + bullets([
         "<b>Assembler</b>: assembler language to machine code",
         "<b>Compiler</b>: structured high-level language to assembler/machine level",
         "<b>Preprocessor</b>: object-oriented language to structured language (early C++ was translated to C this way)",
     ]) + "<br/>MDD/MDA continues this pattern: <b>models are automatically transformed</b> toward code, just as code "
     "is compiled. This analogy is the core argument for why MDD is realistic.",
     "slide 4", short="Translators between levels (assembler, compiler, preprocessor).")

g.qa("MED", "What characterised the traditional era of software development (before enterprise computing)?",
     bullets(["one program per application", "programs are textual documents",
              "one programming language per application", "software development was simply called \"programming\""]),
     "slide 4", short="Four characteristics of the traditional 'programming' era.")

g.sec("B. Enterprise computing and MDA")
g.qa("MED", "What characterises the era of enterprise computing, and why does it cause problems for traditional "
     "programming?",
     "Characteristics on the slide:<br/>" + bullets([
         "<b>distribution</b>, <b>heterogeneity</b>, <b>universal connectivity</b>, <b>mobility</b>",
         "<b>middleware</b>, <b>multi-tier architectures</b>, <b>components/services</b>, <b>application servers</b>",
         "a flood of platform technologies: CORBA, DCOM, EJB, J2EE, .NET, JSP pages, Servlets, XML, SOAP, WSDL, "
         "BPEL4WS, ebXML, ...",
     ]) + "<br/>The problem: one application now spans many machines, platforms and languages. The \"one program, "
     "one language\" assumption breaks, and developers would have to hand-code the same business logic against many "
     "fast-changing platforms. This motivates working at a platform-independent level.",
     "slides 4, 6", short="Enterprise computing: characteristics and the problem it causes.")

g.qa("HIGH", "What is MDA, and who is behind it?",
     "<b>Model Driven Architecture (MDA)</b> is the <b>core vision of the Object Management Group (OMG)</b>, the largest "
     "IT standards organisation (over 700 members). It applies to many domains (finance, e-commerce, telecom, "
     "healthcare, transportation, manufacturing, space, ...). The MDA picture places OMG modeling standards at its core "
     "(<b>UML, MOF, CWM</b>), surrounded by platforms such as CORBA, Java, .NET, XMI/XML and web services, and "
     "pervasive services (security, transactions, events, directory).",
     "slide 5", short="What is MDA; who is behind it.")

g.qa("HIGH", "Explain the vision of MDA.",
     "The software developer <b>no longer programs the many platforms directly</b> (the crossed-out arrow on the slide). "
     "Instead they build a <b>Platform Independent Model (PIM)</b> of the system. The platform-specific system is then "
     "obtained by <b>automatic translation</b> (transformation) from the PIM. Benefit: the business logic is described "
     "once and can be re-targeted to new platforms by changing the transformation, not the model.",
     "slide 7", short="The MDA vision.")

g.qa("HIGH", "Describe the roles, tools and artifacts in the MDA process (be ready to draw the diagram).",
     bullets([
         "<b>Roles:</b> PIM analyst, transformation definition creator, PSM creator",
         "<b>Tools:</b> model editor/validator, transformation definition editor, transformation tool",
         "<b>Artifacts:</b> PIM, transformation definition, PSM",
     ]) + "<br/><b>Flow:</b> the PIM analyst uses the model editor/validator to produce the PIM. The transformation "
     "definition creator uses the transformation definition editor, whose output is the transformation definition. "
     "The <b>PIM and the transformation definition are both inputs</b> to the transformation tool, which "
     "<b>outputs the PSM</b>. The PSM creator uses the transformation tool.",
     "slide 8", short="Draw the MDA roles/tools/artifacts diagram.",
     extra=[mda_diagram(), Paragraph("Redrawn from slide 8. Practise sketching this from memory.", S["small"])])

g.qa("MED", "Why is the transformation definition a separate artifact instead of being built into the tool?",
     "It separates <b>what</b> the system does (PIM) from <b>how</b> a platform implements it (transformation "
     "definition). It is written once by an expert (the transformation definition creator) and can be reused for "
     "many PIMs. Supporting a new platform means writing a new transformation definition, not remodelling the system. "
     "<i>(Reasoning from slide 8.)</i>",
     "slide 8 (reasoning)", short="Why the transformation definition is a separate artifact.")

g.sec("C. CIM, PIM and PSM (from the tutorial)")
g.qa("HIGH", "Define CIM, PIM and PSM.",
     "<b>Computation Independent Model (CIM)</b>:<br/>" + bullets([
         "describes the system <b>in the environment in which it is intended to be used</b>, and so helps define which "
         "<b>behaviour is expected</b> from the system",
         "details of the system infrastructure are <b>hidden or not yet defined</b>",
         "also called the <b>domain model</b>: it uses the technical terms of the <b>problem domain</b>",
         "<b>bridges</b> domain experts (who know the domain and requirements) and the experts who design the artifacts",
         "focuses on the <b>system environment and system requirements</b>",
     ]) + "<br/><b>Platform Independent Model (PIM)</b>:<br/>" + bullets([
         "hides the details that are needed for particular platforms; it is the part of the specification that "
         "<b>does not change if the platform changes</b>",
         "shows a <b>certain degree</b> of platform independence, e.g. suitable for several platforms of the same type",
         "can use a <b>general-purpose</b> modeling language or a <b>domain-specific</b> modeling language",
     ]) + "<br/><b>Platform Specific Model (PSM)</b>:<br/>" + bullets([
         "<b>combines the PIM with the details required for a certain platform</b>; in addition to the PIM it defines "
         "<b>how the platform is used</b> by the system",
     ]) + "<br/>Chain: <b>CIM (what the domain needs) to PIM (how the system works, platform-free) to PSM (how it "
     "runs on one platform)</b>.",
     "Exercise Sheet 1, Q2 (sample solution); official viewpoint definitions: L6 slide 3", tut="1, Q2", short="Define CIM, PIM and PSM.")

g.qa("HIGH", "Define a CIM, PIM and PSM for a robot remote-control system (the robot can be instructed and its body "
     "parts steered) using UML class diagrams. Describe what each contains.",
     "See the table below (summarised from the sample solution's three class diagrams). In the exam, draw three small "
     "class diagrams with this content.", "Exercise Sheet 1, Q2 (sample solution)", tut="1, Q2",
     short="CIM/PIM/PSM class diagrams for the robot remote control.",
     extra=[grid([
         ["Model", "What the diagram shows", "Typical give-away"],
         ["<b>CIM</b>", "Robot, Arm, Leg, Head. Robot <i>consists of</i> 2 arms, 2 legs and a head. "
                        "No operations, no technology.", "domain words only (\"consists of\")"],
         ["<b>PIM</b>", "Same classes with role names (arms, legs, head) and operations: "
                        + c("walkTo(x, y)") + ", " + c("moveHead(side, degree)") + ", " + c("moveArm(x, y, z)") +
                        " on Robot; " + c("moveArm") + " on Arm, " + c("moveHead") + " on Head.",
          "behaviour is defined, still no platform"],
         ["<b>PSM</b>", "Platform classes: " + c("<<WebService>> RemoteControl") + " (robots), " +
                        c("<<JavaBean>> NaoRobot") + " (IP, robotName), " + c("NaoArm/NaoLeg") + " (stiffness), " +
                        c("NaoHead") + ", and an " + c("ALMotionProxy") + " each part uses. Notes give platform "
                        "details: Java SE 1.7, NaoQi 1.3, LinkedList/ArrayList, serializable.",
          "stereotypes, concrete libraries, data structures"],
     ], [18 * mm, 107 * mm, 45 * mm])])

g.qa("MED", "Where does a CIM fit relative to the slide-8 MDA process, and what kind of language can each model use?",
     "The CIM comes <b>before</b> the PIM: the PIM analyst builds the PIM from the requirements captured in the CIM. "
     "The PIM can be written in a general-purpose language (UML) or a DSL; the PSM adds platform specifics, often via "
     "UML stereotypes such as " + c("<<JavaBean>>") + " or " + c("<<WebService>>") +
     ". The PIM-to-PSM step is the automated transformation on slide 8. <i>(Combines slide 8 with the tutorial.)</i>",
     "slide 8 + Exercise Sheet 1", short="Where the CIM fits in the MDA process.")

g.sec("D. What is a model?")
g.qa("HIGH", "Give Stachowiak's definition of a model. <i>(Learn this word-for-word.)</i>",
     "\"A <b>formal representation</b> of <b>entities and relationships in the real world</b> (<b>abstraction</b>) with a "
     "certain <b>correspondence</b> (<b>homomorphism</b>) for a certain <b>purpose</b> (<b>pragmatics</b>).\" "
     "[Stachowiak]<br/>Memory hook: <b>R-P-P</b> = Reduction, Projection, Pragmatics.",
     "slide 9", short="Stachowiak's definition, word-for-word.")

g.qa("HIGH", "Explain the three aspects of a model.", "See the table below.", "slide 9",
     short="Three aspects of a model.",
     extra=[grid([
         ["Aspect", "Meaning"],
         ["<b>Reduction</b> (abstraction)", "A model does not contain all attributes of its original. Details irrelevant "
                                            "to the purpose are left out."],
         ["<b>Projection</b> (homomorphism)", "Every model represents something else. Statements about model elements "
                                              "must hold for the real-world entities."],
         ["<b>Pragmatics</b> (purpose)", "A model can replace the original under certain assumptions or for specific "
                                         "questions. Models and meta-models must be created in a goal-driven way."],
     ], [50 * mm, 120 * mm])])

g.qa("MED", "Apply the three model aspects to the airplane example on slide 9.",
     bullets([
         "<b>Reduction:</b> the diagram omits seats, wiring, paint, engine internals and so on; it shows only the main "
         "parts and control surfaces.",
         "<b>Projection:</b> each labelled part corresponds to a real part. If the model says \"the rudder changes yaw\", "
         "that must be true of the real airplane.",
         "<b>Pragmatics:</b> the model serves one purpose, explaining which part controls what (pitch, yaw, roll, lift, "
         "thrust). It can answer that question in place of the real plane, but not questions about fuel consumption.",
     ]), "slide 9", short="Apply the three aspects to the airplane example.")

g.qa("MED", "Can two different models of the same original both be correct? Justify with the model aspects.",
     "Yes. Because of <b>pragmatics</b> a model is built for a purpose, and <b>reduction</b> drops whatever is irrelevant "
     "to that purpose, so different purposes keep different details. Both are correct as long as <b>projection</b> "
     "holds: what they do say is true of the original. Example: a control-surface model and a seating-plan model of "
     "the same aircraft. (The CIM/PIM/PSM of the robot are another example: three models of one system.)",
     "slide 9 (reasoning)", short="Can two different models of the same thing both be correct?")

g.qa("HIGH", "Name and explain the four benefits of models.",
     bullets([
         "<b>Analysability:</b> reduced complexity allows (automatic) analysis",
         "<b>Increased abstraction level:</b> gives rise to more compact descriptions",
         "<b>Increased communication efficiency:</b> easier to understand than the real thing",
         "<b>Usable by domain experts:</b> via Domain Specific Languages (DSLs)",
     ]) + "<br/>Memory hook: <b>A-A-C-D</b> (Analysis, Abstraction, Communication, Domain experts).",
     "slide 10", short="Four benefits of models.")

g.sec("E. UML and DSLs")
g.qa("HIGH", "What is UML? Give the official definition.",
     "\"The Unified Modeling Language (UML) is the <b>industry standard language</b> for <b>specifying, visualizing, "
     "constructing, and documenting</b> the artifacts of software systems.\" (UML Standard)<br/>"
     "It is a <b>family of general-purpose modeling languages</b> that supports visualising software through a suite of "
     "diagram types, e.g. <b>class diagrams, state diagrams, interaction diagrams</b>. "
     "Memory hook for the four verbs: <b>S-V-C-D</b>.",
     "slide 11", short="UML definition (the four verbs).")

g.qa("HIGH", "Is UML a software development process? Explain.",
     "<b>No.</b> UML is only a language (notation plus meaning). It gives <b>no guidelines</b> about:<br/>" + bullets([
         "<b>what</b> models should be created", "<b>what content</b> models should contain",
         "<b>how</b> models should be created"]) +
     "<br/>A process or method (in MDA: CIM, PIM, transformation, PSM) must supply those decisions.",
     "slide 11", short="Is UML a process? What does it not tell you?")

g.qa("MED", "What is the difference between UML and a DSL?",
     "<b>UML</b> is <b>general purpose</b>: one family of languages meant for modeling any kind of software. A "
     "<b>Domain Specific Language (DSL)</b> is tailored to one domain, using that domain's own concepts, which makes "
     "models <b>usable by domain experts</b>. Both are modeling languages, the level above OO programming languages; "
     "the tutorial notes that a PIM may be written in either.",
     "slides 5, 10, 11; Exercise Sheet 1", short="UML vs DSL.")

g.sec("F. Transfer and discussion questions")
g.qa("MED", "\"Moving from code to models is the same kind of step as moving from assembler to high-level "
     "languages.\" Discuss.",
     "<b>Supporting:</b> every past step raised abstraction (registers to variables to objects) and was made practical by "
     "an automatic translator (assembler, compiler, preprocessor). MDA does the same: modeling languages raise the level "
     "again, and transformation tools play the compiler's role (PIM to PSM).<br/>"
     "<b>Limits:</b> compilers are mature and fully automatic; model transformations need someone to write the "
     "transformation definitions, and models only work this way if they are precise (formal) enough. That precision "
     "is why the course continues with OCL, metamodeling and ATL.",
     "slides 3-8 (reasoning)", short="Code-to-models vs assembler-to-high-level: discuss.")

g.qa("MED", "A colleague says: \"MDA just means drawing UML diagrams as documentation.\" Respond.",
     "In MDA models are <b>primary development artifacts</b>, not documentation: the PIM is <b>automatically "
     "translated</b> into platform-specific models/code by a transformation tool using a transformation definition. For "
     "that, models must be <b>formal</b> (Stachowiak: a formal representation), which plain sketches are not. UML is "
     "also only a language, not a process; MDA supplies the process (CIM, PIM, transformation, PSM).",
     "slides 7-11 (reasoning)", short="Respond to: 'MDA is just drawing UML diagrams'.")

g.qa("LOW", "Name the main topics of the course.",
     bullets([
         "<b>Traditional MDA:</b> OMG modeling infrastructure, profiles",
         "<b>Object Constraint Language (OCL):</b> invariants, pre- and postconditions",
         "<b>Language definition and use:</b> metamodeling, Domain Specific Languages",
         "<b>Transformations:</b> ATLAS Transformation Language (ATL)",
         "<b>PAMoLa:</b> multi-level modeling",
     ]) + "<br/>Recommended reading: Warmer &amp; Kleppe, <i>The Object Constraint Language</i> (2003); "
     "Volter &amp; Stahl, <i>Model-Driven Software Development</i> (2006)."
     "<br/>Traditional MDA is covered in Lecture 6 (MDA infrastructure) and Lecture 7 (profiles, powertypes).",
     "slides 12-13", short="Main course topics.")

g.self_test()
g.build()
