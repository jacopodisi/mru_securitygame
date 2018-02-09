# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def print_srategy_for_n_player(
        gr, n_res, result, cov_set, pos=None, color='r'):
    num_nodes = nx.number_of_nodes(gr)
    placements = result[1]
    strategies = result[2]
    n = n_res
    strategy = np.zeros(shape=(len(strategies[n]), num_nodes))
    prob_strategy = np.zeros(shape=(len(strategies[n])))
    i = 0
    string_routes = [''] * len(strategies[n])
    for stra in strategies[n]:
        for route_pl_id in stra[0]:
            vert = placements[n][route_pl_id[0] - 1][1]
            route = cov_set[vert][route_pl_id[1]].toarray()
            strategy[i] = strategy[i] + route
            r = str(np.where(route == 1)[1]) + '\n'
            string_routes[i] = string_routes[i] + str(vert) + " --> " + r
        prob_strategy[i] = stra[1]
        i += 1
    if pos is None:
        pos = nx.spring_layout(gr)
    for place in range(len(strategies[n])):
        col = ['w'] * num_nodes
        tr = np.where(strategy[place] > 0)[0]
        for i in tr:
            col[i] = color
        plt.figure(place)
        plt.title("probability " + str(prob_strategy[place]))
        plt.figtext(1, 0.5, string_routes[place],
                    verticalalignment='center')
        nx.draw_networkx(gr, node_color=col, pos=pos)
    plt.show()


def print_srategy2_for_n_player(
        gr, n_res, result, pos=None, color='r'):
    num_nodes = nx.number_of_nodes(gr)
    placements = result[1]
    strategies = result[4]
    n = n_res
    strategy = np.zeros(shape=(len(strategies[n]), num_nodes))
    prob_strategy = np.zeros(shape=(len(strategies[n])))
    i = 0
    string_routes = [''] * len(strategies[n])
    for stra in strategies[n]:
        for route_pl_id in stra[0]:
            vert = placements[n][route_pl_id[0] - 1][1]
            route = route_pl_id[1]
            strategy[i] = strategy[i] + route
            r = str(np.where(route == 1)[1]) + '\n'
            string_routes[i] = string_routes[i] + str(vert) + " --> " + r
        prob_strategy[i] = stra[1]
        i += 1
    if pos is None:
        pos = nx.spring_layout(gr)
    for place in range(len(strategies[n])):
        col = ['w'] * num_nodes
        tr = np.where(strategy[place] > 0)[0]
        for i in tr:
            col[i] = color
        plt.figure(place)
        plt.title("probability " + str(prob_strategy[place]))
        plt.figtext(1, 0.5, string_routes[place],
                    verticalalignment='center')
        nx.draw_networkx(gr, node_color=col, pos=pos)
    plt.show()


def print_dead_val(graph):
    tgt = graph.getTargets()
    deadlines = {t: graph.getVertex(t).deadline for t in tgt}
    print("deadlines: " + str(deadlines))
    node_values = {t: graph.getVertex(t).value for t in tgt}
    print("values:")
    for key, val in node_values.items():
        print(str(key) + ": " + str(val))


def compute_nx_graph(graph):
    adj = graph.getAdjacencyMatrix()
    adj[adj > 1] = 0
    gr = nx.from_numpy_matrix(adj)
    pos = nx.spring_layout(gr)
    nx.draw_networkx(gr, node_color='y', pos=pos)
    return gr, pos


def plot_values(result, x_label='# resources', y_label='expected utility'):
    val = sorted(result[0].items())
    x, y = list(zip(*val))

    return x, y
