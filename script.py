# -*- coding: utf-8 -*-
"""Script to run the compute_value algorithm on pregenerated graphs.
Given the parameters of the graph, apply to it the compute_value function with
a predefined time limit and save the results in file (io.save_results function)
Parameters
----------
-d, --density: density of edge of the graph
-t, --target: number of targets/node of the graph
-D, --deadline: deadline of the targets
-i, --graphid: id of the graph
"""

import sys
import getopt
import os
import pickle

from mru import computevalue as cv
from mru import iomanager as io
from mru.patrolling.correlated import correlated_row_gen as cr


def main():

    options, _ = getopt.getopt(sys.argv[1:],
                               'd:t:D:i:',
                               ['density=',
                                'ntarget=',
                                'deadline=',
                                'graphid='])

    for opt, arg in options:
        if opt in ('-d', '--density'):
            den = arg
        elif opt in ('-t', '--target'):
            ntgts = arg
        elif opt in ('-D', '--deadline'):
            dead = arg
        elif opt in ('-i', '--graphid'):
            ix = arg

    graph_path = "graphs_" + ntgts + "_ntgts/instance_ntgts_"\
                 + ntgts + "_den_" + den + "_dead_" + dead + "_ix_" + ix

    if not os.path.isfile("./file/graphs/" + graph_path + ".pickle"):
        m = 'graph {} do not exist'.format("./file/graphs/" + graph_path + ".pickle")
        raise IOError(m)
    with open("./file/graphs/" + graph_path + ".pickle", mode='r') as f:
        graph = pickle.load(f)

    with cr.time_limit(60):
        result = cv.compute_values(graph, rm_dominated=True, enum=10)

    io.save_results(graph_path, result)


if __name__ == '__main__':
    main()
