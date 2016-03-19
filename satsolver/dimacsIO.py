import sys
from boolean import *

def inputDimacsToFormula(filePath):
    frm = []
    with open(filePath) as f:
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

def outputResultToDimacs(values, filePath):
    newF = open(filePath,'w')
    for key, value in values.iteritems():
        if (value):
            newF.write(key + " ")
        else:
            newF.write("-" + key + " ")
    newF.close()

def outputFormulaToDimacs(formula, filePath, comment):
    newF = open(filePath,'w')
    newF.write("c " + comment + " \n" )
    countVars = 0
    variables = {}
    countClauses = 0
    strOut = ""
    for orTerm in formula.lst:
        countClauses += 1
        line = ""
        if (isinstance(orTerm, Literal)):
            lit = orTerm.lit
            if lit not in variables:
                countVars += 1
                variables[lit] = str(countVars)
            line += variables[lit] + " 0\n"
        elif (isinstance(orTerm, Not)):
            lit = orTerm.term.lit
            if lit not in variables:
                countVars += 1
                variables[lit] = str(countVars)
            line += "-" + variables[lit] + " 0\n"
        else:
            line = ""
            for term in orTerm.lst:
                if (isinstance(term, Literal)):
                    lit = term.lit
                    if lit not in variables:
                        countVars += 1
                        variables[lit] = str(countVars)
                    line += variables[lit] + " "
                elif (isinstance(term, Not)):
                    lit = term.term.lit
                    if lit not in variables:
                        countVars += 1
                        variables[lit] = str(countVars)
                    line += "-" + variables[lit] + " "
            line += "0\n"
        strOut += line
    newF.write("p cnf " + str(countVars) + " " + str(countClauses) + "\n")
    newF.write(strOut)

# frm = inputDimacsToFormula("./dimacs/sudoku1.txt")
# print frm
# outputFormulaToDimacs(frm, "./output/sudoku1_dimacs2.txt", " This is the sudoku1.txt read from and written back to Dimacs format.")
