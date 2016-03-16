
from boolean import *

"Solves the SAT problem for the given formula."
def solve(frm, values):
    unitPropagate(frm, values)
    if (frm == T):
        return values
    elif (frm == F):
        return False

    l = findFirstLiteral(frm)
    # print(frm)
    # print("NEW FRM")
    # print(newFrm)
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



def unitPropagate(frm, values):
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

# test unit propagating
formulabano = And([Literal("x"), Or([Not(Literal("x")), Not(Literal("y"))]), Or([Literal("z"), Literal("w")]), Literal("y")])
# unitPropagate(formulabano, {})

#
# formalaFindLit = And([Or([Tru()])])
# print findFirstLiteral(formalaFindLit)
print (solve(formulabano, {}))
