# -*- coding: utf-8 -*-

from gurobipy import *
import numpy as np


def set_cover_solver(sets):
    """ solve the linear integer programming problem using gurobi solver
    Parameters
    ----------
    sets: numpy matrix of (|S| x |universe|) representing the sets,
          i-th column correspond to the i-th element of the universe

    Return
    ------
    res: list of indices of sets in the set_cover optimum
    """
    try:

        m = Model("setcover")

        # VARIABLES
        # tell if a set is choose (1) or not (0)
        x = np.empty(shape=(sets.shape[0]), dtype=object)
        for s in xrange(sets.shape[0]):
            x[s] = m.addVar(vtype=GRB.BINARY, name=str(s))

        m.update()

        # OBJ
        m.setObjective(quicksum(m.getVars()))

        # CONSTRAINTS
        # covering constraint
        m.addConstr(quicksum((x.dot(sets) >= 1)) >= sets.shape[1])

        m.optimize()

        res = np.array([], dtype=np.uint16)
        for s in xrange(sets.shape[0]):
            if m.getVarByName(str(s)).x == 1:
                res = np.append(res, s)

        return res

    except GurobiError:
        print('Error while computing the set cover optimization problem')
        print 'Gurobi Status after the optim: ', m.getAttr(GRB.Attr.Status)
