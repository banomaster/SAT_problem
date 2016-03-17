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
                else:
                    orTerm.append(str(termNum))
            frm.append(orTerm)
    return frm

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
    for orTerm in formula:
        countClauses += 1
        line = ""
        for term in orTerm:
            lit = term.replace("-", "")
            if lit not in variables:
                countVars += 1
                variables[lit] = str(countVars)
            if "-" in term:
                line += "-" + variables[lit] + " "
            else:
                line += variables[lit] + " "

        line += "0\n"
        strOut += line
    newF.write("p cnf " + str(countVars) + " " + str(countClauses) + "\n")
    newF.write(strOut)
    newF.close()

frm = inputDimacsToFormula("./dimacs/sudoku1.txt")
print frm
outputFormulaToDimacs(frm, "./output/sudoku1_dimacs.txt", " This is the sudoku1.txt read from and written back to Dimacs format.")
