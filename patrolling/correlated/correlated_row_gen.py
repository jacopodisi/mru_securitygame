from __future__ import with_statement

import logging
import pickle
import signal
import sys
from contextlib import contextmanager
from random import randint
from time import time

from scipy.sparse import lil_matrix
from scipy.sparse import vstack

import LP_2pl_solver
from oracle import ilp_oracle

##################################################################################################
# Computes the full correlation equilibrium in the patrolling setting
#   Row generation approach is implemented to avoid enumerating on all the possible joint strategies
##################################################################################################

# threshold on the min. improvement to decide when to terminate row generation
EPS=0.0000
TIME_LIMIT=3600

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
    from, seconds to string hh:mm:ss.sss
    :param t: seconds
    :return:
    """
    return "%d:%02d:%02d.%03d" % \
        reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
            [(t*1000,),1000,60,60])

class TimeoutException(Exception): pass

def correlated(I, target_values):
    """
    Computes the full correlation equilibrium for the specified patrolling instance
    Parameters
    ----------
    I: dictionary of type {"vertex_number1": csr_matrix1,
                           "vertex_number2": csr_matrix2, ...}
       csr_matrix represent the covering sets of the vertex
    target_values: value of the targets
    
    Return
    ------
    value of the game, strategy of the team list of tuples ([(pl, route number), ...] , probability)
        (only joint strategies played with prob>0 are listed), number of iterations
    """
    # coverage matrix of selected joint routes
    I_joint=lil_matrix((0,len(target_values)),dtype='int8')

    # dict to store the structure of the selected joint routes
    # <joint route id, [(pl1,route number), ...]
    # the joint route id is the corresponding row number in I_joint
    # the route number is the identifier of the single-player route of player pl
    selected_routes={}

    # value of the game at the previous iteration, used to compute the terminating condition
    old_game_value= - 100

    # init with a randomly drawn joint route
    random_joint_route= pick_random_joint_route(I)
    I_joint=update_joint_I(I_joint, selected_routes, [random_joint_route], I)

    n_iter=0

    while True:

        n_iter+=1

        # minmax to determine attacker's strategy
        attacker_tupla=LP_2pl_solver.minmax(I_joint, target_values)

        delta=abs(attacker_tupla[0] - old_game_value)

        logging.info('partial - eps = %f - n iter = %d - team value = %f',EPS,n_iter,attacker_tupla[0])

        if delta > EPS:
            # compute the best response to the latest attacker's strategy
            br= ilp_oracle.generate_row(I, attacker_tupla[1], target_values)

            I_joint = update_joint_I(I_joint, selected_routes, [br], I)

            old_game_value=attacker_tupla[0]

        else:
            break

    # once the set of actions has been determined, compute the Defender correlated strategy on joint actions
    defender_final=LP_2pl_solver.maxmin(I_joint,target_values)

    # to show in a clear way the strategy profile it builds a list of the joint strategies of the support
    # (played with probability>=0)
    # the format is [ ( [(pl1, route number), ... ] , probability) , ...]
    prob_array=defender_final[1]
    strategy_profile=[]
    for joint_route_id in range(0,len(prob_array)):
        prob=prob_array[joint_route_id]
        if prob > 0:
            strategy_profile.append((selected_routes[joint_route_id], prob_array[joint_route_id]))

    return defender_final[0], strategy_profile, n_iter


def update_joint_I(I_joint, selected_routes, new_joint_routes_list, I):
    """
    update the coverage matrix of the selected joint strategies and the selected joints routes set
    :param I_joint: current lil coverage matrix
    :param selected_routes: dict of selected joint covering routes
        <joint route id, [(pl,route),...]> the joint route id is the row number in I_joint
    :param new_joint_routes_list: list of new joint routes to be added:
        [[(pl1,route_number),...],[(pl2,route_number),...)...]
    :param I: full sparse coverage matrix (csr_matrix)
    :return: updated I_joint
    """
    n_targets=I[1].shape[1]

    for new_joint_route in new_joint_routes_list:
        # row vectors with the coverage of the single-player route for each player
        # <pl,csr_matrix 1 x n_targets>
        row_vectors={}
        for single_pl_route in new_joint_route:
            pl=single_pl_route[0]
            row_vectors[pl]=I[pl][single_pl_route[1],:]

        covered_targets=set()
        for pl in row_vectors.keys():
            non_zero_indexes=row_vectors[pl].nonzero()[1]
            for i in non_zero_indexes:
                covered_targets.add(i)


        joint_vector=lil_matrix((1,n_targets),dtype='int8')

        for t in covered_targets:
            joint_vector[0,t]=1

        # add the new joint route at the bottom of the joint coverage matrix
        if I_joint.shape[0]>0:
            I_joint=vstack([I_joint,joint_vector],format='lil')
        else:
            I_joint=joint_vector.tolil()

        # update selected routes
        joint_route_id=I_joint.shape[0]-1
        selected_routes[joint_route_id]=new_joint_route

        return I_joint

def pick_random_joint_route(I):
    """

    :param I: <pl, csr matrix I>
    :return: random joint route in the form [(pl,route number)...]
    """
    random_joint_strategy=[]
    for pl in I.keys():
        route_number=randint(0,I[pl].shape[0]-1)
        random_joint_strategy.append((pl,route_number))

    return random_joint_strategy


if __name__ == '__main__':
    # input from command line n_target, instance
    n_targets=sys.argv[1]
    instance=sys.argv[2]

    pickle_path='./pickle/ntargets_'+str(n_targets)+'/ntargets_'+str(n_targets)+'_instance_'+str(instance)+'.pickle'
    logging_path='./results/correlated/ntargets_'+str(n_targets)+'/correlated_ntargets_'+str(n_targets)+'_instance_'+str(instance)+'.log'

    logging.basicConfig(filename=logging_path, level=logging.INFO)

    start_time=time()

    try:
        with time_limit(TIME_LIMIT):
            res=correlated(pickle_path)

        logging.info('FINAL correlated - eps = %f - n iter = %d - team value = %f',EPS,res[2],res[0])

        end_time=time()
        logging.info('Total time: %s',secondsToStr(end_time-start_time))


    except TimeoutException:
        logging.warning('TIMEOUT reached')



