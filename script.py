# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np


def compute_shortest_sets(matrix, deadlines):
    """ Compute a list of array containing the reachable
        target from each vetrex.

    Parameters
    ----------
    matrix: adjacency matrix of the graph
    deadlines: dictionary of type {"target_1": deadline_1,
                                    "target_2": deadline_2, ...}

    Return
    ------
    shortest_matrix: numpy matrix of (|nodes| x |nodes|), where the row
                   0 represent the shortest_set of node 0 and so on..
    """
    G = nx.from_numpy_matrix(matrix)
    shortest_matrix = np.zeros(shape=matrix.shape)
    for tgt, dl in deadlines.iteritems():
        cov = nx.single_source_shortest_path_length(G, tgt, cutoff=dl)
        shortest_matrix[cov.keys(), tgt] = 1
    return shortest_matrix
