import numpy as np
from scipy.sparse import lil_matrix

#####################################################################################################################
# Greedy row-generation oracle - it should guarantee an apx ratio of 1/2
#####################################################################################################################

def generate_row(I, attacker_strategy, target_values):
    """
    Computes the best response (on joint strategies) of the Defender to the given attacker's strategy profile usign the
    GREEDY APX algorithm for the row generation oracle

    :param I: dict<pl,csr_matrix>
        the sparse matrix has dimension routes x targets
        csr_matrix[i,j] = 1 iff pl covers target j with route i
    :param attacker_strategy: array containing the current attacker's strategy profile
    :param target_values: array containing the value of each target (sorted in decreasing order)
    :return: a single joint strategy (BR of the Defender) in the form [(pl,route), (pl,route) ...]
    """
    n_selected_routes = 0
    # the solution to be returned
    br = []
    # keep track of the last selection to remove routes of that player
    last_selected_route = []
    # array to keep track of the covered targets
    # covered_targets[t] = 0 iff t is already covered (no additional utility for covering it)
    covered_targets = np.ones((1,len(target_values)))[0]

    # this array is computed only once and it's used when evaluating routes' quality
    target_importance = np.transpose(np.multiply(attacker_strategy, target_values))

    n_players = len(I.keys())

    # STRUCTURED array of arrays [pl, route number, value]
    all_routes = init_arrays(I)

    while n_selected_routes < n_players:
        covered_targets = update_coverage(covered_targets, last_selected_route, I)

        all_routes = update_values(all_routes, covered_targets, last_selected_route, I, target_importance)

        all_routes = np.sort(all_routes, kind='heapsort', order='value')

        last_selected_route = all_routes[-1]
        br.append((last_selected_route[0], last_selected_route[1]))

        n_selected_routes += 1

    return br


def init_arrays(I):
    """

    :param I:
    :return: return a structured array of type (player, route number, 0)
    the route number is the one corresponding to the csc matrix of the player
    """
    all_routes = []

    for pl in I.keys():
        for route in range(0,I[pl].shape[0]):

            all_routes.append((pl, route, 0.0))

    return np.array(all_routes, dtype=[('pl',int),('r',int),('value',float)])


def update_values(all_routes, covered_targets, last_selected_route, I, target_importance):
    """
    delete routes of the last selected player
    update the route values according to the already covered targets

    :param all_routes:
    :param covered_targets:
    :param last_selected_route:
    :param I:
    :param target_importance: array containing the values used to evaluate routes
        greedy_metric[t] = sigma_attacker[t] * target_value[t]
    :return: updated structured array of the remaining routes
    """
    if not last_selected_route:
        pl_to_be_deleted = -1
    else:
        pl_to_be_deleted = last_selected_route[0]

    # set of indexes of routes that will have to be deleted
    to_be_deleted = []

    for i in range(0,len(all_routes)):

        pl = all_routes[i][0]

        if pl == pl_to_be_deleted:
            to_be_deleted.append(i)
        else:
            r = all_routes[i][1]

            # covered targets not already covered by any other route
            useful_targets = I[pl][r,:].multiply(covered_targets)

            new_value = useful_targets.dot(target_importance)[0]

            all_routes[i] = (pl, r, new_value)

    all_routes = np.delete(all_routes, to_be_deleted)

    return all_routes


def update_coverage(covered_targets, last_selected_route, I):
    """

    :param covered_targets: array to keep track of the already covered targets
        covered_target[t] = 0 iff t is already covered (no additional utility for covering it)
    :param last_selected_route:
    :param I:
    :return: the updated array of covered targets after the selection of the last route
    """
    if last_selected_route:
        pl = last_selected_route[0]
        r = last_selected_route[1]

        new_covered_targets = I[pl][r,:].nonzero()[1]

        for t in new_covered_targets:

            if covered_targets[t] == 1:
                covered_targets[t] = 0

    return covered_targets












