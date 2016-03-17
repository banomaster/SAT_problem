# accepts the CNF as list of lists - or clauses
# a, - a etc.



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
            newClause = [x for x in newClause if x != True]
            if not newClause:
                newClause = True
        evaluatedFormula.append(newClause)
    return [x for x in evaluatedFormula if x != True]


print(simplify([["-a" , "b", "c"], ["w"], ["s", "-t"]], {"a":True, "w":False, "t":False}))
