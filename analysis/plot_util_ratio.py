import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from itertools import cycle

        
def plot_utils_ratios_enum(den, dead, markerstyles, linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    data = pd.read_pickle('data/exp_utils_ratios_enum.pickle')
    for et in ['gurobi', 'ls1', 'ls2']:
        row = data.loc[(data.et==et) & (data.dead==dead) &
                      (data.den==den), ['ntgts', 'ratios']]
        plt.plot(row['ntgts'], row['ratios'], marker=next(mark), linestyle=next(line), label=et)
    plt.legend()
    plt.ylim(0.9, 1.20)
    plt.yticks(np.arange(0.9, 1.15, 0.05))
    plt.xlabel('Number Nodes')
    plt.ylabel('Utility Ratio')
    plt.show()

    if save:
        fs = 'figures/utils_ratio_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_enum.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)

        
def plot_utils_ratios_apx(den, dead, markerstyles, linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    data = pd.read_pickle('data/exp_utils_ratios_apx.pickle')
    et = 'gurobi'
    group = data.loc[(data.dead==dead) & (data.den==den), ['apxt', 'ntgts', 'ratios']]
    for apxt in group.apxt.unique():
        row = group.loc[(group.apxt==apxt), ['ntgts', 'ratios']]
        plt.plot(row['ntgts'], row['ratios'], marker=next(mark), linestyle=next(line), label=apxt)
    plt.legend()
    plt.grid(True, axis='y', which='minor')
    plt.ylim(0.6, 1.1)
    plt.yticks(np.arange(0.7, 1.05, 0.1))
    plt.xlabel('Number Nodes')
    plt.ylabel('Utility Ratio')
    plt.show()

    if save:
        fs = 'figures/utils_ratio_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)

    
if __name__=='__main__':
    save = True

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-','--','-.',':']
    markerstyles = ['.']

    plot_utils_ratios_apx(6, 5, markerstyles, linestyles, save)
    plot_utils_ratios_apx(6, 1.5, markerstyles, linestyles, save)
    plot_utils_ratios_enum(6, 5, markerstyles, linestyles, save)
    plot_utils_ratios_enum(6, 1.5, markerstyles, linestyles, save)
