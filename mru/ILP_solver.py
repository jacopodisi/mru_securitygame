# -*- coding: utf-8 -*-

import gurobipy as gu
import numpy as np


VMAT = np.uint16
RMAT = np.uint32


def set_cover_solver(sets, k=None, nsol=1):
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

        m.optimize()

        if k is None:
            obj = int(m.ObjVal)
        else:
            obj = k

        solutions = np.zeros((m.SolCount, obj), dtype=RMAT)

        for e in range(solutions.shape[0]):
            m.setParam(gu.GRB.Param.SolutionNumber, e)
            i = 0
            for iset, v in enumerate(m.getVars()):
                if int(v.Xn):
                    solutions[e, i] = iset
                    i += 1


        return solutions

    except gu.GurobiError:
        stat = m.getAttr(gu.GRB.Attr.Status)
        print 'Error while computing the set cover optimization problem'
        if stat == 3:
            print 'Infeasible solution'
        else:
            print 'Gurobi Status after the optim: ', stat
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
    tot_tgts = csr_matrices[csr_matrices.keys()[0]].shape[1]
    if np.any(targets < 0) or np.any(targets >= tot_tgts):
        raise ValueError('Targets in input of maximum_resources function'
                         'are not tartgets of the csr_matrices')
    mat = np.array([], dtype=np.uint8).reshape((0, tot_tgts))
    vertex_list = np.array([], dtype=VMAT)
    covset_list = np.array([], dtype=RMAT)
    for v in csr_matrices:
        arr = csr_matrices[v].toarray()
        mat = np.vstack((mat, arr))
        t_veli = np.full(shape=(arr.shape[0]), fill_value=v, dtype=VMAT)
        vertex_list = np.append(vertex_list, t_veli)
        t_covli = np.arange(arr.shape[0], dtype=RMAT)
        covset_list = np.append(covset_list, t_covli)
    mat_ix = set_cover_solver(mat[:, targets])[0]
    return zip(vertex_list[mat_ix], covset_list[mat_ix])


def local_search(matrix, deadlines, number_of_resources):
    """ Compute the enumeration of the optimal position of the given
        number of resources.
    Parameters
    ----------
    matrix: adjacency matrix of the graph
    deadlines: dictionary of type {"target_1": deadline_1,
                                    "target_2": deadline_2, ...}
    number_of_resources: the number of resources of the defender for which
                         enumerate their disposition on the graph

    Return
    ------
    enum_matrix: numpy matrix of (|enum| x |num_res|), where each row
                 0 represent the shortest_set of node 0 and so on..
    """
    return


if __name__ == '__main__':
    mat = [[1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
           [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
           [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]]
    mat = np.array(mat)
    min0 = set_cover_solver(mat, nsol=6)
    min1 = set_cover_solver(mat, k=(len(min0) + 1), nsol=6)
    print min0
    print min1
