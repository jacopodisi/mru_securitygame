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
    logfile = den = ntgts = dead = ix = poolname = apxtype = reldead = None
    enumtype = "1"
    enumit = "10"
    options, _ = getopt.getopt(str_opt,
                               'd:t:D:i:l:p:n:e:a:r:T',
                               ['density=',
                                'ntarget=',
                                'deadline=',
                                'graphid=',
                                'logfile=',
                                'poolname=',
                                'enumiter=',
                                'enumtype=',
                                'apxtype=',
                                'reldead=',
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
        elif opt in ('-a', '--apxtype'):
            apxtype = arg
        elif opt in ('-r', '--reldead'):
            reldead = arg
        elif opt in ('-T', '--timeout'):
            timeout = True

#           00    01     02     03     04     05      06        07      08       09        10
    return [den, ntgts, dead, reldead, ix, timeout, enumtype, enumit, apxtype, logfile, poolname]


def run(den, ntgts, dead, reldead, ix, timeout=False, enumtype=1,
        enumit=10, apxtype=None, logfile='script.log'):

    if logfile is None:
        logfile = 'script.log'

    logging.basicConfig(filename=logfile,
                        filemode='a',
                        format='[%(asctime)s.%(msecs)3d] [%(levelname)-8s]'
                               ' --- %(message)s (%(name)s:%(lineno)s)',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    log = logging.getLogger(__name__)

    graph = io.load_graph(ntgts, dead, den, ix, rel_dead=reldead)

    ntgts = str(ntgts)
    dead = str(dead)
    if reldead is not None:
        dead = str(reldead)
    den = str(den)
    ix = str(ix)

    log.debug("START computation for graph " + ntgts + " " + dead +
              " 0." + den + " " + ix)
    log.debug("options timeout=" + str(timeout) + " enumtype=" +
              str(enumtype) + " enumit=" + str(enumit) + " apx=" + str(apxtype))

    covset = None
    oldtimes = None
    if apxtype is None:
        for i in range(5):
            try:
                oldres = io.load_results(ntgts, dead, den, ix, enumtype=(i + 1), rel_dead=reldead)
            except IOError:
                continue
            covset = oldres[4]
            oldtimes = oldres[3]
            log.debug('Using covering set already computed')
            break

    if timeout:
        with cr.time_limit(36000):
            result = cv.compute_values(graph,
                                       rm_dom=True,
                                       enum=enumit,
                                       covset=covset,
                                       times=oldtimes,
                                       enumtype=enumtype,
                                       apxtype=apxtype)
    else:
        result = cv.compute_values(graph,
                                   rm_dom=True,
                                   enum=enumit,
                                   covset=covset,
                                   times=oldtimes,
                                   enumtype=enumtype,
                                   apxtype=apxtype)

    io.save_results(ntgts, dead, den, ix, result, enumtype=enumtype, enumit=enumit, apxtype=apxtype, rel_dead=reldead)

    log.debug("END computation for graph " + ntgts + " " + dead +
              " 0." + den + " " + ix)

    return 1


def main():
    path = os.path.dirname(os.path.realpath(__file__))
    options = read_opt(sys.argv[1:])

    # write in pidprocesses.txt the pid of the process
    with open(path + "/pidprocesses.txt", "a") as fin:
        fcntl.flock(fin, fcntl.LOCK_EX)
        if options[9] is not None:
            pidstr = options[9] + ' pid: ' + str(os.getpid())
        else:
            pidstr = 'pid: ' + str(os.getpid())
        fin.write(pidstr + '\n')
        fcntl.flock(fin, fcntl.LOCK_UN)

    if len(sys.argv[1:]) >= 8:
        # run the algorithm passing the option from terminal
        run(*options[:-1])
    else:
        # run the algorithm pulling the GRAPHS from a pool file
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
            pooloptions = read_opt(str_options)[:-2]
            run(*(pooloptions + [logfile]))


if __name__ == '__main__':
    main()
