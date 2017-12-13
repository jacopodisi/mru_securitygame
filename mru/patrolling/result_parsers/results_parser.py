from __future__ import division
import csv
import logging
import baron_log_parser as bar
import correlated_log_parser as corr
import LP_iterated_log_parser as lp
import log_manager as log


# builds and saves the following csv files
#
# LP_bar: n_target|instance|n_restart|LP/baron
# LP_bar_avg: n_target|n_restart|avg(LP/baron)
#
# corr_bar: n_target|instance|corr/baron
# corr_bar_avg: n_target|avg(corr/baron)
#
# baron_low_up: n_target|n_instance|upper_bound/lower_bound
# baron_low_up_avg: n_target|avg(upper_bound/lower_bound)
#
# n_iter_corr: n_target|instance|n_iterations|terminated
# n_iter_corr_avg: n_target|avg(n_iterations)|terminated
#
# time_all: n_target|instance|correlated_time|baron_time|LP_time
# time_all_avg: n_target|avg(correlated_time)|...
#
def collect_results():

    log_path='./problematic_results.log'
    logging.basicConfig(filename=log_path, level=logging.INFO)

    # set csv paths
    LP_bar_path='./LP_bar.csv'
    LP_bar_avg_path='./LP_bar_avg.csv'

    corr_bar_path='./corr_bar.csv'
    corr_bar_avg_path='./corr_bar_avg.csv'

    greedy_corr_bar_path = './greedy_corr_bar.csv'
    greedy_corr_bar_avg_path = './greedy_corr_bar_avg.csv'

    apx_ratio_path = './apx_ratio.csv'
    apx_ratio_avg_path = './apx_ratio_avg.csv'

    baron_low_up_path='./baron_low_up.csv'
    baron_low_up_avg_path='./baron_low_up_avg.csv'

    n_iter_corr_path='./n_iter_corr.csv'
    n_iter_corr_avg_path='./n_iter_corr_avg.csv'

    n_iter_greedy_corr_path = './n_iter_greedy_corr.csv'
    n_iter_greedy_corr_avg_path = './n_iter_greedy_corr_avg.csv'

    time_all_path='./time_all.csv'
    time_all_avg_path='./time_all_avg.csv'

    # init lists to be converted in csv files
    LP_bar=[['n_target','instance','n_restart','ratio']]
    LP_bar_avg=[['n_target','n_restart','avg_ratio']]

    corr_bar=[['n_target','instance','ratio']]
    corr_bar_avg=[['n_target','avg_ratio']]

    greedy_corr_bar=[['n_target','instance','ratio']]
    greedy_corr_bar_avg=[['n_target','avg_ratio']]

    apx_ratio=[['n_target','instance','ratio']]
    apx_ratio_avg=[['n_target','avg_ratio']]

    baron_low_up=[['n_target','instance','ratio']]
    baron_low_up_avg=[['n_target','avg_ratio']]

    n_iter_corr=[['n_target','instance','n_iter','termination']]
    n_iter_corr_avg=[['n_target','avg_n_iter','termination']]

    n_iter_greedy_corr=[['n_target','instance','n_iter','termination']]
    n_iter_greedy_corr_avg=[['n_target','avg_n_iter','termination']]

    time_all=[['n_target','instance','time_corr','time_bar','time_LP']]
    time_all_avg=[['n_target','time_corr','time_bar','time_LP']]

    for n_target in [20,40,60,80,100,120]:

        partial_bar_ratio=0.0
        partial_corr_ratio=0.0
        partial_greedy_corr_ratio=0.0
        partial_LP_ratio={}
        partial_LP_ratio[1]=(0.0, 0) # partial value, number of instance with 1 restart
        for i in [10*x for x in range(1,16)]:
            partial_LP_ratio[i]=(0.0, 0)
        partial_iter_corr={}
        partial_iter_greedy_corr={}
        partial_iter_corr['terminated']=(0.0,0)
        partial_iter_corr['not_terminated']=(0.0,0) # (sum, counter to avg)
        partial_iter_greedy_corr['terminated']=(0.0,0)
        partial_iter_greedy_corr['not_terminated']=(0.0,0)
        partial_times={}
        for t in ['bar','corr','lp']:
            partial_times[t]=0.0

        partial_apx_ratio = 0.0

        # number of instance to be considered when averaging
        instance_counter=0

        for instance in range(1,51):

            bar_content=log.get_log_content(bar.get_file_path(n_target, instance))

            if bar.is_fine(bar_content):
                instance_counter += 1

                bar_values=bar.get_baron_values(bar_content)
                bar_time=bar.get_baron_time(bar_content)

                lp_content=log.get_log_content(lp.get_file_path(n_target, instance))
                lp_values=lp.get_LP_values(lp_content)
                lp_time=lp.get_LP_time(lp_content)

                corr_content=log.get_log_content(corr.get_file_path(n_target, instance,'ilp'))
                all_corr_values=corr.get_all_correlated_values(corr_content)
                corr_value=all_corr_values[len(all_corr_values.keys())]
                corr_time=corr.get_correlated_time(corr_content)
                corr_iter=len(all_corr_values.keys())
                corr_termination=corr.has_terminated(corr_content)

                greedy_corr_content=log.get_log_content(corr.get_file_path(n_target, instance,'greedy'))
                all_greedy_corr_values=corr.get_all_correlated_values(greedy_corr_content)
                greedy_corr_value=all_greedy_corr_values[len(all_greedy_corr_values.keys())]
                greedy_corr_iter=len(all_greedy_corr_values.keys())
                greedy_corr_termination=corr.has_terminated(greedy_corr_content)

                # update lists
                for n_restart in lp_values.keys():
                    LP_bar.append([n_target, instance, n_restart, lp_values[n_restart][0]/bar_values[1]])

                corr_bar.append([n_target, instance, corr_value/bar_values[1]])
                greedy_corr_bar.append([n_target, instance, greedy_corr_value/bar_values[1]])

                baron_low_up.append([n_target, instance, bar_values[0]/bar_values[2]])

                if corr_termination:
                    n_iter_corr.append([n_target, instance, corr_iter,'terminated'])
                else:
                    n_iter_corr.append([n_target, instance, corr_iter,'not_terminated'])

                if greedy_corr_termination:
                    n_iter_greedy_corr.append([n_target, instance, greedy_corr_iter,'terminated'])
                else:
                    n_iter_greedy_corr.append([n_target, instance, greedy_corr_iter,'not_terminated'])

                time_all.append([n_target, instance, corr_time, bar_time, lp_time])

                apx_ratio.append([n_target, instance, greedy_corr_value/corr_value])

                # update partial values for averages

                partial_bar_ratio += bar_values[0]/bar_values[2]

                partial_corr_ratio += corr_value/bar_values[1]
                partial_greedy_corr_ratio += greedy_corr_value/bar_values[1]

                for r in lp_values.keys():
                    partial_LP_ratio[r] = (partial_LP_ratio[r][0] + lp_values[r][0]/bar_values[1], partial_LP_ratio[r][1] + 1)

                if corr_termination:
                    partial_iter_corr['terminated'] = (partial_iter_corr['terminated'][0] + corr_iter, partial_iter_corr['terminated'][1] + 1)
                else:
                    partial_iter_corr['not_terminated'] = (partial_iter_corr['not_terminated'][0] + corr_iter, partial_iter_corr['not_terminated'][1] + 1)

                if greedy_corr_termination:
                    partial_iter_greedy_corr['terminated'] = (partial_iter_greedy_corr['terminated'][0] + greedy_corr_iter, partial_iter_greedy_corr['terminated'][1] + 1)
                else:
                    partial_iter_greedy_corr['not_terminated'] = (partial_iter_greedy_corr['not_terminated'][0] + greedy_corr_iter, partial_iter_greedy_corr['not_terminated'][1] + 1)

                partial_times['bar'] = partial_times['bar'] + bar_time
                partial_times['corr'] = partial_times['corr'] + corr_time
                partial_times['lp'] = partial_times['lp'] + lp_time

                partial_apx_ratio += greedy_corr_value/corr_value

            else:
                logging.warning('n target %d, n instance %d', n_target, instance)

            print 'Done t ',n_target,' i ',instance

        # update avg lists
        for r in partial_LP_ratio.keys():
            if partial_LP_ratio[r][1] != 0:
                LP_bar_avg.append([n_target, r, partial_LP_ratio[r][0]/partial_LP_ratio[r][1]])

        corr_bar_avg.append([n_target, partial_corr_ratio/instance_counter])
        greedy_corr_bar_avg.append([n_target, partial_greedy_corr_ratio/instance_counter])

        baron_low_up_avg.append([n_target, partial_bar_ratio/instance_counter])

        if partial_iter_corr['terminated'][1] != 0:
            n_iter_corr_avg.append([n_target, partial_iter_corr['terminated'][0]/partial_iter_corr['terminated'][1],'terminated'])
        if partial_iter_corr['not_terminated'][1] != 0:
            n_iter_corr_avg.append([n_target, partial_iter_corr['not_terminated'][0]/partial_iter_corr['not_terminated'][1],'not_terminated'])

        if partial_iter_greedy_corr['terminated'][1] != 0:
            n_iter_greedy_corr_avg.append([n_target, partial_iter_greedy_corr['terminated'][0]/partial_iter_greedy_corr['terminated'][1],'terminated'])
        if partial_iter_greedy_corr['not_terminated'][1] != 0:
            n_iter_greedy_corr_avg.append([n_target, partial_iter_greedy_corr['not_terminated'][0]/partial_iter_greedy_corr['not_terminated'][1],'not_terminated'])

        time_all_avg.append([n_target, partial_times['corr']/instance_counter, partial_times['bar']/instance_counter, partial_times['lp']/instance_counter])

        apx_ratio_avg.append([n_target, partial_apx_ratio/instance_counter])

    with open(LP_bar_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(LP_bar)
    with open(LP_bar_avg_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(LP_bar_avg)

    with open(corr_bar_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(corr_bar)
    with open(corr_bar_avg_path,'w') as f:
        writer = csv.writer(f)
        writer.writerows(corr_bar_avg)

    with open(baron_low_up_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(baron_low_up)
    with open(baron_low_up_avg_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(baron_low_up_avg)

    with open(n_iter_corr_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(n_iter_corr)
    with open(n_iter_corr_avg_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(n_iter_corr_avg)

    with open(time_all_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(time_all)
    with open(time_all_avg_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(time_all_avg)

    with open(greedy_corr_bar_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(greedy_corr_bar)
    with open(greedy_corr_bar_avg_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(greedy_corr_bar_avg)

    with open(n_iter_greedy_corr_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(n_iter_greedy_corr)
    with open(n_iter_greedy_corr_avg_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(n_iter_greedy_corr_avg)

    with open(apx_ratio_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(apx_ratio)
    with open(apx_ratio_avg_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(apx_ratio_avg)



if __name__ == '__main__':
    collect_results()