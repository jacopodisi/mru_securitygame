# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
from scipy import sparse
from srg import computecovsets as cs
from srg import graph as gr


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
    shortest_matrix = np.zeros(shape=matrix.shape)
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
    num_vertices = len(graph_game.getVertices())
    csr_matrices = {}
    for v in xrange(num_vertices):
        covset = cs.computeCovSet(graph_game, v, targets)
        covset_matrix = np.zeros((len(covset), num_vertices), dtype=np.int8)
        # cs_matrices[v] = np.vstack(route[0]
        for route in xrange(len(covset)):
            covset_matrix[route, covset[route][0]] = 1

        csr_matrices[v] = sparse.csr_matrix(covset_matrix)
    return csr_matrices



if __name__ == '__main__':
    import matplotlib.pyplot as plt
    mat = gr.generateRandMatrix(15, 0.3)
    graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 0.8, 0, 3)
    print("Adjacency matrix:")
    print(graph.getAdjacencyMatrix())

    print("\nGraph:\n")
    G = nx.from_numpy_matrix(np.array(mat))
    nx.draw(G, with_labels=True)
    plt.show()

    tgts = graph.getTargets()
    # shortest matrix computation
    shortest_matrix = compute_shortest_sets(graph, tgts)
    print("\nShortest Matrix:\n")
    print(shortest_matrix)
