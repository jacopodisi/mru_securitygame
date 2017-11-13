import unittest

from numpy import array
from scipy.sparse import lil_matrix

import ilp_oracle


class Test_oracle(unittest.TestCase):

    def test_row_generation_trivial(self):
        I={}
        temp=lil_matrix((2,3),dtype='int8')
        temp[0,0]=1
        temp[0,1]=1
        I[1]=temp.tocsc()
        temp=lil_matrix((3,3),dtype='int8')
        temp[1,2]=1
        temp[2,0]=1
        temp[2,1]=1
        I[2]=temp.tocsc()


        target_values=array([0.25, 0.99, 0.1])

        att_strategy=array([0.5, 0.25, 0.25])

        br= ilp_oracle.generate_row(I, att_strategy, target_values)

        self.assertEqual(br,[(1,0),(2,1)])

    def test_row_generation_equal_routes(self):
        I={}
        I[1]=lil_matrix((2,3),dtype='int8')
        I[1][0,0]=1
        I[1][0,1]=1
        I[2]=lil_matrix((3,3),dtype='int8')
        I[2][1,2]=1
        I[2][2,0]=1
        I[2][2,1]=1
        I[2][0,2]=1

        target_values=array([0.25, 0.99, 0.1])

        att_strategy=array([0.5, 0.25, 0.25])

        br= ilp_oracle.generate_row(I, att_strategy, target_values)

        self.assertEqual(len(br),2)

    def test_row_generation(self):
        I={}
        temp=lil_matrix((2,3),dtype='int8')
        temp[0,0]=1
        temp[1,1]=1
        I[1]=temp.tocsc()
        temp=lil_matrix((2,3),dtype='int8')
        temp[0,1]=1
        temp[1,2]=1
        I[2]=temp.tocsc()

        target_values=array([0.9, 0.5, 0.2])
        att_strategy=array([0.33, 0.33, 0.34])

        br= ilp_oracle.generate_row(I, att_strategy, target_values)

        self.assertEqual(br,[(1,0),(2,0)])



if __name__ == '__main__':
    unittest.main()


