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
import logging

from mru import computevalue as cv
from mru import iomanager as io
from mru.patrolling.correlated import correlated_row_gen as cr


def main():

    timeout = False

    logfile = "script.log"

    options, _ = getopt.getopt(sys.argv[1:],
                               'd:t:D:i:l:T',
                               ['density=',
                                'ntarget=',
                                'deadline=',
                                'graphid=',
                                'logfile=',
                                'timeout'])

    for opt, arg in options:
        if opt in ('-d', '--density'):
            den = arg
        elif opt in ('-t', '--target'):
            ntgts = arg
        elif opt in ('-D', '--deadline'):
            dead = arg
        elif opt in ('-i', '--graphid'):
            ix = arg
        elif opt in ('-l', '--logfile'):
            logfile = arg
        elif opt in ('-T', '--timeout'):
            timeout = True

    logging.basicConfig(filename=logfile,
                        filemode='a',
                        format='[%(asctime)s.%(msecs)3d] [%(levelname)-8s]'
                               ' --- %(message)s (%(name)s:%(lineno)s)',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    log = logging.getLogger(__name__)

    graph = io.load_graph(ntgts, dead, den, ix)

    log.debug("START computation for graph " + ntgts + " " + dead +
              " 0." + den + " " + ix)
    if timeout:
        with cr.time_limit(36000):
            result = cv.compute_values(graph, rm_dominated=True, enum=10)
    else:
        result = cv.compute_values(graph, rm_dominated=True, enum=10)

    io.save_results(ntgts, dead, den, ix, result)

    log.debug("END computation for graph " + ntgts + " " + dead +
              " 0." + den + " " + ix)


if __name__ == '__main__':
    main()
