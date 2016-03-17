import time

from boolean import *
from dimacsIO import *
import sys

#Solves the SAT problem for the given formula.
def solve(frm, values):
    frm = setUnitValues(frm, values)

    if (frm == T):
        return values
    elif (frm == F):
        return False

    frm = setPureVarsValues(frm, values)
    print "Formula:"
    print type(frm)

    # if isinstance(frm, Tru):
    #     print "TRUE";

    if (frm == T):
        return values
    elif (frm == F):
        print "SEM TLE"
        return False

    l = findFirstLiteral(frm)
    if not l:
        print "TO NI DOBRO. NI CNF :("

    #try found literal with TRUE
    values[l.lit] = True
    partiallySimplified = frm.partiallySimplify(values)
    newFrmTrue = partiallySimplified.simplify()

    solveTrue = solve(newFrmTrue, values)
    if solveTrue:
        return solveTrue

    #try found literal with FALSE
    values[l.lit] = False
    partiallySimplified = frm.partiallySimplify(values)
    newFrmFalse = partiallySimplified.simplify()

    #return values object if solved or False if not solved
    return solve(newFrmFalse, values)

#Solves the SAT problem for the given formula.
def solveImproved(frm, values):
    frm = setUnitValues(frm, values)

    if (frm == T):
        return values
    elif (frm == F):
        return False

    frm = setPureVarsValues(frm, values)

    if (frm == T):
        return values
    elif (frm == F):
        return False

    l = findBestLiteral(frm)
    if not l:
        print "TO NI DOBRO. NI CNF :("

    #try found literal with TRUE
    values[l.lit] = True
    partiallySimplified = frm.partiallySimplify(values)
    newFrmTrue = partiallySimplified.simplify()

    solveTrue = solve(newFrmTrue, values)
    if solveTrue:
        return solveTrue

    #try found literal with FALSE
    values[l.lit] = False
    partiallySimplified = frm.partiallySimplify(values)
    newFrmFalse = partiallySimplified.simplify()

    #return values object if solved or False if not solved
    return solve(newFrmFalse, values)

def setUnitValues(frm, values):
    while True:
        # partiallySimplified = frm.partiallySimplify(values)
        # frm = partiallySimplified.simplify()
        unitFound = False
        if (not isinstance(frm, And)):
            frm = And([frm])
        for term in frm.lst:
            #return UNSAT
            if (isinstance(term, Literal)):
                values[term.lit] = True
            elif (isinstance(term, Not)):
                values[term.term.lit] = False
            else:
                continue
            unitFound = True
            partiallySimplified = frm.partiallySimplify(values)
            frm = partiallySimplified.simplify()
            break

        if not unitFound:
            break


    return frm

def setPureVarsValues(frm, values):
    dictLit = {}
    if (not isinstance(frm, And)):
        frm = And([frm])
    for orTerm in frm.lst:
        for term in orTerm.lst:
            if (isinstance(term, Literal)):
                if (not term.lit in dictLit):
                    dictLit[term.lit] = [True, False]
                else:
                    dictLit[term.lit][0] = True
            elif (isinstance(term, Not)):
                if (not term.term.lit in dictLit):
                    dictLit[term.term.lit] = [False, True]
                else:
                    dictLit[term.term.lit][1] = True

    for key, value in dictLit.iteritems():
        if (value[0] != value[1]):
            values[key] = value[0]
    partiallySimplified = frm.partiallySimplify(values)
    return partiallySimplified.simplify()

def findFirstLiteral(frm):
    print frm
    if (isinstance(frm, Literal)):
        return frm
    elif (isinstance(frm, Not)):
        return findFirstLiteral(frm.term)
    elif (isinstance(frm, Or) or isinstance(frm, And)):
        for term in frm.lst:
            t = findFirstLiteral(term)
            if (isinstance(t, Literal)):
                return t
    return False

def findBestLiteral(frm):
    dictLit = {}
    bestKey = '';
    bestValue = 0;

    if (not isinstance(frm, And)):
        frm = And([frm])
    print frm
    for orTerm in frm.lst:
        print orTerm
        for term in orTerm.lst:
            if (isinstance(term, Literal)):
                if (not term.lit in dictLit):
                    dictLit[term.lit] = 1 / len(orTerm.lst)
                    if dictLit[term.lit] > bestValue:
                        bestKey = term.lit
                        bestValue = dictLit[term.lit]
                else:
                    dictLit[term.lit] +=  1 / len(orTerm.lst)
                    if dictLit[term.lit] > bestValue:
                        bestKey = term.lit
                        bestValue = dictLit[term.lit]
            elif (isinstance(term, Not)):
                if (not term.term.lit in dictLit):
                    dictLit[term.term.lit] = 1 / len(orTerm.lst)
                    if dictLit[term.term.lit] > bestValue:
                        bestKey = term.term.lit
                        bestValue = dictLit[term.term.lit]
                else:
                    dictLit[term.term.lit] +=  1 / len(orTerm.lst)
                    if dictLit[term.term.lit] > bestValue:
                        bestKey = term.term.lit
                        bestValue = dictLit[term.term.lit]

    return Literal(bestKey)

def evaluate(frm, values):
    return frm.partiallySimplify(values).simplify()


frm = inputDimacsToFormula(sys.argv[1])
print "Basic"
startTime = time.time()
resValues = solve(frm, {})
endTime = time.time()
print endTime - startTime

print "Improved"
startTime = time.time()
resValuesImproved = solveImproved(frm, {})
endTime = time.time()
print endTime - startTime
print (evaluate(frm, resValues))
outputResultToDimacs(resValues, sys.argv[2])
