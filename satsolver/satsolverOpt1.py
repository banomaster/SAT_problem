# accepts the CNF as list of lists - or clauses
# a, - a etc.

import time
from dimacsIO_opt import *

def solve(formula, values):

    formula = setUnitValues(formula, values)

    if formula == True or formula == []:
        return values
    elif formula == False:
        return False

    formula = setPureVarsValues(formula, values)
    if formula == True or formula == []:
        return values
    elif formula == False:
        return False

    selectedUnit = findBestUnit(formula)
    if not selectedUnit:
        return "TO NI DOBRO. NI CNF :("

    values[selectedUnit] = True

    formulaTrue = simplify(formula, values)

    solveTrue = solve(formulaTrue, values)
    if solveTrue:
        return solveTrue


    values[selectedUnit] = False

    formulaFalse = simplify(formula, values)
    #return values object if solved or False if not solved
    return solve(formulaFalse, values)



def isSolveFinished(formula):
    if formula == True or formula == []:
        return True
    else:
        return False


def simplify(formula, values):
    newFormula = []
    #find values
    for clause in formula:
        if not clause:
            return False
        newClause = []
        for term in clause:
            newTerm = term
            lit = term.replace("-", "")
            if lit in values:
                if "-" in term:
                    newTerm = not values[lit]
                else:
                    newTerm = values[lit]
            newClause.append(newTerm)
        newFormula.append(newClause)
    evaluatedFormula = []
    for clause in newFormula:
        # filter clause of falses
        newClause = [x for x in clause if x]
        # print clause
        # clause is empty
        if not newClause:
            return False
        else:
            if True in newClause:
                continue
        evaluatedFormula.append(newClause)
    return evaluatedFormula


def setUnitValues(formula, values):

    while True:
        if isinstance(formula, bool):
            return formula
        unitFound = False
        for orTerm in formula:
            if len(orTerm) == 1:
                unitFound == True
                if isNegated(orTerm[0]):
                    values[getUnitName(orTerm[0])] = False
                else:
                    values[orTerm[0]] = True

                unitFound = True
                formula = simplify(formula, values)
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
            else:
                if not unit in dictLit:
                    dictLit[unit] = [True, False]
                else:
                    dictLit[unit][0] = True

    for key, value in dictLit.iteritems():
        if (value[0] != value[1]):
            values[key] = value[0]

    return simplify(formula, values)


def findFirstUnit(formula):
    for orTerm in formula:
        for unit in orTerm:
            if isinstance(unit, str):
                return getUnitName(unit)

    return False

def findBestUnit(formula):
    dictLit = {}
    bestKey = '';
    bestValue = 0;

    for orTerm in formula:
        for unit in orTerm:
            if not isNegated(unit):
                if not unit in dictLit:
                    dictLit[unit] = 1 / len(orTerm)
                    if dictLit[unit] > bestValue:
                        bestKey = unit
                        bestValue = dictLit[unit]
                else:
                    dictLit[term.lit] +=  1 / len(orTerm)
                    if dictLit[unit] > bestValue:
                        bestKey = unit
                        bestValue = dictLit[unit]
            elif isNegated(unit):
                unit = getUnitName(unit)
                if not unit in dictLit:
                    dictLit[unit] = 1 / len(orTerm)
                    if dictLit[unit] > bestValue:
                        bestKey = unit
                        bestValue = dictLit[unit]
                else:
                    dictLit[unit] +=  1 / len(orTerm)
                    if dictLit[unit] > bestValue:
                        bestKey = unit
                        bestValue = dictLit[unit]
    return bestKey



def isNegated(unit):
    return '-' in unit

def getUnitName(unit):
    return unit.translate(None,'-')

formulaTest = inputDimacsToFormula("./dimacs/test.txt")
print solve(formulaTest, {})

frm = inputDimacsToFormula(sys.argv[1])
print "Basic"
startTime = time.time()
resValues = solve(frm, {})
print resValues
endTime = time.time()
print endTime - startTime

# outputFormulaToDimacs(resValues, sys.argv[2])
# print setUnitValues([['x'], ['-x', 'y']],{})
