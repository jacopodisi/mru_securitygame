import matplotlib.pyplot as plt
import pandas as pd


def plot_ratio_value(dead, den, tgt, gix, data):
    opt = None
    f, ax = plt.subplots()
    #ax.title('tgt' + str(tgt) + ' dead' + str(dead) + ' den' + str(den) + ' gix' + str(gix))
    opt = pd.Series(data.loc[(data.ntgts == tgt) & (data.dead == dead) & (data.graphix == gix) &
                             (data.den == den) & (data.apxt.isnull().values), 'gameval'].item()).copy()
    print opt
    for i in [1, 2, 3, 10, 20, 30]:
        temp = None
        temp = pd.Series(data.loc[(data.ntgts == tgt) & (data.dead == dead) & (
            data.graphix == gix) & (data.den == den) & (data.apxt == i), 'gameval'].item()).copy()
        for t, v in temp.items():
            temp.at[t] = (temp.at[t] / opt.at[t] if t in opt.index else temp.at[t] / 1)
        ax.plot(temp, label='apx' + str(i))
    ax.legend()
    return ax
