
from boolean import *
import sys

#Solves the SAT problem for the given formula.
def solve(frm, values):
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

    l = findFirstLiteral(frm)
    if not l:
        print "SRANJE"

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

def inputDimacsToFormula():
    frm = []
    with open(sys.argv[1]) as f:
        for line in f:
            split = line.split(" ")
            if (split[0] == 'c' or split[0] == 'p'):
                continue

            orTerm = []
            for i in range(len(split)):
                termNum = int(split[i])
                if (termNum == 0):
                    break
                if termNum < 0:
                    orTerm.append(Not(Literal(str(abs(termNum)))))
                else:
                    orTerm.append(Literal(str(termNum)))
            frm.append(Or(orTerm))
    return And(frm)

def outputResultToDimacs(values):
    newF = open(sys.argv[2],'w')
    for key, value in values.iteritems():
        if (value):
            newF.write(key + " ")
        else:
            newF.write("-" + key + " ")
    newF.close()

def evaluate(frm, values):
    return frm.partiallySimplify(values).simplify()


frm = inputDimacsToFormula()
resValues = solve(frm, {})
print (evaluate(frm, resValues))
outputResultToDimacs(resValues)
