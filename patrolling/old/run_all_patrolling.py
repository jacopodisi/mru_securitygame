from __future__ import with_statement
from __future__ import division
import signal
from contextlib import contextmanager
import sys
import csv
from time import time
import logging
import patrolling.mat_parser as parser

# need to import correlated and LP iterated scripts

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException, "Timed out"
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


def secondsToStr(t):
    """
    from seconds to string hh:mm:ss.sss
    :param t: seconds
    :return:
    """
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

def run_all(n_target,instance):
    """

    :param n_target:
    :param instance:
    :return:
    """
    # path to .mat file
    mat_path='./multidefender_instances'
    mat_path=mat_path + '/ntargets_' + n_target
    mat_path=mat_path + '/ntargets_' + n_target +\
             '_instance_' + instance + '.mat'

    output_path='./results/ntargets_' + n_target +\
                '/res_ntargets_' + n_target + '_instance_'+ instance + '.log'
    logging.basicConfig(filename=output_path, level=logging.INFO)

    max_execution_time=3600
    eps_lp_iterated=0.01

    try:
        # utility matrix of the team
         U_team=parser.parse_mat(mat_path)[0]
    except ValueError:
        logging.warning('The ndarry can not be initialized for %s targets instance %s',n_target,instance)

    # Correlated
    try:
        start_time=time()
        with time_limit(max_execution_time):
            res_correlated=correlated.correlatedMaxMin(U_team)

        elapsed=time() - start_time
        logging.info('correlated - time = %s',secondsToStr(elapsed))

    except TimeoutException, msg:
        logging.warning('correlated - TIMEOUT REACHED for %s targets instance %s',n_target,instance)


     # Iterated
    try:
        start_time=time()

        with time_limit(max_execution_time):
            res_iterated=iterated.non_correlated_iterated(U_team,eps_lp_iterated)

        elapsed=time() - start_time
        logging.info('iterated - time = %s',secondsToStr(elapsed))

    except TimeoutException, msg:
        logging.warning('iterated - TIMEOUT REACHED for %s targets instance %s',n_target,instance)




if __name__ == "__main__":
    # chiamare come python run_all.py $n_tartget $inst
    run_all(sys.argv[1],sys.argv[2])