import unittest
import LP_2pl_solver as LP
from scipy.sparse import lil_matrix
from numpy import array
import numpy.testing as nptest

class Test_LP_2pl_solver(unittest.TestCase):
    def test_maxmin_minmax(self):
        # check that minmax and maxmin results coincide
        I_joint=lil_matrix((2,2),dtype='int8')
        I_joint[0,0]=1
        I_joint[1,1]=1

        target_values=array([0.9, 0.4])

        res_maxmin=LP.maxmin(I_joint, target_values)
        res_minmax=LP.minmax(I_joint, target_values)

        nptest.assert_almost_equal(res_maxmin[0], 0.72308, decimal=5)
        nptest.assert_almost_equal(res_minmax[0], 0.72308, decimal=5)

        # check strategies
        nptest.assert_almost_equal(res_maxmin[1], array([0.69231, 0.30769]), decimal=5)
        nptest.assert_almost_equal(res_minmax[1], array([0.30769, 0.69231]), decimal=5)



    def test_trivial_instance(self):

         I_joint=lil_matrix((3,5),dtype='int8')
         for col in range(0,5):
             I_joint[0,col]=1
         I_joint[1,0]=1


         target_values=array([0.9, 0.3, 0.12, 0.0, 0.2])

         res_maxmin=LP.maxmin(I_joint, target_values)
         res_minmax=LP.minmax(I_joint, target_values)

         self.assertEqual(res_maxmin[0],1.0)
         self.assertEqual(res_minmax[0],1.0)

         self.assertEqual(res_maxmin[1][0],1.0)
         self.assertEqual(res_maxmin[1][1],0.0)
         self.assertEqual(res_maxmin[1][2],0.0)

         print('attacker\'s strategy')
         print(res_minmax[1])

    def test_maxmin_minmax_2(self):
        I_joint=lil_matrix((6,3),dtype='int8')
        I_joint[0,0]=1
        I_joint[0,2]=1
        I_joint[1,0]=1
        I_joint[1,1]=1
        I_joint[2,0]=1
        I_joint[3,1]=1
        I_joint[3,2]=1
        I_joint[4,0]=1
        I_joint[4,1]=1
        I_joint[5,0]=1
        I_joint[5,1]=1

        target_values=array([0.9, 0.5, 0.1])

        res_minmax=LP.minmax(I_joint,target_values)
        res_maxmin=LP.maxmin(I_joint,target_values)

        nptest.assert_almost_equal(res_maxmin[0], 0.92373, decimal=5)
        nptest.assert_almost_equal(res_minmax[0], 0.92373, decimal=5)

        # check strategies
        nptest.assert_almost_equal(res_maxmin[1][0], 0.15254, decimal=5)
        nptest.assert_almost_equal(res_maxmin[1][3], 0.08475, decimal=5)
        nptest.assert_almost_equal(res_minmax[1], array([0.08475, 0.15254, 0.76271 ]), decimal=5)


if __name__ == '__main__':
    unittest.main()