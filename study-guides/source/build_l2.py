from guide_lib import *

g = Guide("L2-OCLOverview-Questions.pdf", "MDD - Lecture 2: OCL Overview - Exam question bank",
          "MDD Lecture 2 - Exam Questions")

g.p("Lecture 2: OCL Overview", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "slides 1-21, Exercise Sheet 1 (Q1) and Exercise Sheet 2 (Q1).", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "This lecture has two halves: <b>theory</b> (what OCL is, Design by Contract, invariants, pre/postconditions) and "
    "<b>writing OCL</b> on the Royal &amp; Loyal model. For the writing part, <b>write the OCL by hand</b> before "
    "looking: arrow vs dot, role names and Set vs Bag are where marks are lost.",
    "Page 2 has an OCL cheat sheet and the Royal &amp; Loyal navigation table.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "<b>OCL</b> is a typed, formal language for writing expressions on UML models. A <b>constraint</b> is a valid "
    "OCL expression of type <b>Boolean</b>.",
    "Constraints come from <b>Design by Contract</b>: an object has <b>rights</b> (preconditions) and "
    "<b>obligations</b> (postconditions). <b>Invariants</b> must hold for every instance whenever no operation is running.",
    "OCL is <b>declarative</b> (no side effects) and <b>typed</b> (checkable before execution).",
    "Write a constraint as " + c("context <Class> inv <name>: <Boolean expression>") + ". Navigate associations with the "
    "<b>role name</b> (or the class name in lower case).",
    "Use the <b>dot</b> " + c(".") + " for attributes and navigation, the <b>arrow</b> " + c("->") +
    " for collection operations.",
    "One navigation gives a <b>Set</b> (or <b>OrderedSet</b> for an " + c("{ordered}") + " end); two or more give a "
    "<b>Bag</b> (or <b>Sequence</b>), so use " + c("->asSet()") + " before counting distinct objects.",
]))

g.add(PageBreak())
g.p("Cheat sheet: OCL syntax from this lecture", "h1")
g.add(code_block("""
-- invariant (optionally named)
context Customer
inv ofAge: age >= 18

-- navigation: role name, or class name in lower case if no role name
context CustomerCard
inv: printedName = owner.title.concat(owner.name)

-- collection operations use the arrow
context LoyaltyProgram
inv: levels->size() >= 2

-- several associations -> Bag; asSet() removes duplicates
context ProgramPartner
inv: numberOfCustomers = programs.participants->asSet()->size()

-- {ordered} association end -> ordered collection
context LoyaltyProgram
inv: levels->first().name = 'Silver'

-- pre/postconditions: context is Class::operation(...)
context LoyaltyAccount::isEmpty() : Boolean
pre : -- none
post: result = (points = 0)
"""))
g.add(Spacer(1, 6))
g.p("Royal &amp; Loyal model: how to navigate (from slide 11)", "h1")
g.p("Read a row as: from an object of <i>Class</i>, write <i>Class.role</i> to reach the target. In an exam, always use "
    "the role names printed on the diagram you are given.", "small")
g.add(grid([
    ["From", "Navigate with", "Reaches", "Multiplicity", "Result type"],
    ["ProgramPartner", "programs", "LoyaltyProgram", "1..*", "Set"],
    ["LoyaltyProgram", "partners", "ProgramPartner", "1..*", "Set"],
    ["LoyaltyProgram", "participants", "Customer", "0..*", "Set"],
    ["Customer", "programs", "LoyaltyProgram", "0..*", "Set"],
    ["LoyaltyProgram", "levels {ordered}", "ServiceLevel", "1..*", "OrderedSet (slide 20 says Sequence)"],
    ["Customer", "cards", "CustomerCard", "0..*", "Set"],
    ["CustomerCard", "owner", "Customer", "1", "single object"],
    ["Membership", "account", "LoyaltyAccount", "0..1", "single object (may be absent)"],
    ["Membership", "currentLevel", "ServiceLevel", "1", "single object"],
    ["Membership", "card", "CustomerCard", "1", "single object"],
    ["LoyaltyAccount", "transactions", "Transaction", "0..*", "Set"],
    ["ProgramPartner", "deliveredServices", "Service", "0..*", "Set"],
    ["ServiceLevel", "availableServices", "Service", "0..*", "Set"],
    ["CustomerCard", "transactions", "Transaction", "0..*", "Set"],
], [32 * mm, 34 * mm, 32 * mm, 22 * mm, 50 * mm]))
g.p("Membership is the <b>association class</b> on the LoyaltyProgram-Customer association. Where the slide shows no "
    "multiplicity it is taken as 1, as in the Warmer &amp; Kleppe book the slides come from.", "small")
g.add(PageBreak())

g.sec("A. What OCL is and why we need it")
g.qa("HIGH", "What is OCL? What is a constraint?",
     "<b>OCL (Object Constraint Language)</b> is a language for defining <b>typed expressions on UML models</b>. Every "
     "OCL expression is written according to the rules of OCL's <b>formal grammar</b>.<br/>A <b>constraint</b> is a "
     "<b>valid OCL expression of type Boolean</b>. (" + c("age + 1") + " is an expression but not a constraint; "
     + c("age >= 18") + " is a constraint.)", "slide 2", short="What is OCL? What is a constraint?")

g.qa("LOW", "Summarise the history and standardisation of OCL.",
     bullets([
         "Standardised by the <b>OMG</b> as part of <b>UML 1.4</b>; part of the UML family of standards.",
         "<b>OCL 2.0</b> was standardised in <b>October 2003</b> as part of the OMG's effort to <b>align UML and MOF</b>; "
         "upwardly compatible, with a few added features.",
         "Current version: <b>OCL 2.4 (2014)</b>.",
     ]), "slide 2", short="History/standardisation of OCL.")

g.qa("HIGH", "What does a constraint do, and what are the advantages of using constraints?",
     "A constraint <b>restricts the properties of (instances of) object-oriented models or systems</b>.<br/>Advantages:<br/>"
     + bullets(["<b>Better documentation</b>: visual models are enriched with extra information",
                "<b>Improved precision</b>: more accurate statements",
                "<b>Less ambiguity</b>: misunderstandings are reduced and caught earlier"]) +
     "<br/><i>Why diagrams alone are not enough (reasoning):</i> a class diagram cannot say \"a customer must be at "
     "least 18\" or \"validFrom is before goodThru\". Comments can, but they are ambiguous and cannot be checked by tools.",
     "slide 3", short="What a constraint does; three advantages.")

g.qa("HIGH", "Name and explain the four goals of OCL.",
     bullets([
         "<b>Enrich UML models</b>: allow extra information where necessary and describe behaviour with <b>Design by "
         "Contract</b>.",
         "<b>Precise and unambiguous</b>, yet easy to read and write for <b>all stakeholders</b>, including "
         "non-mathematicians.",
         "<b>Declarative</b>: expressions have <b>no side effects</b>.",
         "<b>Typed</b>: expressions can be <b>checked before execution</b>.",
     ]) + "<br/>Memory hook: <b>E-P-D-T</b>.", "slide 9", short="Four goals of OCL.")

g.qa("MED", "Why is it important that OCL is declarative and has no side effects?",
     "An OCL expression only <b>describes</b> a condition; it does not <b>do</b> anything. Checking a constraint must "
     "never change the state of the system, otherwise checking a rule could break the system or give different results "
     "each time. It also means constraints can be evaluated at any time, in any order, by any tool. "
     "<i>(Explanation goes slightly beyond the slide.)</i>", "slide 9 (reasoning)",
     short="Why declarative / no side effects matters.")

g.sec("B. Design by Contract")
g.qa("HIGH", "Describe the concept of Design by Contract. How is this concept supported by OCL?",
     "<b>Design by Contract</b> is a software design principle derived from the <b>legal notion of a contract</b>: an "
     "agreement between two parties in which <b>both accept obligations</b> and on which <b>both can found their "
     "rights</b>.<br/>" + bullets([
         "In software design, a contract <b>clearly establishes the expectations and responsibilities of an object</b>.",
         "An object is responsible for executing services (the <b>obligations</b>) <b>if and only if</b> certain "
         "stipulations (the <b>rights</b>) are fulfilled.",
         "It provides an <b>exact specification of an object's interface</b>.",
     ]) + "<br/><b>OCL support:</b> Design by Contract is supported by <b>invariants</b> and <b>pre-/postconditions</b>. "
     "They provide a <b>semantic check, not only a type check</b>. Each operation (service) has a precondition and a "
     "postcondition:<br/>" + bullets([
         "<b>Precondition</b>: specifies the <b>rights</b> of the object offering the service; must be true <b>at the "
         "moment the operation is to be executed</b> for the contract to hold.",
         "<b>Postcondition</b>: specifies the <b>obligations</b> of the object offering the service; must be true <b>at "
         "the moment the operation has ended</b>.",
         "<b>Invariant</b>: coupled to classes, types and interfaces, so it <b>transcends any one operation</b>; defines "
         "what must always be true for all instances <b>when no operation is executing</b>; can be viewed as part of the "
         "pre- and postcondition of every operation of the class.",
     ]), "slides 4-8; Exercise Sheet 1, Q1 (sample solution)", tut="1, Q1",
     short="Describe Design by Contract and how OCL supports it.")

g.qa("HIGH", "What does a contract describe for a particular service, and how is it formally defined?",
     "For a service (method) a contract describes:<br/>" + bullets([
         "the <b>starting conditions</b> under which the service is to be provided",
         "the <b>results</b> that should be delivered, given that the starting conditions are fulfilled",
     ]) + "<br/>Rights and obligations must be defined <b>precisely and unambiguously</b>. An object's contract is "
     "formally defined in terms of <b>invariants</b> and <b>pre- and postconditions</b>, shown in UML with the stereotypes "
     + c("<<invariant>>") + ", " + c("<<precondition>>") + ", " + c("<<postcondition>>") + ".",
     "slide 5", short="What a contract describes; formal definition incl. stereotypes.")

g.qa("MED", "Postal example: \"For 4 Euros a letter of at most 80 g is delivered anywhere in the country within "
     "24 hours.\" List each party's obligations and rights.",
     "See the table below. Each party's obligations are the other party's rights.", "slide 6",
     short="Postal contract: obligations and rights of both parties.",
     extra=[grid([
         ["Party", "Obligations", "Rights"],
         ["<b>Customer</b>", "pay 4 Euros; supply letter under 80 g; specify a delivery address within the country",
          "letter delivered within 24 hours"],
         ["<b>Delivery company</b>", "deliver the letter within 24 hours",
          "receive 4 Euros; receive letter under 80 g; delivery address is within the country"],
     ], [35 * mm, 70 * mm, 65 * mm])])

g.qa("HIGH", "Define preconditions and postconditions: whose rights/obligations, and when must they be true?",
     "See the table below.", "slide 7", short="Pre- vs postconditions (whose rights/obligations, when true).",
     extra=[grid([
         ["", "Precondition", "Postcondition"],
         ["Specifies", "the <b>rights</b> of the object <b>offering</b> the service",
          "the <b>obligations</b> of the object <b>offering</b> the service"],
         ["Must be true", "when the operation <b>is about to be executed</b>", "when the operation <b>has finished</b>"],
     ], [30 * mm, 70 * mm, 70 * mm]), Spacer(1, 4),
         Paragraph("Failure of either a pre- or a postcondition <b>breaks the contract</b>. An object's behaviour "
                   "corresponds to the set of services it offers as operations (methods).", S["a"])])

g.qa("MED", "Map the postal example onto an operation " + c("deliver(letter)") + " of the delivery company. What are "
     "the pre- and postconditions? Who is at fault if each one fails?",
     bullets([
         "<b>Preconditions</b> (rights of the provider): fee of 4 Euros paid, weight &lt; 80 g, address within the country.",
         "<b>Postcondition</b> (obligation of the provider): letter delivered within 24 hours.",
         "If a <b>precondition</b> fails, the <b>caller (customer)</b> broke the contract; the company owes nothing.",
         "If a <b>postcondition</b> fails although the preconditions held, the <b>provider (company)</b> broke it.",
     ]) + "<br/><i>The blame assignment is the standard Design-by-Contract reading.</i>",
     "slides 6-7 (reasoning)", short="Postal example as pre/post; who is at fault.")

g.qa("HIGH", "What is an invariant? How does it relate to pre- and postconditions?",
     bullets([
         "A constraint <b>coupled to a class, type or interface</b>; it <b>transcends any one particular operation</b>.",
         "Defines what must <b>always be true for all instances</b> of the class <b>when none of the operations is "
         "executing</b> (during an operation it may be temporarily violated).",
         "Can be viewed as <b>part of the pre- and postcondition of every operation</b> of the class.",
     ]), "slide 8", short="What is an invariant; relation to pre/post.")

g.sec("C. The Royal & Loyal model")
g.qa("MED", "Describe the Royal &amp; Loyal (R&amp;L) domain in your own words.",
     bullets([
         "R&amp;L handles <b>loyalty programs</b> for companies that give good customers bonuses (air miles, reduced "
         "rates, a larger car, better service, ...).",
         "A <b>ProgramPartner</b> offers membership in a <b>LoyaltyProgram</b>; several companies can join the same "
         "program, and customers can use bonuses from any participating company.",
         "<b>Membership</b> in a program entitles a <b>Customer</b> to a <b>CustomerCard</b>.",
         "Bonus points are saved in a <b>LoyaltyAccount</b> associated with each Membership.",
         "Points are gained or spent through <b>Transactions</b>: <b>Earning</b> gains points, <b>Burning</b> spends them.",
         "Customers get different levels of <b>Service</b> depending on their <b>ServiceLevel</b>.",
     ]), "slides 10-11", short="Describe the Royal & Loyal domain.")

g.sec("D. Writing OCL: rules")
g.qa("HIGH", "How do you write an invariant on an attribute? Give the general form and the slide example.",
     bullets([
         "Identify the <b>context</b>: the class that owns the attribute, " + c("context <ClassName>") + ".",
         "Write a <b>Boolean expression</b> after " + c("inv:") + "; all attributes of the context class may be used.",
         "Invariants <b>may be named</b>: " + c("inv <name>: ...") + ".",
     ]) + "<br/>" + ocl("context Customer\ninv ofAge: age >= 18"), "slide 12",
     short="General form of an invariant + age example.")

g.qa("HIGH", "How do you navigate to an associated class in OCL? What if the association end has no role name?",
     "Use the <b>role name</b> at the opposite end of the association. If there is <b>no role name</b>, use the <b>name "
     "of the associated class starting with a lower-case letter</b>.<br/>" +
     ocl("context CustomerCard\ninv: printedName = customer.title.concat(customer.name)") +
     "<br/>On slide 13 there is no role name, so it writes " + c("customer") + ". In the full model (slide 11) the role "
     "is " + c("owner") + ", so there you write " + c("owner.title.concat(owner.name)") + ". The tutorials use the same "
     "rule, e.g. Room to Guest has no role name, so Sheet 2 writes " + c("self.guest") + ".",
     "slide 13; Exercise Sheet 2", short="Navigating to an associated class; no role name.")

g.qa("HIGH", "When does navigation produce a collection, and when do you use " + c(".") + " versus " + c("->") + "?",
     "When the <b>multiplicity is greater than one</b>, navigation may produce a <b>set of objects</b>. Collections have "
     "predefined operations, invoked with the <b>arrow</b>.<br/>" + bullets([
         c(".") + " : attribute access or navigation (" + c("owner.name") + ")",
         c("->") + " : operation on a collection (" + c("levels->size()") + ", " + c("cards->isEmpty()") + ")",
     ]) + "<br/>" + ocl("context LoyaltyProgram\ninv: serviceLevel->size() >= 2") +
     "<br/>The slide writes " + c("serviceLevel") + " because its small diagram has no role name; with the full model "
     "you write " + c("levels->size() >= 2") + ".", "slide 14", short="When navigation gives a collection; dot vs arrow.")

g.qa("HIGH", "Explain \"multiplicity constraints are a shorthand for OCL constraints\". Write the OCL for 1..*, 0..* "
     "and 0..1.",
     ocl("context ProgramPartner\ninv: loyaltyProgram->size() >= 1      -- 1..*\n\n"
         "context LoyaltyProgram\ninv: customer->size() >= 0            -- 0..*\n\n"
         "context Membership\ninv: loyaltyAccount->size() >= 0 and\n     loyaltyAccount->size() <= 1       -- 0..1") +
     "<br/>Worth saying in an exam: the " + c("0..*") + " constraint is always true (a size cannot be negative); for "
     + c("0..1") + " only " + c("<= 1") + " restricts anything.", "slide 15",
     short="Multiplicities as OCL invariants (1..*, 0..*, 0..1).")

g.qa("HIGH", "What is the difference between navigating over one association and over several? How do you get a set "
     "back?",
     "Navigating over <b>one</b> association yields a <b>Set</b>; over <b>two or more</b> yields a <b>Bag</b>. Turn a bag "
     "into a set with " + c("asSet()") + ".<br/>" +
     ocl("context ProgramPartner\nloyaltyProgram                     -- Set of LoyaltyPrograms\n"
         "loyaltyProgram.customer            -- Bag of Customers\nloyaltyProgram.customer->asSet()   -- Set of Customers") +
     "<br/><b>Why a bag?</b> A customer in two programs of the same partner is reached once via each program.",
     "slide 16", short="One vs several associations (Set vs Bag); asSet().")

g.qa("HIGH", "Which invariant is correct? \"The number of customers who participate in one or more loyalty programs "
     "of a partner must equal its numberOfCustomers attribute.\"",
     ocl("-- (1)\ncontext ProgramPartner\ninv: numberOfCustomers = loyaltyProgram.customer->size()\n\n"
         "-- (2)\ncontext ProgramPartner\ninv: numberOfCustomers = loyaltyProgram.customer->asSet()->size()") +
     "<br/><b>(2) is correct.</b> " + c("loyaltyProgram.customer") + " is a <b>Bag</b>, so (1) counts a customer in "
     "several programs more than once. " + c("asSet()") + " removes duplicates.", "slide 17",
     short="numberOfCustomers: which invariant is correct (Set vs Bag).")

g.qa("HIGH", "What kinds of collections are defined in OCL and what are their properties? What is the rule for "
     "collections when navigating over associations in a UML model?",
     "This is the official tutorial answer table. All four are subtypes of the abstract type <b>Collection</b>.",
     "slides 16-20; Exercise Sheet 2, Q1 (sample solution)", tut="2, Q1",
     short="Collection kinds, their properties, and the navigation rule (table).",
     extra=[grid([
         ["Collection", "Ordered", "Duplicates", "Result after how many navigations"],
         ["<b>Set</b>", "No", "No", "1st (one association)"],
         ["<b>OrderedSet</b>", "Yes", "No", "1st (one association, end marked {ordered})"],
         ["<b>Bag</b>", "No", "Yes", "2nd and later (two or more associations)"],
         ["<b>Sequence</b>", "Yes", "Yes", "2nd and later, over {ordered} ends"],
     ], [30 * mm, 22 * mm, 25 * mm, 93 * mm]), Spacer(1, 4),
         Paragraph(careful("slide 20 says navigating an {ordered} end gives a <b>Sequence</b>; the tutorial table says "
                           "<b>OrderedSet</b> after the first navigation (which is OCL 2.x). In the exam, reproduce "
                           "this table; if the question is about slide 20, mention both."), S["a"])])

g.qa("MED", "What two groups of operations does every collection type provide? Give examples.",
     "<b>Standard operations</b> (same meaning on all collection types): " +
     c("size(), isEmpty(), notEmpty(), includes(o), excludes(o), includesAll(c), excludesAll(c), count(o), sum()") +
     "<br/><b>Loop (iterator) operations</b>, taking an expression evaluated per element: " +
     c("select, reject, collect, collectNested, exists, forAll, one, any, isUnique, sortedBy, iterate") +
     "<br/>" + c("isUnique(expr)") + " is true if the expression gives a different value for every element; the "
     "tutorial uses " + c("song->isUnique(title)") + " for \"all titles on a card are unique\" (see Lecture 3 guide).",
     "slide 18; Exercise Sheet 1", short="Standard vs loop operations, with examples.")

g.qa("MED", "What is flattening of collections?",
     "In OCL a collection <b>never contains collections</b>, only simple objects. When a collection is inserted into "
     "another, the result is <b>automatically flattened</b>:<br/>" +
     ocl("Set{ Set{a, b}, Set{c, d}, Set{e, f, g} }\nSet{ a, b, c, d, e, f, g }   -- effectively identical") +
     "<br/>That is why " + c("loyaltyProgram.customer") + " is one flat Bag of Customers.", "slide 19",
     short="Flattening of collections.")

g.qa("MED", "What do you get when you navigate an end marked " + c("{ordered}") + "? Give the example.",
     "An <b>ordered</b> collection, so " + c("first()") + " can be used:<br/>" +
     ocl("context LoyaltyProgram\ninv: levels->first().name = 'Silver'") +
     "<br/>Slide 20 calls it a Sequence; the tutorial (and OCL 2.x) an OrderedSet. Either way it is ordered.",
     "slide 20; Exercise Sheet 2", short="Navigating an {ordered} end; Silver example.")

g.qa("HIGH", "How are pre- and postconditions written in OCL? Explain the " + c("isEmpty()") + " example.",
     bullets([
         "The <b>context is extended to include an operation</b>: " + c("context Class::operation(params) : ReturnType"),
         "All attributes and links of the class can be used; the expressions <b>hold only for that operation</b>.",
         "Keywords " + c("pre") + " and " + c("post") + " mark the two parts; " + c("result") + " is the <b>return value</b>.",
     ]) + "<br/>" + ocl("context LoyaltyAccount::isEmpty() : Boolean\npre : -- none\npost: result = (points = 0)") +
     "<br/>No precondition (" + c("--") + " starts a comment); the result is true exactly when the account has 0 points.",
     "slide 21", short="Syntax of pre/post; isEmpty() example; result.")

g.sec("E. Practice: write the OCL")
g.p("Practice on the R&amp;L model (navigation table on page 2). My own exercises in the slides' style.", "small")

g.qa("HIGH", "Every CustomerCard's validFrom date must be before its goodThru date.",
     ocl("context CustomerCard\ninv checkDates: validFrom.isBefore(goodThru)") +
     "<br/>Date is a datatype with " + c("isBefore(t : Date) : Boolean") + "; call it with the dot.",
     "exercise", short="Write: validFrom before goodThru.")

g.qa("HIGH", "A Service may never earn or burn a negative number of points.",
     ocl("context Service\ninv: pointsEarned >= 0 and pointsBurned >= 0"), "exercise",
     short="Write: no negative pointsEarned/pointsBurned.")

g.qa("HIGH", "Every LoyaltyProgram has at least one partner; a Customer owns at most 5 cards; every ProgramPartner "
     "delivers at least one service.",
     ocl("context LoyaltyProgram\ninv: partners->size() >= 1\n\ncontext Customer\ninv: cards->size() <= 5\n\n"
         "context ProgramPartner\ninv: deliveredServices->notEmpty()"), "exercise",
     short="Write: >= 1 partner; <= 5 cards; >= 1 delivered service.")

g.qa("HIGH", "Using the full model: a ProgramPartner's numberOfCustomers equals the number of distinct customers in "
     "its programs.",
     ocl("context ProgramPartner\ninv: numberOfCustomers = programs.participants->asSet()->size()") +
     "<br/>Two navigations give a Bag; " + c("asSet()") + " makes each customer count once.", "slides 11, 17",
     short="Write: numberOfCustomers = distinct customers (full model).")

g.qa("HIGH", "Give the type of each expression.", "See the table below.", "slides 14-20",
     short="Result types of 8 navigation expressions.",
     extra=[grid([
         ["Context", "Expression", "Type"],
         ["Customer", c("cards"), "Set(CustomerCard)"],
         ["CustomerCard", c("owner"), "Customer (single object)"],
         ["CustomerCard", c("owner.name"), "String"],
         ["ProgramPartner", c("programs.participants"), "Bag(Customer)"],
         ["ProgramPartner", c("programs.participants->asSet()"), "Set(Customer)"],
         ["LoyaltyProgram", c("levels"), "OrderedSet(ServiceLevel) (slide 20: Sequence)"],
         ["Customer", c("cards.transactions"), "Bag(Transaction)"],
         ["LoyaltyProgram", c("levels->size() >= 2"), "Boolean (so it is a constraint)"],
     ], [35 * mm, 70 * mm, 65 * mm])])

g.qa("HIGH", "Find and fix the mistake in each constraint.",
     ocl("-- (a)\ncontext LoyaltyProgram\ninv: levels.size() >= 2\n\n-- (b)\ncontext Customer\ninv: age + 1\n\n"
         "-- (c)\ncontext ProgramPartner\ninv: numberOfCustomers = programs.participants->size()\n\n"
         "-- (d)\ncontext CustomerCard\ninv: printedName = Customer.title.concat(Customer.name)") +
     "<br/>" + bullets([
         "(a) " + c("size()") + " is a collection operation: " + c("levels->size() >= 2") + ".",
         "(b) Not Boolean, so not a constraint; e.g. " + c("age >= 18") + ".",
         "(c) Counts a Bag (duplicates): add " + c("->asSet()") + " before " + c("->size()") + ".",
         "(d) Use the role name (" + c("owner") + ") or the class name in <b>lower case</b>, never the capitalised name.",
     ]), "slides 2, 13, 14, 17", short="Find and fix four broken constraints.")

g.self_test()
g.build()
