import matplotlib.pylab as plt
import pandas as pd
from itertools import cycle
import numpy as np


def plot_opt_time(den, dead, apxt, save=False):
    data = pd.read_pickle('data/exp_opt_resources_times.pickle')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == 'gurobi'),
                  ['ntgts', 'time_max']]
    flat_mat = []
    tgts = np.array(np.sort(tp.ntgts.unique()), dtype='int')
    for tgt in tgts:
        vals = tp.loc[tp.ntgts == tgt, 'time_max'].values
        flat_mat.append(vals.flatten())
    ax.boxplot(flat_mat)
    ax.set_xticklabels(tgts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running time (s)')
    plt.show()

    if save:
        fs = 'figures/boxplot_opt_time_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(apxt) + '.pdf'
        fig.savefig(fs)
        print('saved figure in: ' + fs)


def plot_cov_opt_time(den, dead, apxt, save=False):
    data = pd.read_pickle('data/exp_opt_resources_cov_times.pickle')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == 'gurobi'),
                  ['ntgts', 'time_max']]
    flat_mat = []
    tgts = np.array(np.sort(tp.ntgts.unique()), dtype='int')
    for tgt in tgts:
        vals = tp.loc[tp.ntgts == tgt, 'time_max'].values
        flat_mat.append(vals.flatten())
    ax.boxplot(flat_mat)
    ax.set_xticklabels(tgts)
    ax.set_yscale('log')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running time (s)')
    plt.show()

    if save:
        fs = 'figures/boxplot_cov_opt_time_' + str(dead).replace('.', '') +\
             '_' + str(den) + '_' + str(apxt) + '.pdf'
        fig.savefig(fs)
        print('saved figure in: ' + fs)


def plot_cov_time(den, dead, apxt, save=False):
    data = pd.read_pickle('data/exp_cov_times.pickle')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == 'gurobi'),
                  ['ntgts', 'time_cov']]
    flat_mat = []
    tgts = np.array(np.sort(tp.ntgts.unique()), dtype='int')
    for tgt in tgts:
        vals = tp.loc[tp.ntgts == tgt, 'time_cov'].values
        flat_mat.append(vals.flatten())
    ax.boxplot(flat_mat)
    ax.set_xticklabels(tgts)
    #ax.set_yscale('log')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running time (s)')
    plt.show()

    if save:
        fs = 'figures/boxplot_cov_time_' + str(dead).replace('.', '') +\
             '_' + str(den) + '_' + str(apxt) + '.pdf'
        fig.savefig(fs)
        print('saved figure in: ' + fs)


if __name__ == '__main__':
    save = True

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    plot_opt_time(6, 5, 'exact', save)
    #plot_cov_opt_time(6, 5, 'opt', save)
    #plot_cov_time(6, 5, 'opt', save)
