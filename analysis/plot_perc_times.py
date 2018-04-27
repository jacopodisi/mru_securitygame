import matplotlib.pylab as plt
import pandas as pd
import numpy as np


def plot_perc_times(data, den, dead, ntgts, et, apxt, graphix, save=False):
    plt.figure()
    times_col = [x for x in data.columns if 'time' in x]
    row = data.loc[(data.et==et) & (data.apxt==apxt) & (data.dead==dead) &
                   (data.den==den) & (data.ntgts==ntgts) & (data.graphix==graphix), times_col]
    if row.size==0:
        print('result specified do not exists')
        return
    row.dropna(axis=1, inplace=True)
    row.iloc[0].plot.bar()
    plt.ylabel('Time Ratio')
    plt.ylim(0, 1.05)
    plt.yticks(np.arange(0, 1.05, .20))
    plt.show()
    if save:
        fs = 'figures/perc_times_' + str(dead).replace('.', '') + '_' +\
             str(den) + '_' + str(apxt) + '_' + str(et) + '_' + str(graphix) + '.pdf'
        plt.savefig(fs)
        print('saved figure in: ' + fs)
    

if __name__=='__main__':
    data = pd.read_pickle('data/exp_perc_times.pickle')

    save = True

    # ['opt', 'apx(dead)', 'apx(dead-spc)', 'apx(spc)', 'apx(10)', 'apx(20)', 'apx(30)']
    apxt = 'apx(30)'
    # ['gurobi', 'ls1', 'ls2']
    et = 'gurobi'

    plot_perc_times(data, 6, 5, 50, 'gurobi', 'opt', 0, save)
    plot_perc_times(data, 6, 5, 50, 'gurobi', 'apx(30)', 0, save)
