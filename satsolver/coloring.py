#!/usr/bin/python

from boolean import *
from dimacsIO_old import *
# from satsolverOpt1 import solve
import random
import math

def randomGraph(numOfVertices, density):
    l = []
    for i in range(numOfVertices):
        for j in range(i + 1, numOfVertices):
            if random() < density:
                l.append((i, j))

    return l


def genPrefferentialAttModel(n,m):
    numStarting = int(math.ceil(m/float(n)) + 1)
    nodes=[[] for i in range(n)]
    nodeSelection = []
    #full graph on first math.ceil(k)+1
    for i in range(numStarting):
        for j in range(i+1, numStarting):
            nodes[i].append(j)
            nodes[j].append(i)
        nodeSelection+=[i]*(numStarting-1)
    #add the rest of the nodes
    numConn = numStarting*(numStarting-1)
    for i in range(numStarting, n):
        connToAdd=[]
        #add math.ceil(k/2) edges for a node
        for j in range(int(math.ceil(m/(float(n)*2)))):
            rnd = random.randint(0, numConn -1)
            connToAdd.append(rnd)
        connToAdd= list(set(connToAdd))
        for _conn in connToAdd:
            numConn+=1
            nodes[i].append(nodeSelection[_conn])
            nodes[nodeSelection[_conn]].append(i)
            nodeSelection.append(nodeSelection[_conn])
            nodeSelection.append( i )
    return nodes

def convertToEdgeList(graph):
    edges = []
    for i in range(len(graph)):
        for j in graph[i]:
            edges.append((i, j))
    return edges


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

# formulaColoring = coloring(randomGraph(60, 0.3), 6)
#
# outputFormulaToDimacs(formulaColoring, "./output/coloring_60.txt", "Graph coloring SAT")

g = convertToEdgeList(genPrefferentialAttModel(1000, 2000))
formulaColoring = coloring(g, 6)
outputFormulaToDimacs(formulaColoring, "./output/coloring_pref_1000_2000.txt", "Graph coloring SAT")



# print solve(formulaColoring, {})
