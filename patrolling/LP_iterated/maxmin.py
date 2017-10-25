from gurobipy import *
from scipy.sparse import csc_matrix
from numpy import array


##########################################################################
# Computes the solution to a LINEAR programming problem for patrolling settings
##########################################################################

def maxmin(free_I, fixed_coeff_vect, target_values):
    """
    Computes the value of the game and the optimal strategy for the
    free player

    :param free_I: csc_matrix routes (actions) x targets
        free_I[r,t]=1 iff the free player covers t by following r
    :param fixed_coeff_vect: coefficient computed from the fixed strategy profiles
        of the other players
    :param target_values: vector containing, in position i, the value of target i
    :return: the value of the game FOR THE TEAM
    """
    try:

        m = Model("maxmin")

        # number of routes (actions) for the free player
        n_routes = free_I.shape[0]
        # number of targets
        n_target = len(target_values)

        # VARIABLES
        # value of the game for the attacker
        v = m.addVar(name="v",lb=-1)
        # strategy profile for the (free) team player
        s={}
        for r in range(0,n_routes):
            s[r]=m.addVar(lb=0.0, name=str(r))

        m.update()

        # OBJ
        m.setObjective(v,GRB.MINIMIZE)

        # CONSTRAINTS
        # value constraint
        for t in range(0,n_target):
            m.addConstr(
                v >= target_values[t] * (1 - quicksum(free_I[r,t]*s[r] for r in range(0,n_routes))) * fixed_coeff_vect[t],
                'value_constr_target'+str(t)
            )
        # simplex
        m.addConstr(quicksum(s[r] for r in range(0,n_routes))==1,
                    'simplex')

        m.optimize()

        # returns the value of the game and the strategy profile of the maximizer
        game_value_min=m.getVarByName("v").x # utility of the minimizer (attacker)
        game_value_team=1-game_value_min # constant (1) sum game

        # build the array containing the strategy of the maximizer
        strategy=[]
        for r in range(0,n_routes):
            strategy.extend([m.getVarByName(str(r)).x])

        return game_value_team , array(strategy)

    except GurobiError:
        print('Error while computing the maxmin value for the iterated LP alg.')
        print 'Gurobi Status after the optimization: ',m.getAttr(GRB.Attr.Status)