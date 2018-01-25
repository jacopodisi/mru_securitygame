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
import fcntl
import os

from mru import computevalue as cv
from mru import iomanager as io
from mru.patrolling.correlated import correlated_row_gen as cr


def read_opt(str_opt):
    timeout = False
    logfile = den = ntgts = dead = ix = poolname = None
    options, _ = getopt.getopt(str_opt,
                               'd:t:D:i:l:p:T',
                               ['density=',
                                'ntarget=',
                                'deadline=',
                                'graphid=',
                                'logfile='
                                'poolname=',
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
        elif opt in ('-p', '--poolname'):
            poolname = arg
        elif opt in ('-T', '--timeout'):
            timeout = True

    return den, ntgts, dead, ix, timeout, logfile, poolname


def main(den, ntgts, dead, ix, timeout, logfile):

    if not (den and ntgts and dead and ix):
        print 'Value error: not defined every options of graph'
        return 0

    if logfile is None:
        logfile = 'script.log'

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

    # io.save_results(ntgts, dead, den, ix, result)

    log.debug("END computation for graph " + ntgts + " " + dead +
              " 0." + den + " " + ix)

    return 1


if __name__ == '__main__':
    print os.getpid()
    path = os.path.dirname(os.path.realpath(__file__))
    options = read_opt(sys.argv[1:])

    if len(sys.argv[1:]) >= 8:
        main(*options[:-1])
    else:
        poolname = options[-1] if options[-1] is not None else path +\
            '/pool.txt'
        logfile = options[-2]
        if not os.path.isfile(poolname):
            m = 'File {} do not exist'.format(poolname)
            raise IOError(m)
        while True:
            with open(poolname, "r") as fin:
                fcntl.flock(fin, fcntl.LOCK_EX)
                data = fin.readlines()
                if not data:
                    exit(1)
                str_options = data[0].split()
                with open(poolname, "w") as fout:
                    fout.writelines(data[1:])
                fcntl.flock(fin, fcntl.LOCK_UN)
            options = read_opt(str_options)[:-2]
            main(*(options + (logfile, )))
