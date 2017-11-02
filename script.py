# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
from scipy import sparse
from srg import computecovsets as cs
from srg import graph as gr
from srg import correlated as cr
import set_cover as sc


mtype = np.uint8


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
    matrix = graph_game.getAdjacencyMatrix()
    if gr.inf == 999:
        matrix[matrix == 999] = 0
    deadlines = {t: graph_game.getVertex(t).deadline for t in targets}
    G = nx.from_numpy_matrix(matrix)
    shortest_matrix = np.zeros(shape=matrix.shape, dtype=mtype)
    for tgt, dl in deadlines.iteritems():
        cov = nx.single_source_shortest_path_length(G, tgt, cutoff=dl)
        shortest_matrix[cov.keys(), tgt] = 1
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
    n_vertices = len(graph_game.getVertices())
    csr_matrices = {}
    for v in range(n_vertices):
        covset = cs.computeCovSet(graph_game, v, targets)
        covset_matrix = np.zeros((len(covset), n_vertices), dtype=mtype)
        # cs_matrices[v] = np.vstack(route[0]
        for route in range(len(covset)):
            covset_matrix[route, covset[route][0]] = 1

        csr_matrices[v] = sparse.csr_matrix(covset_matrix)
    return csr_matrices


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


def compute_graph(file_path):
    """ given the path of the file containing the description of the graph
        return a corresponding Graph object
    """
    vertices = np.array([])
    G = gr.Graph(vertices)
    return G


if __name__ == '__main__':
    mat = gr.generateRandMatrix(15, 0.2)
    if not nx.is_connected(nx.from_numpy_matrix(mat)):
        continue
    graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 0.8, 0, 3)
    print("Adjacency matrix:\n")
    print(graph.getAdjacencyMatrix())
    print 'targets'
    print graph.getTargets()
    tgts = graph.getTargets()
    # shortest matrix computation
    shortest_matrix = compute_shortest_sets(graph, tgts)
    csr = compute_covering_routes(graph, tgts)


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
    success, min_resources = sc.set_cover_solver(shortest_matrix[:, tgts])
    if not success:
        return []
    success, max_resources = sc.maximum_resources(csr, tgts)
    if not success:
        return []
    if test:
        print("\nShortest Matrix:\n")
        print(shortest_matrix)
        print("\nMinimum number of resources:\n")
        print(min_resources)
        print("\nMaximum number of resources:\n")
        print(max_resources)
    target_values = np.array([v.value for v in graph.vertices])
    temp_dict = {k: csr[min_resources[k]] for k in range(len(min_resources))}
    values = {}
    if test:
        print(temp_dict)
    values[len(min_resources)], _, _ = cr.correlated(temp_dict, target_values)
    for i in range(len(min_resources), len(max_resources) + 1):
        success, res = sc.set_cover_solver(shortest_matrix[:, tgts], k=i)
        temp_dict = {k: csr[res[k]] for k in range(len(res))}
        values[i], _, _ = cr.correlated(temp_dict, target_values)
    values[len(max_resources)] = 1
    if test:
        for key, val in values.iteritems():
            print("Values of the game with {} res is {}".format(key, val))
    return values


if __name__ == '__main__':
    while True:
        mat = gr.generateRandMatrix(15, 0.2)
        if nx.is_connected(nx.from_numpy_matrix(mat)):
            graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 0.8, 0, 3)
            v = compute_value(graph, test=True)
            print v
            break
