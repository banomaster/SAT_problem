# accepts the CNF as list of lists - or clauses
# a, - a etc.

import time
import heapq

from dimacsIO_opt import *

def solve(formula, values):
    formula = setUnitValues(formula, values)
    # print "formula: " + str(formula)

    if formula == True:
        return values
    elif formula == False:
        return False

    formula = setPureVarsValues(formula, values)
    if formula == True:
        return values
    elif formula == False:
        return False

    selectedUnit = findFirstUnit(formula)
    # print selectedUnit
    if not selectedUnit:
        return "TO NI DOBRO. NI CNF :("

    newValues = values.copy()
    newValues[selectedUnit] = True

    formulaTrue = simplify(formula, newValues)
    # print "formula true: " + str(formulaTrue)

    solveTrue = solve(formulaTrue, newValues)
    if solveTrue:
        return solveTrue

    newValues = values.copy()
    newValues[selectedUnit] = False

    formulaFalse = simplify(formula, newValues)
    # print "formula false: " + str(formulaFalse)
    #return values object if solved or False if not solved
    return solve(formulaFalse, newValues)

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
    if len(evaluatedFormula) == 0:
        return True
    else:
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
    bestKey = getUnitName(formula[0][0])
    for orTerm in formula:
        for unit in orTerm:
            if not isNegated(unit):
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
    return unit.replace("-","")

def solveImproved(formula, values, ranks):
    formula = setUnitValues(formula, values)

    if formula == True:
        return values
    elif formula == False:
        return False

    formula = setPureVarsValues(formula, values)
    if formula == True:
        return values
    elif formula == False:
        return False

    selectedUnit = getLiteralByRank(ranks)
    if not selectedUnit:
        return "TO NI DOBRO. NI CNF :("

    values[selectedUnit[1]] = True

    formulaTrue = simplify(formula, values)

    solveTrue = solveImproved(formulaTrue, values, ranks)
    del values[selectedUnit[1]]
    heapq.heappush(ranks, selectedUnit)

    if solveTrue:
        return solveTrue

    values[selectedUnit[1]] = False
    formulaFalse = simplify(formula, values)

    solveFalse = solveImproved(formulaFalse, values,ranks)
    del values[selectedUnit[1]]
    heapq.heappush(ranks, selectedUnit)
    return solveFalse

def getLiteralRanks(formula):
    ranksDict = {}
    ranks = []
    for clause in formula:
        for term in clause:
            lit = term.replace("-", "")
            if lit in ranksDict:
                ranksDict[lit] -= 1
            else:
                ranksDict[lit] = -1
    for key, value in ranksDict.iteritems():
        heapq.heappush(ranks, (value, key))
    return ranks

def getLiteralByRank(ranks):
    d = heapq.heappop(ranks)
    return d


# frm = [["w"],["a", "b"], ["-b"], ["c", "d"], ["-d", "-w"]]
#
# print solve(frm, {})

frm = inputDimacsToFormula(sys.argv[1])
print "Basic"
startTime = time.time()
resValues = solve(frm, {})
# print resValues
endTime = time.time()
print endTime - startTime
if (resValues):
    print simplify(frm, resValues)



frm = inputDimacsToFormula(sys.argv[1])
print "Improved"
startTime = time.time()
ranks = getLiteralRanks(frm)
resValues = solveImproved(frm, {}, ranks)
# print resValues
endTime = time.time()
print endTime - startTime
#
if (resValues):
    print simplify(frm, resValues)
