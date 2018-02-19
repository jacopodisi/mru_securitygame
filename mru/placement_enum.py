import logging
import pdb
import random
import collections
import numpy as np

from copy import deepcopy
from . import ILP_solver as sc
from .patrolling.correlated import correlated_row_gen as cr


log = logging.getLogger(__name__)


def enumfunction(enumtype=None, covset=None, maxnumres=None,
                 tgt_values=None, sigrec=None, short_path=None,
                 enum=1, short_set=None, depthfirst=False,):
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
        tgts = tgt_values.nonzero()[0]
        res, _ = sc.set_cover_solver(short_set[:, tgts],
                                     k=n_res, nsol=enum)

        n_res = res.shape[1]

        if maxnumres is not None and n_res == maxnumres:
            return None, None

        bestsol = -1, None, None

        log.debug("compute solution for different dispositions of " +
                  str(n_res) + " resources")

        improves = []

        for sol in range(0, res.shape[0]):
            sets_dict = {k + 1: covset[res[sol, k]]
                         for k in range(n_res)}
            solution = cr.correlated(sets_dict, tgt_values)
            improves.append((solution[0],
                             solution[1],
                             res[sol]))
            if solution[0] > bestsol[0]:
                bestsol = (solution[0],
                           solution[1],
                           res[sol])
            if sigrec.kill_now or sigrec.jump:
                break
        return bestsol, improves

    def double_oracle(n_res=None):
        """ Compute correlated solution for defender with multi resources,
        enumerating through different placements using the double oracle.
        """

        improves = []
        placements = collections.deque([None])
        placement_hist = None
        att_hist = None
        bestsol = (0,)
        tgts = tgt_values.nonzero()[0]

        if n_res is None:
            n_res_str = 'minimum'
        else:
            n_res_str = str(n_res)
        log.debug("compute solution for different dispositions of " +
                  n_res_str + " resources")
        better = False

        while len(improves) < enum:

            if (sigrec.kill_now or
                    sigrec.jump or
                    (len(placements) == 0)):
                break

            if depthfirst:
                p = placements.pop()
            else:
                p = placements.popleft()

            p_res, isok = sc.set_cover_solver(short_set[:, tgts],
                                              k=n_res, place=p)
            ifvisited = np.all(placement_hist == p_res, axis=1)
            if (not isok or np.any(ifvisited)):
                continue
            if placement_hist is None:
                att_hist = np.zeros(short_set.shape[1], dtype=np.uint8)
                placement_hist = np.array(p_res)
                n_res = p_res.shape[1]
                if maxnumres is not None and n_res >= maxnumres:
                    return None, None
            else:
                placement_hist = np.vstack((placement_hist, p_res))

            res_dict = {k + 1: covset[p_res[0, k]] for k in range(n_res)}
            solution = cr.correlated(res_dict, tgt_values)
            improves.append((solution[0:2] + (placement_hist[-1],)))

            if solution[0] > bestsol[0]:
                bestsol = deepcopy((solution[0:2] + (placement_hist[-1],)))
                att_strat = np.array(solution[3])
                better = True

            if ((not depthfirst and len(placements) == 0) or
                    (depthfirst and better)):
                att_strat[att_hist == 1] = 0
                count_nz = np.count_nonzero(att_strat)
                new_placements = list(np.argsort(-att_strat)[:count_nz])
                att_hist[new_placements] = 1
                if depthfirst:
                    placements.extend(new_placements[::-1])
                else:
                    placements.extend(new_placements)

            better = False

        return bestsol, improves

    def double_oracle_v2(n_res=None):
        """ Compute correlated solution for defender with multi resources,
        enumerating through different placements using the double oracle.
        """

        improves = []
        placements = collections.deque([None])
        placement_hist = None
        bestsol = (0,)
        tgts = tgt_values.nonzero()[0]
        notgts = (tgt_values <= 0).nonzero()[0]

        if n_res is None:
            n_res_str = 'minimum'
        else:
            n_res_str = str(n_res)
        log.debug("compute solution for different dispositions of " +
                  n_res_str + " resources")

        res, isok = sc.set_cover_solver(short_set[:, tgts],
                                        k=n_res)
        n_res = res.shape[1]
        if maxnumres is not None and n_res >= maxnumres:
            return None, None

        placement_hist = np.array(res)
        res_dict = {k + 1: covset[res[0, k]] for k in range(n_res)}
        solution = cr.correlated(res_dict, tgt_values)
        improves.append((solution[0:2] + (placement_hist[-1],)))
        bestsol = deepcopy((solution[0:2] + (placement_hist[-1],)))

        att_strat = np.array(solution[3])
        count_nz = np.count_nonzero(att_strat)
        new_placements = list(np.argsort(-att_strat)[:count_nz])
        placements = collections.deque(new_placements[::-1])
        better = True

        while len(improves) < enum:

            if (sigrec.kill_now or
                    sigrec.jump or
                    (len(placements) == 0)):
                break

            p = placements.pop()
            # build neighborhood
            if better:
                neigh = {}
                for i, r in enumerate(bestsol[2]):
                    others = np.delete(bestsol[2], i)
                    if len(others) > 0:
                        tocov = np.all(short_set[others] == 0,
                                       axis=0)
                    else:
                        tocov = np.full(tgt_values.shape[0], True)
                    tocov[notgts] = False
                    temp_neigh = np.all(short_set[:, tocov] >= 1, axis=1)
                    temp_neigh[bestsol[2]] = False
                    if np.any(temp_neigh):
                        neigh[r] = temp_neigh
            better = False
            old = -1
            for o, ne in neigh.iteritems():
                if ne[p]:
                    old = o
                    break

            if old < 0:
                continue

            p_res = deepcopy(bestsol[2])
            p_res[p_res == old] = p

            ifvisited = np.all(placement_hist == p_res, axis=1)
            if (not isok or np.any(ifvisited)):
                continue
            placement_hist = np.vstack((placement_hist, p_res))

            res_dict = {k + 1: covset[p_res[k]] for k in range(n_res)}
            solution = cr.correlated(res_dict, tgt_values)
            improves.append((solution[0:2] + (placement_hist[-1],)))

            if solution[0] > bestsol[0]:
                bestsol = deepcopy((solution[0:2] + (placement_hist[-1],)))
                att_strat = np.array(solution[3])
                count_nz = np.count_nonzero(att_strat)
                new_placements = list(np.argsort(-att_strat)[:count_nz])
                placements = collections.deque(new_placements[::-1])
                better = True

        return bestsol, improves

    def local_search(n_res=None):

        tgts = tgt_values.nonzero()[0]
        notgts = (tgt_values <= 0).nonzero()[0]
        if n_res is None:
            n_res_str = 'minimum'
        else:
            n_res_str = str(n_res)
        log.debug("compute solution for different dispositions of " +
                  n_res_str + " resources")

        res, _ = sc.set_cover_solver(short_set[:, tgts],
                                     k=n_res)
        n_res = res.shape[1]
        if maxnumres is not None and n_res == maxnumres:
            return None, None
        sets_dict = {k + 1: covset[res[0, k]]
                     for k in range(n_res)}
        solution = cr.correlated(sets_dict, tgt_values)[0:2]
        bestsol = deepcopy((solution[0], solution[1], res[0]))
        improves = [deepcopy(bestsol)]

        placement_hist = np.array(res)

        while (len(improves) < enum):
            new = False

            # build neighborhood
            neigh = {}
            for i, r in enumerate(bestsol[2]):
                others = np.delete(bestsol[2], i)
                if len(others) > 0:
                    tocov = np.all(short_set[others] == 0,
                                   axis=0)
                else:
                    tocov = np.full(tgt_values.shape[0], True)
                tocov[notgts] = False

                temp_neigh = np.all(short_set[:, tocov] >= 1, axis=1)
                temp_neigh[bestsol[2]] = False
                nonz = temp_neigh.nonzero()[0]
                if len(nonz) > 0:
                    neigh[r] = collections.deque(nonz)

            # explore neighborhood
            res = deepcopy(bestsol[2])
            while len(neigh) > 0:
                if len(improves) >= enum:
                    break
                oldpl = random.choice(list(neigh.keys()))
                newpl = neigh[oldpl].pop()
                if len(neigh[oldpl]) == 0:
                    del neigh[oldpl]
                # swap resource
                temp_res = deepcopy(res)
                temp_res[temp_res == oldpl] = newpl
                if np.any(np.all(placement_hist == temp_res, axis=1)):
                    continue
                placement_hist = np.vstack((placement_hist, temp_res))
                sets_dict = {k + 1: covset[temp_res[k]]
                             for k in range(n_res)}
                solution = cr.correlated(sets_dict, tgt_values)[0:2]
                improves.append(solution + (temp_res,))
                if solution[0] > bestsol[0]:
                    bestsol = deepcopy((solution[0], solution[1], temp_res))
                    new = True
                    break

            if not new:
                break

        return bestsol, improves

    def local_search_v2(n_res=None):

        tgts = tgt_values.nonzero()[0]
        notgts = (tgt_values <= 0).nonzero()[0]
        if n_res is None:
            n_res_str = 'minimum'
        else:
            n_res_str = str(n_res)
        log.debug("compute solution for different dispositions of " +
                  n_res_str + " resources")

        # compute score function
        maxdl = np.max(short_path) + 1
        score = short_path - maxdl
        score[notgts] = 0
        score = np.absolute(score) * tgt_values
        score = np.sum(score, axis=1)

        node_sort = np.argsort(score)

        res, _ = sc.set_cover_solver(short_set[:, tgts],
                                     k=n_res)
        n_res = res.shape[1]
        if maxnumres is not None and n_res == maxnumres:
            return None, None
        sets_dict = {k + 1: covset[res[0, k]]
                     for k in range(n_res)}
        solution = cr.correlated(sets_dict, tgt_values)[0:2]
        bestsol = deepcopy((solution[0], solution[1], res[0]))
        improves = [deepcopy(bestsol)]

        placement_hist = np.array(res)

        while (len(improves) < enum):
            new = False

            # build neighborhood
            neigh = {}
            diffscore = {}
            for i, r in enumerate(bestsol[2]):
                others = np.delete(bestsol[2], i)
                if len(others) > 0:
                    tocov = np.all(short_set[others] == 0,
                                   axis=0)
                else:
                    tocov = np.full(tgt_values.shape[0], True)
                tocov[notgts] = False

                temp_neigh = np.all(short_set[:, tocov] >= 1, axis=1)
                temp_neigh[bestsol[2]] = False
                nonz = temp_neigh.nonzero()[0]
                if len(nonz) > 0:
                    nodeisin = np.isin(node_sort, nonz, assume_unique=True)
                    nonz = [(n, score[n]) for n in node_sort[nodeisin]]
                    neigh[r] = collections.deque(nonz)
                    diffscore[r] = nonz[-1][1] - score[r]

            # explore neighborhood
            res = deepcopy(bestsol[2])
            if n_res == 3:
                pdb.set_trace()
            while len(neigh) > 0:
                if len(improves) >= enum:
                    break

                # choose resources
                oldpl = max(diffscore.iterkeys(), key=diffscore.__getitem__)
                newpl = neigh[oldpl].pop()[0]
                if len(neigh[oldpl]) == 0:
                    del neigh[oldpl]
                    del diffscore[oldpl]
                else:
                    diffscore[oldpl] = neigh[oldpl][-1][1] - score[oldpl]

                # swap resource
                temp_res = deepcopy(res)
                temp_res[temp_res == oldpl] = newpl
                if np.any(np.all(placement_hist == temp_res, axis=1)):
                    continue
                placement_hist = np.vstack((placement_hist, temp_res))
                sets_dict = {k + 1: covset[temp_res[k]]
                             for k in range(n_res)}
                solution = cr.correlated(sets_dict, tgt_values)[0:2]
                improves.append(solution + (temp_res,))
                if solution[0] > bestsol[0]:
                    bestsol = deepcopy((solution[0], solution[1], temp_res))
                    new = True
                    break

            if not new:
                break

        return bestsol, improves

    if (enumtype is None or
            covset is None or
            tgt_values is None or
            sigrec is None or
            short_set is None):
        raise ValueError('Some parameters are not defined')

    enumtype = int(enumtype)
    enum = int(enum)

    if enumtype == 1:
        return gurobi_pool
    elif enumtype == 2:
        return double_oracle
    elif enumtype == 3:
        depthfirst = True
        return double_oracle
    elif enumtype == 4:
        return local_search
    elif enumtype == 5:
        return double_oracle_v2
    elif enumtype == 6:
        return local_search_v2
    else:
        raise ValueError('Enumeration type ' + str(enumtype) +
                         ', wrongly defined')
