import matplotlib.pylab as plt
import pandas as pd
from itertools import cycle


def plot_mean_opt(data, den, dead, et, apxt, mark, line, label=None):
    sel = data.loc[(data.et == et) & (data.apxt == apxt) & (
        data.dead == dead) & (data.den == den), ['ntgts', 'optres']]
    if sel.size != 0:
        plt.plot(sel['ntgts'], sel['optres'],
                 marker=mark, linestyle=line, label=label)


def plot_mean_opt_apxt(data, den, dead, markerstyles, linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in ['exact', '10 orders', '20 orders', '30 orders']:
        plot_mean_opt(data, den, dead, 'gurobi', apx,
                      next(mark), next(line), apx)
    plt.legend()
    plt.xlabel('Number of Nodes')
    plt.ylabel('Maximum Resoures')
    plt.show()

    if save:
        fs = 'figures/mean_optres_' + str(dead).replace('.', '') + '_' +\
             str(den) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_optres(data, den, dead, apxt, markerstyles,
                     linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    plot_mean_opt(data, den, dead, 'gurobi', apxt,
                  next(mark), next(line))
    plt.xlabel('Number of Nodes')
    plt.ylabel('Optimum Resoures')
    plt.show()

    if save:
        fs = 'figures/mean_optres_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(apxt) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


if __name__ == '__main__':
    data = pd.read_pickle('data/exp_opt_resources_mean.pickle')

    save = True

    dead = 10
    den = 6

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    # plot_mean_opt_apxt(data, 6, 5, markerstyles, linestyles, save)
    # plot_mean_opt_apxt(data, 6, 10, markerstyles, linestyles, save)

    plot_mean_optres(data, 6, 5, 'exact', markerstyles, linestyles, save)
    plot_mean_opt_apxt(data, 6, 5, markerstyles, linestyles, save)
