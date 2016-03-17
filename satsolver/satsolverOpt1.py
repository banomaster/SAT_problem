# accepts the CNF as list of lists - or clauses
# a, - a etc.
def solve(formula, values):
    formula = setUnitValues(formula, values)

    isSolveFinished(formula)

    formula = setPureVarsValues(formula, values)

    isSolveFinished(formula)

    selectedUnit = findFirstUnit(formula)

    if not selectedUnit:
        return "TO NI DOBRO. NI CNF :("

    values[selectedUnit] = True
    # TODO partiallySimplify

    solveTrue = solve(formula, values)
    if solveTrue:
        return solveTrue

    values[selectedUnit] = False
    # TODO partiallySimplify

    #return values object if solved or False if not solved
    return solve(formula, values)



def isSolveFinished(formula):
    if formula == True:
        return True
    else:
        return False


def simplify(formula, values):

def evaluate(formula, values):
    for clause in formula:
        for term in clause:
            lit = term.replace("-", "")
            if lit in values:
                if "-" in term:
                    term = not values[lit]
                else:
                    term = values[lit]
    result = []
    for clause in formula:
        clause = [x for x in clause if x]
        # clause is empty
        if not clause:
            return False
        else:
            existsVar = False
            allTrue = True
            for term in clause:
                if term == True:

def setUnitValues(formula, values):
    while True:
        unitFound = False
        for orTerm in formula:
            if len(orTerm) == 1:
                unitFound == True
                if isNegated(orTerm[0]):
                    values[getUnitName(orTerm[0])] = False
                else:
                    values[orTerm[0]] = True

                # TODO call partiallySimplify
                break

        if not unitFound:
            break

    return formula

def setPureVarsValues(formula, values):
    dictLit = {}

    for orTerm in formula:
        for unit in orTerm:
            if isNegated(unit):
                if not getUnitName(unit) in dictLit:
                    dictLit[getUnitName(unit)] = [False, True]
                else:
                    dictLit[getUnitName(unit)][1] = True
            else
                if not unit in dictLit:
                    dictLit[unit] = [True, False]
                else:
                    dictLit[unit][0] = True

    for key, value in dictLit.iteritems():
        if (value[0] != value[1]):
            values[key] = value[0]

    # TODO call partiallySimplify

    return formula

def findFirstUnit(formula):
    for orTerm in formula:
        for unit in orTerm:
            if isinstance(unit, str):
                return getUnitName

    return False



def isNegated(unit):
    return '-' in unit

def getUnitName(unit):
    return unit.translate(None,'-')
