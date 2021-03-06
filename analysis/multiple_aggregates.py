import pandas as pd
import os
from fnmatch import fnmatch
import pickle
import numpy as np


folder = 'data/'


def init_df():
    root = '../../../data/'
    pattern = "res_instance_ntgts*"
    data = []

    for path, subdirs, files in os.walk(root):
        for filename in files:
            if fnmatch(filename, pattern):
                with open(path + '/' + filename, mode='rb') as f:
                    res = pickle.load(f)
                listtype = (path.split('/')[-2]).split('_')[1:]
                namel = filename.split("_")[2:-2]
                namel += listtype
                tempdata = {namel[i]: float(namel[i + 1])
                            for i in range(0, len(namel), 2)}
                if (tempdata['et'] == 3) | (tempdata['et'] == 5):
                    continue
                tempdata.update({'utility_{:02d}'.format(k): v
                                 for k, v in res[0].iteritems()})
                tempdata['time_short'] = res[3][0]
                tempdata['time_cov'] = res[3][1]
                tempdata['time_max'] = res[3][2]
                mink = min(res[0].keys())
                timedict = {}
                timedict['time_res_{:02d}'.format(mink)] = res[3][4]
                for i, v in enumerate(res[3][5]):
                    timedict['time_res_{:02d}'.format(mink + 1 + i)] = v
                tempdata.update(timedict)
                if 3 in res[3]:
                    tempdata['time_dom'] = res[3][3]
                else:
                    tempdata['time_dom'] = 0

                tempdata['time_tot'] = res[3][6]
                tempdata['optres'] = max(res[0].keys())
                if (tempdata['ntgts'] == 25) and (tempdata['den'] == 8):
                    tempdata['den'] = 6
                if (tempdata['ntgts'] == 20) and (tempdata['den'] == 10):
                    tempdata['den'] = 6
                utils_improves = {}
                for nres, improves in res[5].iteritems():
                    utils_improves[nres] = list(zip(*improves)[0])
                tempdata['improves'] = utils_improves
                data.append(tempdata)
    dataMatrix = pd.DataFrame(data)
    dataMatrix.dead.fillna(dataMatrix.reldead, inplace=True)
    dataMatrix.drop('reldead', inplace=True, axis=1)
    dataMatrix['apxt'].replace([0, 1, 2, 3, 10, 20, 30],
                               ['apx--distance', 'apx-distance',
                                'apx-deadline', 'apx-excesstime',
                                '10-Orders', '20-Orders', '30-Orders'],
                               inplace=True)
    dataMatrix['apxt'].fillna('Exact', inplace=True)
    dataMatrix['et'].replace([1, 2, 4],
                             ['CSP-Based', 'Double-Oracle', 'Local-Search'],
                             inplace=True)
    resources = np.sort(
        [x for x in dataMatrix.columns if 'utility_' in x])
    bool_list = dataMatrix[resources].isna().any()
    for i in range(len(bool_list) - 1, -1, -1):
        if not bool_list[i]:
            break
        dataMatrix[resources[i]].fillna(1, inplace=True)
    print('save file in ' + folder)
    return dataMatrix


def aggregate_improves(data):
    improves = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et',
                            'graphix', 'improves']]
    improves.to_pickle(folder + 'exp_improves.pickle')
    print('saved improves in exp_improves.pickle')


def aggregate_mean_times(data):
    times = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'time_tot']]
    mean_times = times.groupby(['ntgts', 'den', 'dead', 'apxt', 'et'],
                               as_index=False).mean()
    mean_times.to_pickle(folder + 'exp_mean_times.pickle')
    print('saved mean times in exp_mean_times.pickle')


def aggregate_utilities(data):
    util_col = [x for x in data.columns if 'utility' in x]
    data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'graphix'] +
             util_col].to_pickle(folder + 'exp_game_values.pickle')
    print('saved utilities in exp_game_values.pickle')


def aggregate_times(data):
    time_col = [x for x in data.columns if 'time' in x]
    data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'graphix'] +
             time_col].to_pickle(folder + 'exp_game_times.pickle')
    print('saved times in exp_game_times.pickle')


def aggregate_res_times(data):
    res_col = [x for x in data.columns if 'time_res' in x]
    data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'graphix'] +
             res_col].to_pickle(folder + 'exp_res_times.pickle')
    print('saved res times in exp_res_times.pickle')


def aggregate_mean_utils(data):

    gameval_list = [x for x in data.columns if 'utility' in x] +\
                   ['ntgts', 'den', 'dead', 'apxt', 'et']
    temp = data.loc[:, gameval_list]

    grouped = temp.groupby(['ntgts', 'den', 'dead', 'apxt', 'et'],
                           as_index=False).mean()
    grouped.to_pickle(folder + 'exp_mean_values.pickle')
    print('saved mean utilities in exp_mean_values.pickle')


def aggregate_mean_res_times(data):

    res_col = [x for x in data.columns if 'time_res' in x] +\
        ['ntgts', 'den', 'dead', 'apxt', 'et']
    temp = data.loc[:, res_col]
    grouped = temp.groupby(['ntgts', 'den', 'dead', 'apxt', 'et'],
                           as_index=False).mean()
    grouped.to_pickle(folder + 'exp_mean_res_times.pickle')
    print('saved mean res times in exp_mean_res_times.pickle')


def aggregate_perc_times(data):
    temp = data.copy()
    temp['time_cov'] += temp['time_dom']
    del(temp['time_dom'])

    time_list = ['time_short', 'time_cov'] +\
                [x for x in temp.columns if 'time_res' in x] +\
                ['time_max']
    time_list_res = [x for x in temp.columns if 'time_res' in x]
    temp = temp.loc[:, time_list +
                    ['ntgts', 'den', 'dead', 'apxt',
                     'et', 'graphix']]
    time_sum = temp.loc[:, time_list].sum(axis=1)
    for cn in time_list:
        temp[cn] /= time_sum
    temp['time_res'] = temp[time_list_res].sum(axis=1)
    temp = temp[['time_short', 'time_cov', 'time_res', 'time_max'] +
                ['ntgts', 'den', 'dead', 'apxt', 'et']]
    temp = temp.groupby(['ntgts', 'den', 'dead', 'apxt', 'et'],
                        as_index=False).mean()
    temp.to_pickle(folder + 'exp_perc_times.pickle')
    print('saved percentage times in exp_perc_times.pickle')


def aggregate_ratios_apx(data):
    collist = [i for i in data.columns if 'utility' in i] +\
        ['apxt', 'dead', 'den', 'graphix', 'ntgts', 'et']
    temp = data.loc[data.et == 'CSP-Based', collist].copy()
    temp['ratios'] = np.nan
    del(temp['et'])
    for ix, row in temp.iterrows():
        best = temp.loc[(temp.dead == row.dead) & (temp.den == row.den) &
                        (temp.ntgts == row.ntgts) &
                        (temp.graphix == row.graphix)]
        if 'opt' in best.apxt.unique():
            opt = best.loc[temp.apxt == 'Exact', :]
        else:
            opt = best.loc[temp.apxt == '30-Orders', :]
        ratios = []
        count = 0
        for i in [i for i in data.columns if 'utility' in i]:
            if opt[i].item() == 1:
                if count == 1:
                    break
                count = 1
            ratio = row[i] / opt[i].item()
            if pd.isnull(ratio):
                continue
            ratios.append(ratio)
        temp.loc[ix, 'ratios'] = np.mean(ratios)
    df_ratios = temp.loc[:, ['dead', 'den', 'ntgts', 'apxt', 'ratios']]
    df_ratios = df_ratios.groupby(
        ['dead', 'den', 'ntgts', 'apxt'], as_index=False).mean()
    df_ratios.to_pickle(folder + 'exp_utils_ratios_apx.pickle')
    print('saved utilities ratio of apx in exp_utils_ratios_apx.pickle')


def aggregate_ratios_enum(data):
    collist = [i for i in data.columns if 'utility' in i] +\
        ['dead', 'den', 'graphix', 'ntgts', 'et']
    temp = data.loc[(data.apxt == 'opt') | (
        (data.apxt == '30-Orders') & (data.dead < 3)), collist].copy()
    temp['ratios'] = np.nan
    for ix, row in temp.iterrows():
        best = temp.loc[(temp.dead == row.dead) & (temp.den == row.den) &
                        (temp.ntgts == row.ntgts) &
                        (temp.graphix == row.graphix)]
        opt = best.loc[temp.et == 'CSP-Based', :]
        ratios = []
        count = 0
        for i in [i for i in data.columns if 'utility' in i]:
            if opt[i].item() == 1:
                if count == 1:
                    break
                count = 1
            ratio = row[i] / opt[i].item()
            if pd.isnull(ratio):
                continue
            ratios.append(ratio)
        temp.loc[ix, 'ratios'] = np.mean(ratios)
    df_ratios = temp.loc[:, ['dead', 'den', 'ntgts', 'et', 'ratios']]
    df_ratios = df_ratios.groupby(
        ['dead', 'den', 'ntgts', 'et'], as_index=False).mean()
    df_ratios.to_pickle(folder + 'exp_utils_ratios_enum.pickle')
    print('saved utilities ratio of enum in exp_utils_ratios_enum.pickle')


def aggregate_opt_resources_mean(data):
    optres = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'optres']]
    mean_optres = optres.groupby(['ntgts', 'den', 'dead', 'apxt', 'et'],
                                 as_index=False).mean()
    mean_optres.to_pickle(folder + 'exp_opt_resources_mean.pickle')
    print('saved mean optimum resources in exp_opt_resources_mean.pickle')


def aggregate_opt_resources_time_mean(data):
    times = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'time_max']]
    mean_times = times.groupby(['ntgts', 'den', 'dead', 'et', 'apxt'],
                               as_index=False).mean()
    mean_times.to_pickle(folder + 'exp_opt_resources_times_mean.pickle')
    print('saved mean compute time of optimum resources in'
          'exp_opt_resources_times_mean.pickle')


def aggregate_opt_resources_cov_time_mean(data):
    times = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et',
                         'time_short', 'time_cov', 'time_dom', 'time_max']]
    times['time_max'] = times['time_short'] + times['time_cov'] +\
        times['time_dom'] + times['time_max']
    times = times[['ntgts', 'den', 'dead', 'apxt', 'et', 'time_max']]
    mean_times = times.groupby(['ntgts', 'den', 'dead', 'et', 'apxt'],
                               as_index=False).mean()
    mean_times.to_pickle(folder + 'exp_opt_resources_cov_times_mean.pickle')
    print('saved mean compute time of optimum resources in'
          'exp_opt_resources_cov_times_mean.pickle')


def aggregate_opt_resources(data):
    optres = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'optres']]
    optres.to_pickle(folder + 'exp_opt_resources.pickle')
    print('saved optimum resources in exp_opt_resources.pickle')


def aggregate_opt_resources_time(data):
    times = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'time_max']]
    times.to_pickle(folder + 'exp_opt_resources_times.pickle')
    print('saved compute time of optimum resources in'
          'exp_opt_resources_times.pickle')


def aggregate_opt_resources_cov_time(data):
    times = data.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et',
                         'time_short', 'time_cov', 'time_dom', 'time_max']]
    times['time_max'] = times['time_short'] + times['time_cov'] +\
        times['time_dom'] + times['time_max']
    times = times[['ntgts', 'den', 'dead', 'apxt', 'et', 'time_max']]
    times.to_pickle(folder + 'exp_opt_resources_cov_times.pickle')
    print('saved compute time of optimum resources in'
          'exp_opt_resources_cov_times.pickle')


def aggregate_cov_times(data):
    times = data.copy()
    times['time_cov'] = times['time_short'] + times['time_cov'] +\
        times['time_dom']
    times = times.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'time_cov']]
    times.to_pickle(folder + 'exp_cov_times.pickle')
    print('saved compute time of covering sets in'
          'exp_cov_times.pickle')


def aggregate_mean_cov_times(data):
    times = data.copy()
    times['time_cov'] = times['time_short'] + times['time_cov'] +\
        times['time_dom']
    times = times.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'time_cov']]
    times = times.groupby(['ntgts', 'den', 'dead', 'et', 'apxt'],
                          as_index=False).mean()
    times.to_pickle(folder + 'exp_mean_cov_times.pickle')
    print('saved mean compute time of covering sets in'
          'exp_mean_cov_times.pickle')


def aggregate_mean_cov_times_nodom(data):
    times = data.copy()
    times['time_cov'] = times['time_short'] + times['time_cov']
    times = times.loc[:, ['ntgts', 'den', 'dead', 'apxt', 'et', 'time_cov']]
    times = times.groupby(['ntgts', 'den', 'dead', 'et', 'apxt'],
                          as_index=False).mean()
    times.to_pickle(folder + 'exp_mean_cov_times_nodom.pickle')
    print('saved mean compute time of covering sets without dom in'
          'exp_mean_cov_times_nodom.pickle')


if __name__ == '__main__':
    data = init_df()
    aggregate_improves(data)
    aggregate_times(data)
    aggregate_mean_times(data)
    aggregate_opt_resources(data)
    aggregate_opt_resources_time(data)
    aggregate_opt_resources_cov_time(data)
    aggregate_opt_resources_mean(data)
    aggregate_opt_resources_time_mean(data)
    aggregate_opt_resources_cov_time_mean(data)
    aggregate_utilities(data)
    aggregate_mean_utils(data)
    aggregate_perc_times(data)
    aggregate_ratios_apx(data)
    aggregate_ratios_enum(data)
    aggregate_res_times(data)
    aggregate_mean_res_times(data)
    aggregate_cov_times(data)
    aggregate_mean_cov_times(data)
