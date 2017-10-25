import sys
import scipy.io as scipyio
from scipy.sparse import lil_matrix
from scipy.sparse import csc_matrix
import patrolling.LP_iterated.pickle


#####################################################################################
# It reads .mat file containing the given patrolling instance
# It outputs a .pickle file containing, in order:
#       1 -  dict <pl,csc_matrix> (where the matrix is I for the key player, so routes x target matrix)
#       2 - array with ordered target values
#####################################################################################

def build_pickle(mat_path, pickle_path):
    """
    Builds data required to run LP iterated alg.
    Saves them in a pickle file for later use.

    :param mat_path: path of the patrolling instance .mat file
    :param pickle_path: where to save the new .pickle file
    :return:
    """
    try:
        mat_dict = scipyio.loadmat(mat_path, variable_names=['n_targets','M_routes','I'])

        n_pl_team = len(mat_dict['M_routes'])
        n_targets = mat_dict['n_targets'][0][0]
        target_values=mat_dict['I']['valuesVec'][0][0][0]

        # I is the final dict to be saved
        I={}
        for pl in range(0,n_pl_team):
            I[pl+1]={}
            routes_list=mat_dict['M_routes'][pl][0]

            # empty lil_matrix used to build efficiently the sparse matrix for player pl
            # later converted to csc matrix for better performance on column slicing
            temp_i=lil_matrix((len(routes_list),n_targets), dtype='int8')

            # fill the lil_matrix with 1s when target t is covered by route r
            for r in range(0,len(routes_list)):
                route=routes_list[r]
                for covered_target in route:
                    temp_i[r, covered_target-1]=1

            # lil_matrix -> csc_matrix
            temp_i=temp_i.tocsc()

            I[pl+1]=temp_i


        # save data to the pickle file
        with open(pickle_path,'wb') as f:
            pickle.dump(I, f, -1)
            pickle.dump(target_values, f, -1)

    except IOError:
        print('Error building pickle file for mat file:')
        print(mat_path)


if __name__ == '__main__':
    ntargets=sys.argv[1]
    instance=sys.argv[2]

    mat_path='./mat/ntargets_'+ntargets+'/ntargets_'+ntargets+'_instance_'+instance+'.mat'
    pickle_path='./pickle/ntargets_'+ntargets+'/ntargets_'+ntargets+'_instance_'+instance+'.pickle'

    build_pickle(mat_path, pickle_path)

