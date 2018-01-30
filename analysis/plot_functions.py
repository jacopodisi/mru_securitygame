import pickle
import matplotlib.pyplot as plt
import numpy as np


def plot_meantimes(dead, den, save=False):
    timesfile = "aggregate_times_0.pickle"
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

    ax = plt.gca()
    ax.grid(which='both')

    plt.xlabel('# of targets')
    plt.ylabel('mean computation time')

    if save:
        plt.savefig("figures/meantimes" + str(dead) + "_" + str(den) + ".svg")

    plt.show()


def plot_meantimesnoenum(dead, den, save=False):
    timesfile = "aggregate_timesnoen_0.pickle"
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
    ax = plt.gca()
    ax.grid(which='both')

    plt.xlabel('# of targets')
    plt.ylabel('computation time wihtout enumeration')

    if save:
        plt.savefig("figures/meantimesnoenum" + str(dead) + "_" + str(den) + ".svg")

    plt.show()


def plot_maxres(dead, den, save=False):
    maxresfile = "aggregate_maxres_0.pickle"
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
    ax = plt.gca()
    ax.grid(which='both')

    plt.xlabel('# of targets')
    plt.ylabel('optimal num of resources')

    if save:
        plt.savefig("figures/maxres" + str(dead) + "_" + str(den) + ".svg")

    plt.show()


def plot_gamevalue(dead, den, ntgts, ix, save=False):
    gamevalsfile = "aggregate_gamevals_0.pickle"
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
        ax = plt.gca()
        ax.grid(which='both')

        plt.xlabel('# of resources')
        plt.ylabel('game value')

        if save:
            plt.savefig("figures/utility" + str(dead) + "_" +
                        str(den) + "_" +
                        str(ntgts) + "_" +
                        str(ix) + ".svg")

        plt.show()

    else:
        print 'results not yet computed'


def plot_margin(dead, den, ntgts, ix, costres, save=False):
    gamevalsfile = "aggregate_gamevals_0.pickle"
    with open(gamevalsfile, mode='r') as f:
        gamevalstuple = pickle.load(f)

    deadix = gamevalstuple[1]
    ntgtsix = gamevalstuple[2]
    denix = gamevalstuple[3]
    gamevalsarr = gamevalstuple[0]
    vals = gamevalsarr[deadix[dead], ntgtsix[ntgts], denix[den]][ix]
    if vals is not None:
        marg = {k: i - k * costres for k, i in vals.iteritems()}
        val = sorted(marg.items())
        x, y = zip(*val)

        plt.plot(x, y)
        ax = plt.gca()
        ax.grid(which='both')

        plt.xlabel('# of resources')
        plt.ylabel('margin')

        if save:
            plt.savefig("figures/margin" + str(dead) + "_" +
                        str(den) + "_" +
                        str(ntgts) + "_" +
                        str(ix) + ".svg")

        plt.show()

    else:
        print 'results not yet computed'
