# -*- coding: utf-8 -*-

import gurobipy as gu
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

        m = gu.Model("setcover")
        m.setParam('OutputFlag', False)

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

        m.write('set_cover.lp')

        variables = m.getAttr('x', variables)

        return np.nonzero(variables)[0]

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
    vertex_list = np.array([], dtype=np.uint16)
    covset_list = np.array([], dtype=np.uint16)
    for v in csr_matrices:
        arr = csr_matrices[v].toarray()
        mat = np.vstack((mat, arr))
        t_veli = np.full(shape=(arr.shape[0]), fill_value=v, dtype=np.uint16)
        vertex_list = np.append(vertex_list, t_veli)
        t_covli = np.arange(arr.shape[0], dtype=np.uint16)
        covset_list = np.append(covset_list, t_covli)
    mat_ix = set_cover_solver(mat[:, targets])
    return [(vertex_list[ix], covset_list[ix]) for ix in mat_ix]


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
    randmat = np.random.randint(2, size=(50, 10), dtype=np.uint8)
    success, min0 = set_cover_solver(randmat)
    if not success:
        exit()
    success, min1 = set_cover_solver(randmat, k=(len(min0) + 1))
    if len(min1) != (len(min0) + 1):
        print 'Error in lengths' + min0 + min1
