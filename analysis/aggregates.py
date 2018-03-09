import os
import pandas as pd
from fnmatch import fnmatch
import pickle

root = '../file'
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
            tempdata = {namel[i]: float(namel[i + 1]) for i in range(0, len(namel), 2)}
            tempdata['gameval'] = pd.Series(res[0])
            tempdata['time_short'] = res[3][0]
            tempdata['time_cov'] = res[3][1]
            tempdata['time_max'] = res[3][2]
            mink = min(res[0].keys())
            timedict = {}
            timedict[mink] = res[3][4]
            for i, v in enumerate(res[3][5]):
                timedict[mink + 1 + i] = v
            tempdata['time_res'] = pd.Series(timedict)
            if len(res) > 5:
                timenoendict = {}
                timenoendict[mink] = res[3][4] / (len(res[5][mink]))
                for i, v in enumerate(res[3][5]):
                    timenoendict[mink + 1 + i] = v / (len(res[5][mink + 1 + i]))
                tempdata['time_res_noenum'] = pd.Series(timenoendict)
                tempdata['improves'] = res[5]

            if 3 in res[3]:
                tempdata['time_dom'] = res[3][3]

            tempdata['time_tot'] = res[3][6]
            tempdata['optres'] = max(res[0].keys())
            data.append(tempdata)
dataMatrix = pd.DataFrame(data)
dataMatrix.to_pickle('data_aggregates.pickle', protocol=2)
