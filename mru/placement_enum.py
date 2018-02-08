import logging
import numpy as np

import ILP_solver as sc
from patrolling.correlated import correlated_row_gen as cr


log = logging.getLogger(__name__)


def enumfunction(enumtype=None, covset=None, maxnumres=None,
                 tgt_values=None, sigrec=None,
                 enum=1, short_set=None):
    """ Function that given the a code (1, 2 or 3) return the corresponding
        function used to enumerate the solutions.
    Parameters
    ----------
    enumtype: type of algorithm used to iterate through different solutions
    covset: covering set of every node of the graph
    tgt_values: value of each target
    sigrec: instance of signal receiver
    short_set: shortest set of every node
    maxnumres: maximum number of resources (optional)
    enum: number of solution to iterate to find the best one

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

        bestsol = -1, None, None

        log.debug("compute solution for different dispositions of " +
                  str(n_res) + " resources")

        for sol in range(0, res.shape[0]):
            sets_dict = {k + 1: covset[res[sol, k]]
                         for k in range(n_res)}
            solution = cr.correlated(sets_dict, tgt_values)
            if solution[0] > bestsol[0]:
                bestsol = (solution[0],
                           solution[1],
                           res[sol])
            num_iter += 1
            if sigrec.kill_now or sigrec.jump:
                break
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
        solution = cr.correlated(sets_dict, tgt_values)
        att_strat = np.array(solution[3])
        bestsol = (solution[0:2] + (placement_hist[-1],))
        num_iter += 1

        # update placement history and list of placements to analyze
        new_placements = att_strat.nonzero()[0]
        att_hist[new_placements] = 1

        log.debug("compute solution for different dispositions of " +
                  str(n_res) + " resources")

        while True:

            for _ in range(len(new_placements)):
                if (sigrec.kill_now or
                        sigrec.jump or
                        (num_iter >= enum)):
                    break
                # pop a random node from the attacked ones
                r = np.random.randint(len(new_placements))
                p = new_placements[r]
                new_placements = np.delete(new_placements, [r])
                # solve the set cover with a placed resource
                p_res, isok = sc.set_cover_solver(short_set[:, tgts],
                                                  k=n_res, place=p)
                if (not isok or
                        np.any(np.all(placement_hist == p_res[0], axis=1))):
                    continue
                placement_hist = np.vstack((placement_hist, p_res))
                res_dict = {k + 1: covset[p_res[0, k]] for k in range(n_res)}
                solution = cr.correlated(res_dict, tgt_values)
                num_iter += 1
                if solution[0] > bestsol[0]:
                    bestsol = (solution[0:2] + (placement_hist[-1],))
                    att_strat = np.array(solution[3])

            att_strat[att_hist == 1] = 0
            new_placements = att_strat.nonzero()[0]
            att_hist[new_placements] = 1

            if (sigrec.kill_now or
                    sigrec.jump or
                    (num_iter >= enum) or
                    new_placements.size == 0):
                break

        return bestsol, num_iter

    def local_search(n_res=None):
        num_iter = 0
        tgts = tgt_values.nonzero()[0]
        res, _ = sc.set_cover_solver(short_set[:, tgts],
                                     k=n_res, nsol=enum)

        n_res = res.shape[1]

        if maxnumres is not None and n_res == maxnumres:
            return None, None

        sets_dict = {k + 1: covset[res[0, k]]
                     for k in range(n_res)}

        res = res[0]
        solution = cr.correlated(sets_dict, tgt_values)[0:2]
        best_sol = (solution[0],
                    solution[1],
                    res)

        log.debug("compute solution for different dispositions of " +
                  str(n_res) + " resources")

        ss = short_set
        ss[:, tgts] = 1

        for _ in range(enum):
            neigh = {}
            for r in res:
                noncov = np.all(ss[np.delete(res, r)] == 0,
                                axis=0)
                neigh[r] = np.all(ss[:, noncov] == 1, axis=1)
                neigh[r][r] = False
                neigh[r] = list(neigh[r].nonzero()[0])
            while True:
                if len(neigh) == 0 or num_iter >= enum:
                    break
                oldix = np.random.choice(len(neigh))
                old = neigh.keys()[oldix]
                new = neigh[old].pop()
                if len(neigh[old]) == 0:
                    del neigh[old]
                temp_res = res
                temp_res[oldix] = new
                solution = cr.correlated(sets_dict, tgt_values)[0:2]
                if solution[0] > best_sol[0]:
                    best_sol = solution
                    best_res = temp_res
                    new = True
                num_iter += 1

            if num_iter >= enum or not new:
                break


    if (enumtype is None or
            covset is None or
            tgt_values is None or
            sigrec is None or
            short_set is None):
        raise ValueError('Some parameters are not defined')

    enumtype = int(enumtype)

    if enumtype == 1:
        return gurobi_pool
    elif enumtype == 2:
        return double_oracle
    else:
        raise ValueError('Enumeration type ' + str(enumtype) +
                         ', wrongly defined')
