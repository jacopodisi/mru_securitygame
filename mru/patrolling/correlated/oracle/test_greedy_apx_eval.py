import unittest

from numpy import array
from scipy.sparse import lil_matrix

import greedy_apx_eval

class Test_oracle(unittest.TestCase):

    def test_get_ratio(self):

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


        val = greedy_apx_eval.get_value([(1,1), (2,0), (3,0)], I, t_val, sigma)

        self.assertEqual(val, 0.8)

if __name__ == '__main__':
    unittest.main()