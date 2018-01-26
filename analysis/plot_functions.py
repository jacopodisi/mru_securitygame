import pickle
import matplotlib.pyplot as plt
import numpy as np


def plot_meantimes(dead, den):
    timesfile = "aggregate_times_1.pickle"
    with open(timesfile, mode='r') as f:
        timestuple = pickle.load(f)

    deadix = timestuple[1]
    ntgtsix = timestuple[2]
    denix = timestuple[3]
    timesarr = timestuple[0]

    meantime = []
    ntgts = []
    for ix, li in enumerate(timesarr[deadix[dead], :, denix[den]]):
        if li is not None:
            ntgts.append(ntgtsix.keys()[ntgtsix.values().index(ix)])
            meantime.append(np.mean(li))
    plt.plot(ntgts, meantime)

    plt.xlabel('# of targets')
    plt.ylabel('mean computation time')

    plt.show()


def plot_maxres(dead, den):
    maxresfile = "aggregate_maxres_1.pickle"
    with open(maxresfile, mode='r') as f:
        maxrestuple = pickle.load(f)

    deadix = maxrestuple[1]
    ntgtsix = maxrestuple[2]
    denix = maxrestuple[3]
    maxresarr = maxrestuple[0]

    maxres = []
    ntgts = []
    for ix, li in enumerate(maxresarr[deadix[dead], :, denix[den]]):
        if li is not None:
            ntgts.append(ntgtsix.keys()[ntgtsix.values().index(ix)])
            maxres.append(np.mean(li))
    plt.plot(ntgts, maxres)

    plt.xlabel('# of targets')
    plt.ylabel('optimal num of resources')

    plt.show()


def plot_gamevalue(dead, den, ntgts, ix):
    gamevalsfile = "aggregate_gamevals_1.pickle"
    with open(gamevalsfile, mode='r') as f:
        gamevalstuple = pickle.load(f)

    deadix = gamevalstuple[1]
    ntgtsix = gamevalstuple[2]
    denix = gamevalstuple[3]
    gamevalsarr = gamevalstuple[0]
    vals = gamevalsarr[deadix[dead], ntgtsix[ntgts], denix[den]][ix]
    if vals is not None:
        val = sorted(vals.items())
        x, y = zip(*val)

        plt.plot(x, y)

        plt.xlabel('# of resources')
        plt.ylabel('game value')

        plt.show()

    else:
        print 'results not yet computed'
