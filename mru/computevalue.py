# -*- coding: utf-8 -*-

import time
import logging
import numpy as np
import pdb
from . import ILP_solver as sc
from . import signal_receiver as sr
from . import placement_enum as pe
from . import apx_covering_sets as apx

from scipy import sparse
from scipy.sparse import csgraph
from .srg import graph as gr
from .srg import computecovsets as cs
from .patrolling.correlated import correlated_row_gen as cr


MTYPE = np.bool_

log = logging.getLogger(__name__)


def reformat(solutionlist, improveslist):
    """ Modify the format to respect compatibility of the solutions
    """
    game_values = {}
    strategies = {}
    placements = {}
    impro = {}
    for nres, sol in solutionlist.iteritems():
        if sol[0] is not None and\
           sol[1] is not None and\
           sol[2] is not None:
            game_values[nres] = sol[0]
            placements[nres] = [
                (r + 1, p) for r, p in enumerate(sol[2])]
            strategies[nres] = sol[1]
    for nres, imp in improveslist.iteritems():
        impro[nres] = []
        for sol in imp:
            temp = (sol[0],
                    [(r + 1, p) for r, p in enumerate(sol[2])],
                    sol[1])
            impro[nres].append(temp)

    return game_values, placements, strategies, impro


def compute_values(graph, rm_dom=False, enum=1, covset=None, times=None, enumtype=1, apxtype=None):
    """ Compute the values of the graph for every number of resources
        (from the minimum to the optimum)
    Parameters
    ----------
    graph: instance of gr.Graph class
    rm_dom: If set to True the dominanted route for each vertex
                  are eliminated
    enum: number of solution to iterate to find the best one
    covset: covering set (if already computed)
    enumtype: type of algorithm used to iterate through different solutions
    apxtype: type of permutation to be used in the apx_covering_sets. The approximation
             will be used only if an "apxtype" will be specified.

    Return
    ------
    game_values: dictionary of type {"num_resources": game_value, ...}
    placements: dictionary of type {"num_resources":
                                    [(resource, position), ...]}
    strategies: dictionary of type {"num_resources":
                                    [([(res, routeid), ..], prob), ...]}
    time_list: list of computation times of each operation(shortest_sets,
                                                           covering_routes,
                                                           max_resources,
                                                           remove_dom,
                                                           correlated_min,
                                                           correlated_k,
                                                           tot_time
                                                           )
    csr: covering sets of every node
    iter_sol: dictionary of type {"num_resources":
                                  improvements, ...}
              improvements is a list of (expected utlity, defender's strategy,
              resource placement) tuples, one for each placement analysed.

    """
    enum = int(enum)
    enumtype = int(enumtype)
    if apxtype is not None:
        apxtype = int(apxtype)
    signal_receiver = sr.SignalReceiver(log)
    log.debug("start compute_values function")
    start_time = time.clock()
    tgts = graph.getTargets()
    node_values = np.array([v.value for v in graph.vertices])

    solutionlist = {}
    times_list = {}
    improves = {}

    log.debug("compute shortest sets")
    st_time = time.clock()
    shortest_matrix, shortest_paths = compute_shortest_sets(graph, tgts)
    times_list[0] = time.clock() - st_time
    if covset is None:
        log.debug("compute covering routes")
        st_time = time.clock()
        sol = compute_covering_routes(graph, tgts, sp=shortest_paths,
                                      rm_dominated=rm_dom, apxtype=apxtype)
        times_list[1] = time.clock() - st_time
        csr = sol[0]
        times_list[3] = sol[1]
    else:
        csr = covset
        times_list[1] = times[1]
    # optimum resource game solution

    retcsr = None
    if apxtype is None:
        retcsr = csr

    if signal_receiver.kill_now:
        f_sol = reformat(solutionlist, improves)
        return f_sol[0], f_sol[1], f_sol[2], times_list, retcsr, f_sol[3]
    log.debug("compute solution with maximum resources")
    st_time = time.clock()
    max_res_strategy = sc.maximum_resources(csr, tgts)
    times_list[2] = time.clock() - st_time
    max_num_res = len(max_res_strategy)
    solutionlist[max_num_res] = (
        1,
        [([(ve + 1, x[1]) for ve, x in enumerate(max_res_strategy)], 1.0)],
        [x[0] for x in max_res_strategy])

    if signal_receiver.kill_now:
        f_sol = reformat(solutionlist, improves)
        return f_sol[0], f_sol[1], f_sol[2], times_list, retcsr, f_sol[3]

    enumfunc = pe.enumfunction(enumtype=enumtype, covset=csr,
                               node_values=node_values,
                               sigrec=signal_receiver,
                               enum=enum,
                               short_set=shortest_matrix,
                               short_path=shortest_paths,
                               maxnumres=max_num_res)

    # minimum resource game solution
    log.debug("compute solution with minimum resources")
    st_time = time.clock()
    best_enum_sol = enumfunc()
    times_list[4] = time.clock() - st_time
    # pdb.set_trace()
    if best_enum_sol[0] is not None:
        corr_sol, imp = best_enum_sol
        min_num_res = corr_sol[2].shape[0]
        solutionlist[min_num_res] = corr_sol
        improves[min_num_res] = imp
    else:
        min_num_res = max_num_res

    if signal_receiver.kill_now:
        f_sol = reformat(solutionlist, improves)
        return f_sol[0], f_sol[1], f_sol[2], times_list, retcsr, f_sol[3]

    # what happen between
    times_list[5] = []
    for i in range(min_num_res + 1, max_num_res):
        log.debug("compute solution with " + str(i) + " resources")
        st_time = time.clock()
        solutionlist[i], improves[i] = enumfunc(n_res=i)
        times_list[5].append(time.clock() - st_time)

        if signal_receiver.kill_now:
            f_sol = reformat(solutionlist, improves)
            return f_sol[0], f_sol[1], f_sol[2], times_list, retcsr, f_sol[3]

    times_list[6] = time.clock() - start_time
    if covset is not None:
        times_list[6] += times[1]

    # change solution format in a more readable ones
    f_sol = reformat(solutionlist, improves)
    return f_sol[0], f_sol[1], f_sol[2], times_list, retcsr, f_sol[3]


def compute_shortest_sets(graph_game, targets):
    """ Compute a list of array containing the reachable
        target from each vetrex. Column corresponding to non-targets
        are set to 0.

    Parameters
    ----------
    graph_game: instance of Graph class representing the game
    targets: list of targets for which compute the covering routes

    Return
    ------
    shortest_matrix: numpy matrix of (|nodes| x |nodes|), where the row
                   0 represent the shortest_set of node 0 and so on..
    shortest_paths: numpy matrix of (|nodes| x |nodes|), where the row
                    0 represent the shortest path cost of node 0 and so on..
    """
    if not np.all(
            np.in1d(targets, graph_game.getTargets())):
        raise ValueError('Targets in input of compute_shortest_sets function'
                         'are not tartgets of the graph_game')
    matrix = graph_game.getAdjacencyMatrix()
    if gr.inf == 999:
        matrix[matrix == 999] = 0

    deadlines = {t: graph_game.getVertex(t).deadline for t in targets}

    shortest_paths, pred = csgraph.shortest_path(
        matrix, directed=False, unweighted=True, return_predecessors=True)

    shortest_matrix = np.zeros(shape=matrix.shape, dtype=MTYPE)

    for tgt, dl in deadlines.iteritems():
        covered = shortest_paths[:, tgt] <= dl
        shortest_matrix[covered, tgt] = 1

    return shortest_matrix, shortest_paths


def compute_covering_routes(graph_game, targets, rm_dominated=False, sp=None, apxtype=None):
    """ compute all the covering routes, from each vertex, for the given
        set of targets. The covering routes will contain always the starting
        vertex, wheteher it is a target or not. Other non-target vertex will
        be set to 0.
    Parameters
    ----------
    graph_game: instance of Graph class representing the game
    targets: list of targets for which compute the covering routes
    rm_dominated: If set to True the dominanted route for each vertex
                  are eliminated
    apxtype: define which permutation is used during the computation of the apx_covering_sets,
             the approximation will be performed only if a type will be defined.
             0  --> decreasing distance from v0
             1  --> increasing distance from v0
             2  --> increasing deadline
             3  --> increasing order of excess time (dead(t) - dist(v0, t))
             >3 --> every type of permutation + random order repeated (apxtype)-times

    Return
    ------
    csr_matrices: dictionary of type {"vertex_number1": csr_matrix1,
                                      "vertex_number2": csr_matrix2, ...}
                  csr_matrix represent the covering sets of the vertex
    """
    everytgts = graph_game.getTargets()
    if not np.all(
            np.in1d(targets, everytgts)):
        raise ValueError('Targets in input of compute_covering_routes function'
                         'are not tartgets of the graph_game')
    vertices = graph_game.getVertices()
    deadlines = np.array([v.deadline for v in vertices])
    n_vertices = len(vertices)
    csr_matrices = {}
    timermdom = 0

    for ver in range(n_vertices):
        if apxtype is not None and sp is None:
            raise ValueError("No shortest path cost with apxtype specified")
        if apxtype is None:
            covset = cs.computeCovSet(graph_game, ver, targets)
            covset_matrix = np.zeros((len(covset), n_vertices), dtype=MTYPE)
            for route in range(len(covset)):
                covset_matrix[route, covset[route][0]] = 1
        elif apxtype in [0, 1, 2, 3]:
            covset_matrix = apx.compute_apxcoveringsets(ver, sp, targets,
                                                        deadlines, apxtype)
        elif apxtype > 3:
            covset_matrix = np.empty((0, n_vertices), dtype=MTYPE)
            for apxtp in range(apxtype + 4):
                temp_covset = apx.compute_apxcoveringsets(ver, sp, targets,
                                                          deadlines, apxtp)
                covset_matrix = np.vstack((covset_matrix, temp_covset))
        else:
            m = "Apxtype " + str(apxtype) + " does not exists."
            raise ValueError(m)

        strm = time.clock()
        if rm_dominated:
            best = np.full(covset_matrix.shape[0], True, dtype=np.bool_)
            for i, c in enumerate(covset_matrix):
                if best[i]:
                    best[best] = np.logical_not(np.all(covset_matrix[best] <= c, axis=1))
                    best[i] = True
            covset_matrix = covset_matrix[best]
        timermdom += time.clock() - strm

        csr_matrices[ver] = sparse.csr_matrix(covset_matrix)
    return csr_matrices, timermdom
