import unittest
import correlated_row_gen
from scipy.sparse import lil_matrix
from scipy.sparse import isspmatrix_lil
from numpy import testing

class Test_update_joint_I(unittest.TestCase):

    def test_empty_joint_I(self):

        n_targets=3
        joint_I=lil_matrix((0,n_targets),dtype='int8')

        I={}
        I[1]=lil_matrix((2,3),dtype='int8')
        I[1][0,0]=1
        I[1][1,1]=1
        I[1]=I[1].tocsr()
        I[2]=lil_matrix((2,3),dtype='int8')
        I[2][0,0]=1
        I[2][1,1]=1
        I[2][1,2]=1
        I[2]=I[2].tocsr()

        selected_routes={}

        new_joint_route=[[(1,0),(2,0)]]

        joint_I=correlated_row_gen.update_joint_I(joint_I, selected_routes, new_joint_route, I)

        self.assertEqual(joint_I.shape,(1,3))
        self.assertEqual(joint_I.toarray().tolist(),[[1,0,0]])

        self.assertEqual(selected_routes, {0:[(1,0),(2,0)]})

    def test_update_joint_I(self):

        n_targets=3
        joint_I=lil_matrix((1,n_targets),dtype='int8')
        joint_I[0,0]=1

        I={}
        I[1]=lil_matrix((2,3),dtype='int8')
        I[1][0,0]=1
        I[1][1,1]=1
        I[1]=I[1].tocsr()
        I[2]=lil_matrix((2,3),dtype='int8')
        I[2][0,0]=1
        I[2][1,1]=1
        I[2][1,2]=1
        I[2]=I[2].tocsr()

        selected_routes={}
        selected_routes[0]=[(1,0),(2,0)]

        new_route=[[(1,0),(2,1)]]

        joint_I=correlated_row_gen.update_joint_I(joint_I, selected_routes, new_route, I)

        self.assertEqual(joint_I.toarray().tolist(), [[1,0,0],[1,1,1]])

        self.assertEqual(isspmatrix_lil(joint_I),True)

        self.assertEqual(selected_routes,{0:[(1,0),(2,0)], 1:[(1,0),(2,1)]})


# class Test_correlated_row_gen(unittest.TestCase):

#     def test_random_game_basic(self):
#         pickle_path='./pickle_test.pickle'

#         res=correlated_row_gen.correlated(pickle_path)

#         testing.assert_almost_equal(res[0], 0.96667, decimal=5)


#     def test_random_game_advanced(self):
#          pickle_path='./pickle_test2.pickle'

#          res=correlated_row_gen.correlated(pickle_path)

#          testing.assert_almost_equal(res[0], 0.92373, decimal=5)

class Test_random_init(unittest.TestCase):

    def test_init_random_routes(self):
        I={}
        I[1]=lil_matrix((2,3),dtype='int8')
        I[2]=lil_matrix((3,3),dtype='int8')
        I[1][0,0]=1
        I[1][1,1]=1
        I[2][0,2]=1
        I[2][1,0]=1
        I[2][1,1]=1
        I[2][2,0]=1
        I[1]=I[1].tocsr()
        I[2]=I[2].tocsr()

        for i in range(0,10):
            r=correlated_row_gen.pick_random_joint_route(I)

            self.assertEqual(len(r),2)
            for s in r:
                if s[0]==1:
                    self.assertTrue(s[1]>=0 and s[1]<2)
                elif s[0]==2:
                    self.assertTrue(s[1]>=0 and s[1]<3)



        

if __name__ == '__main__':
    unittest.main()