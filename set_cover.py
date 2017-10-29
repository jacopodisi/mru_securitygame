# -*- coding: utf-8 -*-

from gurobipy import *
import numpy as np


def set_cover_solver(sets, k=None):
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
        m.setParam('OutputFlag', False)

        univ = sets.shape[1]
        nsets = sets.shape[0]

        # VARIABLES
        # tell if a set is choose (1) or not (0)
        vars = []
        for s in range(nsets):
            vars.append(m.addVar(vtype=GRB.BINARY))

        m.update()

        # CONSTRAINTS
        # covering constraint
        for t in range(univ):
            m.addConstr(
                quicksum(sets[r, t] * vars[r] for r in range(nsets)) >= 1)

        if k is None:
            # OBJ
            m.setObjective(quicksum(m.getVars()))
        else:
            # CONSTRAINT
            m.addConstr(quicksum(vars) == k)

        m.optimize()

        m.write('set_cover.lp')

        vars = m.getAttr('x', vars)

        return True, np.nonzero(vars)[0]

    except GurobiError:
        stat = m.getAttr(GRB.Attr.Status)
        print('Error while computing the set cover optimization problem')
        if stat == 3:
            print 'Infeasible solution'
        else:
            print 'Gurobi Status after the optim: ', stat
        return False, np.array([])
