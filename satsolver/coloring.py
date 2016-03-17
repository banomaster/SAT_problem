#!/usr/bin/python

from boolean import *
from dimacsIO import *
from satsolver import *
from random import random

def randomGraph(numOfVertices, density):
    l = []
    for i in range(numOfVertices):
        for j in range(i + 1, numOfVertices):
            if random() < density:
                l.append((i, j))

    return l


def coloring(l,k):
    ZEROS = 3

    terms = []
    vertices = set(sum([list(e) for e in l], []))

    for v in vertices:
        orTerm = []
        for i in range(k):
            lit = Literal(str(v).zfill(ZEROS) + str(i).zfill(ZEROS))
            orTerm.append(lit)

        terms.append(Or(orTerm))

    for v in vertices:
        for i in range(k):
            for j in range(i + 1,k):
                terms.append(Or([Not(Literal(str(v).zfill(ZEROS) + str(i).zfill(ZEROS))), Not(Literal(str(v).zfill(ZEROS) + str(j).zfill(ZEROS)))]))

    for u, v in l:
        for i in range(k):
            terms.append(Or([Not(Literal(str(u).zfill(ZEROS) + str(i).zfill(ZEROS))), Not(Literal(str(v).zfill(ZEROS) + str(i).zfill(ZEROS)))]))

    return And(terms)

formulaColoring = coloring(randomGraph(45, 0.2), 6)

outputFormulaToDimacs(formulaColoring, "./output/coloring100.txt", "Graph coloring SAT")

print solve(formulaColoring, {})
