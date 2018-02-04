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
    enumtype = "1"
    enumit = "10"
    options, _ = getopt.getopt(str_opt,
                               'd:t:D:i:l:p:n:e:T',
                               ['density=',
                                'ntarget=',
                                'deadline=',
                                'graphid=',
                                'logfile=',
                                'poolname=',
                                'enumiter=',
                                'enumtype=',
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
        elif opt in ('-n', '--enumiter'):
            enumit = arg
        elif opt in ('-e', '--enumtype'):
            enumtype = arg
        elif opt in ('-T', '--timeout'):
            timeout = True

    return den, ntgts, dead, ix, timeout, logfile, enumtype, enumit, poolname


def main(den, ntgts, dead, ix, timeout, logfile, enumtype, enumit):

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
    log.debug("options timeout=" + str(timeout) + " enumtype=" + enumtype +
              " enumit=" + enumit)

    try:
        oldres = io.load_results(ntgts, dead, den, ix)
        if len(oldres) > 4:
            covset = oldres[4]
    except IOError:
        covset = None

    if timeout:
        with cr.time_limit(36000):
            result = cv.compute_values(graph,
                                       rm_dom=True,
                                       enum=enumit,
                                       covset=covset,
                                       enumtype=enumtype)
    else:
        result = cv.compute_values(graph,
                                   rm_dom=True,
                                   enum=enumit,
                                   covset=covset,
                                   enumtype=enumtype)

    io.save_results(ntgts, dead, den, ix, result, enumtype)

    log.debug("END computation for graph " + ntgts + " " + dead +
              " 0." + den + " " + ix)

    return 1


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    options = read_opt(sys.argv[1:])
    enumtp = options[6]
    enumit = options[7]

    # write in pidprocesses.txt the pid of the process
    with open(path + "/pidprocesses.txt", "a") as fin:
        fcntl.flock(fin, fcntl.LOCK_EX)
        if options[5] is not None:
            pidstr = options[5] + ' pid: ' + str(os.getpid())
        else:
            pidstr = 'pid: ' + str(os.getpid())
        fin.write(pidstr + '\n')
        fcntl.flock(fin, fcntl.LOCK_UN)

    if len(sys.argv[1:]) >= 8:
        # run the algorithm passing the option from terminal
        main(*options[:-1])
    else:
        # run the algorithm pulling the GRAPHS option and timeout option
        # from a pool file every other option is chose from terminal
        poolname = options[-1] if options[-1] is not None else path +\
            '/pool2.txt'
        logfile = options[5]
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
            options = read_opt(str_options)[:-3]
            main(*(options + (logfile, enumtp, enumit)))
