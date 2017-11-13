import unittest

from numpy import array
import numpy as np
from scipy.sparse import lil_matrix

import greedy_oracle


class Test_oracle(unittest.TestCase):

    def test_greedy_trivial(self):
        I={}
        I[1]=lil_matrix((2,2),dtype='int8')
        I[1][0,0]=1
        I[1][0,1]=1
        I[1][1,0]=1
        I[2]=lil_matrix((2,2),dtype='int8')
        I[2][0,0]=1
        I[2][1,1]=1
        I[1] = I[1].tocsr()
        I[2] = I[2].tocsr()

        br = greedy_oracle.generate_row(I, array([0.5, 0.5]), array([0.5, 0.9]))

        self.assertEqual(2,len(br))

        self.assertTrue((1,0) in br)

    def test_greedy_2(self):
        I={}
        I[1] = lil_matrix((3,4), dtype='int8')
        I[1][0,0] = 1
        I[1][1,0] = 1
        I[1][1,1] = 1
        I[1][2,1] = 1
        I[2] = lil_matrix((2,4), dtype='int8')
        I[2][0,2] = 1
        I[2][1,3] = 1
        I[3] = lil_matrix((2,4), dtype='int8')
        I[3][0,1] = 1
        I[3][1,1] = 1
        I[1] = I[1].tocsr()
        I[2] = I[2].tocsr()
        I[3] = I[3].tocsr()

        t_val = array([0.5, 0.5, 0.5, 0.5])
        sigma = array([0.4, 0.2, 0.0, 0.4])

        br = greedy_oracle.generate_row(I, sigma, t_val)

        self.assertEqual(3, len(br))
        self.assertTrue(((1,1) in br) and ((2,1) in br) )


    def test_greedy_not_optimal_choice(self):
        I={}
        I[1] = lil_matrix((3,4), dtype='int8')
        I[1][0,0] = 1
        I[1][1,0] = 1
        I[1][1,1] = 1
        I[1][2,2] = 1
        I[2] = lil_matrix((1,4), dtype='int8')
        I[2][0,0] = 1
        I[3] = lil_matrix((1,4), dtype='int8')
        I[3][0,1] = 1
        I[1] = I[1].tocsr()
        I[2] = I[2].tocsr()
        I[3] = I[3].tocsr()

        t_val = array([0.5, 0.5, 0.5, 0.5])
        sigma = array([0.2, 0.4, 0.4, 0.0])

        br = greedy_oracle.generate_row(I, sigma, t_val)

        self.assertEqual(3, len(br))
        self.assertTrue((1,1) in br)

    def test_different_t_val(self):
        I={}
        I[1] = lil_matrix((3,4), dtype='int8')
        I[1][0,0] = 1
        I[1][1,0] = 1
        I[1][1,1] = 1
        I[1][2,2] = 1
        I[2] = lil_matrix((1,4), dtype='int8')
        I[2][0,0] = 1
        I[3] = lil_matrix((1,4), dtype='int8')
        I[3][0,1] = 1
        I[1] = I[1].tocsr()
        I[2] = I[2].tocsr()
        I[3] = I[3].tocsr()

        t_val = array([0.1, 0.1, 0.9, 0.5])
        sigma = array([0.3, 0.3, 0.3, 0.1])

        br = greedy_oracle.generate_row(I, sigma, t_val)

        self.assertEqual(3, len(br))
        self.assertTrue((1,2) in br)


if __name__ == '__main__':
    unittest.main()