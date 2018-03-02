import logging
import collections
import numpy as np

from copy import deepcopy
from . import ILP_solver as sc
from .patrolling.correlated import correlated_row_gen as cr


log = logging.getLogger(__name__)


def enumfunction(enumtype=None, covset=None, maxnumres=None,
                 node_values=None, sigrec=None, short_path=None,
                 enum=1, short_set=None):
    """ Function that given the a code (1, 2 or 3) return the corresponding
        function used to enumerate the solutions.
    Parameters
    ----------
    enumtype: type of algorithm used to iterate through different solutions.
              1 --> gurobi enumeration
              2 --> double oracle (computing each time the set cover)
              3 --> double oracle v2 (using the neighborhood)
              4 --> local search + score(tgt_value)
              5 --> local_search + score(tgt_value, distance)
    covset: covering set of every node of the graph
    maxnumres: maximum number of resources (optional)
    node_values: value of each node, included non targets
    sigrec: instance of signal receiver
    short_path: shortest path cost matrix
    enum: number of solution to iterate to find the best one (optional)
    short_set: shortest set matrix covered targets. NB: the shortest set,
               from each node to every node, not just the targets.
               numpy matrix (|nodes|, |nodes|)

    Return
    ------
    bestsol: best computed solution for the given number of resources
    improves: improvement computed
    """

    def build_neigh(loc_res, nontgts, loc_node_sort=None):
        neigh = {}
        for i, r in enumerate(loc_res):
            # compute target to be covered
            others = np.delete(loc_res, i)
            if len(others) > 0:
                tocov = np.all(short_set[others] == 0, axis=0)
            else:
                tocov = np.full(short_set.shape[0], True)
            tocov[nontgts] = False

            # compute neighbors
            temp_neigh = np.all(short_set[:, tocov] >= 1, axis=1)
            temp_neigh[loc_res] = False
            temp_neigh = temp_neigh.nonzero()[0]

            # order neighbors based on loc_node_sort
            if len(temp_neigh) > 0:
                if loc_node_sort is not None:
                    sortneigh = np.in1d(loc_node_sort, temp_neigh,
                                        assume_unique=True)
                    temp_neigh = loc_node_sort[sortneigh.nonzero()[0]]
                neigh[r] = collections.deque(temp_neigh)
        return neigh

    def gurobi_pool(n_res=None):
        """ Compute correlated solution for defender with multi resources
        enumerating thorugh the different solution using
        poolSolution parameter of gurobi.
        """
        tgts = node_values.nonzero()[0]
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
            solution = cr.correlated(sets_dict, node_values)
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
        tgts = node_values.nonzero()[0]

        if n_res is None:
            n_res_str = 'minimum'
        else:
            n_res_str = str(n_res)
        log.debug("compute solution for different dispositions of " +
                  n_res_str + " resources")

        while len(improves) < enum:

            if (sigrec.kill_now or sigrec.jump or
                    (len(placements) == 0)):
                break

            p = placements.pop()

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
            solution = cr.correlated(res_dict, node_values)
            improves.append((solution[0:2] + (placement_hist[-1],)))

            if solution[0] > bestsol[0]:
                bestsol = deepcopy((solution[0:2] + (placement_hist[-1],)))
                att_strat = np.array(solution[3])
                att_strat[att_hist == 1] = 0
                count_nz = np.count_nonzero(att_strat)
                new_placements = np.argsort(-att_strat)[:count_nz]
                att_hist[new_placements] = 1
                placements.extend(new_placements[::-1])

        return bestsol, improves

    def double_oracle_v2(n_res=None):
        """ Compute correlated solution for defender with multi resources,
        enumerating through different placements using the double oracle.
        """

        improves = []
        placements = collections.deque([None])
        placement_hist = None
        bestsol = (0,)
        tgts = node_values.nonzero()[0]
        notgts = (node_values <= 0).nonzero()[0]

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
        solution = cr.correlated(res_dict, node_values)
        improves.append((solution[0:2] + (placement_hist[-1],)))
        bestsol = deepcopy((solution[0:2] + (placement_hist[-1],)))

        att_strat = np.array(solution[3])
        count_nz = np.count_nonzero(att_strat)
        new_placements = np.argsort(-att_strat)[:count_nz]
        placements = collections.deque(new_placements[::-1])
        better = True

        while len(improves) < enum:

            if (sigrec.kill_now or sigrec.jump or
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
                        tocov = np.full(node_values.shape[0], True)
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
            solution = cr.correlated(res_dict, node_values)
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
        """ Compute correlated solution for defender with multi resources,
        enumerating through different placements using the local search.
        """

        def swap_min(resources, loc_neigh, score, tabu, better=False):
            if len(loc_neigh) == 0:
                return resources, None, None
            sw_res = deepcopy(resources)
            keys = np.array(loc_neigh.keys())
            notabu = np.logical_not(np.in1d(keys, tabu))
            if not np.any(notabu):
                notabu[:] = True
            oldpl = min(keys[notabu], key=lambda x: score[x])
            newpl = loc_neigh[oldpl].pop()
            if len(loc_neigh[oldpl]) == 0:
                del loc_neigh[oldpl]
            if better:
                if score[oldpl] >= score[newpl]:
                    if oldpl in loc_neigh.keys():
                        del(loc_neigh[oldpl])
                    return swap_min(resources, loc_neigh,
                                    score, tabu, better=True)
            tabu.append(oldpl)
            sw_res[sw_res == oldpl] = newpl
            return sw_res, oldpl, newpl

        tgts = node_values.nonzero()[0]
        notgts = (node_values <= 0).nonzero()[0]
        if n_res is None:
            n_res_str = 'minimum'
        else:
            n_res_str = str(n_res)
        log.debug("compute solution for different dispositions of " +
                  n_res_str + " resources")

        # compute score function
        score = node_values
        if enumtype == 5:
            short_path[short_set == 0] = -1
            score = short_path + 1.0
            for ix, sco in enumerate(score):
                score[ix] = [(1 / s) if (s > 0) else 0 for s in sco]
            score = np.sum(score * node_values, axis=1)
        node_sort = np.argsort(score)

        res, _ = sc.set_cover_solver(short_set[:, tgts],
                                     k=n_res)
        n_res = res.shape[1]
        if maxnumres is not None and n_res == maxnumres:
            return None, None

        place_tabu = collections.deque([])
        res = res[0]

        while True:
            neigh = build_neigh(res, notgts, node_sort)
            res, old, new = swap_min(res, neigh, score,
                                     place_tabu, better=True)
            if old is None:
                break

        sets_dict = {k + 1: covset[res[k]] for k in range(n_res)}
        solution = cr.correlated(sets_dict, node_values)[0:2]
        bestsol = deepcopy((solution[0], solution[1], res))
        improves = [deepcopy(bestsol)]

        placement_hist = np.empty((1, res.shape[0]))
        placement_hist[0] = res

        place_tabu = collections.deque([], maxlen=(n_res))

        while (len(improves) < enum):
            if (sigrec.kill_now or sigrec.jump):
                break
            new = False

            # build neighborhood
            neigh = build_neigh(res, notgts, node_sort)

            # explore neighborhood
            while len(neigh) > 0:
                if sigrec.kill_now or sigrec.jump or (len(improves) >= enum):
                    break

                # choose resources
                temp_res, oldpl, newpl = swap_min(res, neigh, score,
                                                  place_tabu)
                if np.any(np.all(placement_hist == temp_res, axis=1)):
                    continue
                placement_hist = np.vstack((placement_hist, temp_res))
                sets_dict = {k + 1: covset[temp_res[k]]
                             for k in range(n_res)}
                solution = cr.correlated(sets_dict, node_values)[0:2]
                improves.append(solution + (temp_res,))
                if solution[0] > bestsol[0]:
                    bestsol = deepcopy((solution[0], solution[1], temp_res))
                    res = temp_res
                    new = True
                    break

            if not new:
                break

        return bestsol, improves

    if (enumtype is None or
            covset is None or
            node_values is None or
            sigrec is None or
            short_set is None):
        raise ValueError('Missing some parameters')

    enumtype = int(enumtype)
    enum = int(enum)

    if enumtype == 1:
        return gurobi_pool
    elif enumtype == 2:
        return double_oracle
    elif enumtype == 3:
        return double_oracle_v2
    elif enumtype == 4:
        return local_search
    elif enumtype == 5:
        if short_path is None:
            raise ValueError('Missing short_path parmater')
        return local_search
    else:
        raise ValueError('Enumeration type ' + str(enumtype) +
                         ' does not exists')
