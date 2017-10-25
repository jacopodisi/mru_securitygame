import unittest
from scipy.sparse import lil_matrix
from scipy.sparse import csc_matrix
from numpy import array
import LP_iterated as lp


class Test_LP_iterated(unittest.TestCase):

    def test_compute_coefficients(self):
        I={}

        m0=lil_matrix((3,3),dtype='int8').tocsc()
        I[0]=m0

        m1=lil_matrix((3,3),dtype='int8')
        m1[0,1]=1
        m1[0,2]=1
        m1[1,0]=1
        m1[2,1]=1
        I[1]=m1.tocsc()

        m2=lil_matrix((4,3),dtype='int8')
        m2[0,1]=1
        m2[1,0]=1
        m2[2,0]=1
        m2[2,1]=1
        m2[3,1]=1
        m2[3,2]=1
        I[2]=m2.tocsc()

        P={}
        P[0]=array([1,0,0])
        P[1]=array([0.5, 0.25, 0.25])
        P[2]=array([0.0, 0.4, 0.6, 0.0])

        free_pl=0

        coeff=lp.compute_coefficients(free_pl,I,P)

        self.assertListEqual(coeff,[0,0.1,0.5])

if __name__ == '__main__':
    unittest.main()