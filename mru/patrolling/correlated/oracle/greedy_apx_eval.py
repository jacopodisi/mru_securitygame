from __future__ import division
import ilp_oracle as ilp
import greedy_oracle as greedy
from scipy.sparse import lil_matrix
from random import uniform
from random import randint
from random import random
from random import choice
import numpy as np
import csv
from time import time
import logging

#######################################################################################################################
# evaluate the apx ration between the greedy alg and the exact (ILP) version of the oracle
#######################################################################################################################


MAX_TARGETS = 15
MAX_PL = 5
# max number of routes for a single player
MAX_ROUTES = 3
MAX_ROUTE_LEN = 6

def get_random_attacker_strategy(n_target):
    """

    :param n_target:
    :return: a random strategy in the attacker's simplex
    """
    # generate a vector of n_actions - 1 random numbers in [0,1]
    v = [uniform(0,1) for i in range(0,n_target-1)]

    # sort v and add 0 at the beginning and 1 at the end [0 , ... , 1]
    v_sorted=[0]
    v_sorted.extend(sorted(v))
    v_sorted.extend([1])

    # compute the differences among consecutive elements of the array
    # the obtained vector is in the simplex
    strategy=[j-i for i, j in zip(v_sorted[:-1], v_sorted[1:])]

    return strategy

def apx_ratio_eval():
    """
    computes the apx ratio for a random instance
    if apx/opt >= 1/2 log the instance for further investigations
    :return: apx/opt ratio, time opt, time apx
    """
    print 'starting random eval'

    n_pl = randint(2, MAX_PL)
    n_target = randint(n_pl + 1, MAX_TARGETS)

    target_values = []
    for t in range(0,n_target):
        target_values.append(random())
    target_values = np.array(target_values)

    attacker_strategy = get_random_attacker_strategy(n_target)

    #I = get_random_covering_routes(n_pl, n_target)
    I = get_pathologic_covering_routes(n_pl, n_target, attacker_strategy, target_values)

    start_opt = time()
    br_opt = ilp.generate_row(I, attacker_strategy, target_values)
    opt_time = time() - start_opt

    start_apx = time()
    br_apx = greedy.generate_row(I, attacker_strategy, target_values)
    apx_time = time() - start_apx

    print 'opt time: ', opt_time, 'apx time: ', apx_time

    apx_val = get_value(br_apx, I, target_values, attacker_strategy)
    opt_val = get_value(br_opt, I, target_values, attacker_strategy)

    logging.info('ratio = %f - target = %d - pl = %f - max_r = %d - max_cov_t = %d',apx_val/opt_val, n_target, n_pl, MAX_ROUTES, MAX_ROUTE_LEN)

    return apx_val/opt_val, opt_time, apx_time


def get_value(br, I, target_values, attacker_strategy):
    """

    :param br: joint action in the form [(pl, route number), ...]
    :param I:
    :param target_values:
    :param attacker_strategy:
    :return: the value associated to the given br computed as:
        1 - sum[targets] ( sigma(t)*pi(t)*(1-y(t)) ) (see oracle formulation)
    """
    # compute the array of target coverage
    # not_covered[t] = 1 - y[t] = 1 iff t is NOT covered
    not_covered = np.ones((1, len(target_values)))[0]

    for route in br:

        pl = route[0]
        route_number = route[1]

        y = I[pl][route_number, :].nonzero()[1]

        for covered in y:
            not_covered[covered] = 0

    attacker_value = np.dot(
        np.multiply(target_values, not_covered), attacker_strategy
    )

    return 1 - attacker_value


def get_random_covering_routes(n_pl, n_target):
    I = {}
    for pl in range(1, n_pl+1):
        n_r = randint(1, MAX_ROUTES)

        temp = lil_matrix((n_r, n_target), dtype='int8')

        total_covered_targets = randint(1, n_r * n_target)

        for i in range(0, total_covered_targets):

            t = randint(0, n_target - 1)
            r = randint(0, n_r-1)

            temp[r,t] = 1

        I[pl] = temp.tocsr()

    return I

def get_pathologic_covering_routes(n_pl, n_target, attacker_strategy, target_values):
    """
    Builds an instance where a greedy choice is forced to be non optimal

    :param n_pl:
    :param n_target:
    :param attacker_strategy:
    :param target_values:
    :return: I <pl, csr matrix>
    """
    # computes the coefficient used by the greedy oracle to choose routes
    targets_coeff = np.transpose(np.multiply(attacker_strategy, target_values))

    # randomly selects the player for which the non optimal choice will be made
    wrong_pl = randint(1, n_pl)

    # generate the non optimal route randomly
    n_covered_targets = randint(n_pl,n_target-1)
    non_opt_action = np.zeros(n_target)
    for i in range(0, n_covered_targets):
        random_covered_target = randint(0, n_target-1)
        non_opt_action[random_covered_target] = 1

    # compute the value of the non optimal route
    non_opt_val = get_value_single_route(non_opt_action, targets_coeff)

    # generate routes that have, as a single, values smaller than the best greedy route but taken togher perform
    # at least as well. [[0,1,...],[...],...] a[r][t]=1 iff t is covered by r.
    # The returned list should have n_pl - 1 routes
    opt_routes = get_opt_routes(n_pl, non_opt_action)

    I={}
    for pl in range(1, n_pl+1):

        n_r = randint(0, MAX_ROUTES)
        temp = lil_matrix((n_r+1, n_target), dtype='int8')

        if pl == wrong_pl:
            # put the non opt route in the bucket
            for t in non_opt_action.nonzero():
                temp[0,t] = 1
        else:
            for t in opt_routes.pop().nonzero():
                temp[0,t] = 1

        # generate other random routes with single value less than the non_opt_value
        for r in range(1, n_r):
            new_route = get_r_limited_val(non_opt_val, targets_coeff)

            for t in new_route.nonzero():
                temp[r,t] = 1

        I[pl] = temp.tocsr()

    return I


def get_value_single_route(route, targets_coeff):
    """

    :param route: array, route[t]=1 iff t is covered by r, 0 otherwise
    :param target_values:
    :param attacker_strategy:
    :return: the value associated to given the route by the greedy oracle
    """
    return np.dot(route, targets_coeff)

def split_list(alist, wanted_parts=1):
    """

    :param alist:
    :param wanted_parts:
    :return: the specified list splitted in wanted_parts parts
    """
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
             for i in range(wanted_parts) ]

def get_opt_routes(n_pl, non_opt_action):
    """

    :param n_pl:
    :param non_opt_action:
    :param non_opt_val:
    :param targets_coeff:
    :return: a list of routes that together guarante the same coverage of the non_opt route
    """
    cov_targets = non_opt_action.nonzero()[0]

    remaining_pl = n_pl - 1

    splitted_cov_targets = split_list(cov_targets.tolist(), wanted_parts=remaining_pl)

    opt_actions = []

    for covered_target_set in splitted_cov_targets:
        new_route = np.zeros(len(non_opt_action))

        for target in covered_target_set:
            new_route[target] = 1

        opt_actions.append(new_route)

    return opt_actions

def get_r_limited_val(non_opt_val, targets_coeff):
    """

    :param non_opt_val: value of the wrong action selected by the greedy oracle
    :param targets_coeff:
    :return: an array representing a route with a value less than non_opt_val
    """
    n_targets = len(targets_coeff)

    # find targets that, alone, have a value less than non_opt_val
    init_targets = []
    for t in range(0,n_targets):
        if targets_coeff[t] < non_opt_val:
            init_targets.append(t)

    # init the route with one of the feasible targets
    new_route = np.zeros(n_targets)
    if init_targets:
        new_route[choice(init_targets)] = 1

    last_selectet_t = -1
    new_t = 0 #added covered targets
    n_additional_t = randint(0, MAX_ROUTE_LEN) # random limit over the number of additional covered targets

    while get_value_single_route(new_route, targets_coeff) < non_opt_val and new_t < n_additional_t:
        last_selectet_t = randint(0, n_targets-1)
        new_route[last_selectet_t] = 1
        new_t += 1

    if last_selectet_t >= 0:
        new_route[last_selectet_t] = 0

    return new_route



if __name__ == '__main__':
    N_SAMPLE = 10000

    logging_path='./apx_log.log'

    logging.basicConfig(filename=logging_path, level=logging.INFO)

    csv_path = './apx_ratio_pathologic_new.csv'

    ratio_list = [['ratio', 'opt_time', 'apx_time']]

    for i in range(0,N_SAMPLE):
        res = apx_ratio_eval()
        ratio_list.append([res[0], res[1], res[2]])

    with open(csv_path, 'a') as f:
        writer = csv.writer(f)
        writer.writerows(ratio_list)








