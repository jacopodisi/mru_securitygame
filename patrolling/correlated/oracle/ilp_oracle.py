from gurobipy import *

#######################################################################################################################
# ILP formulation of the row-generation oracle.
#######################################################################################################################

def generate_row(I, attacker_strategy, target_values):
    """
    Computes the best response (on joint strategies) of the Defender to the given attacker's strategy profile.
    ILP problem.

    :param I: dict<pl,csr_matrix>
        the sparse matrix has dimension routes x targets
        csr_matrix[i,j] = 1 iff pl covers target j with route i
    :param attacker_strategy: array containing the current attacker's strategy profile
    :param target_values: array containing the value of each target (sorted in decreasing order)
    :return: a single joint strategy (BR of the Defender) in the form [(pl,route), (pl,route) ...]
    """
    try:
        m=Model('oracle')
        m.setParam('OutputFlag',False)

        n_routes={}
        for pl in I.keys():
            n_routes[pl]=I[pl].shape[0]
        n_target=len(target_values)

        # VARIABLES
        y={}
        for t in range(0,n_target):
            y[t]=m.addVar(
                vtype=GRB.BINARY, name='y'+str(t)
            )

        x={} # <pl,<route,variable>>
        for pl in I.keys():
            x[pl]={}
            for r in range(0,n_routes[pl]):
                x[pl][r]=m.addVar(
                    vtype=GRB.BINARY, name='x'+str(pl)+'_'+str(r)
                )

        m.update()

        # OBJECTIVE FUNCTION
        m.setObjective(
            1 - quicksum(
                attacker_strategy[t]*target_values[t]*(1-y[t]) for t in range(0,n_target)
            ), GRB.MAXIMIZE
        )

        # CONSTRAINTS

        # upper bound
        for t in range(0,n_target):
            m.addConstr(
                quicksum(quicksum( I[i][r,t]*x[i][r] for r in range(0,n_routes[i])) for i in I.keys()) >= y[t],
                'upper_bound_t'+str(t)
            )

        # simplex
        for pl in I.keys():
            m.addConstr(
                quicksum(x[pl][r] for r in range(0,n_routes[pl]))==1,
                'simplex_pl'+str(pl)
            )

        m.optimize()

        # build the list representing the BR (joint strategy) to be returned
        br=[]
        for pl in I.keys():
            for r in range(0,n_routes[pl]):
                x=m.getVarByName('x'+str(pl)+'_'+str(r)).x
                if x==1.0:
                    br.extend([(pl,r)])
                    # there will be one route selected for each player
                    break

        return br

    except GurobiError:
        print('Error while generating Defender BR with the Oracle')

