from guide_lib import *

g = Guide("L3-OCLFeatures-Questions.pdf", "MDD - Lecture 3: OCL Features - Exam question bank",
          "MDD Lecture 3 - Exam Questions")
T = "See the table below."

g.p("Lecture 3: OCL Features", "title")
g.p("Model-Driven Development, University of Mannheim, Fall 2026. Exam question bank with model answers, built from "
    "slides 1-45 and Exercise Sheets 1 (Q3), 2 (Q2-Q3) and 3.", "sub")
g.add(Spacer(1, 10))

g.p("How to use this", "h1")
g.p(bullets(HOW_TO_USE_COMMON + [
    "This is the core OCL lecture. Three kinds of questions: <b>explain</b> (definitions, differences), <b>evaluate</b> "
    "(what does this return?) and <b>write</b> (turn an English rule into OCL for a given class diagram).",
    "<b>Section K (tutorials) is the most exam-like part of this guide.</b> The exercise sheets give a class diagram "
    "and ask for invariants, derive/init rules, def operations and pre/postconditions. Expect the exam to look like that.",
    "Pages 2-4 are cheat sheets. Section J lists slide errors.",
]))

g.p("The 60-second summary", "h1")
g.p(bullets([
    "<b>Types:</b> basic (Integer, Real, String, Boolean), collection (Set, OrderedSet, Bag, Sequence), and model types. "
    "Basic/collection types and UML datatypes/enumerations are <b>value types</b>; classes are <b>object types</b>.",
    "Only <b>query operations</b> (no side effects) may be called in OCL.",
    "Navigating <b>from</b> an association class gives a <b>single object</b>; <b>over</b> one gives a <b>Bag</b>.",
    "Besides " + c("inv/pre/post") + ": " + c("init") + " (initial value), " + c("derive") + " (derived attribute), " +
    c("body") + " (query result), " + c("def") + " (new attribute/operation), " + c("let") + " (local name).",
    "In postconditions: " + c("x@pre") + " = old value, " + c("result") + " = return value, " + c("oclIsNew()") +
    " = created during the operation.",
    c("oclIsTypeOf") + " = exact type; " + c("oclIsKindOf") + " = type or subtype.",
    "Undefined spreads, <b>except</b> " + c("true or undefined = true") + " and " + c("false and undefined = false") + ".",
    c("select/reject/collect") + " return collections, " + c("forAll/exists") + " Boolean, " + c("iterate") +
    " is the general form behind all of them.",
]))

g.add(PageBreak())
g.p("Cheat sheet 1: every kind of OCL expression", "h1")
g.add(code_block("""
-- invariant
context Customer inv adult: age >= 18
-- initial value
context LoyaltyAccount::points init: 0
-- derived attribute
context CustomerCard::printedName
  derive: owner.title.concat(' ').concat(owner.name)
-- result of a query operation
context LoyaltyProgram::getServices(pp : ProgramPartner) : Set(Service)
  body: if partners->includes(pp) then pp.deliveredServices else Set{} endif
-- new attribute / new operation
context LoyaltyAccount
  def: turnover : Real = transactions.amount->sum()
context Hotel
  def: freeRoomNumbers() : Set(Integer) =
         room->select(not occupied).number->asSet()
-- @pre = value before the operation
context LoyaltyProgram::enroll(c : Customer)
  pre : not (participants->includes(c))
  post: participants = participants@pre->including(c)
-- result = the return value
context Transaction::program() : LoyaltyProgram
  post: result = self.card.membership.programs
-- let = local name inside one expression
context CustomerCard
  inv: let correctDate : Boolean =
         validFrom.isBefore(Date::now) and goodThru.isAfter(Date::now)
       in if valid then correctDate = true else correctDate = false endif
"""))
g.add(Spacer(1, 6))
g.p("What " + c("::") + " means in each place", "h1")
g.add(grid([
    ["Written as", "Meaning", "Slide"],
    [c("context LoyaltyAccount::earn(i : Integer)"), "an operation as the context (pre/post/body)", "L2-21, 19"],
    [c("context LoyaltyAccount::points"), "an attribute as the context (init/derive)", "18"],
    [c("self.PartnerAspects::partners"), "package name, to avoid a name clash", "15"],
    [c("self.Cassette::volume"), "inheritance pathname: which superclass's property", "16"],
    [c("Date::now"), "class-level (static) attribute or operation", "17"],
    [c("Customer::allInstances()"), "class-level operation: the set of all instances", "26"],
    [c("StringType::plastic"), "enumeration literal", "L4-12"],
], [82 * mm, 68 * mm, 20 * mm]))

g.add(PageBreak())
g.p("Cheat sheet 2: collection operations", "h1")
g.add(grid([
    ["Operation", "Result", "Notes"],
    [c("size()"), "Integer", "number of elements"],
    [c("count(o)"), "Integer", "how often o occurs"],
    [c("includes(o) / excludes(o)"), "Boolean", "is o (not) an element"],
    [c("includesAll(c)"), "Boolean", "all elements of c are present"],
    [c("isEmpty() / notEmpty()"), "Boolean", ""],
    [c("sum()"), "Integer/Real", "adds all elements"],
    [c("=") + " (equals)", "Boolean", "Bag: same counts; Sequence/OrderedSet: same order too"],
    [c("union(c)"), "collection", "Bag + Set gives Bag; Sequence/OrderedSet only with Sequence/OrderedSet"],
    [c("including(o)"), "collection", "Set: only if not present; Sequence/OrderedSet: added at the end"],
    [c("excluding(o)"), "collection", "Set/OrderedSet: removes the element; Bag/Sequence: removes ALL occurrences"],
    [c("intersection(c)"), "collection", "common elements; not with Sequence/OrderedSet; Bag involved gives Bag"],
    [c("s1 - s2"), "Set/OrderedSet", "elements of s1 not in s2"],
    [c("symmetricDifference(s)"), "Set", "in one set but not in both"],
    [c("subOrderedSet(l, u)"), "OrderedSet", "elements from position l to u"],
    [c("first() / last() / at(i)"), "element", "Sequence and OrderedSet only"],
    [c("append(o) / prepend(o)"), "collection", "append = add at the end, prepend = add at the front"],
    [c("asSet()"), "Set", "removes duplicates"],
], [50 * mm, 32 * mm, 88 * mm]))
g.add(Spacer(1, 6))
g.p("Iterators", "h1")
g.add(grid([
    ["Iterator", "Returns", "Meaning"],
    [c("c->select(e | cond)"), "collection (same kind)", "elements where cond is true"],
    [c("c->reject(e | cond)"), "collection (same kind)", "elements where cond is false"],
    [c("c->collect(e | expr)"), "Bag (from Set/Bag), Sequence (from Sequence)",
     "expr per element. Shorthand: " + c("c.attr")],
    [c("c->forAll(e | cond)"), "Boolean", "cond true for every element"],
    [c("c->exists(e | cond)"), "Boolean", "cond true for at least one element"],
    [c("c->isUnique(e | expr)"), "Boolean", "expr different for every element (tutorial, L2 slide 18)"],
    [c("c->iterate(e : T; acc : R = init | expr)"), "type R", "general fold; all of the above are special cases"],
], [55 * mm, 45 * mm, 70 * mm]))
g.p("All iterators (except iterate) have three forms: " + c("(e : Type | expr)") + ", " + c("(e | expr)") + ", "
    + c("(expr)") + ".", "small")

g.add(PageBreak())
g.p("Cheat sheet 3: patterns the tutorials keep asking for", "h1")
g.add(grid([
    ["English", "OCL pattern"],
    ["\"at least one X\"", c("x->notEmpty()") + "  or  " + c("x->size() >= 1")],
    ["\"exactly one X\" (end is *)", c("x->size() = 1")],
    ["\"every X satisfies P\"", c("x->forAll(e | P)")],
    ["\"some X satisfies P\"", c("x->exists(e | P)") + "  =  " + c("not x->forAll(e | not P)")],
    ["\"number of X with P\"", c("x->select(e | P)->size()")],
    ["\"all values unique\"", c("x->isUnique(attr)")],
    ["\"number of distinct Y over two hops\"", c("x.y->asSet()->size()")],
    ["\"average of attr\"", c("x.attr->sum() / x->size()") + "  (guard empty: if-then-else)"],
    ["\"remaining = total - used\"", c("derive: size - x.size->sum()")],
    ["\"one more X afterwards\"", c("post: x->size() = x@pre->size() + 1")],
    ["\"not already contained\"", c("pre: not m.x->includes(self)") + "  or  " + c("m.x->excludes(self)")],
    ["\"if A then B must hold\"", c("A implies B")],
    ["\"value is one of a fixed list\"", c("Set{'a', 'b', 'c'}->includes(v)")],
    ["\"values of the elements that satisfy P\"", c("x->select(P)->collect(attr)->asSet()")],
], [65 * mm, 105 * mm]))
g.p("Use <b>single quotes</b> for strings (" + c("'KLM'") + "). The tutorial solutions sometimes use double quotes; "
    "that is not valid OCL.", "small")

g.add(PageBreak())

g.sec("A. Types, expressions and constraints")
g.qa("HIGH", "What are the basic building blocks of OCL expressions, and which types does OCL recognise?",
     "The building blocks are <b>objects and object properties</b>. Each object has a <b>type</b>, which defines the "
     "operations that can be applied to it. OCL recognises:<br/>" + bullets([
         "<b>Predefined types</b>: <b>basic types</b> Integer, Real, String, Boolean; <b>collection types</b> Set, "
         "OrderedSet, Bag, Sequence",
         "<b>User-defined model types</b>: every class, interface or type in the UML model is automatically an OCL type",
     ]), "slide 2", short="Building blocks of OCL expressions; which types OCL recognises.")

g.qa("HIGH", "Explain the difference between value types and object types. Which types belong to which?",
     T, "slide 3", short="Value types vs object types; which types are which.",
     extra=[grid([
         ["", "Value type", "Object type"],
         ["Instances", "<b>never change</b> their value; the value <b>is</b> the instance (1 never becomes 2)",
          "<b>can change</b> their values (a Customer can change its name)"],
         ["Equality", "by value", "by <b>identity</b>, not by values"],
         ["Which types", "OCL basic and collection types; UML <b>datatypes</b> and <b>enumerations</b>",
          "normal UML <b>classes</b>"],
     ], [25 * mm, 72 * mm, 73 * mm])])

g.qa("MED", "When is an OCL expression valid, and when is it a constraint?",
     bullets([
         "An <b>expression</b> has a result, which defines its <b>type</b> (user-defined or predefined). It is <b>valid if "
         "and only if</b> it follows the rules of OCL and includes other expressions correctly.",
         "A <b>constraint</b> is a valid expression <b>of type Boolean</b>; true if it holds, false if not.",
     ]), "slide 4", short="Valid expression vs constraint.")

g.qa("MED", "What are model types, and what can OCL expressions refer to on them?",
     "User-defined types: <b>classes, interfaces, association classes, datatypes, enumeration types</b>. OCL can refer "
     "to their <b>attributes</b>, <b>operations/methods</b>, and <b>associations</b> (via navigation).",
     "slide 10", short="Model types; what OCL can refer to.")

g.qa("HIGH", "Which operations of a model type may be used in OCL, and why? How are they written?",
     bullets([
         "Only <b>query operations</b>, because OCL is <b>side-effect free</b>. A query operation returns a value but "
         "<b>doesn't change anything</b>; in UML it is marked <b>isQuery</b>.",
         "Model-type operations are <b>always followed by parentheses</b>, which may contain parameters.",
     ]) + "<br/>" + ocl("context Customer inv: self.age() >= 0\ncontext Customer inv: self.isRelatedTo(self) = true\n"
                        "context Customer inv: self.name = 'Jos senior' implies self.age() > 21") +
     "<br/>So " + c("earn(i)") + " or " + c("transfer(m)") + " (they change state) cannot be called in an invariant.",
     "slide 11", short="Which operations may be used in OCL and why; syntax.")

g.sec("B. Boolean, Integer, Real, String")
g.qa("HIGH", "List the Boolean operators of OCL and give the truth table of " + c("implies") + ".",
     "Operators: " + c("or, and, xor, not, =, <>, implies, if-then-else-endif") + ". All return Boolean except "
     + c("if a then b1 else b2 endif") + ", which has the type of b1/b2.<br/>" + c("a implies b") + " is <b>only false "
     "when a is true and b is false</b>; same as " + c("not a or b") + ".",
     "slides 5-6", short="Boolean operators; truth table of implies.",
     extra=[grid([["a", "b", "a implies b"], ["true", "true", "true"], ["true", "false", "<b>false</b>"],
                  ["false", "true", "true"], ["false", "false", "true"]], [30 * mm, 30 * mm, 40 * mm])])

g.qa("HIGH", "Explain " + c("context Service inv: pointsEarned > 0 implies pointsBurned = 0") + ".",
     "<b>A customer cannot burn bonus points using a service that is \"bought\" using bonus points</b>: if a service "
     "earns points it must not burn any. If it earns none, the implication is true no matter what.",
     "slide 6", short="Explain pointsEarned > 0 implies pointsBurned = 0.")

g.qa("HIGH", "How does if-then-else work in OCL? Why is the else part mandatory?",
     "The result is the value of the <b>then</b> or the <b>else</b> expression depending on the <b>if</b> condition. The "
     "<b>else clause must be present because the expression must always have a value</b>.<br/>" +
     ocl("context Customer\ninv: title = (if isMale = true then 'Mr.' else 'Ms.' endif)"),
     "slide 7", short="if-then-else; why else is mandatory; title example.")

g.qa("MED", "Integer and Real operations: which return Boolean, Integer, Real?",
     bullets([
         "<b>Boolean:</b> " + c("=, <>, <, >, <=, >="),
         "<b>Integer or Real</b> (depends on operands): " + c("+, -, *, abs, max(b), min(b)"),
         "<b>Always Real:</b> " + c("a / b"),
         "<b>Always Integer:</b> " + c("a.mod(b), a.div(b), a.round, a.floor"),
     ]) + "<br/>" + c("7 / 2 = 3.5") + ", " + c("7.div(2) = 3") + ", " + c("7.mod(2) = 1") + ", " + c("3.7.floor = 3") +
     ", " + c("3.5.round = 4") + ". The tutorial's average (" + c("sum() / size()") + ") is therefore a <b>Real</b>.",
     "slide 8", short="Integer/Real operations and result types.")

g.qa("MED", "What are the String operations? Evaluate " + c("'apple'.size()") + ", " + c("'apple'.toUpper()") + ", "
     + c("'apple'.concat('s')") + ", " + c("'apple'.substring(2,4)") + ".",
     "Literals use <b>single quotes</b>. Operations: " + c("concat, size, toLower, toUpper, substring(int, int), =, <>") +
     ".<br/>" + bullets([c("'apple'.size()") + " = 5", c("'apple'.toUpper()") + " = 'APPLE'",
                         c("'apple'.concat('s')") + " = 'apples'",
                         c("'apple'.substring(2,4)") + " = 'ppl' (positions from 1, both ends included)"]) +
     "<br/>Tutorial use: \"text at least 20 characters\" is " + c("text.size() >= 20") + ".",
     "slide 9; Exercise Sheet 3", short="String operations; evaluate on 'apple'.")

g.sec("C. Navigation: association classes, self, packages, inheritance, class level")
g.qa("HIGH", "What do you get when navigating FROM an association class, and OVER one? Explain both slide examples.",
     bullets([
         "<b>From</b> an association class to a class at an end: a <b>single object</b>.",
         "<b>Over</b> an association class (from a class through it onwards): a <b>Bag</b>.",
     ]) + "<br/>" + ocl("context Membership\ninv: program.levels->includes(currentLevel)") +
     "<br/>A membership's current level must be one of its own program's levels.<br/>" +
     ocl("context LoyaltyProgram\ninv: levels->includesAll(membership.currentLevel)") +
     "<br/>" + c("membership.currentLevel") + " is a <b>Bag</b> (many memberships can share a level). Every current level "
     "used by the program's memberships is one of its levels.", "slides 12-13",
     short="Navigating FROM vs OVER an association class; both examples.")

g.qa("HIGH", "What is " + c("self") + "? When is it needed?",
     c("self") + " <b>always refers to the context object</b>. " + c("inv: age >= 18") + " and " +
     c("inv: self.age >= 18") + " are identical. It <b>cannot be avoided</b> when the context object itself is a value:<br/>"
     + ocl("context Membership\ninv: customer.cards.membership->includes(self)") +
     "<br/>This membership must be among the memberships of its customer's cards. Tutorial use: "
     + c("pre: not m.song->includes(self)") + " (this song is not already on the card).",
     "slide 14; Exercise Sheet 1", short="What is self; when it is needed.")

g.qa("MED", "How and why do you use package names and inheritance pathnames in navigation?",
     bullets([
         "<b>Package names</b> avoid <b>name clashes</b> across packages: " +
         c("context LoyaltyProgram inv: self.PartnerAspects::partners->size() < 10"),
         "<b>Inheritance pathnames</b>: with <b>multiple inheritance</b> two superclasses may provide properties with the "
         "same name; use the class name: " + c("context CassetteBook inv: self.Cassette::volume < 10"),
     ]), "slides 15-16", short="Package names and inheritance pathnames.")

g.qa("MED", "What are class-level attributes and operations, and how are they referenced?",
     "Properties of the <b>type itself</b> (like static members). Syntax: <b>class name, two colons, name</b>:<br/>" +
     ocl("context CustomerCard\ninv: goodThru.isAfter(Date::now)"), "slide 17", short="Class-level features; Date::now.")

g.sec("D. init, derive, body, def, let, @pre, result")
g.qa("HIGH", "What are initial values and derivation rules? Write the two slide examples.",
     ocl("context LoyaltyAccount::points\ninit: 0\n\ncontext CustomerCard::printedName\n"
         "derive: owner.title.concat(' ').concat(owner.name)") + "<br/>" + bullets([
         c("init") + ": the value an attribute has <b>when the object is created</b>; may change later.",
         c("derive") + ": how a <b>derived</b> attribute (marked " + c("/") + ") is <b>always computed</b>.",
         "Context is the <b>attribute</b>: " + c("Class::attribute") + " (optionally with its type: "
         + c("context Room::occupied : Boolean") + ").",
     ]), "slide 18; Exercise Sheets 2-3", short="init and derive: meaning, difference, examples.")

g.qa("HIGH", "What is a body expression? Explain the " + c("getServices") + " example.",
     "A " + c("body") + " expression defines the <b>result of a query operation</b>.<br/>" +
     ocl("context LoyaltyProgram::getServices(pp : ProgramPartner) : Set(Service)\n"
         "body: if partners->includes(pp) then pp.deliveredServices else Set{} endif") +
     "<br/>If pp is a partner of this program, its delivered services; otherwise the empty set " + c("Set{}") + ".",
     "slide 19", short="Body expression; getServices.")

g.qa("HIGH", "What does " + c("def") + " do? Explain both slide examples.",
     c("def") + " <b>adds new attributes and operations</b> to the model.<br/>" +
     ocl("context LoyaltyAccount\ndef: turnover : Real = transactions.amount->sum()\n\n"
         "context LoyaltyProgram\ndef: getServicesByLevel(levelName : String) : Set(Service)\n"
         "  = levels->select(name = levelName).availableServices->asSet()") +
     "<br/>Attribute form: " + c("def: name : Type = expr") + ". Operation form: " +
     c("def: name(params) : Type = expr") + ". If a question says <b>method/operation</b>, use the form with parentheses.",
     "slide 20", short="def: new attribute vs new operation.")

g.qa("HIGH", "What is a " + c("let") + " expression for? Explain and simplify the slide example.",
     c("let") + " names a <b>large, repeated sub-expression</b>, usable after " + c("in") + "; unlike " + c("def") +
     " it exists only <b>inside that one expression</b>.<br/>" +
     ocl("context CustomerCard\ninv: let correctDate : Boolean =\n        self.validFrom.isBefore(Date::now) and\n"
         "        self.goodThru.isAfter(Date::now)\n    in if valid then correctDate = true\n"
         "       else correctDate = false endif") +
     "<br/>A card is valid <b>exactly when</b> today is between validFrom and goodThru; equivalent to "
     + c("valid = correctDate") + ".", "slide 21", short="let: purpose; simplify the correctDate example.")

g.qa("HIGH", "What is " + c("@pre") + "? Explain the " + c("enroll") + " example.",
     "Postconditions often need a value <b>at the start of the operation</b>; " + c("@pre") + " is <b>postfixed</b> to the "
     "attribute or association.<br/>" +
     ocl("context LoyaltyProgram::enroll(c : Customer)\npre : not (participants->includes(c))\n"
         "post: participants = participants@pre->including(c)") +
     "<br/>Tutorial use (Sheet 3): " + c("post: review->size() = review@pre->size() + 1") + ".",
     "slide 22; Exercise Sheet 3", short="@pre; enroll example.")

g.qa("HIGH", "What is the keyword " + c("result") + "? Explain " + c("Transaction::program()") + ".",
     c("result") + " is the <b>value returned by an operation</b>; its type is the return type.<br/>" +
     ocl("context Transaction::program() : LoyaltyProgram\npost: result = self.card.membership.programs") +
     "<br/>Transaction to its card, to the card's membership, to that membership's program.",
     "slide 23", short="result keyword; Transaction::program().")

g.qa("HIGH", "Compare all OCL constraint kinds: inv, pre, post, init, derive, body, def, let.",
     T, "L2/L3 slides", short="Compare inv, pre, post, init, derive, body, def, let.",
     extra=[grid([
         ["Keyword", "Context", "Purpose"],
         [c("inv"), "class", "holds for all instances whenever no operation runs"],
         [c("pre"), "operation", "must hold when the operation starts"],
         [c("post"), "operation", "must hold when it ends; may use " + c("@pre") + ", " + c("result") + ", " +
          c("oclIsNew()")],
         [c("body"), "query operation", "defines the result value"],
         [c("init"), "attribute", "initial value at creation"],
         [c("derive"), "derived attribute", "how its value is always computed"],
         [c("def"), "class", "adds a new attribute/operation"],
         [c("let"), "inside any expression", "local name for a sub-expression"],
     ], [22 * mm, 40 * mm, 108 * mm])])

g.sec("E. OclAny, OclType, OclVoid and undefined")
g.qa("HIGH", "What are OclAny and OclType? Why do OclAny's properties start with \"ocl\"?",
     bullets([
         "<b>OclAny</b> is the <b>supertype of all types</b>; all OCL types, including model types, inherit from it.",
         "Its property names start with <b>\"ocl\"</b> to <b>avoid name clashes</b> with user-defined properties.",
         "<b>OclType</b> is the <b>(meta)type of OclAny</b>: all OCL types are <b>instances of OclType</b>.",
     ]), "slides 24-25", short="OclAny and OclType; why the ocl prefix.")

g.qa("MED", "List the operations defined on OclAny with their result types.", T, "slide 26",
     short="Operations of OclAny.",
     extra=[grid([
         ["Expression", "Result"],
         [c("o = o2") + ", " + c("o <> o2"), "Boolean"],
         [c("o.oclIsUndefined()"), "Boolean"],
         [c("o.oclIsKindOf(t)") + ", " + c("o.oclIsTypeOf(t)"), "Boolean"],
         [c("o.oclIsNew()"), "Boolean"],
         [c("o.oclAsType(t)"), "the type t (a cast)"],
         [c("o.oclInState(s)"), "Boolean"],
         [c("Type::allInstances()"), "Set(Type)"],
     ], [80 * mm, 90 * mm])])

g.qa("HIGH", "Explain " + c("oclIsTypeOf") + " vs " + c("oclIsKindOf") + " and fill in the slide-27 table.",
     c("oclIsTypeOf(T)") + ": the type is <b>identical</b> to T. " + c("oclIsKindOf(T)") + ": T <b>or any subtype</b>.",
     "slide 27", short="oclIsTypeOf vs oclIsKindOf (Transaction table).",
     extra=[grid([
         ["Expression", "self is a Transaction", "self is a BurningTransaction"],
         [c("oclIsKindOf(Transaction)"), "true", "<b>true</b>"],
         [c("oclIsTypeOf(Transaction)"), "true", "<b>false</b>"],
         [c("oclIsKindOf(BurningTransaction)"), "false", "true"],
         [c("oclIsTypeOf(BurningTransaction)"), "false", "true"],
         [c("oclIsKindOf(EarningTransaction)"), "false", "false"],
         [c("oclIsTypeOf(EarningTransaction)"), "false", "false"],
     ], [70 * mm, 45 * mm, 55 * mm])])

g.qa("MED", "What do " + c("oclAsType") + " and " + c("allInstances") + " do?",
     bullets([
         c("o.oclAsType(T)") + " <b>casts</b> o to T so T's properties can be used; if o is not of kind T the result is "
         "<b>undefined</b>.",
         c("T::allInstances()") + " returns the <b>Set of all instances</b> of T.",
     ]) + "<br/>" + ocl("context Customer\ninv: Customer::allInstances()->forAll(c |\n       c <> self implies c.name <> self.name)") +
     "<br/>(No two customers share a name. Shorter: " + c("Customer::allInstances()->isUnique(name)") + ".)",
     "slides 26, 29", short="oclAsType and allInstances.")

g.qa("HIGH", "When is an OCL expression undefined, and how does undefined propagate? What are the exceptions?",
     bullets([
         "E.g. when taking the attribute value of a <b>nonexistent object</b>.",
         "<b>Any expression with an undefined part is undefined as a whole</b>.",
         "<b>Exceptions:</b> " + c("true or undefined") + " is true; " + c("false and undefined") + " is false.",
     ]) + "<br/>But " + c("false or undefined") + " and " + c("true and undefined") + " are <b>undefined</b>.",
     "slide 28", short="Undefined: propagation and the or/and exceptions.")

g.qa("HIGH", "What is OclVoid?",
     bullets([
         "The <b>type of the undefined value</b>, returned when an operation fails, e.g. <b>incorrect type casting</b> or "
         "<b>getting an element from an empty collection</b>.",
         "It has <b>only one value</b> (undefined) and <b>conforms to all types</b>.",
         c("oclIsUndefined()") + " returns true if its argument is undefined.",
     ]), "slide 29", short="OclVoid.")

g.qa("HIGH", "What does " + c("oclIsNew()") + " do? Explain " + c("enrollAndCreateCustomer") + ".",
     "True if the object was <b>created during the operation</b> (did not exist when the precondition was evaluated), "
     "so only meaningful in <b>postconditions</b>.<br/>" +
     ocl("context LoyaltyProgram::enrollAndCreateCustomer(n : String, d : Date) : Customer\npre : -- none\n"
         "post: result.oclIsNew() and result.name = n and\n      result.dateOfBirth = d and participants->includes(result)"),
     "slide 30", short="oclIsNew; enrollAndCreateCustomer.")

g.sec("F. Collection types and operations")
g.qa("HIGH", "Define the four concrete collection types precisely.",
     bullets([
         "<b>Set</b>: <b>no duplicates</b>, unordered",
         "<b>OrderedSet</b>: a set whose elements are <b>ordered</b>",
         "<b>Bag</b>: <b>duplicates allowed</b>, unordered",
         "<b>Sequence</b>: an <b>ordered Bag</b> (ordered, <b>not sorted</b>); each element has a sequence number",
         "<b>Collection</b> is their <b>abstract supertype</b>.",
     ]) + "<br/>See also the tutorial table in the Lecture 2 guide (which navigation gives which type).",
     "slide 31; Exercise Sheet 2", short="Define Set, OrderedSet, Bag, Sequence.")

g.qa("HIGH", "Explain the difference between " + c("account->isEmpty()") + " and " + c("account.isEmpty()") + ".",
     "Applying " + c("->") + " to a single object treats it as a <b>Set with that one object</b> (or empty).<br/>" +
     bullets([c("account->isEmpty()") + ": the membership has <b>no LoyaltyAccount</b>.",
              c("account.isEmpty()") + ": calls LoyaltyAccount's own " + c("isEmpty()") + ": the account <b>has 0 "
              "points</b>."]) +
     "<br/>The tutorials use the same trick: " + c("self.guest->size() > 0") + " on a 0..1 end (Sheet 2).",
     "slide 32; Exercise Sheet 2", short="account->isEmpty() vs account.isEmpty().")

g.qa("HIGH", "Explain equals, union, including, excluding and intersection for the different collection types.",
     T, "slides 34-35", short="Variant-meaning operations per collection type.",
     extra=[grid([
         ["Operation", "Behaviour"],
         ["<b>=</b>", "same elements; <b>Bag</b>: same counts; <b>Sequence/OrderedSet</b>: same order too"],
         ["<b>union</b>", "all elements; Bag with Set gives <b>Bag</b>; Sequence/OrderedSet only with Sequence/OrderedSet"],
         ["<b>including</b>", "adds one element; <b>Set</b>: only if new; <b>Sequence/OrderedSet</b>: at the end"],
         ["<b>excluding</b>", "removes; <b>Set/OrderedSet</b>: the one element; <b>Bag/Sequence</b>: <b>all occurrences</b>"],
         ["<b>intersection</b>", "common elements; <b>not valid</b> with Sequence/OrderedSet; Bag involved gives Bag"],
     ], [30 * mm, 140 * mm])])

g.qa("MED", "Which operations exist only for Set/OrderedSet, and which only for Sequence/OrderedSet?",
     "<b>Set and/or OrderedSet:</b> " + c("s1 - s2") + ", " + c("symmetricDifference(s)") + " (Set), " +
     c("subOrderedSet(l, u)") + ".<br/><b>Sequence and OrderedSet</b> (five): " + c("first(), last(), at(i)") + ", " +
     c("append(o)") + " (<b>end</b>), " + c("prepend(o)") + " (<b>front</b>).<br/>" +
     careful("slide 37 has append/prepend the wrong way round."), "slides 36-37",
     short="Set-only and Sequence/OrderedSet-only operations.")

g.sec("G. Iteration operations")
g.qa("HIGH", "Name the iteration operations and their result types.",
     c("select, reject, collect, iterate, forAll, exists") + ":<br/>" + bullets([
         c("select, reject, collect") + ": a <b>new collection</b>",
         c("forAll, exists") + ": a <b>Boolean</b>",
         c("iterate") + ": <b>depends on its arguments</b>"]), "slide 38", short="Iterators and result types.")

g.qa("HIGH", "What does select do? Give its three syntactic forms.",
     "Selects the <b>subset</b> for which a Boolean criterion holds; inside, the context is <b>the current element</b>.<br/>"
     + ocl("membership.account->select(a : LoyaltyAccount | a.points > 0)\n"
           "membership.account->select(a | a.points > 0)\nmembership.account->select(points > 0)"),
     "slide 39", short="select: meaning and three forms.")

g.qa("HIGH", "What does reject do, and why is it strictly redundant?",
     "Keeps elements where the expression is <b>false</b>. Redundant because<br/>" +
     ocl("c->reject(e : T | <expr>)   ==   c->select(e : T | not <expr>)"), "slide 40", short="reject; why redundant.")

g.qa("HIGH", "What does collect do? Result type? Shorthand?",
     bullets([
         "Computes a value per element and gathers them in a <b>new collection</b> (element type usually differs).",
         "From a <b>Set or Bag</b>: a <b>Bag</b>; from a <b>Sequence</b>: a <b>Sequence</b>.",
         "Shorthand: " + c("transactions->collect(points)") + " = " + c("transactions.points") + ".",
     ]) + "<br/><b>Why a Bag?</b> Two songs of 3 kb give 3 twice; a Set would lose one and the sum would be wrong. "
     "Tutorial: " + c("self.song->collect(size)->sum()") + " = " + c("self.song.size->sum()") + ".",
     "slide 41; Exercise Sheet 1", short="collect: result type rules, shorthand; why a Bag.")

g.qa("HIGH", "Explain forAll and exists. How can exists be expressed with forAll?",
     bullets([c("forAll") + ": true if the expression holds for <b>all</b> elements.",
              c("exists") + ": true if it holds for <b>at least one</b> element."]) + "<br/>" +
     ocl("context LoyaltyProgram\ninv: participants->forAll(c | c.age() <= 70)\n\n"
         "context LoyaltyAccount\ninv: points > 0 implies transactions->exists(points > 0)") +
     "<br/>De Morgan: " + c("c->exists(P)  ==  not c->forAll(not P)") + ".<br/>" +
     careful("negate the <b>whole</b> condition: not (A and B) is (not A <b>or</b> not B). This is exactly where the "
             "Sheet 3 sample solution goes wrong (Q in section K)."), "slides 42-43",
     short="forAll and exists; exists via forAll (De Morgan).")

g.qa("HIGH", "Explain iterate: syntax, evaluation, and why it is the most fundamental iterator.",
     ocl("collection->iterate(element : Type1;\n                    result : Type2 = <expression>\n"
         "                    | <expression-with-element-and-result>)") + "<br/>" +
     ocl("result = <expression>\nwhile (collection.notEmpty()) do\n  element = collection.nextElement();\n"
         "  result = <expression-with-element-and-result>;\nendwhile\nreturn result;") +
     "<br/>It is the <b>most fundamental and generic</b> operation: <b>select, reject, collect, forAll and exists are "
     "special cases</b>.", "slides 44-45", short="iterate: syntax, pseudocode, why fundamental.")

g.qa("HIGH", "Express " + c("sum()") + ", " + c("forAll") + ", " + c("exists") + " and " + c("select") + " using iterate.",
     ocl("-- sum\ntransactions->iterate(t : Transaction; s : Integer = 0 | s + t.points)\n"
         "-- forAll\nc->iterate(e; acc : Boolean = true  | acc and P(e))\n"
         "-- exists\nc->iterate(e; acc : Boolean = false | acc or P(e))\n"
         "-- select\ns->iterate(e; acc : Set(T) = Set{} |\n          if P(e) then acc->including(e) else acc endif)") +
     "<br/>Pattern: a <b>neutral start value</b> plus how each element <b>updates</b> it. <i>(My own derivations.)</i>",
     "slides 44-45 (reasoning)", short="Express sum, forAll, exists, select with iterate.")

g.sec("H. Practice: evaluate")
g.qa("HIGH", "Evaluate each expression.", T, "slides 5-9, 28 (exercise)",
     short="Evaluate: implies, xor, if, div/mod, undefined (10 items).",
     extra=[grid([
         ["Expression", "Value"],
         [c("false implies false"), "true"], [c("true implies false"), "false"], [c("true xor true"), "false"],
         [c("if 3 > 2 then 'a' else 'b' endif"), "'a'"],
         [c("10.div(3)") + " / " + c("10.mod(3)") + " / " + c("10 / 4"), "3 / 1 / 2.5"],
         [c("2.7.round") + " / " + c("2.7.floor"), "3 / 2"],
         [c("'Royal'.concat(' ').concat('Loyal').size()"), "11"],
         [c("true or undefined"), "true"], [c("true and undefined"), "undefined"],
         [c("false and undefined"), "false"],
     ], [100 * mm, 70 * mm])])

g.qa("HIGH", "Evaluate the collection expressions.", T, "slides 31-37 (exercise)",
     short="Evaluate: including/excluding/union/intersection/equals/at (12 items).",
     extra=[grid([
         ["Expression", "Value"],
         [c("Set{1,2}->including(2)"), "Set{1,2}"], [c("Bag{1,2}->including(2)"), "Bag{1,2,2}"],
         [c("Sequence{1,2}->including(3)"), "Sequence{1,2,3}"],
         [c("Bag{1,2,2,3}->excluding(2)"), "Bag{1,3}"],
         [c("Set{1,2,3}->intersection(Set{2,3,4})"), "Set{2,3}"],
         [c("Set{1,2}->union(Bag{2,3})"), "Bag{1,2,2,3}"], [c("Set{1,2,3} - Set{2}"), "Set{1,3}"],
         [c("Set{1,2,3}->symmetricDifference(Set{3,4})"), "Set{1,2,4}"],
         [c("Set{1,2} = Set{2,1}"), "true"], [c("Sequence{1,2} = Sequence{2,1}"), "false"],
         [c("Bag{1,1,2} = Bag{1,2}"), "false"],
         [c("Sequence{'a','b','c'}->at(2)") + " / " + c("->prepend('z')->first()"), "'b' / 'z'"],
     ], [100 * mm, 70 * mm])])

g.qa("HIGH", "An account has transactions with points 100, 20, 20. Evaluate in context LoyaltyAccount.", T,
     "slides 33, 38-44 (exercise)", short="Transactions 100, 20, 20: evaluate 8 expressions.",
     extra=[grid([
         ["Expression", "Value"],
         [c("transactions.points"), "Bag{100, 20, 20}"], [c("transactions.points->sum()"), "140"],
         [c("transactions.points->asSet()->sum()"), "120 (duplicate 20 lost!)"],
         [c("transactions.points->count(20)"), "2"], [c("transactions->select(points > 50)->size()"), "1"],
         [c("transactions->exists(points = 20)"), "true"], [c("transactions->forAll(points > 20)"), "false"],
         [c("transactions->isUnique(points)"), "false"],
     ], [110 * mm, 60 * mm])])

g.qa("MED", "Is each of these a valid OCL constraint? If not, why?",
     ocl("-- (a) context LoyaltyAccount inv: self.earn(10)\n-- (b) context Customer inv: title = if isMale then 'Mr.' endif\n"
         "-- (c) context Customer inv: Sequence{1,2}->union(Set{3})->size() = 3\n"
         "-- (d) context LoyaltyAccount inv: transactions.points->sum()\n"
         "-- (e) context Airline\n       inv: flight->select(f | f.passenger.needAssistance = true)->notEmpty()") +
     "<br/>" + bullets([
         "(a) Invalid: " + c("earn") + " is not a query operation.",
         "(b) Invalid: " + c("else") + " is mandatory.",
         "(c) Invalid: a Sequence can only be unioned with Sequences/OrderedSets.",
         "(d) Not a constraint: Integer, not Boolean.",
         "(e) Type error: " + c("f.passenger.needAssistance") + " is a <b>Bag(Boolean)</b>, which cannot be compared with "
         + c("true") + ". Use " + c("f.passenger->exists(needAssistance)") + ". (This mistake is in the Sheet 2 sample "
         "solution, see section K.)",
     ]), "slides 4, 7, 11, 34; Exercise Sheet 2", short="Spot the invalid constraints (5 cases).")

g.sec("I. Practice: write the OCL (Royal & Loyal)")
g.qa("HIGH", "Every card owned by a customer has that customer as its owner.",
     ocl("context Customer\ninv: cards->forAll(c | c.owner = self)"), "slides 14, 42",
     short="Write: every card of a customer has that customer as owner.")

g.qa("HIGH", "A customer has at most one valid card, and at least one card if they are in any program.",
     ocl("context Customer\ninv: cards->select(valid)->size() <= 1\ninv: programs->notEmpty() implies cards->notEmpty()"),
     "slides 6, 39", short="Write: at most one valid card; programs imply a card.")

g.qa("HIGH", "Pre/postconditions for " + c("LoyaltyAccount::burn(i : Integer)") + " and " + c("earn(i : Integer)") + ".",
     ocl("context LoyaltyAccount::burn(i : Integer)\npre : i > 0 and i <= points\npost: points = points@pre - i\n\n"
         "context LoyaltyAccount::earn(i : Integer)\npre : i > 0\npost: points = points@pre + i"),
     "slide 22", short="Write pre/post for burn(i) and earn(i).")

g.qa("HIGH", "Define the number of Earning transactions of an account, and an invariant that points equal earned "
     "minus burned points.",
     ocl("context LoyaltyAccount\ndef: numberOfEarnings : Integer =\n     transactions->select(oclIsTypeOf(Earning))->size()\n\n"
         "context LoyaltyAccount\ninv: points = transactions->select(oclIsTypeOf(Earning)).points->sum()\n"
         "              - transactions->select(oclIsTypeOf(Burning)).points->sum()"),
     "slides 20, 27, 39, 41", short="Write: def numberOfEarnings; points = earned - burned.")

g.qa("MED", "All participants of a program are adults, and at least one partner delivers some service.",
     ocl("context LoyaltyProgram\ninv: participants->forAll(c | c.age() >= 18)\n"
         "inv: partners->exists(p | p.deliveredServices->notEmpty())"), "slides 42-43",
     short="Write: participants adults; some partner delivers a service.")

g.sec("J. Slide errors to be aware of")
g.qa("LOW", "Which statements on the slides are mistakes or inconsistencies?",
     bullets([
         "<b>Slide 37:</b> append/prepend reversed: <b>append = end, prepend = front</b>.",
         "<b>Slide 38:</b> \"exits\" means <b>exists</b>.",
         "<b>Slide 33:</b> lists iterate/exists/forAll as standard operations; slide 38 calls them iterators.",
         "<b>Slide 20:</b> " + c("turnover : real") + " should be " + c("Real") + ".",
         "<b>Slide 42:</b> writes " + c("customer") + " although the role name is " + c("participants") + ".",
         "<b>Slide 12 vs 23:</b> role " + c("program") + " vs " + c("programs") + ".",
         "<b>Slide 23:</b> \"LoyalityProgram\" typo.",
         "<b>Slide 21:</b> the if-then-else equals " + c("valid = correctDate") + ".",
     ]), "various slides", short="Slide errors/inconsistencies.")

# ---------------- K tutorials
g.add(PageBreak())
g.sec("K. Tutorial exercises (Exercise Sheets 1-3)")
g.p("These are the official exercise questions with the official sample solution and, where needed, a corrected "
    "version. Re-draw the class diagram from the exercise sheet before answering; role names matter.", "small")

g.p("Sheet 1, Q3: Songs and SD cards", "h1")
g.p("Model: <b>Song</b> (artist : String, title : String, size : Real [kb], length : Real [s]; operation "
    + c("transfer(m : SD-Card)") + ") and <b>SD-Card</b> (number : Integer [unique], size : Real, remainingSize : Real, "
    "averageSongLength : Real). Association: an SD-Card has many songs (role " + c("song") + ", *), a song is on one card "
    "(role " + c("card") + ", 1). Write the class as " + c("SDCard") + ": a hyphen is not allowed in an OCL name.", "body")

g.qa("HIGH", "(a) Write an invariant that all titles of all songs stored on an SD-Card are unique.",
     "<b>Official:</b><br/>" + ocl("context SDCard\ninv unique: song->isUnique(title)") +
     "<br/>" + c("isUnique(expr)") + " is true if the expression gives a different value for every element. Equivalent "
     "with forAll:<br/>" + ocl("context SDCard\ninv: song->forAll(s1, s2 | s1 <> s2 implies s1.title <> s2.title)"),
     "Exercise Sheet 1, Q3(a)", tut="1, Q3(a)", short="Song titles on a card are unique (isUnique).")

g.qa("HIGH", "(b) Write an expression that derives the remainingSize of an SD-Card.",
     "<b>Official (both are fine):</b><br/>" +
     ocl("context SDCard::remainingSize : Real\nderive: self.size - self.song->collect(size)->sum()\n\n"
         "context SDCard::remainingSize : Real\nderive: self.size - self.song.size->sum()") +
     "<br/>The second uses the collect shorthand. " + c("song.size") + " is a <b>Bag</b> of sizes, so equal sizes are "
     "all counted (with a Set they would not be).", "Exercise Sheet 1, Q3(b)", tut="1, Q3(b)",
     short="Derive remainingSize of an SD card.")

g.qa("HIGH", "(c) Define an expression that calculates the averageSongLength of all songs on an SD-Card.",
     "<b>Official:</b><br/>" +
     ocl("context SDCard::averageSongLength : Real\nderive: self.song->collect(length)->sum() / self.song->size()") +
     "<br/>" + careful("on an empty card this divides by 0 (result undefined). A safer version:") + "<br/>" +
     ocl("derive: if song->isEmpty() then 0\n        else song.length->sum() / song->size() endif"),
     "Exercise Sheet 1, Q3(c)", tut="1, Q3(c)", short="Derive averageSongLength (watch empty card).")

g.qa("HIGH", "(d) Define a precondition for transfer so that only songs that fit on the SD-Card can be transferred.",
     "<b>Official:</b><br/>" + ocl("context Song::transfer(m : SDCard)\npre: not (m.remainingSize < self.size)") +
     "<br/>Same as " + c("pre: self.size <= m.remainingSize") + ". The context is the operation on <b>Song</b>; " +
     c("m") + " is the parameter.", "Exercise Sheet 1, Q3(d)", tut="1, Q3(d)", short="Pre: song fits on the card.")

g.qa("HIGH", "(e) Is there a way to prevent a song from being transferred twice to an SD-Card?",
     "<b>Yes</b>, add to the precondition that the song is not already on the card.<br/><b>Official:</b><br/>" +
     ocl("context Song::transfer(m : SDCard)\npre: self.size < m.remainingSize and not m.song->includes(self)") +
     "<br/>" + careful("the official answer switches to <b>&lt;</b>, so a song that exactly fills the card is now "
                       "rejected, unlike in (d). Consistent version:") + "<br/>" +
     ocl("pre: self.size <= m.remainingSize and m.song->excludes(self)") +
     "<br/>(Strictly, with multiplicity 1 a song is on exactly one card anyway; the check guards against transferring "
     "the same song to the same card again.)", "Exercise Sheet 1, Q3(e)", tut="1, Q3(e)",
     short="Pre: prevent transferring a song twice.")

g.p("Sheet 2, Q2: Hotels", "h1")
g.p("Model: <b>Hotel</b> (maxRooms : Integer, address : String, freeRooms : Integer) aggregates <b>Room</b>s (role "
    + c("room") + "; back to the hotel: " + c("hotel") + "). <b>Room</b> (occupied : Boolean, number : Integer) has 0..1 "
    "<b>Guest</b> (no role name, so " + c("guest") + ").", "body")

g.qa("HIGH", "(a) Make occupied a derived attribute.",
     "<b>Official:</b><br/>" + ocl("context Room::occupied : Boolean\nderive: self.guest->size() > 0") +
     "<br/>Equivalent: " + c("guest->notEmpty()") + ". The arrow on a 0..1 end treats it as a set of 0 or 1 guests.",
     "Exercise Sheet 2, Q2(a)", tut="2, Q2(a)", short="Derive Room::occupied.")

g.qa("HIGH", "(b) Prevent a Hotel from having more rooms than maxRooms.",
     "<b>Official:</b><br/>" + ocl("context Hotel\ninv: self.room->size() <= self.maxRooms"),
     "Exercise Sheet 2, Q2(b)", tut="2, Q2(b)", short="Hotel has at most maxRooms rooms.")

g.qa("HIGH", "(c) Define the derived attribute freeRooms (the number of free rooms).",
     "<b>Official:</b><br/>" +
     ocl("context Hotel::freeRooms : Integer\nderive: self.room->select(r | r.occupied = false)->size()") +
     "<br/>Shorter: " + c("room->reject(occupied)->size()") + " or " + c("room->select(not occupied)->size()") + ".",
     "Exercise Sheet 2, Q2(c)", tut="2, Q2(c)", short="Derive Hotel::freeRooms.")

g.qa("HIGH", "(d) Define a method of Hotel that returns the room numbers of the free rooms.",
     "<b>Official:</b><br/>" +
     ocl("context Hotel\ndef: numbers : Set(Integer) =\n  self.room->select(occupied = false)->collect(number)->asSet()") +
     "<br/>" + careful("the question asks for a <b>method</b>, but the official answer defines an <b>attribute</b> "
                       "(no parentheses). As an operation:") + "<br/>" +
     ocl("context Hotel\ndef: freeRoomNumbers() : Set(Integer) =\n  room->select(not occupied).number->asSet()") +
     "<br/>" + c("asSet()") + " is needed because " + c("collect") + " returns a Bag.",
     "Exercise Sheet 2, Q2(d)", tut="2, Q2(d)", short="def: room numbers of free rooms (method).")

g.p("Sheet 2, Q3: Flights", "h1")
g.p("Model: <b>Flight</b> (/arrivalTime, duration : Integer, departTime : Integer) has an " + c("origin") + " and a "
    + c("destination") + " <b>Airport</b> (name : String), exactly one " + c("airline") + " (<b>Airline</b>, name; an "
    "airline has 1..* flights, no role name, so " + c("flight") + ") and 0..* " + c("passenger") + "s (<b>Passenger</b>: "
    "name, needAssistance : Boolean).", "body")

g.qa("HIGH", "(a) Write a constraint that calculates the arrivalTime of a flight.",
     "<b>Official:</b><br/>" + ocl("context Flight::arrivalTime : Integer\nderive: self.departTime + self.duration"),
     "Exercise Sheet 2, Q3(a)", tut="2, Q3(a)", short="Derive Flight::arrivalTime.")

g.qa("HIGH", "(b) Define a method of Airline that returns all flights in which a passenger needs assistance.",
     "<b>Official:</b><br/>" +
     ocl("context Airline\ndef: assistanceFlights : Set{} =\n  self.flight->select(f | f.passenger.needAssistance = true)") +
     "<br/>" + careful("two mistakes. " + c("Set{}") + " is a value, not a type (write " + c("Set(Flight)") + "). And "
                       + c("f.passenger.needAssistance") + " is a <b>Bag of Booleans</b> (one per passenger), which "
                       "cannot be compared with " + c("true") + ". Correct:") + "<br/>" +
     ocl("context Airline\ndef: assistanceFlights() : Set(Flight) =\n  flight->select(f | f.passenger->exists(needAssistance))") +
     "<br/>Also accepted: " + c("f.passenger.needAssistance->includes(true)") + ".",
     "Exercise Sheet 2, Q3(b)", tut="2, Q3(b)", short="def: flights where some passenger needs assistance.")

g.qa("HIGH", "(c) The destination airport is not the origin airport.",
     "<b>Official:</b><br/>" + ocl("context Flight\ninv: self.origin <> self.destination") +
     "<br/>Compares the two Airport <b>objects</b> (identity). To also forbid two airport objects with the same name: "
     + c("origin.name <> destination.name") + ".", "Exercise Sheet 2, Q3(c)", tut="2, Q3(c)",
     short="Origin is not destination.")

g.qa("HIGH", "(d) If origin and destination are both among Amsterdam, Eindhoven and Den Haag, the airline must be KLM.",
     "<b>Official</b> (quotes as on the sheet):<br/>" +
     ocl("context Flight\ninv: Set{\"Amsterdam\", \"Den Haag\", \"Eindhoven\"}->includes(self.origin.name) and\n"
         "     Set{\"Amsterdam\", \"Den Haag\", \"Eindhoven\"}->includes(self.destination.name)\n"
         "     implies self.airline.name = 'KLM'") +
     "<br/>" + careful("OCL strings use <b>single</b> quotes. A cleaner version with " + c("let") + ":") + "<br/>" +
     ocl("context Flight\ninv: let nl : Set(String) = Set{'Amsterdam', 'Eindhoven', 'Den Haag'} in\n"
         "     (nl->includes(origin.name) and nl->includes(destination.name))\n     implies airline.name = 'KLM'") +
     "<br/>Precedence: " + c("implies") + " binds weakest, so " + c("A and B implies C") + " already means "
     + c("(A and B) implies C") + "; the brackets just make it obvious.", "Exercise Sheet 2, Q3(d)", tut="2, Q3(d)",
     short="Dutch airports imply airline KLM.")

g.p("Sheet 3, Q1: Online bookstore", "h1")
g.p("Model: <b>Book</b> (title, ISBN, amountPages, publishingDate, category, prize, /rating; operation "
    + c("review(reviewer : Customer, text : String, stars : Integer)") + "). Book * -- * <b>Author</b> (firstName, "
    "lastName; roles " + c("author") + "/" + c("book") + "). Book * -- * <b>Publisher</b> (name, ZIPCode, city; roles "
    + c("publisher") + "/" + c("book") + "). Book 1 -- * <b>Review</b> (amountStars : Integer, text; roles " + c("review")
    + "/" + c("book") + "). <b>Customer</b> (firstName, lastName, email, login, password) is reviewer (1) of reviews and "
    "buyer/wish-lister of books.", "body")

g.qa("HIGH", "(a) A book has at least one author and exactly one publisher.",
     "<b>Official:</b><br/>" +
     ocl("context Book\ninv authorpublisher: author->size() > 0 and publisher->size() = 1") +
     "<br/>Needed because the diagram allows * on both ends.", "Exercise Sheet 3, Q1(a)", tut="3, Q1(a)",
     short="Book: >= 1 author and exactly 1 publisher.")

g.qa("HIGH", "(b) Initial values: login = the customer's last name, password = '1234'.",
     "<b>Official:</b><br/>" + ocl("context Customer::login\ninit: lastname\n\ncontext Customer::password\ninit: '1234'") +
     "<br/>" + careful("the attribute is " + c("lastName") + " (capital N); OCL is case-sensitive.") +
     " Correct: " + c("init: lastName") + ".", "Exercise Sheet 3, Q1(b)", tut="3, Q1(b)",
     short="init login and password of Customer.")

g.qa("HIGH", "(c) Derive rating: the arithmetic mean of the stars of the book's reviews.",
     "<b>Official:</b><br/>" + ocl("context Book::rating\nderive: review.amountStars->sum() / review->size()") +
     "<br/>" + careful("undefined for a book without reviews; guard with " +
                       c("if review->isEmpty() then 0 else ... endif") + ". The question says numberOfStars but the "
                       "attribute is amountStars."), "Exercise Sheet 3, Q1(c)", tut="3, Q1(c)",
     short="Derive Book::rating (mean of stars).")

g.qa("HIGH", "(d) Define an operation allAuthors() of Publisher returning all its authors as a set.",
     "<b>Official:</b><br/>" + ocl("context Publisher\ndef: allAuthors() : Set(Author) = book.author->asSet()") +
     "<br/>" + c("book.author") + " is two navigations, so a <b>Bag</b> (an author of two books appears twice); "
     + c("asSet()") + " is required.", "Exercise Sheet 3, Q1(d)", tut="3, Q1(d)", short="def allAuthors() of Publisher.")

g.qa("HIGH", "(e) Pre/post for review: reviewer's first and last name differ from the author's; text at least 20 "
     "characters; afterwards one more review exists for the book.",
     "<b>Official:</b><br/>" +
     ocl("context Book::review(reviewer : Customer, text : String, stars : Integer)\n"
         "pre: author->forAll(firstName <> reviewer.firstName and\n                    lastName <> reviewer.lastName)\n"
         "pre: text.size() > 20\npost: review->size() = review@pre->size() + 1") +
     "<br/>" + careful("\"at least 20\" is " + c(">= 20") + ", not " + c("> 20") + ".") + "<br/>" +
     "Note on the name rule: the official version demands that <b>both</b> names differ, so it also rejects a reviewer "
     "who only shares the first name with an author. If \"must not be the same\" means \"not the same person\", write:<br/>"
     + ocl("pre: author->forAll(a | not (a.firstName = reviewer.firstName and\n                         a.lastName = reviewer.lastName))") +
     "<br/>Either reading is defensible; say which one you mean. The postcondition uses " + c("@pre") +
     " to compare with the old number of reviews.", "Exercise Sheet 3, Q1(e)", tut="3, Q1(e)",
     short="Pre/post for Book::review (names, text length, one more review).")

g.qa("HIGH", "(f) Publisher methods bookOfAuthor1/2(authorFirstName, authorLastName) : Boolean; one with exists, one "
     "with forAll.",
     "<b>Official:</b><br/>" +
     ocl("context Publisher\ndef: bookOfAuthor1(authorFirstName : String, authorLastName : String) : Boolean\n"
         "  = book.author->exists((firstName = authorFirstName) and\n                         (lastName = authorLastName))\n\n"
         "def: bookOfAuthor2(authorFirstName : String, authorLastName : String) : Boolean\n"
         "  = not (book.author->forAll((firstName <> authorFirstName) and\n                              (lastName <> authorLastName)))") +
     "<br/>" + careful("bookOfAuthor2 is <b>not</b> equivalent to bookOfAuthor1. By De Morgan, "
                       "not (A and B) is (not A <b>or</b> not B). The official version returns true when some author "
                       "matches the first name <b>or</b> the last name. Correct forAll version:") + "<br/>" +
     ocl("def: bookOfAuthor2(authorFirstName : String, authorLastName : String) : Boolean\n"
         "  = not book.author->forAll(firstName <> authorFirstName or\n                             lastName <> authorLastName)") +
     "<br/>(The official solution also writes the parameters as " + c("authorfirstName") + " in one place; keep the "
     "spelling consistent.)", "Exercise Sheet 3, Q1(f)", tut="3, Q1(f)",
     short="bookOfAuthor1 (exists) and bookOfAuthor2 (forAll): correct De Morgan.")

g.p("Sheet 3, Q2: Student administration", "h1")
g.p("Model: <b>Project</b> 1 -- * <b>Projectpart</b> 1 -- * <b>Contract</b> (duration : Integer, /cost : Real). "
    "Contract * -- 1 <b>Assistant</b> (roles " + c("contract") + "/" + c("assistant") + "). Assistant (login, password, "
    "/active : Boolean) <b>is a</b> Person (name : String, age : String). Assistant 1 -- * <b>Authorization</b> (kind, "
    "start : Date, end : Date, duration : Integer; operation " + c("create(kind : String)") + ").", "body")

g.qa("HIGH", "(a) Derive cost of Contract = duration times 9.89.",
     "<b>Official:</b><br/>" + ocl("context Contract::cost\nderive: duration * 9.89"),
     "Exercise Sheet 3, Q2(a)", tut="3, Q2(a)", short="Derive Contract::cost.")

g.qa("HIGH", "(b) An authorization's duration is 100 or more time units.",
     "<b>Official:</b><br/>" + ocl("context Authorization\ninv: duration >= 100"),
     "Exercise Sheet 3, Q2(b)", tut="3, Q2(b)", short="Authorization duration >= 100.")

g.qa("HIGH", "(c) Initial values: Assistant login = the person's name, password = 'test'.",
     "<b>Official:</b><br/>" + ocl("context Assistant::login\ninit: name\n\ncontext Assistant::password\ninit: 'test'") +
     "<br/>" + c("name") + " is inherited from Person, so it can be used directly in Assistant's context.",
     "Exercise Sheet 3, Q2(c)", tut="3, Q2(c)", short="init login/password of Assistant (inherited name).")

g.qa("HIGH", "(d) Precondition for Authorization::create(): only for an assistant with at least one contract.",
     "<b>Official:</b><br/>" + ocl("context Authorization::create(kind : String)\npre: assistant.contract->size() >= 1"),
     "Exercise Sheet 3, Q2(d)", tut="3, Q2(d)", short="Pre for create(): assistant has a contract.")

g.qa("HIGH", "(e) Complete with true or false.", "<b>Official answers:</b>", "Exercise Sheet 3, Q2(e)", tut="3, Q2(e)",
     short="oclIsKindOf/oclIsTypeOf with Person/Assistant: true or false.",
     extra=[grid([
         ["Context", "Expression", "Value", "Why"],
         ["Person", c("self.oclIsKindOf(Person)"), "true", "same type"],
         ["Person", c("self.oclIsKindOf(Assistant)"), "false", "Assistant is a subtype, not a supertype"],
         ["Person", c("self.oclIsTypeOf(Person)"), "true", "exact type"],
         ["Assistant", c("self.oclIsTypeOf(Person)"), "false", "exact type is Assistant"],
         ["Assistant", c("self.oclIsKindOf(Person)"), "true", "(extra) Person is a supertype"],
     ], [24 * mm, 62 * mm, 16 * mm, 68 * mm]), Spacer(1, 4),
         Paragraph(careful("\"context Person\" means an object whose type is <b>exactly</b> Person here (as the "
                           "official answer assumes). For an Assistant object, " + c("oclIsTypeOf(Person)") +
                           " is false but " + c("oclIsKindOf(Person)") + " is true."), S["a"])])

g.qa("HIGH", "(f) Methods contractExists1/2(assistantName) of Contract: true if an assistant (with that name) has at "
     "least one contract; one with exists, one with forAll.",
     "<b>Official:</b><br/>" +
     ocl("context Contract\ndef: contractExists1(assistantName : String) : Boolean\n"
         "  = assistant->exists(name = assistantName)\n\n"
         "def: contractExists2(assistantName : String) : Boolean\n  = not (assistant->forAll(name <> assistantName))") +
     "<br/>Here the De Morgan step is correct (only one condition). " +
     careful("the official version only looks at <b>this</b> contract's single assistant. To check \"does any contract "
             "belong to an assistant with this name\", use allInstances:") + "<br/>" +
     ocl("def: contractExists1(assistantName : String) : Boolean\n"
         "  = Contract::allInstances()->exists(c | c.assistant.name = assistantName)\n"
         "def: contractExists2(assistantName : String) : Boolean\n"
         "  = not Contract::allInstances()->forAll(c | c.assistant.name <> assistantName)"),
     "Exercise Sheet 3, Q2(f)", tut="3, Q2(f)", short="contractExists1 (exists) / contractExists2 (forAll).")

g.qa("HIGH", "(g) Derive active of Assistant: at least 8 contracts and at least three different projects.",
     "<b>Official:</b><br/>" +
     ocl("context Assistant::active\nderive: contract->size() >= 8\n"
         "    and contract.projectpart.project->asSet()->size() >= 3") +
     "<br/>" + c("contract.projectpart.project") + " navigates over several associations, so it is a <b>Bag</b> with "
     "repeated projects; " + c("asSet()") + " gives the <b>different</b> projects.", "Exercise Sheet 3, Q2(g)",
     tut="3, Q2(g)", short="Derive Assistant::active (contracts and distinct projects).")

g.self_test()
g.build()
