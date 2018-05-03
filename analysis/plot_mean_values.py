import matplotlib.pylab as plt
import pandas as pd
from itertools import cycle

linestyles = ['-', '--', '-.', ':']
markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']


def plot_mean_values(data, den, dead, ntgts, et, apxt,
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


def plot_mean_values_enum(data, den, dead, ntgts, apxt,
                          markerstyles=['.', 'o', '*',
                                        'v', 'x', 'd', '+', 's'],
                          linestyles=['-', '--', '-.', ':'], save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for et in ['gurobi', 'do1', 'do2', 'ls1', 'ls2']:
        plot_mean_values(data, den, dead, ntgts, et,
                         apxt, next(mark), next(line), et)
    plt.legend()
    plt.xlabel('Number of Resources')
    plt.ylabel('Game Value')
    plt.show()

    if save:
        fs = 'figures/mean_values_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(ntgts) + '_' + str(apxt) + '_enum.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


def plot_mean_values_apxt(data, den, dead, ntgts, et,
                          markerstyles=['.', 'o', '*',
                                        'v', 'x', 'd', '+', 's'],
                          linestyles=['-', '--', '-.', ':'], save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in ['opt', 'apx(-spc)', 'apx(spc)', 'apx(dead)',
                'apx(dead-spc)', 'apx(10)', 'apx(20)', 'apx(30)']:
        plot_mean_values(data, den, dead, ntgts, et,
                         apx, next(mark), next(line), apx)
    plt.legend()
    plt.xlabel('Number of Resources')
    plt.ylabel('Game Value')
    plt.show()

    if save:
        fs = 'figures/mean_values_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(ntgts) + '_' + str(et) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


if __name__ == '__main__':
    data = pd.read_pickle('data/exp_mean_values.pickle')

    save = True

    # ['opt', 'apx(dead)', 'apx(dead-spc)', 'apx(spc)',
    #  'apx(10)', 'apx(20)', 'apx(30)']
    apxt = 'apx(30)'
    # ['gurobi', 'ls1', 'ls2']
    et = 'gurobi'

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    plot_mean_values_apxt(data, 6, 5, 50, 'gurobi',
                          markerstyles, linestyles, save)
    plot_mean_values_apxt(data, 6, 5, 40, 'gurobi',
                          markerstyles, linestyles, save)
    plot_mean_values_enum(data, 6, 5, 50, 'opt',
                          markerstyles, linestyles, save)
    plot_mean_values_enum(data, 6, 1.5, 50, 'apx(30)',
                          markerstyles, linestyles, save)
    plot_mean_values_enum(data, 6, 1.5, 40, 'apx(30)',
                          markerstyles, linestyles, save)
