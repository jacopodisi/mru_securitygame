# Model for the exact solution of the maxmin problem in the patrolling setting
# The model employed leverages the specific structure of the problem and does not
#   need to use the complete utility matrix.

# set of team players
set P;
# set of targets
set T;
# set of covering routes for each patroller
set R {P};

# PARAMS
# matrix I: I[p,r,t]=1 iff p covers t by following route r, otherwise I[p,r,t]=0
param I{pl in P, R[pl], T} >= 0;
# values of each target
param V {T};

#VARIABLES
# value of the game for the attacker
var v;
# strategy profile for each team player
var s{pl in P, R[pl]} >= 0;


#OBJ
minimize obj: v;


#CONSTRAINTS
# strategy on the simplex
subject to simplex{pl in P}:
  sum{r in R[pl]} s[pl,r] = 1;
# constraint on the game value
subject to value_constraint{t in T}:
  v - V[t] * prod{pl in P}(1 - sum{r in R[pl]}( I[pl,r,t]*s[pl,r] )) >= 0;
