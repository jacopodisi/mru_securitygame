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
    success: boolean (describe the success of the computation)
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


def maximum_resources(csr_matrices, targets):
    """
    Parameter
    ---------
    csr_matrices: dictionary of type {"vertex_number1": csr_matrix1,
                                      "vertex_number2": csr_matrix2, ...}
                  csr_matrix represent the covering sets of the vertex
    targets: list of targets for which compute the covering routes

    Return
    ------
    vertex_list: list of optimal resource position
    """
    mat = np.array([], dtype=np.uint8).reshape(
        (0, csr_matrices[csr_matrices.keys()[0]].shape[1]))
    vertex_list = np.array([], dtype=np.uint16)
    for v in csr_matrices:
        arr = csr_matrices[v].toarray()
        mat = np.vstack((mat, arr))
        t_li = np.full(shape=(arr.shape[0]), fill_value=v, dtype=np.uint16)
        vertex_list = np.append(vertex_list, t_li)
    success, mat_ix = set_cover_solver(mat[:, targets])
    return success, vertex_list[mat_ix]


if __name__ == '__main__':
    m = np.random.randint(2, size=(50, 10), dtype=np.uint8)
    success, min0 = set_cover_solver(m)
    if not success:
        exit()
    success, min1 = set_cover_solver(m, k=(len(min0) + 1))
    if len(min1) != (len(min0) + 1):
        print 'Error in lengths' + min0 + min1