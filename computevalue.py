import numpy as np
import networkx as nx
import set_cover as sc
import functions as fn
from srg import graph as gr
from patrolling.correlated import correlated_row_gen as cr


def value_computation(graph, test=False, plot=False):
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
    shortest_matrix = fn.compute_shortest_sets(graph, tgts)
    csr = fn.compute_covering_routes(graph, tgts)
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
    print(temp_dict)
    values[len(min_resources)], _, _ = cr.correlated(temp_dict, target_values)
    print(cr.correlated(temp_dict, target_values)[0])
    for i in range(len(min_resources), len(max_resources) + 1):
        success, res = sc.set_cover_solver(shortest_matrix[:, tgts], k=i)
        temp_dict = {k: csr[res[k]] for k in range(len(res))}
        values[i], _, _ = cr.correlated(temp_dict, target_values)
    values[len(max_resources)] = 1
    for key, val in values.iteritems():
        print("Values of the game with {} resources is {}".format(key, val))
    return values


if __name__ == '__main__':
    while True:
        mat = gr.generateRandMatrix(15, 0.2)
        graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 0.8, 0, 3)
        if nx.is_connected(nx.from_numpy_matrix(mat)):
            value_computation(graph, test=True)
            break
