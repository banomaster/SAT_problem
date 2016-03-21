import time
import sys
import copy
from dimacsIO import *

def inputDimacsToFormula(filePath):
    frm = []
    dictLit = {}
    countClauses = 0
    with open(filePath) as f:
        for line in f:
            split = line.split(" ")
            if (split[0] == 'c' or split[0] == 'p'):
                continue

            orTerm = []
            for i in range(len(split)):
                term = split[i]
                if (term[0] == "0"):
                    break
                else:
                    lit = term.replace("-", "")
                    if lit not in dictLit:
                        dictLit[lit] = ([],[])

                    if "-" not in term:
                        dictLit[lit][0].append(countClauses)
                    else:
                        dictLit[lit][1].append(countClauses)
                    orTerm.append(term)
            frm.append(orTerm)
            countClauses+=1
    return (frm, dictLit)

def simplifyWithValue(formula, dictLit, values, lit, value, changesFrm, changesDictLit, valuesSet ):
    valuesSet.append(lit)
    values[lit] = value
    # print "IN simplifyWithValue"
    changesDictLit.append((lit, dictLit[lit][:]))
    for i in dictLit[lit][0]:
        changesFrm.append((i,formula[i][:]))
        if value == True:
            for neighbourTerm in formula[i]:
                neighbourLit = neighbourTerm.replace("-", "")
                if neighbourLit != lit:
                    changesDictLit.append((neighbourLit, (dictLit[neighbourLit][0][:], dictLit[neighbourLit][1][:]) ))
                    if i in dictLit[neighbourLit][0]:
                        dictLit[neighbourLit][0].remove(i)
                    if i in dictLit[neighbourLit][1]:
                        dictLit[neighbourLit][1].remove(i)
                if len(dictLit[neighbourLit][0]) + len(dictLit[neighbourLit][1]) == 0:
                    del dictLit[neighbourLit]
            formula[i] = True
        else:
            if lit in formula[i]:
                formula[i].remove(lit)
            if len(formula[i]) == 0:
                # print "FORMULA BEFORE REVERT: "
                # print formula
                return False

    for i in dictLit[lit][1]:
        changesFrm.append((i,formula[i][:]))
        if value == False:
            for neighbourTerm in formula[i]:
                neighbourLit = neighbourTerm.replace("-", "")
                if neighbourLit != lit:
                    changesDictLit.append((neighbourLit, (dictLit[neighbourLit][0][:], dictLit[neighbourLit][1][:])))
                    if i in dictLit[neighbourLit][0]:
                        dictLit[neighbourLit][0].remove(i)
                    if i in dictLit[neighbourLit][1]:
                        dictLit[neighbourLit][1].remove(i)
                if len(dictLit[neighbourLit][0]) + len(dictLit[neighbourLit][1]) == 0:
                    del dictLit[neighbourLit]
            formula[i] = True
        else:
            term = "-" + lit
            if term in formula[i]:
                formula[i].remove(term)
            if len(formula[i]) == 0:
                # print "FORMULA BEFORE REVERT: "
                # print formula
                return False

    del dictLit[lit]

    # print "FORMULA:"
    # print formula
    # print "DICT LIT:"
    # print dictLit
    # print "CHANGES FRM:"
    # print changesFrm
    # print "CHANGES DICT LIT:"
    # print changesDictLit
    # print "VALUES SET:"
    # print valuesSet

    return True

def solve(formula, values, dictLit):
    # print "START OF RECURSION: "
    # print formula
    changesFrm = []
    changesDictLit = []
    valuesSet = []

    # print dictLit

    unsat = False
    # print "SETTING UNIT"
    # clear units
    while True:
        unitFound = False
        for key, value in dictLit.iteritems():
            isUnit = False
            unitVal = False
            for i in value[0]:
                if len(formula[i]) == 1:
                    isUnit = True
                    unitVal = True
                    break
            for i in value[1]:
                if len(formula[i]) == 1:
                    isUnit = True
                    unitVal = False
                    break
            if isUnit:
                # print "FOUND UNIT: " + key + " " + str(unitVal)
                unitFound = True
                unsat = not simplifyWithValue(formula, dictLit, values, key, unitVal, changesFrm, changesDictLit, valuesSet)
                break
        if not unitFound or unsat:
            break

    # revert the changes made
    if unsat:
        revertChanges(formula, dictLit, values, changesFrm, changesDictLit, valuesSet)
        return False
    elif len(dictLit) == 0:
        return True

    # pure vars
    # print "SETTING PURE VARS"
    unsat = False
    while True:
        pureVarFound = False
        for key, value in dictLit.iteritems():
            if len(value[0]) == 0  or len (value[1]) == 0:
                # print "PURE VAR FOUND " + key
                pureVarFound == True
                unsat = not simplifyWithValue(formula, dictLit, values, key, not len(value[0]) == 0, changesFrm, changesDictLit, valuesSet)
                break
        if not pureVarFound or unsat:
            break

    if unsat:
        # print "UNSAT"
        revertChanges(formula, dictLit, values, changesFrm, changesDictLit, valuesSet)
        return False
    elif len(dictLit) == 0:
        return True

    lit, clauses = dictLit.items()[0]
    # print "TRUE VAR: " + lit
    simplifyWithValue(formula, dictLit, values, lit, True, changesFrm, changesDictLit, valuesSet)

    res = solve(formula, values, dictLit)
    if res != False:
        return values

    revertChanges(formula, dictLit, values, changesFrm, changesDictLit, valuesSet)

    # print "FALSE VAR: " + lit
    simplifyWithValue(formula, dictLit, values, lit, False, changesFrm, changesDictLit, valuesSet)

    res = solve(formula, values, dictLit)
    if res != False:
        return values
    revertChanges(formula, dictLit, values, changesFrm, changesDictLit, valuesSet)
    return res

def revertChanges(formula, dictLit, values, changesFrm, changesDictLit, valuesSet):
    # print "REVERT CHANGES"
    for i in range(len(changesFrm)):
        change = changesFrm.pop()
        formula[change[0]] = change[1]
    for i in range(len(changesDictLit)):
        change = changesDictLit.pop()
        dictLit[change[0]] = change[1]
    for i in range(len(valuesSet)):
        del values[valuesSet.pop()]
    changesFrm = []
    changesDictLit = []
    valuesSet = []

    # print "FORMULA:"
    # print formula
    # print "DICT LIT:"
    # print dictLit
    # print "VALUES: "
    # print values


frm, dictLit = inputDimacsToFormula(sys.argv[1])
# frm = [["-a", "b"], ["c", "-w"], ["a", "-c"], ["-a", "-b"], ["-w", "-b"] ]
# dictLit = {'a':([2], [0,3]), 'b':([0],[3, 4]), 'c':([1], [2]), 'w':([],[1,4])}
startTime = time.time()
values = {}
SAT = solve(frm, values, dictLit)
# print SAT
# print SAT
endTime = time.time()
print "Time:" + str(endTime - startTime)
if SAT:
    #print values
    print "SATISFIABLE"
    outputResultToDimacs(values, sys.argv[2])
else:
    print "UNSATISFIABLE"
