import logging
import numpy as np

import ILP_solver as sc
from patrolling.correlated import correlated_row_gen as cr


log = logging.getLogger(__name__)


def enumfunction(enumtype=None, covset=None, maxnumres=None,
                 tgt_values=None, sigrec=None,
                 enum=None, short_set=None):
    """ function that given the a code (1, 2 or 3) return the corresponding
        function used to enumerate the solutions.
    Parameters
    ----------
    enumtype: type of algorithm used to iterate through different solutions
    covset: covering set of every node of the graph
    tgt_values: value of each target
    sigrec: instance of signal receiver
    short_set: shortest set of every node
    maxnumres: maximum number of resources (optional)
    enum: number of disposition to analyze (default 1)

    Return
    ------
    bestsol: best computed solution for the given number of resources
    num_iter: number of iterated solution

    NB
    --
    short_set must be the shortest set from each node to every node,
    not just the targets
    """
    def gurobi_pool(n_res=None):
        """ Compute correlated solution for defender with multi resources
        enumerating thorugh the different solution using
        poolSolution parameter of gurobi.
        """
        num_iter = 0
        tgts = tgt_values.nonzero()[0]
        res, _ = sc.set_cover_solver(short_set[:, tgts],
                                     k=n_res, nsol=enum)

        n_res = res.shape[1]

        if maxnumres is not None and n_res == maxnumres:
            return None, None

        sets_dict = {k + 1: covset[res[0, k]] for k in range(n_res)}
        tempcorrsol = cr.correlated(sets_dict, tgt_values)
        bestsol = (tempcorrsol[0:2] + (res[0],))
        num_iter += 1

        log.debug("compute solution for different dispositions of " +
                  str(n_res) + " resources")
        for sol in range(1, res.shape[0]):
            if sigrec.kill_now:
                return bestsol, num_iter
            if sigrec.jump:
                break
            sets_dict = {k + 1: covset[res[sol, k]]
                         for k in range(n_res)}
            solution = cr.correlated(sets_dict, tgt_values)
            if bestsol[0] < solution[0]:
                bestsol = (solution[0],
                           solution[1],
                           res[sol])
            num_iter += 1
        return bestsol, num_iter

    def double_oracle(n_res=None):
        """ Compute correlated solution for defender with multi resources,
        enumerating through different placements using the double oracle.
        """
        num_iter = 0
        tgts = tgt_values.nonzero()[0]
        res, _ = sc.set_cover_solver(short_set[:, tgts], k=n_res)

        n_res = res.shape[1]

        if maxnumres is not None and n_res == maxnumres:
            return None, None

        placement_hist = res
        att_hist = np.zeros(short_set.shape[1], dtype=np.uint8)

        # compute correlated solution with initial placement
        sets_dict = {k + 1: covset[res[0, k]] for k in range(n_res)}
        tempcorrsol = cr.correlated(sets_dict, tgt_values)
        att_strat = np.array(tempcorrsol[3])
        bestsol = (tempcorrsol[0:2] + (placement_hist[-1],))
        num_iter += 1

        # update placement history and list of placements to analyze
        new_placements = att_strat.nonzero()[0]
        att_hist[new_placements] = 1

        log.debug("compute solution for different dispositions of " +
                  str(n_res) + " resources")

        while True:
            if sigrec.kill_now:
                return bestsol, num_iter
            if sigrec.jump or num_iter == enum:
                break
            # choose a random attacked node
            r = np.random.randint(len(new_placements))
            p = new_placements[r]
            # remove the chose node from the list
            new_placements = np.delete(new_placements, [r])
            # try to solve the set cover with a placed resource
            p_res, isok = sc.set_cover_solver(short_set[:, tgts],
                                              k=n_res, place=p)
            # check if a cover exist or if it is not already visited
            if isok and not np.any(np.all(placement_hist == p_res[0], axis=1)):
                # solve the game with the computed resources
                temp_dict = {k + 1: covset[p_res[0, k]] for k in range(n_res)}
                tempcorrsol = cr.correlated(temp_dict, tgt_values)
                # update placement to history
                placement_hist = np.vstack((placement_hist, p_res))
                # update the best solution
                if tempcorrsol[0] >= bestsol[0]:
                    bestsol = (tempcorrsol[0:2] + (placement_hist[-1],))
                    att_strat = np.array(tempcorrsol[3])
                num_iter += 1

            # last cycle
            if new_placements.size == 0:
                # update the list of attacked node with the ones
                # in the best solution. When the algorithm end,
                # the list 'new_placements' will be empty, and the
                # cycle will not start (every attacked node will be present
                # in history.
                att_strat[att_hist == 1] = 0
                new_placements = att_strat.nonzero()[0]
                att_hist[new_placements] = 1

            if new_placements.size == 0:
                break

        return bestsol, num_iter

    if (enumtype is None or
            covset is None or
            tgt_values is None or
            sigrec is None or
            short_set is None):
        raise ValueError('Some parameters are not defined')

    enumtype = int(enumtype)

    if enumtype == 1:
        return gurobi_pool
    elif enumtype == 2 and enum is not None:
        return double_oracle
    else:
        raise ValueError('Enumeration type ' + str(enumtype) +
                         ', wrongly defined')
