import matplotlib.pylab as plt
import pandas as pd
import numpy as np
from itertools import cycle


def plot_mean_times(data, den, dead, et, apxt, mark, line, label=None):
    tp = data.loc[(data.et==et) & (data.apxt==apxt) & (data.dead==dead) & (data.den==den), ['ntgts', 'time_tot']]
    if tp.size != 0:
        plt.semilogy(tp['ntgts'], tp['time_tot'], marker=mark, linestyle=line, label=label)

        
def plot_mean_times_enum(data, den, dead, markerstyles, linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    if int(dead) <= 2:
        apxt = 'apx(30)'
    else:
        apxt='opt'
    for et in ['gurobi', 'ls1', 'ls2']:
        plot_mean_times(data, den, dead, et, apxt, next(mark), next(line), et)
    plt.legend()
    plt.grid(True, axis='y', which='minor')
    plt.xlabel('Number Nodes')
    plt.ylabel('Compute Time(s)')
    plt.show()

    if save:
        fs = 'figures/mean_time_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_enum.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)

    
def plot_mean_times_apxt(data, den, dead, markerstyles, linestyles, save=False):
    plt.figure()
    mark = cycle(markerstyles)
    line = cycle(linestyles)
    for apx in ['opt', 'apx(-spc)', 'apx(spc)', 'apx(dead)', 'apx(dead-spc)', 'apx(10)', 'apx(20)', 'apx(30)']:
        plot_mean_times(data, den, dead, 'gurobi', apx, next(mark), next(line), apx)
    plt.legend()
    plt.grid(True, axis='y', which='minor')
    plt.xlabel('Number Nodes')
    plt.ylabel('Compute Time(s)')
    plt.show()

    if save:
        fs = 'figures/mean_time_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_apx.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)

    
if __name__=='__main__':
    save = True
    
    data = pd.read_pickle('data/exp_mean_times.pickle')

    # linestyles = ['-','--','-.',':']
    # markerstyles = ['.', 'o', '*', 'v', 'x', 'd', '+', 's']
    linestyles = ['-','--','-.',':']
    markerstyles = ['.']

    plot_mean_times_apxt(data, 6, 5, markerstyles, linestyles, save)
    plot_mean_times_apxt(data, 6, 1.5, markerstyles, linestyles, save)
    plot_mean_times_apxt(data, 6, 10, markerstyles, linestyles, save)
    plot_mean_times_apxt(data, 6, 2, markerstyles, linestyles, save)
    plot_mean_times_enum(data, 6, 5, markerstyles, linestyles, save)
    plot_mean_times_enum(data, 6, 1.5, markerstyles, linestyles, save)
