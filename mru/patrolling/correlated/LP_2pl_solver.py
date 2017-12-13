from gurobipy import *
from numpy import array

##########################################################################
# Compute the minmax/maxmin solutions for a 2 pl. game in the patrolling setting.
# The defender plays as a single player(full coordination) over its joint strategies.
##########################################################################

def maxmin(I_joint, target_values):
    """
    Computes the value of the game and the DEFENDER's optimal strategy

    :param I_joint: lil_matrix joint routes (actions) x targets
        I_joint[r,t]=1 iff a team player covers t following one of the routes of the joint route r
    :param target_values: vector containing, in position i, the value of target i
    :return: the value of the game FOR THE TEAM, and its optimal DEFENSIVE strategy (over joint covering routes)
    """
    try:

        m = Model("maxmin")
        m.setParam('OutputFlag',False)

        # number of routes (actions) for the defender
        n_routes = I_joint.shape[0]
        # number of targets
        n_target = len(target_values)

        # VARIABLES
        # value of the game for the attacker
        v = m.addVar(name="v",lb=-1)
        # strategy profile for the defender
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
                v >= target_values[t] * (1 - quicksum(I_joint[r,t]*s[r] for r in range(0,n_routes))),
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
        print('Error while computing the maxmin value for the correlated alg.')
        print 'Gurobi Status after the optimization: ',m.getAttr(GRB.Attr.Status)

def minmax(I_joint, target_values):
    """
    Compute the value of the game (for the team) and the ATTACKER's optimal strategy

    :param I_joint: lil_matrix joint routes (actions) x targets
        I_joint[r,t]=1 iff a team player covers t following one of the routes of the joint route r
    :param target_values: vector containing, in position i, the value of target i
    :return: value of the game, attacker's optimal strategy profile
    """
    try:
        m = Model('minmax')
        m.setParam('OutputFlag',False)

        # number of routes (actions) for the defender
        n_routes = I_joint.shape[0]
        # number of targets
        n_target = len(target_values)

        # VARIABLES
        # value of the game for the attacker
        v = m.addVar(name='v',lb=-1)
        # strategy profile of the attacker
        s={}
        for t in range(0,n_target):
            s[t]=m.addVar(name=str(t), lb=0.0)

        m.update()

        #OBJ
        m.setObjective(v,GRB.MAXIMIZE)

        # CONSTRAINTS
        # upper bounds
        for r in range(0,n_routes):
            m.addConstr(
                v <= quicksum(
                    target_values[t]*(1-I_joint[r,t])*s[t] for t in range(0,n_target)
                ), 'upper_bound_route'+str(r)
            )

        # simplex
        m.addConstr(quicksum(s[t] for t in range(0,n_target))==1,
                    'simplex')

        m.optimize()

        game_value_attacker=m.getVarByName('v').x
        game_value_team=1-game_value_attacker

        att_strategy=[]
        for t in range(0,n_target):
            att_strategy.extend([m.getVarByName(str(t)).x])

        return game_value_team, array(att_strategy)

    except GurobiError:
        print('Error while computing the minmax value for the correlated alg.')
        print 'Gurobi Status after the optimization: ',m.getAttr(GRB.Attr.Status)




