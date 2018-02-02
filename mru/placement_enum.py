import time
import numpy as np

import ILP_solver as sc
from patrolling.correlated import correlated_row_gen as cr


def enumfunction(enumtype=None, covset=None, maxnumres=None,
                 tgt_values=None, sigrec=None, log=None,
                 enum=None, short_set=None):
    """ function that given the a code (1, 2 or 3) return the corresponding
    function used to enumerate the solutions
    """
    def gurobi_pool(n_res=None):
        """ Compute correlated solution for defender with multi resources
        enumerating thorugh the different solution using
        poolSolution parameter of gurobi.
        """
        tgts = tgt_values.nonzero()[0]
        st_time_set = time.time()
        res, _ = sc.set_cover_solver(short_set[:, tgts],
                                     k=n_res, nsol=enum)
        set_cov_time = time.time() - st_time_set

        n_res = res.shape[1]

        if maxnumres is not None and n_res == maxnumres:
            return None, set_cov_time, None

        sets_dict = {k + 1: covset[res[0, k]] for k in range(n_res)}
        st_time_corr = time.time()
        tempcorrsol = cr.correlated(sets_dict, tgt_values)
        comptime = time.time() - st_time_corr
        corrsol = (tempcorrsol[0:2] +
                   (res[0],))

        if not sigrec.jump:
            log.debug("compute solution for different dispositions of " +
                      str(n_res) + " resources")
            for sol in range(1, res.shape[0]):
                if sigrec.kill_now:
                    return corrsol, set_cov_time, comptime
                if not sigrec.jump:
                    sets_dict = {k + 1: covset[res[sol, k]]
                                 for k in range(n_res)}
                    solution = cr.correlated(sets_dict, tgt_values)
                    if corrsol[0] < solution[0]:
                        corrsol = (solution[0],
                                   solution[1],
                                   res[sol])
        return corrsol, set_cov_time, comptime

    def double_oracle(resources):
        """ Compute correlated solution for defender with multi resources,
        enumerating through different placements using the double oracle.
        """
        n_res = resources.shape[1]
        resources = resources[0].reshape((1, n_res))
        placement_hist = resources
        att_hist = np.zeros(short_set.shape[1], dtype=np.uint8)

        # compute correlated solution with initial placement
        sets_dict = {k + 1: covset[resources[0, k]]
                     for k in range(n_res)}
        st_time = time.time()
        tempcorrsol = cr.correlated(sets_dict, tgt_values)
        comptime = time.time() - st_time
        att_strat = np.array(tempcorrsol[3])
        corrsol = (tempcorrsol[0:2] + (placement_hist[-1],))

        # remove already visited placements
        att_strat[att_hist] = 0
        new_placements = att_strat.nonzero()[0]
        att_hist[new_placements] = 1
        len_place = len(new_placements)

        for i in range(len_place):
            if sigrec.jump:
                break
            # choose a random attacked node
            r = np.random.randint(len(new_placements))
            p = new_placements[r]
            # remove the chose node from the list
            new_placements = np.delete(new_placements, [r])
            # try to solve the set cover with a placed resource
            p_res, isok = sc.set_cover_solver(short_set, k=n_res, place=p)
            # check if a cover exist or if it is not already visited
            if isok and not np.any(placement_hist == p_res):
                # solve the game with the computed resources
                temp_dict = {k + 1: covset[p_res[0, k]] for k in range(n_res)}
                tempcorrsol = cr.correlated(temp_dict, tgt_values)
                # add the analyzed placement to history
                placement_hist = np.vstack((placement_hist, p_res))

                if tempcorrsol[0] > corrsol[0]:
                    corrsol = (tempcorrsol[0:2] + (placement_hist[-1],))
                    new_att_strat = np.array(tempcorrsol[3])

            # last cycle
            if i == len_place - 1:
                # update the list of attacked node with the ones
                # in the best solution. When the algorithm end,
                # the list 'new_placements' will be empty, and the
                # cycle will not start.
                new_att_strat[att_hist] = 0
                new_placements = new_att_strat.nonzero()[0]
                att_hist[new_placements] = 1
                len_place = len(new_placements)
                i = 0

        return corrsol, comptime

    if (enumtype is None or
            covset is None or
            tgt_values is None or
            sigrec is None or
            log is None or
            short_set is None):
        raise ValueError('some parameters are not defined')

    if enumtype == 1:
        return gurobi_pool
    elif (enumtype == 2 and
          enum is not None and
          short_set is not None):
        return double_oracle
    else:
        raise ValueError('Enumeration type wrongly defined')
