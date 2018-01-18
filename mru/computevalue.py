# -*- coding: utf-8 -*-

import time
import logging
import numpy as np
import ILP_solver as sc

from scipy import sparse
from srg import computecovsets as cs
from srg import graph as gr
from patrolling.correlated import correlated_row_gen as cr


MTYPE = np.uint8

log = logging.getLogger(__name__)


def compute_values(graph, rm_dominated=False, enum=1):
    """ Compute the values of the graph for every number of resources
        (from the minimum to the optimum)
    Parameters
    ----------
    graph: instance of gr.Graph class
    rm_dominated: If set to True the dominanted route for each vertex
                  are eliminated

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
                                                           setcover_min,
                                                           correlated min,
                                                           setcover_k,
                                                           )
    """
    try:
        log.debug("start compute_values function")
        start_time = time.time()
        tgts = graph.getTargets()
        tgt_values = np.array([v.value for v in graph.vertices])

        game_values = {}
        strategies = {}
        placements = {}
        solutionlist = []
        times_list = {}
        max_res_strategy = None

        log.debug("compute shortest sets")
        st_time = time.time()
        shortest_matrix = compute_shortest_sets(graph, tgts)
        times_list[0] = time.time() - st_time
        log.debug("compute covering routes")
        st_time = time.time()
        csr = compute_covering_routes(graph, tgts, rm_dominated=rm_dominated)
        times_list[1] = time.time() - st_time

        # optimum resource game solution
        log.debug("compute solution with maximum resources")
        st_time = time.time()
        max_res_strategy = sc.maximum_resources(csr, tgts)
        times_list[2] = time.time() - st_time
        max_num_res = len(max_res_strategy)

        # minimum resource game solution
        log.debug("compute solution with minimum resources")
        st_time = time.time()
        min_res = sc.set_cover_solver(shortest_matrix[:, tgts], nsol=enum)
        times_list[3] = time.time() - st_time
        min_n_res = min_res.shape[1]
        if min_n_res < max_num_res:
            road_dict = {k + 1: csr[min_res[0, k]]
                         for k in range(min_n_res)}
            st_time = time.time()
            solutionlist.append(cr.correlated(road_dict, tgt_values)[0:2] +
                                (min_res[0],))
            times_list[4] = time.time() - st_time
            log.debug("compute solution for different dispositions of" +
                      " minimum resources")
            for sol in range(1, min_res.shape[0]):
                road_dict = {k + 1: csr[min_res[sol, k]]
                             for k in range(min_n_res)}
                solution = cr.correlated(road_dict, tgt_values)
                if solutionlist[-1][0] < solution[0]:
                    solutionlist[-1] = (solution[0], solution[1], min_res[sol])

        # what happen between
        times_list[5] = []
        for i in range(min_res.shape[1] + 1, max_num_res):
            log.debug("compute solution with " + str(i) + " resources")
            st_time = time.time()
            res = sc.set_cover_solver(shortest_matrix[:, tgts],
                                      k=i, nsol=enum)
            times_list[5].append(time.time() - st_time)
            road_dict = {k + 1: csr[res[0, k]]
                         for k in range(res.shape[1])}
            st_time = time.time()
            solutionlist.append(cr.correlated(road_dict, tgt_values)[0:2] +
                                (res[0],))
            times_list[5].append(time.time() - st_time)
            log.debug("compute solution for different disposition of " +
                      str(i) + " resources")
            for sol in range(1, res.shape[0]):
                road_dict = {k + 1: csr[res[sol, k]]
                             for k in range(res.shape[1])}
                solution = cr.correlated(road_dict, tgt_values)
                if solutionlist[-1][0] < solution[0]:
                    solutionlist[-1] = (solution[0], solution[1], res[sol])

        times_list[6] = time.time() - start_time

        # change solution format in a more readable ones
        for sol in solutionlist:
            game_values[sol[2].shape[0]] = sol[0]
            strategies[sol[2].shape[0]] = sol[1]
            placements[sol[2].shape[0]] = [
                (r + 1, p) for r, p in enumerate(sol[2])]

        placements[max_num_res] = [
            (re + 1, x[0]) for re, x in enumerate(max_res_strategy)]
        game_values[max_num_res] = 1
        strategies[max_num_res] = [(
            [(ve + 1, x[1]) for ve, x in enumerate(max_res_strategy)],
            1.0)]

        return game_values, placements, strategies, times_list

    except (cr.TimeoutException, KeyboardInterrupt) as ex:

        log.exception(ex)

        for sol in solutionlist:
            if sol[0] is not None and\
               sol[1] is not None and\
               sol[2] is not None:
                game_values[sol[2].shape[0]] = sol[0]
                strategies[sol[2].shape[0]] = sol[1]
                placements[sol[2].shape[0]] = [
                    (r + 1, p) for r, p in enumerate(sol[2])]
        if max_res_strategy is not None:
            placements[max_num_res] = [
                (re + 1, x[0]) for re, x in enumerate(max_res_strategy)]
            game_values[max_num_res] = 1
            strategies[max_num_res] = [(
                [(ve + 1, x[1]) for ve, x in enumerate(max_res_strategy)],
                1.0)]

        return game_values, placements, strategies, times_list


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
    """
    if not np.all(
            np.in1d(targets, graph_game.getTargets())):
        raise ValueError('Targets in input of compute_shortest_sets function'
                         'are not tartgets of the graph_game')
    matrix = graph_game.getAdjacencyMatrix()
    if gr.inf == 999:
        matrix[matrix == 999] = 0
    deadlines = {t: graph_game.getVertex(t).deadline for t in targets}
    shortest_paths = sparse.csgraph.shortest_path(
        matrix, directed=False, unweighted=True)
    shortest_matrix = np.zeros(shape=matrix.shape, dtype=MTYPE)
    for tgt, dl in deadlines.iteritems():
        covered = shortest_paths[:, tgt] <= dl
        shortest_matrix[covered, tgt] = 1
    return shortest_matrix


def compute_covering_routes(graph_game, targets, rm_dominated=False):
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

    Return
    ------
    csr_matrices: dictionary of type {"vertex_number1": csr_matrix1,
                                      "vertex_number2": csr_matrix2, ...}
                  csr_matrix represent the covering sets of the vertex
    """
    if not np.all(
            np.in1d(targets, graph_game.getTargets())):
        raise ValueError('Targets in input of compute_covering_routes function'
                         'are not tartgets of the graph_game')
    n_vertices = len(graph_game.getVertices())
    csr_matrices = {}
    for ver in range(n_vertices):
        covset = cs.computeCovSet(graph_game, ver, targets)
        covset_matrix = np.zeros((len(covset), n_vertices), dtype=MTYPE)

        l_covset = len(covset)
        if rm_dominated:
            for route in range(l_covset):
                covset_matrix[route, covset[route][0]] = 1
            covset_matrix = np.vstack({tuple(row) for row in covset_matrix})
            for route in range(covset_matrix.shape[0]):
                dom_rows = covset_matrix[route] <= covset_matrix
                dom = np.all(dom_rows, axis=1)
                dom[route] = False
                if np.any(dom):
                    covset_matrix[route] = 0
            covset_matrix = covset_matrix[~np.all(
                covset_matrix == 0, axis=1)]
        else:
            for route in range(l_covset):
                covset_matrix[route, covset[route][0]] = 1

        csr_matrices[ver] = sparse.csr_matrix(covset_matrix)
    return csr_matrices


if __name__ == '__main__':
    import iomanager as io
    domopt = True
    nodes = 10
    # mat = gr.generateRandMatrix(nodes, 0.25, density=True)
    # rand_graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 1, 4, 4)
    file_gr = "graph_n" + str(nodes) + "_d0.25_dead4_ix_1"
    # io.save(rand_graph, filename=file_gr)
    rand_graph = io.load(io.FILEDIR + file_gr + ".pickle")

    with cr.time_limit(6):
        result = compute_values(rand_graph, rm_dominated=domopt, enum=10)

    print "game values: " + str(result[0])
    print "placements: " + str(result[1])
    print "strategies: " + str(result[2])
    print "comptime:" + str(result[3])
    file_res = ''
    if domopt:
        file_res = "results_" + file_gr + "vps_dom"
    else:
        file_res = "results_" + file_gr + "vps"
    # io.save_results(result, filename=file_res)
