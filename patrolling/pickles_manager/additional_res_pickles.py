import pickle
import sys

#######################################################################################################################
# This script is used to generate pickles with an increasing number of patrollers per guard post.
# A standard pickle is made of:
#       1 -  dict <pl,csc_matrix> (where the matrix is I for the key player, so routes x target matrix)
#       2 - array with ordered target values
# (2) remains unchanged.
# (1) -> for each pl add X new pl with the same csc_matrix
#######################################################################################################################

def add_players(original_pickle_path, new_pickle_path, n_additional_res):
    """

    :param original_pickle_path:
    :param new_pickle_path:
    :param n_additional_res: number of resources to be added to each guard post
    :return:
    """
    # read original pickle
    with open(original_pickle_path,'rb') as pickle_file:
        I = pickle.load(pickle_file) # dict <pl, csc_matrix>
        target_values = pickle.load(pickle_file) # ordered array of targets' values

    original_n_pl = len(I.keys())

    # id (key) of the new players
    new_pl_id = original_n_pl + 1

    for original_pl in I.keys():

        m = I[original_pl]

        for i in range(0,n_additional_res):

            I[new_pl_id] = m
            new_pl_id += 1

    # save data to the new pickle file
    with open(new_pickle_path,'wb') as f:
        pickle.dump(I, f, -1)
        pickle.dump(target_values, f, -1)


if __name__ == '__main__':
    ntargets = sys.argv[1]
    instance = sys.argv[2]
    n_res_to_add = sys.argv[3]

    old_pickle_path = './pickle/ntargets_'+ntargets+'/ntargets_'+ntargets+'_instance_'+instance+'.pickle'
    new_pickle_path = './extended_pickles/ntargets_'+ntargets+\
                      '/added_'+n_res_to_add+'/ntargets_'+ntargets+\
                      '_instance_'+instance+'_added_'+n_res_to_add+'.pickle'

    add_players(old_pickle_path, new_pickle_path, int(n_res_to_add))

