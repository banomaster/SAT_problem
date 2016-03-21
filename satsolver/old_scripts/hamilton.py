#!/usr/bin/python

"""
Conversion of the Hamiltonian cycle problem to SAT.
"""

from boolean import *

def hamiltonian_cycle(l):
    """
    Convert a directed graph to an instance of SAT that is satisfiable
    precisely when the graph has a Hamiltonian cycle.

    The graph is given as a list of ordered tuples representing directed edges.
    Parallel edges (in the same direction) are not supported. The vertices of
    the graph are assumed to be the endpoints of the listed edges (e.g., no
    isolated vertices can be specified).

    The function returns a boolean expression whose literals are of two types:
    - ("e", u, v), where (u, v) is a directed edge in the given graph, and
    - ("v", u, i), where u is a vertex and i is an integer between 0 and n-1,
                   where n is the number of vertices of the graph.

    The returned expression is satisfiable precisely when the graph has a
    Hamiltonian cycle. If a satisfying valuation is found, a Hamiltonian
    cycle can be retrieved as follows:
    - the set of all literals ("e", u, v) whose value is true corresponds to
      the set of directed edges (u, v) in the Hamiltonian cycle, or
    - the set of all literals ("v", u_i, i) whose value is true corresponds to
      the cyclically ordered sequence (u_0, u_1, ..., u_{n-1}) of vertices
      visited by the Hamiltonian cycle.
    """
    terms = []
    vertices = set(sum([list(e) for e in l], []))
    lin = {u: [] for u in vertices}
    lout = {u: [] for u in vertices}
    for u, v in l:
        lin[v].append(u)
        lout[u].append(v)
    n = len(vertices)
    terms.append(("v", next(iter(vertices)), 0))
    for u in vertices:
        terms.append(Or([("v", u, i) for i in range(n)]))
        terms.append(Or([("e", v, u) for v in lin[u]]))
        terms.append(Or([("e", u, v) for v in lout[u]]))
        for i in range(n):
            for j in range(i+1, n):
                terms.append(Not(And(("v", u, i), ("v", u, j))))
        ll = lin[u]
        m = len(ll)
        for i in range(m):
            v = ll[i]
            for j in range(i+1, m):
                terms.append(Not(And(("e", v, u), ("e", ll[j], u))))
        ll = lout[u]
        m = len(ll)
        for i in range(m):
            v = ll[i]
            for j in range(i+1, m):
                terms.append(Not(And(("e", u, v), ("e", u, ll[j]))))
            for i in range(n):
                    terms.append(Implies(And(("v", u, i), ("e", u, v)),
                                         ("v", v, (i+1) % n)))
    return And(terms)
