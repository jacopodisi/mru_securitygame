import unittest

import numpy
import scipy.io as scio

import mat_parser

file_path='/Users/macosx/Documents/polimi/tesi/patrolling_games/ntargets_40_instance_1.mat'

class Test_mat_parser(unittest.TestCase):


    def test_sum_to_one(self):

        U= mat_parser.parse_mat(file_path)

        u_team=U[0]
        u_attacker=U[1]

        # iterates over the cells of one of the two matrix and check that corresponding
        # elements sum to 0
        it=numpy.nditer(u_team,flags=['multi_index'])

        while not it.finished:
            index=it.multi_index

            self.assertEqual(0.0, it[0]+u_attacker[index])

            it.iternext()



    def test_utilities(self):

        mat_file=scio.loadmat(file_path)

        n_pl_team=len(mat_file['M_routes'])

        values=mat_file['I']['valuesVec'][0][0][0]

        # Dict <pl, Dict <action, route>>
        d={}
        for pl in range(0,n_pl_team):
            d[pl]={}

            routes=mat_file['M_routes'][pl][0]

            action_number=0
            for route in routes:
                d[pl][action_number]=route[0][0]
                action_number+=1

        U= mat_parser.parse_mat('/Users/macosx/Documents/polimi/tesi/patrolling_games/ntargets_40_instance_1.mat')
        u_team=U[0]

        it=numpy.nditer(u_team,flags=['multi_index'])
        while not it.finished:

            indexes=it.multi_index

            covered=[]

            for pl in range(0,n_pl_team):

                n_a=indexes[pl+1] # +1 --> first position: action of the minimizer

                covered.extend(list(d[pl][n_a]))

            covered=set(covered)

            if it[0]==0.5:
                self.assertTrue(indexes[0] in covered)
            else:
                self.assertEqual(it[0],0.5-values[indexes[0]])

            if indexes[0] in covered:
                self.assertEqual(0.5,it[0])
            else:
                self.assertEqual(0.5-values[indexes[0]],it[0])


            it.iternext()





if __name__ == '__main__':
    unittest.main()