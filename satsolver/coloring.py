#!/usr/bin/python

from boolean import *

def coloring(l,k):
    ZEROS = 3

    terms = []
    vertices = set(sum([list(e) for e in l], []))
    lin = {u: [] for u in vertices}
    lout = {u: [] for u in vertices}
    for u, v in l:
        lin[v].append(u)
        lout[u].append(v)
    n = len(vertices)

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


print coloring([(1,2), (1, 3), (2,3)], 3)
