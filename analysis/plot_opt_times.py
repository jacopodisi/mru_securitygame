import matplotlib.pylab as plt
import pandas as pd
from itertools import cycle


def plot_opt_times(data, den, dead, apxt, mark, line, label=None):
    tp = data.loc[(data.apxt == apxt) & (
        data.dead == dead) & (data.den == den), ['ntgts', 'time_max']]
    if tp.size != 0:
        plt.semilogy(tp['ntgts'], tp['time_max'],
                     marker=mark, linestyle=line, label=label)


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


def plot_opt_time_single(data, den, dead, apxt, markerstyles,
                         linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    plot_opt_times(data, den, dead, apxt, next(mark), next(line))
    plt.grid(True, axis='y', which='minor')
    plt.xlabel('Number Nodes')
    plt.ylabel('Compute Time(s)')
    plt.show()

    if save:
        fs = 'figures/mean_opt_time_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(apxt) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


if __name__ == '__main__':
    save = True

    data = pd.read_pickle('data/exp_opt_resources_cov_times_mean.pickle')

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    plot_opt_time_single(data, 6, 5, 'opt', markerstyles, linestyles, save)
    plot_opt_times_apxt(data, 6, 5, markerstyles, linestyles, save)
    plot_opt_times_apxt(data, 6, 10, markerstyles, linestyles, save)
