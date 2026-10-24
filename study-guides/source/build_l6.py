from guide_lib import *

g = Guide("L6-MDA-Infrastructure-Questions.pdf", "MDD - Lecture 6: MDA Infrastructure - Exam question bank",
          "MDD Lecture 6 - Exam Questions")
T = "See the table below."

g.p("Lecture 6: MDA Infrastructure", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "slides 1-18. No exercise sheet covers this lecture yet; links to Sheet 1 and Lectures 1 and 5 are marked.", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "This lecture is <b>definition-heavy</b>: no OCL to write, but many short \"define / explain / draw\" questions. "
    "The most testable items are the <b>three MDA goals</b>, the <b>three viewpoints</b>, the <b>infrastructure "
    "diagram</b> (slide 4), the <b>four parts of a language definition</b> (slide 5) and <b>how UML is specified</b> "
    "(slide 6).",
    "It connects Lecture 1 (PIM/PSM, MDA) with Lecture 5 (metamodels, Ecore, the M3/M2/M1 picture).",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "MDA separates <b>what a system does</b> from <b>how it runs on a platform</b>. Goals: <b>portability, "
    "interoperability, reusability</b> through architectural separation of concerns.",
    "Three viewpoints/models: <b>CIM</b> (environment), <b>PIM</b> (platform-independent architecture and operation), "
    "<b>PSM</b> (refined with platform details).",
    "Infrastructure: PIM and PSM are written in languages that are written in <b>MOF</b>; the transformation definition "
    "is written in <b>QVT</b>, which extends MOF; a transformation tool uses it to turn PIM into PSM.",
    "A language = <b>abstract syntax</b> + <b>concrete syntax</b> + <b>static semantics</b> + <b>dynamic semantics</b>. "
    "UML: abstract syntax by class diagrams and static semantics by OCL (together: the <b>metamodel</b>); the other two "
    "in natural language.",
    "<b>MOF</b> is the OMG meta-language for metamodels (UML, CWM, MOF itself). Since UML 2.0, UML = "
    "<b>infrastructure</b> + <b>superstructure</b>; the Infrastructure Library (Core + Profiles) is shared by UML and MOF.",
    "<b>XMI</b> serialises MOF-based models and metamodels as XML. <b>EMF</b>'s <b>Ecore</b> is the Eclipse counterpart "
    "of MOF.",
]))

g.p("Cheat sheet: the MDA infrastructure (slide 4) as relations", "h1")
g.add(grid([
    ["Element", "Relation", "Element"],
    ["PIM", "is written in", "a (source) language"],
    ["PSM", "is written in", "a (target) language"],
    ["each language", "is written in", "the metalanguage <b>MOF</b>"],
    ["Transformation Definition", "is written in", "the transformation definition language <b>QVT</b>"],
    ["QVT", "extends", "MOF"],
    ["Transformation Definition", "relates", "source language to target language (arrows in and out)"],
    ["Transformation Tool", "uses", "the Transformation Definition"],
    ["Transformation Tool", "takes / produces", "PIM as input, PSM as output"],
], [52 * mm, 33 * mm, 85 * mm]))
g.p("ATL (Lecture 5) plays the role of QVT here: it was developed as a submission to the QVT RFP.", "small")
g.add(PageBreak())

g.sec("A. MDA motivation and viewpoints")
g.qa("HIGH", "What idea does MDA start from, and what does it provide an approach for?",
     "MDA starts from the long-established idea of <b>separating the specification of the functionality of a system "
     "from the details of the way that system is realised on a particular platform</b>.<br/>It provides an approach "
     "for:<br/>" + bullets([
         "<b>modeling execution platforms</b>",
         "<b>specifying a system independently</b> of a particular execution platform",
         "<b>transforming</b> a platform-independent specification into a platform-specific one",
     ]), "slide 2", short="MDA's starting idea; what it provides an approach for.")

g.qa("HIGH", "What are the three primary goals of MDA, and how are they achieved?",
     "<b>Portability, interoperability and reusability</b>, achieved <b>through architectural separation of "
     "concerns</b> (platform-independent vs platform-specific parts).<br/><i>Explanation (reasoning):</i>" + bullets([
         "<b>Portability</b>: the same PIM can be transformed to a new platform.",
         "<b>Interoperability</b>: systems on different platforms derived from shared models can work together.",
         "<b>Reusability</b>: PIMs and transformation definitions are reused across projects and platforms.",
     ]) + "Memory hook: <b>P-I-R</b>.", "slide 2", short="Three goals of MDA (P-I-R) and how they are achieved.")

g.qa("HIGH", "Describe the three MDA viewpoints (models).", T, "slide 3; Exercise Sheet 1, Q2", tut="1, Q2 (related)",
     short="The three MDA viewpoints: CIM, PIM, PSM.",
     extra=[grid([
         ["Viewpoint (model)", "Slide definition"],
         ["<b>Computation Independent (CIM)</b>", "describes the <b>environment</b> into which the system should fit; "
          "details of the structure and processing of the system are <b>hidden or as yet undetermined</b>"],
         ["<b>Platform Independent (PIM)</b>", "describes the <b>high-level architecture and operation</b> of the system "
          "while omitting the details needed for execution on a particular platform; shows the part of the specification "
          "that <b>does not change from one platform to another</b>"],
         ["<b>Platform Specific (PSM)</b>", "<b>refines</b> the platform-independent viewpoint with additional detail about "
          "<b>how the system is executed on a specific platform</b>"],
     ], [50 * mm, 120 * mm]), Spacer(1, 4),
         Paragraph("Exercise Sheet 1, Q2 asked for exactly these three models for a robot remote control (see the "
                   "Lecture 1 guide, section C, for the worked answer).", S["small"])])

g.qa("HIGH", "Explain the MDA infrastructure diagram (slide 4). Be ready to draw it.",
     "See the cheat sheet on page 1. In words: the PIM and the PSM are each <b>written in a language</b>, and both "
     "languages are <b>written in the metalanguage MOF</b>. A <b>transformation definition</b>, written in the "
     "transformation definition language <b>QVT</b> (which <b>extends MOF</b>), describes how constructs of the source "
     "language map to the target language. The <b>transformation tool uses</b> the transformation definition to turn "
     "the PIM into the PSM.<br/>Compared with Lecture 1 (slide 8, roles/tools/artifacts), this picture adds the "
     "<b>language level</b>: models are instances of languages, and languages are defined with MOF.",
     "slide 4; L1 slide 8", short="Explain/draw the MDA infrastructure diagram.")

g.qa("MED", "Why must the PIM and PSM languages be written in MOF for MDA to work?",
     "A transformation definition maps <b>constructs of one language</b> to <b>constructs of another</b>. If both "
     "languages are defined in the same metalanguage (MOF), the transformation language (QVT, which extends MOF) can "
     "refer to their elements uniformly, and one generic tool can execute any transformation. Lecture 5 shows the same "
     "idea in EMF: Families, Persons and ATL metamodels all conform to Ecore. <i>(Reasoning.)</i>",
     "slides 4, 9; L5 slide 17", short="Why PIM/PSM languages must be defined in MOF.")

g.sec("B. Defining a language")
g.qa("HIGH", "What are the core ingredients of a formal language? Explain all four parts.",
     "Two core ingredients, <b>syntax</b> and <b>semantics</b>, each with two parts:", "slide 5",
     short="Four parts of a language definition (abstract/concrete syntax, static/dynamic semantics).",
     extra=[grid([
         ["Part", "Defines"],
         ["<b>Abstract syntax</b>", "<b>what constructs exist</b> in the language and how they are built up from other "
                                    "constructs"],
         ["<b>Concrete syntax</b>", "<b>how the constructs</b> of the abstract syntax <b>are visualised</b> (notation)"],
         ["<b>Static semantics</b>", "how an instance of a construct must be <b>connected to other instances to be "
                                     "meaningful</b> (well-formedness rules)"],
         ["<b>Dynamic semantics</b>", "the <b>meaning</b> of a set of well-formed constructs in terms of their <b>effect on "
                                      "the real world</b>"],
     ], [40 * mm, 130 * mm]), Spacer(1, 4),
         Paragraph("Example with a UML class diagram: abstract syntax = there are Classes with Attributes; concrete "
                   "syntax = a class is drawn as a box with compartments; static semantics = e.g. a class cannot "
                   "generalize itself; dynamic semantics = what an object of the class does at runtime. "
                   "<i>(Example is mine.)</i>", S["small"])])

g.qa("HIGH", "How is UML specified? Which part is the metamodel?",
     "UML is primarily specified with a <b>metamodeling approach</b>:<br/>" + bullets([
         "<b>abstract syntax</b>: defined using <b>class diagrams</b>",
         "<b>static semantics</b>: defined using <b>OCL</b>",
         "<b>concrete syntax</b>: defined using <b>natural language</b>",
         "<b>dynamic semantics</b>: defined using <b>natural language</b>",
     ]) + "<br/>The <b>metamodel</b> = abstract syntax (class diagrams) + static semantics (OCL).<br/>This <b>lacks some "
     "of the rigor</b> of a formal specification method but is <b>more intuitive and pragmatic</b>, and does not prevent "
     "a mathematically formal definition: <b>fUML (Foundational UML)</b> formally defines the dynamic semantics of a "
     "<b>subset</b> of UML.", "slide 6", short="How UML is specified (4 parts); what the metamodel is; fUML.")

g.qa("HIGH", "Why is OCL needed in a metamodel? Give an example of a static-semantics rule.",
     "Class diagrams (abstract syntax) can say which constructs exist and how they connect, but not every "
     "well-formedness rule; OCL adds those rules. This is the link between Lectures 2-4 and metamodeling.<br/>"
     "Example in the style of the UML metamodel (my own):<br/>" +
     ocl("context Class\ninv noSelfGeneralization: not self.superClass->includes(self)") +
     "<br/>(No class may be its own direct superclass.)", "slide 6 (reasoning)",
     short="Why OCL is part of a metamodel; example rule.")

g.qa("HIGH", "Explain language definition by metamodeling with the use-case example (slide 7).",
     "Upper level: a <b>MOF metamodel of use cases</b> with metaclasses " + c("actor") + " (+name), " + c("useCase") +
     " (+title) and " + c("system") + " (+name). Associations: actor to useCase (1..*), useCase " + c("extends") + " and "
     + c("includes") + " useCase, actor " + c("extends") + " actor (0..1), system composes useCases.<br/>Lower level: a "
     "<b>UML use-case diagram</b>: system <b>e-Store</b> with use cases <b>OrderItem</b> and <b>ValidateCart</b> and an "
     "actor. The dashed arrows show that each model element is an <b>instance of</b> a metaclass (the actor of "
     "actor, the ellipses of useCase, the box of system, the lines of the actor-useCase association).<br/>Point: the "
     "<b>metamodel defines the language</b>; a diagram is valid if it can be expressed as instances of the metamodel.",
     "slide 7", short="Language definition by metamodeling: the use-case example.")

g.sec("C. MOF and the UML language architecture")
g.qa("HIGH", "What is the MOF (Meta-Object Facility)? Summarise its history.",
     bullets([
         "Defines an <b>abstract language and a framework</b> for specifying, constructing and managing "
         "<b>technology-neutral metamodels</b>, e.g. <b>UML, CWM and the MOF itself</b>.",
         "Defines a framework for implementing <b>repositories that hold metadata</b> (e.g. models) described by the "
         "metamodels; it uses <b>standard technology mappings</b> to turn MOF metamodels into <b>metadata APIs</b>.",
     ]) + "<br/><b>History:</b>" + bullets([
         "originally a <b>distributed metadata repository</b> as part of the <b>CORBA OMA</b>",
         "became famous as the <b>meta-meta-model for UML 1.x</b>",
         "<b>fully revised to align with UML 2.0</b>, giving <b>MOF 2.0</b>",
     ]), "slide 9", short="What MOF is; its history.")

g.qa("MED", "Describe the core structure of MOF (and of UML) shown on slide 8.",
     "Root: abstract <b>ModelElement</b>. Below it: <b>NameSpace</b> (which contains ModelElements), <b>Feature</b> and "
     "<b>TypedElement</b>.<br/>" + bullets([
         "NameSpace to <b>GeneralizableElement</b> (which can generalize itself), specialised into <b>Package</b> and "
         "<b>Classifier</b>; Classifier into <b>Association, DataType, Class</b>.",
         "Feature into <b>BehavioralElement</b> (<b>Operation, Exception</b>) and <b>StructuralFeature</b> "
         "(<b>Attribute, Reference</b>).",
     ]) + "<br/>Italic names are abstract metaclasses. Point: <b>MOF and the core of UML share this structure</b>.",
     "slide 8", short="MOF core metaclass hierarchy (slide 8).")

g.qa("HIGH", "What are the UML infrastructure and the UML superstructure?",
     "Since <b>UML 2.0</b> the UML definition is split into two parts:<br/>" + bullets([
         "<b>Infrastructure</b>: the <b>foundational language constructs</b> required for UML; defines the relationship "
         "of UML to <b>other OMG technologies</b>; essentially defines the <b>OMG's framework for MDA</b>.",
         "<b>Superstructure</b>: the <b>user-level constructs</b>, i.e. the UML modeling features for <b>normal users</b> "
         "(class diagrams, state machines, ...).",
     ]), "slide 10", short="UML infrastructure vs superstructure.")

g.qa("HIGH", "What is the Infrastructure Library, and which packages does it consist of?",
     bullets([
         "Defines a <b>meta-language core</b> that can be <b>reused to define a variety of metamodels</b>, including "
         "<b>UML and MOF</b>.",
         "Facilitates the <b>architectural alignment of UML, MOF and XMI</b> so that <b>model interchange</b> is fully "
         "supported.",
         "Allows <b>customisation of UML and MOF through profiles</b> (Lecture 7).",
     ]) + "<br/>Two packages: <b>Core</b> (core concepts used when metamodeling) and <b>Profiles</b> (mechanisms used to "
     "customise metamodels); Profiles depends on Core.", "slide 11", short="Infrastructure Library: purpose; Core and Profiles.")

g.qa("HIGH", "How was the alignment of UML and MOF accomplished? Explain both diagrams on slide 12.",
     "Two ways:<br/>" + bullets([
         "<b>1. Shared common core:</b> the common core is defined so that model elements are <b>shared by UML and "
         "MOF</b>; <b>UML, MOF, CWM and Profiles all specialize («specializes») the Core</b> package (left "
         "diagram).",
         "<b>2. UML is a MOF metamodel:</b> UML is defined <b>as an instance of MOF</b>: MOF sits on <b>M3</b>; the "
         "metamodels <b>UML</b> and <b>CWM</b> on <b>M2</b> are «instanceOf» MOF (right diagram).",
     ]) + "<br/>So MOF and UML both <b>specialize</b> the common core and both <b>instantiate</b> it (via MOF).",
     "slide 12", short="UML/MOF alignment: specialize the core, and UML as an instance of MOF.")

g.qa("HIGH", "Explain the metamodeling levels M3, M2, M1 (and M0).", T, "slide 12; L5 slide 17 (M0: standard OMG)",
     short="The metamodeling levels M3-M0 with examples.",
     extra=[grid([
         ["Level", "Contains", "Example"],
         ["<b>M3</b> meta-metamodel", "the language for defining metamodels", "MOF (OMG), Ecore (EMF)"],
         ["<b>M2</b> metamodel", "languages defined in M3", "UML, CWM, Families.ecore, ATL.ecore"],
         ["<b>M1</b> model", "models written in an M2 language", "a class diagram with class Customer; "
                                                                "sample-Families; a .atl transformation"],
         ["<b>M0</b> runtime/real world", "instances of M1 elements", "the customer object \"Jos\" at runtime"],
     ], [40 * mm, 60 * mm, 70 * mm]), Spacer(1, 4),
         Paragraph("Each level is an <b>instance of</b> / <b>conforms to</b> the level above; MOF/Ecore conforms to "
                   "<b>itself</b>. The slides show M3 and M2 (slide 12) and M3-M1 (Lecture 5, slide 17); M0 is the "
                   "standard OMG completion.", S["small"])])

g.qa("MED", "What is the MOF 2.0 family of specifications, and why was this approach adopted?",
     "MOF 2.0 is the <b>basis for a suite of standards</b>:<br/>" + bullets([
         "MOF 2.0 to <b>XMI</b> mapping", "MOF 2.0 to <b>CORBA IDL</b> mapping", "MOF 2.0 to <b>Java (JMI2)</b> mapping",
         "MOF 2.0 <b>Versioning and Life Cycle Management</b>", "MOF 2.0 <b>Query/Views/Transformations (QVT)</b>",
         "MOF 2.0 <b>Federation/Facility/Directory</b>, ...",
     ]) + "<br/>Adopted to <b>provide modelers with enhanced but optional capabilities</b> and to <b>help align MOF with "
     "UML</b>.", "slide 13", short="MOF 2.0 family; why it was adopted.")

g.sec("D. XMI and model serialization")
g.qa("HIGH", "What is XMI (XML Metadata Interchange)?",
     bullets([
         "Uses <b>XML as a (meta)data transfer syntax and interchange format</b>.",
         "XML <b>DTDs or schemas</b> enable transfer and verification of UML-based models, data warehouse models, Java "
         "and EJB artifacts, and <b>MOF-based metamodels and their instances</b>.",
         "Specifies a <b>precise MOF-to-XML mapping</b>: allows <b>interchange of any MOF-based metamodel and its "
         "models</b> (MOF to XML stream) and <b>automatic generation of XML documents</b> that can be validated with "
         "<b>generated DTDs</b>.",
         "Uses UML and MOF for metamodel design and implementation.",
     ]), "slide 14", short="What XMI is and does.")

g.qa("MED", "Explain the model serialization picture (slide 15).",
     "XMI combines <b>XML</b>, <b>models</b> and <b>MOF</b>. Its outputs are <b>serialized models as XML streams</b> "
     "(e.g. UML, SPEM, CWM models) and <b>serialized metamodels as XML DTDs or schemas</b>. So both levels, metamodel "
     "and model, can be exchanged between tools as XML.", "slide 15", short="Model serialization with XMI (slide 15).")

g.qa("MED", "Read the XMI on slide 16: what model does it describe?",
     "A model (package) <b>Business</b> (public) containing a class <b>Customer</b> with an attribute <b>id</b> of "
     "multiplicity 1..1 and type <b>CustId</b> (a DataType referenced by id), and an operation <b>update()</b> with "
     "instance scope. Elements get <b>xmi.id</b>s so they can be referenced (" + c('href="|a247"') + ").<br/>"
     "Note the nesting: Model, ownedElement, Class, feature, Attribute/Operation, mirroring the metamodel structure. "
     "(The slide's XML has small slips, e.g. " + c("</Operation>") + " after an already self-closed tag.)",
     "slide 16", short="Interpret the XMI example (Business/Customer).")

g.qa("MED", "Earlier lectures showed XMI files. Where?",
     "Lecture 5, slides 15-16: the input and output models of Families2Persons are XMI documents ("
     + c('<xmi:XMI ... xmlns="Families">') + " with " + c("<Family lastName=\"March\">") + " elements). That is XMI "
     "serialising an M1 model whose metamodel (Families) is MOF/Ecore-based.", "L5 slides 15-16",
     short="Where XMI appeared before (Families2Persons).")

g.sec("E. Eclipse, EMF and Ecore")
g.qa("MED", "Summarise the history of Eclipse, EMF and Ecore.", T, "slide 17",
     short="History of Eclipse, EMF, Ecore (dates).",
     extra=[grid([
         ["", "Milestones"],
         ["<b>Eclipse IDE</b>", "1998-2001 internal IBM project; 2001 Eclipse 1.0 public; 2004 Eclipse Foundation"],
         ["<b>EMF</b> (Eclipse Modeling Framework)", "2002-2004 internal IBM project; 2004 EMF 2.0 released in Eclipse "
                                                     "3.0 and embedded in the EMP"],
         ["<b>Ecore</b> (EMF Core)", "2004: core metamodel of EMF from the start; EMF 2.0 released as part of the UML/MOF "
                                     "2.0 alignment; embedded in EMP. 2024: latest EMF 2.28.0"],
     ], [45 * mm, 125 * mm])])

g.qa("HIGH", "Describe the Ecore hierarchy, and map the main Ecore classes to MOF.",
     "Root <b>EObject</b>, then abstract <b>EModelElement</b> with <b>EFactory</b>, abstract <b>ENamedElement</b> and "
     "<b>EAnnotation</b>. ENamedElement: <b>EPackage</b>, abstract <b>EClassifier</b> (<b>EClass</b>, <b>EDataType</b> "
     "with subclass <b>EEnum</b>), <b>EEnumLiteral</b>, abstract <b>ETypedElement</b> (abstract "
     "<b>EStructuralFeature</b> with <b>EAttribute</b> and <b>EReference</b>; <b>EOperation</b>; <b>EParameter</b>).",
     "slides 8, 18 (mapping: reasoning)", short="Ecore hierarchy and its MOF counterparts.",
     extra=[grid([
         ["MOF (slide 8)", "Ecore (slide 18)"],
         ["ModelElement", "EModelElement (root: EObject)"], ["Package", "EPackage"], ["Classifier", "EClassifier"],
         ["Class", "EClass"], ["DataType", "EDataType (EEnum for enumerations)"],
         ["StructuralFeature", "EStructuralFeature"], ["Attribute", "EAttribute"], ["Reference", "EReference"],
         ["Operation", "EOperation (with EParameter)"],
     ], [70 * mm, 100 * mm]), Spacer(1, 4),
         Paragraph("Ecore is EMF's <b>M3</b> language, the counterpart of MOF (it is close to the \"Essential MOF\" "
                   "subset). Lecture 5's Families.ecore and Persons.ecore are written in it.", S["small"])])

g.qa("MED", "Express the Families metamodel (Lecture 5) in Ecore terms.",
     bullets([
         c("Family") + " and " + c("Member") + ": <b>EClass</b>es inside one <b>EPackage</b> (Families).",
         c("lastName") + ", " + c("firstName") + ": <b>EAttribute</b>s typed by the <b>EDataType</b> EString.",
         c("father, mother, sons, daughters") + ": containment <b>EReference</b>s from Family to Member; "
         + c("familyFather") + " etc. are their opposite EReferences.",
         "Persons: " + c("Person") + " an abstract EClass with EAttribute " + c("fullName") + "; " + c("Male") + "/"
         + c("Female") + " EClasses with Person as supertype.",
     ]) + "<br/><i>(My own exercise connecting Lectures 5 and 6.)</i>", "slide 18; L5 slide 18",
     short="Express Families/Persons metamodels in Ecore terms.")

g.sec("F. Slide details to be aware of")
g.qa("LOW", "Which slide details are inconsistent?",
     bullets([
         "<b>Slide 5:</b> \"Sematics\" is a typo for Semantics; \"both of which are have two parts\".",
         "<b>Slide 12:</b> \"UML is defined as a MOF metamodel MOF\": read as \"UML is defined as a MOF metamodel\".",
         "<b>Slide 16:</b> the XMI is illustrative, not well-formed (" + c("xmi. id") + " with a space, a closing "
         + c("</Operation>") + " after a self-closed tag).",
     ]), "slides 5, 12, 16", short="Slide typos/inconsistencies.")

g.self_test()
g.build()
