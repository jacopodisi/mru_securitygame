"""Aggregate results and save them in  pickle files under 'analysis/'
Results are saved in 3D np.array.
First index indicate the deadline, second the #tgts, third the density.
Data is saved as lists and each i-th element correspond to the results
of the i-th graph
"""
from mru import iomanager as io
import os
import pickle
import numpy as np

maxdeadlist = [4, 5, 10, 15, 19]
nist = {20: 10, 25: 10, 30: 10, 35: 2, 40: 2, 45: 2, 50: 2}
ndead = {20: [4, 5, 10, 15, 19],
         25: [5, 10],
         30: [5, 10],
         35: [5, 10],
         40: [5, 10],
         45: [5, 10],
         50: [5, 10]}
nden = {25: [20, 25, 30, 35, 40, 45, 50],
        10: [20, 25, 30, 35, 40, 45, 50],
        8: [25, 30],
        6: [35, 40, 45, 50]}

ntgtsix = {d: ix for ix, d in enumerate(sorted(ndead.keys()))}
denix = {d: ix for ix, d in enumerate(sorted(nden.keys()))}
deadix = {d: ix for ix, d in enumerate(maxdeadlist)}

timesarr = np.empty((len(deadix), len(ntgtsix), len(denix)), dtype=object)
timesnoenarr = np.empty((len(deadix), len(ntgtsix), len(denix)), dtype=object)
maxresarr = np.empty((len(deadix), len(ntgtsix), len(denix)), dtype=object)
gamevalarr = np.empty((len(deadix), len(ntgtsix), len(denix)), dtype=object)


def it(den, tgts):
    for tgt in tgts:
        for dea in ndead[tgt]:
            temptimes = []
            temptimesnoen = []
            tempmaxres = []
            tempgameval = []
            for ist in range(nist[tgt]):
                if ((den == 25 and
                     tgt == 20 and
                     dea == 10 and
                     ist == 0) or
                    (den == 10 and
                     tgt == 30 and
                     dea == 10 and
                     ist == 0) or
                    (den == 8 and
                     tgt == 30 and
                     dea == 10 and
                     ist == 4)):
                    return
                try:
                    result = io.load_results(tgt, dea, den, ist)
                except IOError:
                    continue
                temptimes.append(result[3][6])
                temp = (result[3][0] + result[3][1] + result[3][2] +
                        result[3][3] + result[3][4] + sum(result[3][5]))
                temptimesnoen.append(temp)
                tempmaxres.append(max(result[0].keys()))
                tempgameval.append(result[0])
            timesarr[deadix[dea], ntgtsix[tgt], denix[den]] = temptimes
            timesnoenarr[deadix[dea], ntgtsix[tgt], denix[den]] = temptimesnoen
            maxresarr[deadix[dea], ntgtsix[tgt], denix[den]] = tempmaxres
            gamevalarr[deadix[dea], ntgtsix[tgt], denix[den]] = tempgameval
    return


for den, tgts in nden.iteritems():
    it(den, tgts)

timesarr = (timesarr, deadix, ntgtsix, denix)
timesnoenarr = (timesnoenarr, deadix, ntgtsix, denix)
maxresarr = (maxresarr, deadix, ntgtsix, denix)
gamevalarr = (gamevalarr, deadix, ntgtsix, denix)
# save computational times
fntime = "analysis/aggregate_times_"
fid = 0
while True:

    if not os.path.isfile(fntime + str(fid) + '.pickle'):
        fntime += str(fid) + '.pickle'
        with open(fntime, mode='wb') as f:
            pickle.dump(timesarr, f, protocol=pickle.HIGHEST_PROTOCOL)
        print 'Saved times in ' + fntime
        break
    fid += 1

# save computational times without enumeration
fntimenoen = "analysis/aggregate_timesnoen_"
fid = 0
while True:

    if not os.path.isfile(fntimenoen + str(fid) + '.pickle'):
        fntimenoen += str(fid) + '.pickle'
        with open(fntimenoen, mode='wb') as f:
            pickle.dump(timesnoenarr, f, protocol=pickle.HIGHEST_PROTOCOL)
        print 'Saved times in ' + fntimenoen
        break
    fid += 1

# save maximum resources
fnmax = "analysis/aggregate_maxres_"
fid = 0
while True:
    pass
    if not os.path.isfile(fnmax + str(fid) + '.pickle'):
        fnmax += str(fid) + '.pickle'
        with open(fnmax, mode='wb') as f:
            pickle.dump(maxresarr, f, protocol=pickle.HIGHEST_PROTOCOL)
        print 'Saved maxres in ' + fnmax
        break
    fid += 1

# save game values
fnval = "analysis/aggregate_gamevals_"
fid = 0
while True:
    pass
    if not os.path.isfile(fnval + str(fid) + '.pickle'):
        fnval += str(fid) + '.pickle'
        with open(fnval, mode='wb') as f:
            pickle.dump(gamevalarr, f, protocol=pickle.HIGHEST_PROTOCOL)
        print 'Saved gameval in ' + fnval
        break
    fid += 1
