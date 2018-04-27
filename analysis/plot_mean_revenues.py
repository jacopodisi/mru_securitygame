import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from itertools import cycle


def plot_mean_revenues(data, den, dead, ntgts, cost, et='gurobi', apxt=None,
                          markerstyles=['.', 'o', '*', 'v', 'x', 'd', '+', 's'],
                          linestyles=['-','--','-.',':'], save=False):
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    utils_col = [x for x in data.columns if 'utility' in x]
    row = data.loc[(data.et==et) & (data.dead==dead) &
                   (data.den==den) & (data.ntgts==ntgts), utils_col + ['apxt']]
    if apxt is None:
        if 'opt' in row.apxt.unique():
            apxt = 'opt'
        else:
            apxt = 'apx(30)'
    row = row.loc[row.apxt==apxt, utils_col]
    
    if row.size == 0:
        return

    count=0
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
    row.rename(index=str, columns={x: int(x.split('_')[-1]) for x in used_cols}, inplace=True)
    val = row.values[0]
    nres = row.columns

    plt.figure()
    for c in cost:
        plt.plot(nres, val - nres*c, marker=next(mark), linestyle=next(line), label='cost: ' + str(c))
    plt.legend()
    plt.ylim(0, 1.05)
    plt.yticks(np.arange(0, 1.05, .20))
    plt.xlabel('Number of Resources')
    plt.ylabel('Game Revenue')
    plt.show()

    if save:
        fs = 'figures/mean_revenues_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(ntgts) + '_' + et + '_' + apxt + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)


if __name__=='__main__':
    data = pd.read_pickle('data/exp_mean_values.pickle')

    save = True

    # ['opt', 'apx(dead)', 'apx(dead-spc)', 'apx(spc)', 'apx(10)', 'apx(20)', 'apx(30)']
    apxt = 'apx(30)'
    # ['gurobi', 'ls1', 'ls2']
    et = 'gurobi'

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-','--','-.',':']
    markerstyles = ['.']

    plot_mean_revenues(data, 6, 5, 50,
                       [0.05, 0.07, 0.1],
                       markerstyles=markerstyles,
                       linestyles=linestyles,
                       save=save)
