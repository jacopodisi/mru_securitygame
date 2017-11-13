# -*- coding: utf-8 -*-

import numpy as np
from scipy import sparse
from srg import computecovsets as cs
from srg import graph as gr
from patrolling.correlated import correlated_row_gen as cr
import ILP_solver as sc


mtype = np.uint8


def compute_value(graph, test=False, plot=False):
    """ Compute the values of the graph for every number of resources
        (from the minimum to the optimum)
    Parameters
    ----------
    graph: instance of gr.Graph class

    Return
    ------
    values: dictionary of type {"num_resources": game_value, ...}
    """
    if test:
        print("Adjacency matrix:\n")
        print(graph.getAdjacencyMatrix())

    tgts = graph.getTargets()
    # shortest matrix computation
    shortest_matrix = compute_shortest_sets(graph, tgts)
    csr = compute_covering_routes(graph, tgts)
    min_resources = sc.set_cover_solver(shortest_matrix[:, tgts])
    max_resources = sc.maximum_resources(csr, tgts)
    if test:
        print("\nShortest Matrix:\n")
        print(shortest_matrix)
        print("\nMinimum number of resources:\n")
        print(min_resources)
        print("\nMaximum number of resources:\n")
        print(max_resources)
    values = np.array([v.value for v in graph.vertices])
    temp_dict = {k: csr[min_resources[k]] for k in range(len(min_resources))}
    if test:
        print(temp_dict)
    game_values = {}
    game_values[len(min_resources)], _, _ = cr.correlated(temp_dict, values)
    for i in range(len(min_resources) + 1, len(max_resources)):
        res = sc.set_cover_solver(shortest_matrix[:, tgts], k=i)
        temp_dict = {k: csr[res[k]] for k in range(len(res))}
        game_values[i], _, _ = cr.correlated(temp_dict, values)
    game_values[len(max_resources)] = 1
    if test:
        for key, val in game_values.iteritems():
            print("Values of the game with {} res is {}".format(key, val))
    return game_values


def compute_shortest_sets(graph_game, targets):
    """ Compute a list of array containing the reachable
        target from each vetrex.

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


def compute_covering_routes(graph_game, targets):
    """ compute all the covering routes, from each vertex, for the given
        set of targets.
    Parameters
    ----------
    graph_game: instance of Graph class representing the game
    targets: list of targets for which compute the covering routes

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
    for v in range(n_vertices):
        covset = cs.computeCovSet(graph_game, v, targets)
        covset_matrix = np.zeros((len(covset), n_vertices), dtype=mtype)
        for route in range(len(covset)):
            covset_matrix[route, covset[route][0]] = 1
        csr_matrices[v] = sparse.csr_matrix(covset_matrix)
    return csr_matrices


if __name__ == '__main__':
    import iomanager as io
    while True:
        mat = gr.generateRandMatrix(15, 0.9)
        if is_connected(mat):
            graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 0.8, 0, 3)
            res = compute_value(graph)
            # io.save_results(v, filename="re.pickle")
            # succ, res = io.load_results("re.pickle")
            if True:
                print res
            break
