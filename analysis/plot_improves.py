import matplotlib.pylab as plt
import pandas as pd
from itertools import cycle


def plot_improves(data, den, dead, apxt, et, mark, line, label=None):
    resimp = data.loc[(data.et == et) & (data.dead == dead) &
                      (data.den == den) & (data.apxt == apxt) &
                      (data.ntgts == ntgts)  & (data.graphix == graphix),
                      'improves'].iat[0]
    improves = {}
    for nres, utils in resimp.iteritems():
        improves[nres] = [utils[0]]
        for u in utils[1:]:
            improves[nres].append(u if u > improves[nres][-1] else improves[nres][-1])
    plt.plot(improves[max(improves.keys())], marker=mark, linestyle=line, label=label)


def plot_opt_times_apxt(data, den, dead,
                        markerstyles, linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in ['opt', 'apx(-spc)', 'apx(spc)', 'apx(dead)', 'apx(dead-spc)',
                'apx(10)', 'apx(20)', 'apx(30)']:
        plot_opt_times(data, den, dead, apx,
                       next(mark), next(line), apx)
    plt.legend()
    plt.grid(True, axis='y', which='minor')
    plt.xlabel('Number Nodes')
    plt.ylabel('Compute Time(s)')
    plt.show()

    if save:
        fs = 'figures/mean_opt_time_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_improves_enum(data, den, dead, apxt, ntgts, graphix, markerstyles,
                  linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for et in ['gurobi', 'do1', 'ls1']:
        plot_improves(data, den, dead, apxt, et, next(mark), next(line), label=et)
    plt.xlabel('Iteration')
    plt.ylabel('Expected Utility')
    plt.legend()
    plt.show()

    if save:
        fs = 'figures/mean_opt_time_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(apxt) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


if __name__ == '__main__':
    save = True

    data = pd.read_pickle('data/exp_improves.pickle')

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    plot_opt_time_single(data, 6, 5, 'opt', markerstyles, linestyles, save)
    plot_opt_times_apxt(data, 6, 5, markerstyles, linestyles, save)
    plot_opt_times_apxt(data, 6, 10, markerstyles, linestyles, save)
