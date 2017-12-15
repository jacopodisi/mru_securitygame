# -*- coding: utf-8 -*-

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

    graph_path = "graphs/graphs_" + ntgts + "_ntgts/instance_ntgts_"\
                 + ntgts + "_den_" + den + "_dead_" + dead + "_ix_" + ix

    if not os.path.isfile("./file/" + graph_path + ".pickle"):
        m = 'graph {} do not exist'.format("./file/" + graph_path + ".pickle")
        raise IOError(m)
    with open("./file/" + graph_path + ".pickle", mode='r') as f:
        graph = pickle.load(f)

    with cr.time_limit(3600):
        result = cv.compute_values(graph, rm_dominated=True, enum=10)

    print result

    io.save_results(graph_path, result)


if __name__ == '__main__':
    main()
