# -*- coding: utf-8 -*-

import gurobipy as gu
import numpy as np
import pdb


VMAT = np.uint16
RMAT = np.uint32


def set_cover_solver(sets, k=None, nsol=1, place=None, sets_hist=None):
    """ solve the linear integer programming problem using gurobi solver
    Parameters
    ----------
    sets: numpy matrix of (|S| x |universe|) representing the sets,
          i-th column correspond to the i-th element of the universe
    k: number of sets to be used (decision version)
    nsol: number of solution that gurobi return
    place: index of set that will belong to solution

    Return
    ------
    res: numpy matrix (nsol x nres) of indices of sets in the set_cover optimum
    isok: when option 'place' is defined take value False if
          do not exist a covering solution. (avoid Error)
    """
    solutions = None
    nsol = int(nsol)
    try:

        m = gu.Model("setcover")
        m.setParam(gu.GRB.Param.OutputFlag, 0)
        # find solutions that are the best
        m.setParam(gu.GRB.Param.PoolSearchMode, 2)
        # Limit how many solutions to collect
        m.setParam(gu.GRB.Param.PoolSolutions, nsol)
        # Limit the search space by setting a gap
        # for the worst possible solution that will be accepted
        m.setParam(gu.GRB.Param.PoolGap, 0)
        # remove presolve operation
        m.setParam(gu.GRB.Param.Presolve, 0)
        # set num threads
        m.setParam(gu.GRB.Param.Threads, 1)

        universe = sets.shape[1]
        nsets = sets.shape[0]

        # VARIABLES
        # tell if a set is choose (1) or not (0)
        variables = []
        for _ in range(nsets):
            variables.append(m.addVar(vtype=gu.GRB.BINARY))

        m.update()

        # CONSTRAINTS
        # covering constraint
        for t in range(universe):
            m.addConstr(
                gu.quicksum(
                    sets[r, t] * variables[r] for r in range(nsets)) >= 1)

        if k is None:
            # OBJ
            m.setObjective(gu.quicksum(m.getVars()))
        else:
            # CONSTRAINT
            m.addConstr(gu.quicksum(variables) == k)

        if place is not None:
            m.addConstr(variables[place] == 1)

        if sets_hist is not None:
            # pdb.set_trace()
            sets_hist = np.array(sets_hist)
            lenset = sets_hist.shape[1]
            for sh in sets_hist:
                m.addConstr(
                    gu.quicksum(variables[d] for d in sh) <= lenset - 1)
        m.optimize()

        try:
            obj = int(round(m.ObjVal))
        except AttributeError:
            raise gu.GurobiError("GurobiError", 3)

        if k is not None:
            obj = k

        solutions = np.zeros((m.SolCount, obj), dtype=RMAT)

        for e in range(solutions.shape[0]):
            m.setParam(gu.GRB.Param.SolutionNumber, e)
            i = 0
            for iset, v in enumerate(m.getVars()):
                if int(round(v.x)):
                    solutions[e, i] = iset
                    i += 1

        # m.write('model.lp')

        return solutions, True

    except gu.GurobiError:
        stat = m.getAttr(gu.GRB.Attr.Status)
        if stat == 3 and place is not None:
            return solutions, False
        elif stat == 3:
            print('Error while computing the set cover optimization problem')
        else:
            print('Gurobi Status after the optimization: ', stat)
        raise


def maximum_resources(csr_matrices, targets):
    """
    Parameter
    ---------
    csr_matrices: dictionary of type {"vertex_number1": csr_matrix1,
                                      "vertex_number2": csr_matrix2, ...}
                  csr_matrix represent the covering sets of the vertex
    targets: list of targets

    Return
    ------
    vertex_list: list of tuples representing the position and the route of
                 the optimal resources (ex. [(pos, route), ...])
    """
    tot_tgts = next(iter(csr_matrices.values())).shape[1]
    if np.any(targets < 0) or np.any(targets >= tot_tgts):
        raise ValueError('Targets in input of maximum_resources function'
                         'are not tartgets of the csr_matrices')
    mat = np.array([], dtype=np.uint8).reshape((0, tot_tgts))
    tot_len = 0
    for v in csr_matrices:
        tot_len += csr_matrices[v].shape[0]
    vertex_list = np.empty(tot_len, dtype=VMAT)
    covset_list = np.empty(tot_len, dtype=RMAT)
    start = 0
    for v in csr_matrices:
        arr = csr_matrices[v].toarray()
        mat = np.vstack((mat, arr))
        end = start + arr.shape[0]
        vertex_list[start:end] = v
        covset_list[start:end] = np.arange(arr.shape[0], dtype=RMAT)
        start = end
    mat_ix, isok = set_cover_solver(mat[:, targets])
    if not isok:
        raise gu.GurobiError("GurobiError", 3)
    mat_ix = mat_ix[0]
    return list(zip(vertex_list[mat_ix], covset_list[mat_ix]))


if __name__ == '__main__':
    matri = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
             [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]
    matri = np.array(matri)
    min0, _ = set_cover_solver(matri, k=2, nsol=1, place=1)
    # min1 = set_cover_solver(matri, k=(len(min0) + 1), nsol=6)
    print(min0)
    # print min1
