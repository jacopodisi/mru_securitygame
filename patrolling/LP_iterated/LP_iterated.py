import maxmin
from random import uniform
from numpy import array
from scipy.sparse import csc_matrix

def LP_iterated(I,V,eps):
    """
    LP iterated alg. starting from a random point on the simplex

    :param I: dict <pl,csc_matrix (routes x targets)>
    :param V: ordered array with target values
    :param eps: delta to terminate alg.
    :return: game value for the TEAM
    """
    # draw a random initial strategy from the simplex of each pl.
    P = init_strategies(I)

    old_game_value=-1
    delta = 100

    iter = 0

    while delta > eps:

        iter += 1

        # best result in the current iteration (value,player,strategy)
        current_best = [ -1, -1, {}]

        for free_pl in I.keys():

            # compute the coefficients' vector (one for each target) from the fixed strategies
            coeff_v = compute_coefficients(free_pl, I, P)

            res = maxmin.maxmin( I[free_pl], coeff_v, V)

            if res[0] > current_best[0]:
                # value, pl, strategy
                current_best=[res[0], free_pl, res[1]]

        delta = current_best[0] - old_game_value
        old_game_value = current_best[0]

        # update the strategy profile
        P[current_best[1]] = current_best[2]

    return current_best[0], iter


def init_strategies(I):
    """
    Perform random sampling from each team player's simplex
    Returns the intial strategies

    :param I: dict<pl,csc_matrix>
    :return: dict<pl,strategy array>
    """
    strategies={}

    for pl in I.keys():

        # generate a vector of n_actions - 1 random numbers in [0,1]
        n_actions=I[pl].shape[0]
        v=[uniform(0,1) for i in range(0,n_actions-1)]

        # sort v and add 0 at the beginning and 1 at the end [0 , ... , 1]
        v_sorted=[0]
        v_sorted.extend(sorted(v))
        v_sorted.extend([1])

        # compute the differences among consecutive elements of the array
        # the obtained vector is in the simplex
        strategy=[j-i for i, j in zip(v_sorted[:-1], v_sorted[1:])]

        strategies[pl]=array(strategy)

    return strategies


def compute_coefficients(free_pl, I, P):
    """
    Compute the coefficients' vector concerning fixed strategy players

    :param free_pl: the free player
    :param I: dict<pl,csc_matrix>
    :param P: dict <pl,strategy profile vector (position i -> prob. of playing action i)>
    :return: vector of fixed strategy coefficients (position i -> coeff. for target i+1)
    """
    fixed_players = set(I.keys())
    fixed_players.discard(free_pl)
    n_targets=I[1].shape[1]

    final_vect=[]

    for t in range(0,n_targets):
        coeff=1.0

        if fixed_players!=None:

            for pl in fixed_players:

                routes_vect=I[pl][:,t].transpose()

                coeff *= (1 - routes_vect.dot(P[pl])[0])

        final_vect.extend([coeff])

    return final_vect


