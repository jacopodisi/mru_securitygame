import matplotlib.pylab as plt
import pandas as pd
from itertools import cycle
import numpy as np
from matplotlib.ticker import MaxNLocator, LogLocator


folder = '../../thesis/images/graphs1/'
font = {'size': 18,
        'weight': 'ultralight'}
plt.rc('font', **font)
plt.tight_layout()


def boxplot_opt_time(den, dead, apxt, et, save):
    data = pd.read_pickle('data/exp_opt_resources_times.pickle')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == et),
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
    plt.ylabel('Running Time (s)')
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'boxplot_opt_time_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(apxt) + '.pdf'
        fig.savefig(fs)
        print('saved figure in: ' + fs)


def boxplot_opt(den, dead, apxt, et, save):
    data = pd.read_pickle('data/exp_opt_resources.pickle')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == et),
                  ['ntgts', 'optres']]
    res_list = []
    tgts = np.array(np.sort(tp.ntgts.unique()), dtype='int')
    for tgt in tgts:
        vals = tp.loc[tp.ntgts == tgt, 'optres'].values
        res_list.append(vals.flatten())
    ax.boxplot(res_list)
    ax.set_xticklabels(tgts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Maximum Resources')
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'boxplot_opt_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(apxt) + '.pdf'
        fig.savefig(fs)
        print('saved figure in: ' + fs)


def plot_opt_time(den, dead, apxt, et, markerstyles,
                  linestyles, save):
    data = pd.read_pickle('data/exp_opt_resources_times_mean.pickle')
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    tp = data.loc[(data.apxt == apxt) & (data.et == et) &
                  (data.dead == dead) & (data.den == den),
                  ['ntgts', 'time_max']]
    if tp.size != 0:
        plt.plot(tp['ntgts'], tp['time_max'],
                 marker=next(mark), linestyle=next(line))
    plt.grid(True, axis='y', which='minor')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running Time (s)')
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'mean_opt_time_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(apxt) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_optres(den, dead, apxt, et, markerstyles,
                     linestyles, save):
    data = pd.read_pickle('data/exp_opt_resources_mean.pickle')
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    sel = data.loc[(data.et == et) & (data.apxt == apxt) & (
        data.dead == dead) & (data.den == den), ['ntgts', 'optres']]
    if sel.size != 0:
        plt.plot(sel['ntgts'], sel['optres'],
                 marker=next(mark), linestyle=next(line))
    plt.xlabel('Number of Nodes')
    plt.ylabel('Maximum Resoures')
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'mean_optres_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(apxt) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def boxplot_and_plot_opt_time(den, dead, apxt, et, markerstyles,
                              linestyles, save):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    data = pd.read_pickle('data/exp_opt_resources_times_mean.pickle')
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    tp = data.loc[(data.apxt == apxt) & (data.et == et) &
                  (data.dead == dead) & (data.den == den),
                  ['ntgts', 'time_max']]
    if tp.size != 0:
        ax.plot(tp['ntgts'], tp['time_max'],
                marker=next(mark), linestyle=next(line))
    locs, labels = plt.xticks()

    data = pd.read_pickle('data/exp_opt_resources_times.pickle')
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == et),
                  ['ntgts', 'time_max']]
    flat_mat = []
    tgts = np.array(np.sort(tp.ntgts.unique()), dtype='int')
    for tgt in tgts:
        vals = tp.loc[tp.ntgts == tgt, 'time_max'].values
        flat_mat.append(vals.flatten())
    ax.boxplot(flat_mat, positions=tgts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running Time (s)')
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'meanbox_opt_time_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(apxt) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_utils(data, den, dead, ntgts, et, apxt,
                    mark='.', line='-', label=None):
    utils_col = [x for x in data.columns if 'utility' in x]
    row = data.loc[(data.et == et) & (data.apxt == apxt) &
                   (data.dead == dead) & (data.den == den) &
                   (data.ntgts == ntgts), utils_col]

    if row.size != 0:

        count = 0
        used_cols = []
        for col in utils_col:
            if pd.isnull(row[col].iloc[0]):
                continue
            if (row[col].item() == 1) & (count == 1):
                break
            elif row[col].item() == 1:
                count = 1
            used_cols.append(col)

        row = row.loc[:, used_cols]
        row.rename(index=str, columns={x: int(
            x.split('_')[-1]) for x in used_cols}, inplace=True)
        plt.plot(row.transpose(), marker=mark, linestyle=line, label=label)


def plot_mean_utils_enum(den, dead, ntgts, apxt, etlist,
                         markerstyles, linestyles, save):

    data = pd.read_pickle('data/exp_mean_values.pickle')
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for et in etlist:
        plot_mean_utils(data, den, dead, ntgts, et,
                        apxt, next(mark), next(line),
                        et.replace('-', ' '))
    plt.xlabel('Number of Resources')
    plt.ylabel('Maximum Expected Utility')
    plt.ylim(0, 1.05)
    plt.yticks(np.arange(0, 1.05, .20))
    plt.xlim(xmax=10.5)
    plt.xticks(np.arange(2, 11, 2))

    plt.tight_layout()
    plt.legend()
    plt.show()

    if save:
        fs = folder + 'mean_values_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(ntgts) + '_' + str(apxt) + '_enum.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_utils_times(data, den, dead, ntgts, et, apxt,
                          mark='.', line='-', label=None):
    res_col = [x for x in data.columns if 'time_res' in x]
    row = data.loc[(data.et == et) & (data.apxt == apxt) &
                   (data.dead == dead) & (data.den == den) &
                   (data.ntgts == ntgts), res_col]

    if row.size != 0:
        used_cols = [x for x in res_col if not pd.isnull(row[x].iloc[0])]

        row = row.loc[:, used_cols]
        row.rename(index=str, columns={x: int(
            x.split('_')[-1]) for x in used_cols}, inplace=True)

        plt.plot(row.transpose(), marker=mark, linestyle=line, label=label)


def plot_mean_utils_times_enum(den, dead, ntgts, apxt, etlist,
                               markerstyles, linestyles, save):
    data = pd.read_pickle('data/exp_mean_res_times.pickle')
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for et in etlist:
        plot_mean_utils_times(data, den, dead, ntgts, et,
                              apxt, next(mark), next(line),
                              et.replace('-', ' '))
    plt.legend()
    plt.xlabel('Number of Resources')
    plt.ylabel('Running Time (s)')
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'mean_utils_times_' + str(dead).replace('.', '') +\
            '_' + str(den) + '_' + str(ntgts) + '_' + str(apxt) + '_enum.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def boxplot_cov_time(den, dead, apxt, et, save):
    data = pd.read_pickle('data/exp_cov_times.pickle')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == et),
                  ['ntgts', 'time_cov']]
    flat_mat = []
    tgts = np.array(np.sort(tp.ntgts.unique()), dtype='int')
    for tgt in tgts:
        vals = tp.loc[tp.ntgts == tgt, 'time_cov'].values
        flat_mat.append(vals.flatten())
    ax.boxplot(flat_mat)
    ax.set_xticklabels(tgts)
    # ax.set_yscale('log')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running Time (s)')
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'boxplot_cov_time_' + str(dead).replace('.', '') +\
            '_' + str(den) + '_' + str(apxt) + '.pdf'
        fig.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_cov_times_apxt(den, dead, apxlist, et, markerstyles,
                             linestyles, save):
    data = pd.read_pickle('data/exp_mean_cov_times.pickle')
    f = plt.figure()
    ax = f.add_subplot(111)
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in apxlist:
        tp = data.loc[(data.et == et) & (data.apxt == apx) & (
            data.dead == dead) & (data.den == den), ['ntgts', 'time_cov']]
        apx = apx.replace('-', ' ')
        label = apx
        if tp.size == 0:
            label = '_nolegend_'
        plt.semilogy(tp['ntgts'], tp['time_cov'],
                     marker=next(mark), linestyle=next(line), label=label)

    plt.legend()
    # ax.set_yscale('symlog', subsy=[2, 4, 6, 8])
    ax.grid(True, axis='y', which='both')
    plt.xlabel('Number of Nodes')
    plt.ylabel('Running Time (s)')

    if save:
        fs = folder + 'mean_cov_time_' + str(dead).replace('.', '') +\
            '_' + str(den) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)

    plt.tight_layout()
    plt.show()


def plot_mean_opt_apxt(den, dead, apxlist, et, markerstyles,
                       linestyles, save):
    data = pd.read_pickle('data/exp_opt_resources_mean.pickle')
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in apxlist:
        sel = data.loc[(data.et == et) & (data.apxt == apx) & (
            data.dead == dead) & (data.den == den), ['ntgts', 'optres']]
        apx = apx.replace('-', ' ')
        if sel.size != 0:
            plt.plot(sel['ntgts'], sel['optres'],
                     marker=next(mark), linestyle=next(line), label=apx)
    plt.legend()
    plt.xlabel('Number of Nodes')
    plt.ylabel('Maximum Resoures')
    plt.ylim(ymin=0)
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'mean_optres_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_utils_apxt(den, dead, ntgts, apxlist, et,
                         markerstyles, linestyles, save):
    data = pd.read_pickle('data/exp_mean_values.pickle')
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in apxlist:
        plot_mean_utils(data, den, dead, ntgts, et,
                        apx, next(mark), next(line),
                        apx.replace('-', ' '))
    plt.legend()
    plt.xlabel('Number of Resources')
    plt.ylabel('Maximum Expected Utility')
    plt.ylim(0, 1.05)
    plt.yticks(np.arange(0, 1.05, .20))
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'mean_values_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(ntgts) + '_' + str(et) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_utils_times_apxt(den, dead, ntgts, apxlist, et,
                               markerstyles, linestyles, save):
    data = pd.read_pickle('data/exp_mean_res_times.pickle')
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in apxlist:
        plot_mean_utils_times(data, den, dead, ntgts, et,
                              apx, next(mark), next(line),
                              apx.replace('-', ' '))
    plt.legend()
    plt.xlabel('Number of Resources')
    plt.ylabel('Running Time(s)')
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'mean_utils_times_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(ntgts) + '_' + str(et) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_revenues(den, dead, ntgts, apxt, et, costs,
                       markerstyles, linestyles, save):
    data = pd.read_pickle('data/exp_mean_values.pickle')
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    utils_col = [x for x in data.columns if 'utility' in x]
    row = data.loc[(data.et == et) & (data.dead == dead) &
                   (data.den == den) & (data.ntgts == ntgts) &
                   (data.apxt == apxt), utils_col]

    if row.size == 0:
        return

    count = 0
    used_cols = []
    for col in utils_col:
        if pd.isnull(row[col].iloc[0]):
            continue
        if (row[col].item() == 1) & (count == 1):
            break
        elif row[col].item() == 1:
            count = 1
        used_cols.append(col)

    row = row.loc[:, used_cols]
    row.rename(index=str, columns={x: int(
        x.split('_')[-1]) for x in used_cols}, inplace=True)
    val = row.values[0]
    nres = row.columns

    plt.figure()
    for c in costs:
        plt.plot(nres, val - nres * c, marker=next(mark),
                 linestyle=next(line), label='cost: ' + str(c))
    plt.legend()
    plt.ylim(0, 1.05)
    plt.yticks(np.arange(0, 1.05, .20))
    plt.xlabel('Number of Resources')
    plt.ylabel('Expected Revenue')
    plt.tight_layout()
    plt.show()

    if save:
        fs = folder + 'mean_revenues_' + str(dead).replace('.', '') + '_' +\
            str(den) + '_' + str(ntgts) + '_' + et + '_' + apxt + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


if __name__ == '__main__':
    save = True

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    den = 6
    dead = 5
    apxt = 'Exact'
    et = 'CSP-Based'
    etlist = ['CSP-Based', 'Double-Oracle', 'Local-Search']
    apxlist = ['Exact', '10-Orders', '20-Orders', '30-Orders']
    costs = [0.05, 0.07, 0.1]

    # boxplot_opt_time(den, dead, apxt, et, save)
    # plot_opt_time(den, dead, apxt, et, markerstyles, linestyles, save)

    # boxplot_opt(den, dead, apxt, et, save)
    # plot_mean_optres(den, dead, apxt, et, markerstyles, linestyles, save)

    # plot_mean_utils_enum(den, dead, 25, apxt, etlist,
    #                      markerstyles, linestyles, save)
    # plot_mean_utils_enum(den, dead, 50, apxt, etlist,
    #                      markerstyles, linestyles, save)

    # plot_mean_utils_times_enum(den, dead, 25, apxt, etlist, markerstyles,
    #                            linestyles, save)
    # plot_mean_utils_times_enum(den, dead, 50, apxt, etlist, markerstyles,
    #                            linestyles, save)

    # boxplot_cov_time(den, dead, apxt, et, save)

    # plot_mean_cov_times_apxt(
    #     den, dead, apxlist, et, markerstyles, linestyles, save)
    plot_mean_opt_apxt(den, dead, apxlist, et, markerstyles,
                       linestyles, save)

    plot_mean_utils_apxt(den, dead, 50, apxlist, et,
                         markerstyles, linestyles, save)
    # plot_mean_utils_times_apxt(den, dead, 50, apxlist, et,
    #                            markerstyles, linestyles, save)

    # plot_mean_cov_times_apxt(den, 1.5, apxlist, et, markerstyles,
    #                          linestyles, save)

    # plot_mean_revenues(den, dead, 25, apxt, et, costs,
    #                    markerstyles, linestyles, save)
    # plot_mean_revenues(den, dead, 50, apxt, et, costs,
    #                    markerstyles, linestyles, save)

    # boxplot_and_plot_opt_time(den, dead, apxt, et, markerstyles,
    #                           linestyles, save)
