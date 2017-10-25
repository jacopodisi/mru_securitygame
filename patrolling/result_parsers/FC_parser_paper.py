from __future__ import division
import basic_parsers.correlated_log_parser as corr
import basic_parsers.log_manager as log_manager
import csv

# output the csv for the FULL COORDINATION plot of the paper
# csv: <n_targets, avg(greedy_timelimit/OPT, avg(milp_time_limit/OPT),)
# OPT is milp without time thresholds

if __name__ == '__main__':

    FC_csv_path = './csv/FC.csv'
    FC_avg_csv_path = './csv/FC_avg.csv'

    FC = [['n_target', 'instance', 'ratio_apxTL_opt', 'ratio_exactTL_opt']]
    FC_avg = [['n_target', 'avg_ratio_apxTL_opt', 'avg_ratio_exactTL_opt']]

    for n_target in [20, 40, 60, 80, 100 ,120]:

        partial_apxTL_opt_ratio = 0.0
        partial_exactTL_opt_ratio = 0.0

        for i in range(1,51):

            apx_content = log_manager.get_log_content(
                corr.get_file_path(n_target, i, 'greedy')
            )
            all_val_apx = corr.get_all_correlated_values(apx_content)
            apx_val = all_val_apx[len(all_val_apx.keys())]

            milp_TL_content = log_manager.get_log_content(
                corr.get_file_path(n_target, i, 'ilp')
            )
            all_val_milp = corr.get_all_correlated_values(milp_TL_content)
            milp_TL_val = all_val_milp[len(all_val_milp.keys())]

            opt_content = log_manager.get_log_content(
                corr.get_file_path(n_target, i, 'ilp_unlimited')
            )
            all_val_opt = corr.get_all_correlated_values(opt_content)
            opt_val = all_val_opt[len(all_val_opt.keys())]

            apx_opt_ratio = apx_val/opt_val
            milp_TL_opt_ratio = milp_TL_val/opt_val

            FC.append([n_target, i, apx_opt_ratio, milp_TL_opt_ratio])

            partial_apxTL_opt_ratio += apx_opt_ratio
            partial_exactTL_opt_ratio += milp_TL_opt_ratio

        FC_avg.append([n_target, partial_apxTL_opt_ratio/50, partial_exactTL_opt_ratio/50])

    with open(FC_csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(FC)
    with open(FC_avg_csv_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(FC_avg)





