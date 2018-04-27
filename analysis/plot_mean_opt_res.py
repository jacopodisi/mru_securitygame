import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from itertools import cycle
import sys


def plot_mean_opt(data, den, dead, et, apxt, mark, line, label=None):
    sel = data.loc[(data.et==et) & (data.apxt==apxt) & (data.dead==dead) & (data.den==den), ['ntgts', 'optres']]
    if sel.size != 0:
        plt.plot(sel['ntgts'], sel['optres'], marker=mark, linestyle=line, label=label)

    
def plot_mean_opt_apxt(data, den, dead, markerstyles, linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in ['opt', 'apx(-spc)', 'apx(spc)', 'apx(dead)', 'apx(dead-spc)', 'apx(10)', 'apx(20)', 'apx(30)']:
        plot_mean_opt(data, den, dead, 'gurobi', apx, next(mark), next(line), apx)
    plt.legend()
    plt.xlabel('Number Nodes')
    plt.ylabel('Optimum Resoures')
    plt.show()

    if save:
        fs = 'figures/mean_optres_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(typ) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)

    
if __name__=='__main__':
    data = pd.read_pickle('data/exp_opt_resources_mean.pickle')

    save = False

    dead = 10
    den = 6

    # type: 'apxt' or 'enum'
    typ = 'apxt'

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-','--','-.',':']
    markerstyles = ['.']

    plot_mean_opt_apxt(data, den, dead, markerstyles, linestyles, save)
