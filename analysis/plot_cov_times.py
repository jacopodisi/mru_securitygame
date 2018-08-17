import matplotlib.pylab as plt
import pandas as pd
from itertools import cycle


def plot_mean_cov_times(data, den, dead, et, apxt, mark, line,
                        label=None, ylog=False):
    tp = data.loc[(data.et == et) & (data.apxt == apxt) & (
        data.dead == dead) & (data.den == den), ['ntgts', 'time_cov']]
    if tp.size==0:
        print('empty')
        label='_nolegend_'
    if ylog:
        plt.semilogy(tp['ntgts'], tp['time_cov'],
                     marker=mark, linestyle=line, label=label)
    else:
        plt.plot(tp['ntgts'], tp['time_cov'],
                 marker=mark, linestyle=line, label=label)


def plot_mean_cov_times_apxt(data, den, dead, apxlist, markerstyles,
                             linestyles, save=False, ylog=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in apxlist:
        plot_mean_cov_times(data, den, dead, 'gurobi', apx,
                            next(mark), next(line), apx, ylog)
    plt.legend()
    plt.grid(True, axis='y', which='minor')
    plt.xlabel('Number Nodes')
    plt.ylabel('Compute Time(s)')

    if save:
        fs = 'figures/mean_cov_time_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_apx'
        # i = 0
        # while os.path.exists('{}_{:d}.pdf'.format(fs, i)):
        #     i += 1
        # fs = '{}_{:d}'.format(fs, i)
        fs += '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)

    plt.show()


if __name__ == '__main__':
    save = True

    # 'exact', 'apx--distance', 'apx-distance', 'apx-deadline',
    # 'apx-excesstime', 'apx-10', 'apx-20', 'apx-30'
    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    data = pd.read_pickle('data/exp_mean_cov_times.pickle')
    apxlist = ['exact', '10 orders', '20 orders', '30 orders']
    plot_mean_cov_times_apxt(data, 6, 5, apxlist, markerstyles,
                             linestyles, save, True)
    apxlist = ['10 orders', '20 orders', '30 orders']
    plot_mean_cov_times_apxt(data, 6, 1.5, apxlist, markerstyles,
                             linestyles, save, True)
