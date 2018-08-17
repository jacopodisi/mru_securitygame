import numpy as np


def compute_apxcoveringsets(v0, sp, tgts, dead, type_permut):
    """ compute the approximate covering routes, from a specified vertex, for the
        given set of targets. The permutation of the tgts will be computed using the
        heuristic specified in "type_permut". The result will be a matrix where each
        row correspond to a covering set.
    Parameters
    ----------
    v0: starting node.
    sp: shortest path matrix, from each node to every other node (including
        non target ones).
    tgt: list of targets for which compute the covering sets.
    dead: list of deadlines of every nodes (including non target ones).
    type_permut: define which permutation is used during the computation:
                 0 --> decreasing distance from v0
                 1 --> increasing distance from v0
                 2 --> increasing deadline
                 3 --> increasing order of excess time (dead(t) - dist(v0, t))
                 others --> random order

    Return
    ------
    cov_matrix: numpy matrix of (n_sets x |nodes|) containing in each row a
                covering set for v0. If the set cover a target, the column corresponding
                to the target will be set to 1 for the current row.
    """

    def tgt_permutation():
        if type_permut == 0:
            temp_permut = np.argsort(-sp[v0])
        elif type_permut == 1:
            temp_permut = np.argsort(sp[v0])
        elif type_permut == 2:
            temp_permut = np.argsort(dead)
        elif type_permut == 3:
            temp_permut = np.argsort(dead - sp[v0])
        else:
            temp_permut = np.random.permutation(len(dead))

        temp_permut = temp_permut[np.in1d(temp_permut, tgts, assume_unique=True)]
        temp_permut = [p for p in temp_permut if sp[v0, p] <= dead[p]]

        return temp_permut

    R = {}
    L = {}

    permut = tgt_permutation()

    for x in range(len(permut)):
        for y in range(1, x + 2):
            if y == 1:
                lateness = sp[v0, permut[x]] - dead[permut[x]]
                if lateness <= 0:
                    R[(x, y)] = [v0, permut[x]]
                    L[(x, y)] = lateness

            else:
                Cr = {}
                Cl = {}
                for z in range(x):
                    if (z, y - 1) not in R:
                        continue
                    Cr[z] = R[(x, 1)] + R[(z, y - 1)][1:]
                    Cl[z] = max(L[(x, 1)],
                                L[(z, y - 1)] - sp[v0, permut[z]] +
                                sp[v0, permut[x]] + sp[permut[x], permut[z]])

                if len(Cl) > 0:
                    j = min(Cl.keys(), key=lambda i: Cl[i])
                    if Cl[j] <= 0:
                        R[(x, y)] = Cr[j]
                        L[(x, y)] = Cl[j]

    cov_matrix = np.zeros((len(R), sp.shape[0]), dtype=bool)
    for i, r in enumerate(R.values()):
        cov_matrix[i, r] = 1

    return cov_matrix
