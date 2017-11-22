# -*- coding: utf-8 -*-

import numpy as np
from scipy import sparse
from srg import computecovsets as cs
from srg import graph as gr
from patrolling.correlated import correlated_row_gen as cr
import ILP_solver as sc
import tqdm


mtype = np.uint8


# @profile
def compute_values(graph, dominance=False):
    """ Compute the values of the graph for every number of resources
        (from the minimum to the optimum)
    Parameters
    ----------
    graph: instance of gr.Graph class

    Return
    ------
    values: dictionary of type {"num_resources": game_value, ...}
    """
    tgts = graph.getTargets()
    # shortest matrix computation
    shortest_matrix = compute_shortest_sets(graph, tgts)
    csr = compute_covering_routes(graph, tgts, dominance=dominance)

    min_res = sc.set_cover_solver(shortest_matrix[:, tgts])
    max_res = sc.maximum_resources(csr, tgts)

    tgt_values = np.array([v.value for v in graph.vertices])
    # build a dictionary with cov routes of selected resources
    temp_dict = {k + 1: csr[min_res[k]] for k in range(len(min_res))}

    game_values = {}
    strategies = {}
    placements = {}

    placements[len(min_res)] = min_res
    game_values[len(min_res)], strategies[len(min_res)], _ = cr.correlated(temp_dict, tgt_values)
    for i in range(len(min_res) + 1, len(max_res)):
        res = sc.set_cover_solver(shortest_matrix[:, tgts], k=i)
        temp_dict = {k + 1: csr[res[k]] for k in range(len(res))}
        placements[i] = res
        game_values[i], strategies[i], _ = cr.correlated(temp_dict, tgt_values)
    
    temp_dict = {k + 1: csr[max_res[k]] for k in range(len(max_res))}
    placements[len(max_res)] = max_res
    game_values[len(max_res)] = 1
    strategies[len(max_res)] = 0

    return game_values, placements, strategies


# @profile
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
    shortest_matrix = np.zeros(shape=matrix.shape, dtype=mtype)
    for tgt, dl in deadlines.iteritems():
        ok = shortest_paths[:, tgt] <= dl
        shortest_matrix[ok, tgt] = 1
    return shortest_matrix


# @profile
def compute_covering_routes(graph_game, targets, dominance=False):
    """ compute all the covering routes, from each vertex, for the given
        set of targets. The covering routes will contain always the starting
        vertex, wheteher it is a target or not. Other non-target vertex will
        be set to 0.
    Parameters
    ----------
    graph_game: instance of Graph class representing the game
    targets: list of targets for which compute the covering routes
    dominance: If set to True the dominanted route for each vertex
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
    t_range = tqdm.trange(n_vertices)
    for v in t_range:
        covset = cs.computeCovSet(graph_game, v, targets)
        covset_matrix = np.zeros((len(covset), n_vertices), dtype=mtype)

        if dominance:
            for route in range(len(covset)):
                covset_matrix[route, covset[route][0]] = 1
            covset_matrix = np.unique(covset_matrix, axis=0)
            for route in range(covset_matrix.shape[0]):
                a = covset_matrix[route] <= covset_matrix
                dom = np.all(a, axis=1)
                dom[route] = False
                if np.any(dom):
                    covset_matrix[route] = 0
            covset_matrix = covset_matrix[~np.all(
                covset_matrix == 0, axis=1)]
        else:
            for route in range(len(covset)):
                covset_matrix[route, covset[route][0]] = 1

        csr_matrices[v] = sparse.csr_matrix(covset_matrix)
    return csr_matrices


if __name__ == '__main__':
    import iomanager as io
    dominance = False
    # mat = gr.generateRandMatrix(16, 0.25, density=True)
    # graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 1, 4, 4)
    file_gr = "graph_n16_d0.25_dead4"
    # io.save_results(graph, filename=file_gr)
    graph = io.load_results(file_gr)

    res = compute_values(graph, dominance=dominance)

    print res
    file_res = ''
    if dominance:
        file_res = "results_" + file_gr + "vps_dom"
    else:
        file_res = "results_" + file_gr + "vps"
    io.save_results(res, filename=file_res)
