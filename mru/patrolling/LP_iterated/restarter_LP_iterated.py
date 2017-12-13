from __future__ import with_statement
from __future__ import division
import LP_iterated
import signal
from contextlib import contextmanager
import pickle
import sys
from time import time
import logging

###################################################################
# Use this to call the LP iterated.
# It reads the pickle file containing data and tries different number of
#   restarts for the basic LP iterated algorithm.
# It also performs logging of the solutions and sets the time limit on the
#   computation
###################################################################


# constants
EPS=0.01
TIME_LIMIT=3600
MAX_RESTART=150


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


def run_LP_iterated(ntargets, instance):

    res_path='./results/LP_iterated/ntargets_'+str(ntargets)+'/'
    log_path= res_path + 'LP_iterated_log_ntargets_'+str(ntargets)+'_instance_'+str(instance)+'.log'
    pickle_path='./pickle/ntargets_'+str(ntargets)+'/ntargets_'+str(ntargets)+'_instance_'+str(instance)+'.pickle'

    # read files
    with open(pickle_path,'rb') as pickle_file:
        I=pickle.load(pickle_file) # dict <pl, csc_matrix>
        target_values=pickle.load(pickle_file) # ordered array of targets' values


    logging.basicConfig(filename=log_path, level=logging.INFO)
    logging.info('LP iterated - eps = %s - ntargets = %s - instance = %s',
                 str(EPS),str(ntargets),str(instance))

    try:

        best_result_total= -1.0

        n_restart=1
        iter=0
        start_time=time()

        with time_limit(TIME_LIMIT):

            while(n_restart<=150):
                iter+=1

                best_result_partial=[-1.0,0]

                for iteration in range(0,n_restart):

                    res = LP_iterated.LP_iterated(I,target_values,EPS)

                    if (res[0]>best_result_partial[0]):
                        best_result_partial=[res[0], res[1]] # value, iter

                logging.info('LP iterated - n restart = %d - value = %f - iterations = %d',
                             n_restart, best_result_partial[0], best_result_partial[1])

                if (best_result_partial[0]>best_result_total):
                    best_result_total=best_result_partial[0]

                n_restart=iter*10


    except TimeoutException, msg:
        logging.warning('TIMEOUT reached')

    end_time=time()
    logging.info('Total time: %s',secondsToStr(end_time-start_time))

    logging.info('Best result overall = %f',best_result_total)


if __name__ == "__main__":
    run_LP_iterated(sys.argv[1],sys.argv[2])