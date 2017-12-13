import scipy.io as scipyio
import os
import sys

#####################################
# .mat --> .dat
# From the patrolling instance in a given .mat file it builds the corresponding
#   .dat  required to run the exact alg. for team-maxmin (ampl + baron)
#####################################

def build_dat(mat_path, result_path):
    """
    create a .dat file from the patrolling instance of the given .mat file

    Required data in the .dat:
        - Sets: players, targets, routes for each pl.
        - Params: I (I[p,r,t]=1 iff player p covers t with route r, 0 otherwise),
            values of targets

    :param mat_path: .mat file path
    :param result_path: where to save the .dat
    :return: -
    """
    try:
        mat_dict = scipyio.loadmat(mat_path, variable_names=['n_targets','M_routes','I'])

        n_pl_team = len(mat_dict['M_routes'])
        n_targets = mat_dict['n_targets'][0][0]
        target_values=mat_dict['I']['valuesVec'][0][0][0]

        # build a dict of type <pl,<route_id,covered targets>>
        covering_routes={}
        for pl in range(0,n_pl_team):
            covering_routes[pl+1]={}
            routes_list=mat_dict['M_routes'][pl][0]
            for route in range(1,len(routes_list)+1):
                covering_routes[pl+1][route]=routes_list[route-1][0][0]


        fout=open(os.path.join(os.getcwd(),result_path), "w")

        fout.write("data;\n\n")

        # set of players
        s='set P := '
        for pl in range(1,n_pl_team+1):
            s = s + ' ' + str(pl)
        s = s + ';\n'
        fout.write(s)

        # set of targets
        s='set T := '
        for t in range(1,n_targets+1):
            s = s + ' ' + str(t)
        s = s + ';\n'
        fout.write(s)

        # set of routes for each target
        s=''
        for pl in range(1,n_pl_team+1):
            s=s + 'set R[' + str(pl) + '] :='
            for r in covering_routes[pl].keys():
                s = s + ' ' + str(r)
            s = s + ';\n'
        s = s + '\n'
        fout.write(s)

        # param I
        p='param I default 0 :=\n'
        fout.write(p);

        default_top_string=',*,*]:'
        for t in range(1,n_targets+1):
            default_top_string = default_top_string + ' ' + str (t)
        default_top_string = default_top_string + ' :=\n'

        p=''
        for pl in range(1,n_pl_team+1):
            p = '[' + str(pl) + default_top_string
            for r in covering_routes[pl].keys():
                p = p + ' ' + str(r)
                for t in range(1,n_targets+1):
                    if t in covering_routes[pl][r]:
                        p = p + ' 1'
                    else:
                        p = p + ' .'
                p = p + '\n'
            fout.write(p)

        # param V
        fout.write(';\nparam V := \n')
        p = ''
        for t in range(1,n_targets+1):
            p = p + str(t) + ' ' + str(target_values[t-1]) + '\n'
        p = p +';'
        fout.write(p)

        fout.close()

    except IOError:
        print ('Patrolling .mat file not found. Wrong path:')
        print (mat_path)



if __name__ == '__main__':

    ntargets=sys.argv[1]
    instance=sys.argv[2]

    mat_path='./mat/ntargets_'+ntargets+'/ntargets_'+ntargets+'_instance_'+instance+'.mat'
    dat_path='./dat/ntargets_'+ntargets+'/ntargets_'+ntargets+'_instance_'+instance+'.dat'

    build_dat(mat_path,dat_path)