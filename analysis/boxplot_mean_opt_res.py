import matplotlib.pylab as plt
import pandas as pd
import numpy as np


def plot_opt_single(data, den, dead, apxt, save=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    tp = data.loc[(data.apxt == apxt) & (data.dead == dead) &
                  (data.den == den) & (data.et == 'gurobi'), ['ntgts', 'optres']]
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
    plt.show()

    if save:
        fs = 'figures/boxplot_opt_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(apxt) + '.pdf'
        fig.savefig(fs)
        print('saved figure in: ' + fs)


if __name__ == '__main__':
    save = True

    data = pd.read_pickle('data/exp_opt_resources.pickle')

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-', '--', '-.', ':']
    markerstyles = ['.']

    plot_opt_single(data, 6, 5, 'exact', save)
