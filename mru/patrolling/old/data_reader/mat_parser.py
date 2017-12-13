import numpy as np
import scipy.io as scipyio
from itertools import product

##########################################################################################################
# Read from the .mat file the set of routes for each player located in 'M_routes'
# In the case of n team players and 1 attacker the Utility matrix will be represented with a numpy.ndarray
# as follows:
#   U[side, aAtt, a1, a2 ... aN] = u
#   side = 0 --> u is the team's payoff when players play aAtt, a1, a2...
#   side = 1 --> u is the attacker's payoff when players play aAtt, a1, a2 ...
#   NB: the attacker (minimizer) is the MOST EXTERNAL player
#
#   Payoffs are calculated as follows:
#       team: 1/2 if the target is covered, ( 1/2-value_target ) otherwise
#       minimizer: -1/2 if the target is covered, ( value_target - 1/2 ) otherwise
##########################################################################################################




def parse_mat(file_path):
    """
    builds the payoffs matrix from the patrolling .mat file

    :param file_path: path to the .mat file
    :return: numpy.ndarray representing the utility matrix as explained before
    """

    try:
        mat_dict = scipyio.loadmat(file_path, variable_names=['n_targets','M_routes','I'])

        n_pl_team = len(mat_dict['M_routes'])
        n_targets = mat_dict['n_targets'][0][0]
        target_values=mat_dict['I']['valuesVec'][0][0][0]


        # compute the shape of the ndarray
        # [2, n_a_att, n_a_1 ... n_a_N] (2: team or minimizer,
        #       n_a_att: number of actions of the attacker,
        #       n_a_I: number of actions of team player i)
        #
        # also compute a list of lists containing the available routes for each team player and they're
        #   corresponding action number in the matrix
        shape=[2]
        shape.append(n_targets) # number of actions of the attacker = number of targets
        all_routes=[]

        for pl in range(0,n_pl_team):
            a_list=mat_dict['M_routes'][pl][0]
            n_a=len(a_list)
            shape.append(n_a)

            single_pl_list=[]
            action_number = 0
            for route in a_list:
                single_pl_list.append((action_number, route[0][0]))
                action_number+=1

            all_routes.append(single_pl_list)

        # initialize the ndarray
        utility_matrix=np.zeros(shape)

        # for each joint strategy of the team compute the payoffs for each attacker's action (targets)
        joint_strategies_iterator=product(*all_routes)

        for joint_strategy in joint_strategies_iterator:

            # set of covered targets
            covered_targets=[]
            # cells' indexes of the utility matrix corresponding to the joint team strategy
            indexes=[]

            for strategy in joint_strategy:
                indexes.append(strategy[0])
                covered_targets.extend(strategy[1])

            covered_targets=set(covered_targets)
            indexes=tuple(indexes)


            for attacker_action in range(0,n_targets):

                cell=(attacker_action,) + indexes

                if (attacker_action in covered_targets):
                    # PROTECTED
                    utility_matrix[(0,)+cell]=0.5 # team
                    utility_matrix[(1,)+cell]= -0.5 # minimizer
                else:
                    # NOT PROTECTED
                    utility_matrix[(0,)+cell]= 0.5 - target_values[attacker_action] # team
                    utility_matrix[(1,)+cell]= target_values[attacker_action] - 0.5 # minimizer

        return utility_matrix

    except IOError:
        print ('Patrolling .mat file not found. Wrong path:')
        print (file_path)
