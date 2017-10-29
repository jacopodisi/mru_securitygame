import matplotlib.pyplot as plt
import sys
import numpy as np
import networkx as nx
import set_cover as sc
import functions as fn
from srg import graph as gr
from patrolling.correlated import correlated_row_gen as cr


def value_computation(test=False):
    mat = gr.generateRandMatrix(15, 0.2)
    graph = gr.generateRandomGraph(mat, np.shape(mat)[0], 0.8, 0, 3)
    if test:
        print("Adjacency matrix:\n")
        print(graph.getAdjacencyMatrix())

    # to display the graph in OS X, must be used "frameworkpython"
    # or "jupyter notebook" and argument "plot"
    if len(sys.argv) > 1 and sys.argv[1] == "plot" and test:
        print("\nGraph:\n")
        G = nx.from_numpy_matrix(np.array(mat))
        nx.draw(G, with_labels=True)
        plt.show()

    tgts = graph.getTargets()
    # shortest matrix computation
    shortest_matrix = fn.compute_shortest_sets(graph, tgts)
    csr = fn.compute_covering_routes(graph, tgts)
    min_resources = sc.set_cover_solver(shortest_matrix[:, tgts])
    max_resources = sc.maximum_resources(csr, tgts)
    if test:
        print("\nShortest Matrix:\n")
        print(shortest_matrix)
        print("\nShortest Matrix min res:\n")
        print(shortest_matrix[:, tgts][min_resources, :])
        print("\nMaximum number of resources:\n")
        print(max_resources)
    target_values = np.array([v.value for v in graph.vertices])
    temp_dict = {k: csr[min_resources[k]] for k in range(len(min_resources))}
    values = {}
    print(temp_dict)
    values[len(min_resources)], _, _ = cr.correlated(temp_dict, target_values)
    print(cr.correlated(temp_dict, target_values)[0])
    for i in range(len(min_resources), len(max_resources) + 1):
        res = sc.set_cover_solver(shortest_matrix[:, tgts], k=i)
        temp_dict = {k: csr[k] for k in res if k in csr}
        values[i], _, _ = cr.correlated(temp_dict, target_values)
    values[len(max_resources)] = 1
    for key, val in values.iteritems():
        print("Values of the game with {} resources is {}".format(key, val))


if __name__ == '__main__':
    value_computation(test=True)