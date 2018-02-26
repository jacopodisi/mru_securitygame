import unittest
from .. import computevalue as cv
from ..srg import graph as gr
import numpy as np
import testfunctions as tf


class TestComputeValue1(unittest.TestCase):
    """
    Figure 1 Graph  (1 SS, 1 MR)
    """

    @classmethod
    def setUpClass(cls):
        print 'setupClass'
        cls.v0 = gr.Vertex(0, 0, 0)
        cls.v1 = gr.Vertex(1, 0.5, 4)
        cls.v2 = gr.Vertex(1, 0.5, 4)
        cls.v3 = gr.Vertex(1, 0.5, 4)
        cls.v4 = gr.Vertex(1, 0.5, 4)

        cls.G = gr.Graph(np.array([cls.v0, cls.v1, cls.v2, cls.v3, cls.v4]))
        cls.G.setAdjacents(cls.v0, np.array([0, 1, 1, 1, 1]))
        cls.G.setAdjacents(cls.v1, np.array([1, 0, 1, 0, 0]))
        cls.G.setAdjacents(cls.v2, np.array([1, 1, 0, 0, 0]))
        cls.G.setAdjacents(cls.v3, np.array([1, 0, 0, 0, 1]))
        cls.G.setAdjacents(cls.v4, np.array([1, 0, 0, 1, 0]))

    def test_compute_shortest_sets(self):
        f = cv.compute_shortest_sets
        result, _ = f(self.G, self.G.getTargets())

        shortest_sets = np.array(
            [[0, 1, 1, 1, 1],
             [0, 1, 1, 1, 1],
             [0, 1, 1, 1, 1],
             [0, 1, 1, 1, 1],
             [0, 1, 1, 1, 1]])
        ok = (result == shortest_sets).all()
        ms = "Error computing the shortest sets\nResult:\n" \
            + str(result) + "\nShould be:\n" + str(shortest_sets)
        self.assertTrue(ok, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_covering_routes(self):
        f = cv.compute_covering_routes
        cov_routes = f(self.G, self.G.getTargets())

        result0 = cov_routes[self.v0.getVertexNumber()].toarray()
        cov_route_0 = np.array(
            [[1, 0, 0, 0, 0],
             [1, 1, 0, 0, 0],
             [1, 0, 1, 0, 0],
             [1, 0, 0, 1, 0],
             [1, 0, 0, 0, 1],
             [1, 1, 1, 0, 0],
             [1, 1, 0, 1, 0],
             [1, 1, 0, 0, 1],
             [1, 0, 1, 1, 0],
             [1, 0, 1, 0, 1],
             [1, 0, 0, 1, 1],
             [1, 1, 1, 1, 0],
             [1, 1, 1, 0, 1],
             [1, 1, 0, 1, 1],
             [1, 0, 1, 1, 1]])
        ok0 = tf.compare_row_mat(result0, cov_route_0)
        ms = "Error computing the covering routes v0\nResult:\n" \
            + str(result0) + "\nShould be:\n" + str(cov_route_0)
        self.assertTrue(ok0, msg=ms)

        result4 = cov_routes[self.v4.getVertexNumber()].toarray()
        cov_route_4 = np.array(
            [[0, 0, 0, 0, 1],
             [0, 1, 0, 0, 1],
             [0, 0, 1, 0, 1],
             [0, 0, 0, 1, 1],
             [0, 1, 1, 0, 1],
             [0, 0, 1, 1, 1],
             [0, 1, 0, 1, 1],
             [0, 1, 1, 1, 1]])
        ok4 = tf.compare_row_mat(result4, cov_route_4)
        ms = "Error computing the covering routes v4\nResult:\n" \
            + str(result4) + "\nShould be:\n" + str(cov_route_4)
        self.assertTrue(ok4, msg=ms)

        dom_cov_routes = f(self.G, self.G.getTargets(), True)
        dom_result0 = dom_cov_routes[self.v0.getVertexNumber()].toarray()
        dom_cov_route_0 = np.array(
            [[1, 1, 1, 1, 0],
             [1, 1, 1, 0, 1],
             [1, 1, 0, 1, 1],
             [1, 0, 1, 1, 1]])
        ok0_d = tf.compare_row_mat(dom_result0, dom_cov_route_0)
        ms = "Error computing the dominating covering routes v0\nResult:\n" \
            + str(dom_result0) + "\nShould be:\n" + str(dom_cov_route_0)
        self.assertTrue(ok0_d, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_values(self):
        compvalres = cv.compute_values(self.G, True)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 1}
        res_num_iter = 0
        res_plac = {1: [(1, 4)]}
        res_strat = {1: [([(1, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertEqual(strat, res_strat, msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_2(self):
        compvalres = cv.compute_values(self.G, True, enumtype=2)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 1}
        res_num_iter = 0
        res_plac = {1: [(1, 4)]}
        res_strat = {1: [([(1, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertEqual(strat, res_strat, msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)


class TestComputeValue2(unittest.TestCase):
    """
    Figure 1 Graph  (4 SS, 4 MR)
    """

    @classmethod
    def setUpClass(cls):
        print 'setupClass'
        cls.v0 = gr.Vertex(0, 0, 0)
        cls.v1 = gr.Vertex(1, 0.5, 0)
        cls.v2 = gr.Vertex(1, 0.5, 0)
        cls.v3 = gr.Vertex(1, 0.5, 0)
        cls.v4 = gr.Vertex(1, 0.5, 0)

        cls.G = gr.Graph(np.array([cls.v0, cls.v1, cls.v2, cls.v3, cls.v4]))
        cls.G.setAdjacents(cls.v0, np.array([0, 1, 1, 1, 1]))
        cls.G.setAdjacents(cls.v1, np.array([1, 0, 1, 0, 0]))
        cls.G.setAdjacents(cls.v2, np.array([1, 1, 0, 0, 0]))
        cls.G.setAdjacents(cls.v3, np.array([1, 0, 0, 0, 1]))
        cls.G.setAdjacents(cls.v4, np.array([1, 0, 0, 1, 0]))

    def test_compute_shortest_sets(self):
        f = cv.compute_shortest_sets
        result, _ = f(self.G, self.G.getTargets())

        shortest_sets = np.array(
            [[0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 0, 1]])
        ok = (result == shortest_sets).all()
        ms = "Error computing the shortest sets\nResult:\n" \
            + str(result) + "\nShould be:\n" + str(shortest_sets)
        self.assertTrue(ok, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_covering_routes(self):
        f = cv.compute_covering_routes
        cov_routes = f(self.G, self.G.getTargets())

        result0 = cov_routes[self.v0.getVertexNumber()].toarray()
        cov_route_0 = np.array([[1, 0, 0, 0, 0]])
        ok = tf.compare_row_mat(result0, cov_route_0)
        ms = "Error computing the covering routes v0\nResult:\n" \
            + str(result0) + "\nShould be:\n" + str(cov_route_0)
        self.assertTrue(ok, msg=ms)

        result4 = cov_routes[self.v4.getVertexNumber()].toarray()
        cov_route_4 = np.array([[0, 0, 0, 0, 1]])
        ok = tf.compare_row_mat(result4, cov_route_4)
        ms = "Error computing the covering routes v4\nResult:\n" \
            + str(result4) + "\nShould be:\n" + str(cov_route_4)
        self.assertTrue(ok, msg=ms)

        dom_cov_routes = f(self.G, self.G.getTargets(), True)
        dom_result0 = dom_cov_routes[self.v0.getVertexNumber()].toarray()
        dom_cov_route_0 = np.array(
            [[1, 0, 0, 0, 0]])
        ok0_d = tf.compare_row_mat(dom_result0, dom_cov_route_0)
        ms = "Error computing the dominating covering routes v0\nResult:\n" \
            + str(dom_result0) + "\nShould be:\n" + str(dom_cov_route_0)
        self.assertTrue(ok0_d, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_values(self):
        compvalres = cv.compute_values(self.G, True)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {4: 1}
        res_num_iter = 0
        res_plac = {4: [(1, 1), (2, 2), (3, 3), (4, 4)]}
        res_strat = {4: [([(1, 0), (2, 0), (3, 0), (4, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertEqual(strat, res_strat, msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_2(self):
        compvalres = cv.compute_values(self.G, True, enumtype=2)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {4: 1}
        res_num_iter = 0
        res_plac = {4: [(1, 1), (2, 2), (3, 3), (4, 4)]}
        res_strat = {4: [([(1, 0), (2, 0), (3, 0), (4, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertEqual(strat, res_strat, msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)


class TestComputeValue3(unittest.TestCase):
    """
    Linear graph (1 SS, 1 MR)
    """

    @classmethod
    def setUpClass(cls):
        print 'setupClass'
        cls.v0 = gr.Vertex(1, 0.5, 6)
        cls.v1 = gr.Vertex(1, 0.5, 1)
        cls.v2 = gr.Vertex(1, 0.5, 0)
        cls.v3 = gr.Vertex(1, 0.5, 3)
        cls.v4 = gr.Vertex(1, 0.5, 10)

        cls.G = gr.Graph(np.array([cls.v0, cls.v1, cls.v2, cls.v3, cls.v4]))
        cls.G.setAdjacents(cls.v0, np.array([0, 1, 0, 0, 0]))
        cls.G.setAdjacents(cls.v1, np.array([1, 0, 1, 0, 0]))
        cls.G.setAdjacents(cls.v2, np.array([0, 1, 0, 1, 0]))
        cls.G.setAdjacents(cls.v3, np.array([0, 0, 1, 0, 1]))
        cls.G.setAdjacents(cls.v4, np.array([0, 0, 0, 1, 0]))

    def test_compute_shortest_sets(self):
        f = cv.compute_shortest_sets
        result, _ = f(self.G, self.G.getTargets())

        shortest_sets = np.array(
            [[1, 1, 0, 1, 1],
             [1, 1, 0, 1, 1],
             [1, 1, 1, 1, 1],
             [1, 0, 0, 1, 1],
             [1, 0, 0, 1, 1]])
        ok = (result == shortest_sets).all()
        ms = "Error computing the shortest sets\nResult:\n" \
            + str(result) + "\nShould be:\n" + str(shortest_sets)
        self.assertTrue(ok, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_covering_routes(self):
        f = cv.compute_covering_routes
        cov_routes = f(self.G, self.G.getTargets())

        result2 = cov_routes[self.v2.getVertexNumber()].toarray()
        cov_route_2 = np.array(
            [[0, 0, 1, 0, 0],
             [0, 1, 1, 0, 0],
             [0, 1, 1, 1, 0],
             [1, 1, 1, 1, 0],
             [0, 1, 1, 1, 1],
             [1, 1, 1, 1, 1],
             [1, 1, 1, 0, 0],
             [1, 1, 1, 0, 1],
             [0, 0, 1, 1, 0],
             [1, 0, 1, 1, 0],
             [0, 0, 1, 1, 1],
             [1, 0, 1, 1, 1]])
        ok = tf.compare_row_mat(result2, cov_route_2)
        ms = "Error computing the covering routes v2\nResult:\n" \
            + str(result2) + "\nShould be:\n" + str(cov_route_2)
        self.assertTrue(ok, msg=ms)

        result4 = cov_routes[self.v4.getVertexNumber()].toarray()
        cov_route_4 = np.array(
            [[0, 0, 0, 0, 1],
             [0, 0, 0, 1, 1],
             [1, 0, 0, 1, 1]])
        ok = tf.compare_row_mat(result4, cov_route_4)
        ms = "Error computing the covering routes v4\nResult:\n" \
            + str(result4) + "\nShould be:\n" + str(cov_route_4)
        self.assertTrue(ok, msg=ms)

        dom_cov_routes = f(self.G, self.G.getTargets(), True)
        dom_result2 = dom_cov_routes[self.v2.getVertexNumber()].toarray()
        dom_cov_route_2 = np.array(
            [[1, 1, 1, 1, 1]])
        ok2_d = tf.compare_row_mat(dom_result2, dom_cov_route_2)
        ms = "Error computing the dominating covering routes v0\nResult:\n" \
            + str(dom_result2) + "\nShould be:\n" + str(dom_cov_route_2)
        self.assertTrue(ok2_d, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_values(self):
        compvalres = cv.compute_values(self.G, True)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 1}
        res_num_iter = 0
        res_plac = {1: [(1, 2)]}
        res_strat = {1: [([(1, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertEqual(strat, res_strat, msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_2(self):
        compvalres = cv.compute_values(self.G, True, enumtype=2)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 1}
        res_num_iter = 0
        res_plac = {1: [(1, 2)]}
        res_strat = {1: [([(1, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertEqual(strat, res_strat, msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)


class TestComputeValue4(unittest.TestCase):
    """
    Linear graph (1 SS, 2 MR)
    """

    @classmethod
    def setUpClass(cls):
        print 'setupClass'
        cls.v0 = gr.Vertex(1, 0.5, 2)
        cls.v1 = gr.Vertex(1, 0.5, 1)
        cls.v2 = gr.Vertex(1, 0.5, 0)
        cls.v3 = gr.Vertex(1, 0.5, 3)
        cls.v4 = gr.Vertex(1, 0.5, 10)

        cls.G = gr.Graph(np.array([cls.v0, cls.v1, cls.v2, cls.v3, cls.v4]))
        cls.G.setAdjacents(cls.v0, np.array([0, 1, 0, 0, 0]))
        cls.G.setAdjacents(cls.v1, np.array([1, 0, 1, 0, 0]))
        cls.G.setAdjacents(cls.v2, np.array([0, 1, 0, 1, 0]))
        cls.G.setAdjacents(cls.v3, np.array([0, 0, 1, 0, 1]))
        cls.G.setAdjacents(cls.v4, np.array([0, 0, 0, 1, 0]))

    def test_compute_shortest_sets(self):
        f = cv.compute_shortest_sets
        result, _ = f(self.G, self.G.getTargets())

        shortest_sets = np.array(
            [[1, 1, 0, 1, 1],
             [1, 1, 0, 1, 1],
             [1, 1, 1, 1, 1],
             [0, 0, 0, 1, 1],
             [0, 0, 0, 1, 1]])
        ok = (result == shortest_sets).all()
        ms = "Error computing the shortest sets\nResult:\n" \
            + str(result) + "\nShould be:\n" + str(shortest_sets)
        self.assertTrue(ok, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_covering_routes(self):
        f = cv.compute_covering_routes
        cov_routes = f(self.G, self.G.getTargets())

        result2 = cov_routes[self.v2.getVertexNumber()].toarray()
        cov_route_2 = np.array(
            [[0, 0, 1, 0, 0],
             [0, 1, 1, 0, 0],
             [0, 1, 1, 1, 0],
             [0, 1, 1, 1, 1],
             [1, 1, 1, 0, 0],
             [1, 1, 1, 0, 1],
             [0, 0, 1, 1, 0],
             [0, 0, 1, 1, 1]])
        ok = tf.compare_row_mat(result2, cov_route_2)
        ms = "Error computing the covering routes v2\nResult:\n" \
            + str(result2) + "\nShould be:\n" + str(cov_route_2)
        self.assertTrue(ok, msg=ms)

        result4 = cov_routes[self.v4.getVertexNumber()].toarray()
        cov_route_4 = np.array(
            [[0, 0, 0, 0, 1],
             [0, 0, 0, 1, 1]])
        ok = tf.compare_row_mat(result4, cov_route_4)
        ms = "Error computing the covering routes v4\nResult:\n" \
            + str(result4) + "\nShould be:\n" + str(cov_route_4)
        self.assertTrue(ok, msg=ms)

        dom_cov_routes = f(self.G, self.G.getTargets(), True)
        dom_result2 = dom_cov_routes[self.v2.getVertexNumber()].toarray()
        dom_cov_route_2 = np.array(
            [[0, 1, 1, 1, 1],
             [1, 1, 1, 0, 1]])
        ok2_d = tf.compare_row_mat(dom_result2, dom_cov_route_2)
        ms = "Error computing the dominating covering routes v0\nResult:\n" \
            + str(dom_result2) + "\nShould be:\n" + str(dom_cov_route_2)
        self.assertTrue(ok2_d, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_values(self):
        compvalres = cv.compute_values(self.G, True, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 1
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 4)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertItemsEqual(strat[1], res_strat[1], msg=ms)
        self.assertItemsEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_2(self):
        compvalres = cv.compute_values(self.G, True, enum=10, enumtype=2)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 1
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 4)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertItemsEqual(strat[1], res_strat[1], msg=ms)
        self.assertItemsEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_3(self):
        compvalres = cv.compute_values(self.G, True, enum=10, enumtype=3)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 1
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 4)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertItemsEqual(strat[1], res_strat[1], msg=ms)
        self.assertItemsEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_4(self):
        compvalres = cv.compute_values(self.G, True, enum=10, enumtype=4)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 1
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 4)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 0)], 1.0)]}
        self.assertEqual(game_val, res_game_val, msg=ms)
        self.assertEqual(plac, res_plac, msg=ms)
        self.assertItemsEqual(strat[1], res_strat[1], msg=ms)
        self.assertItemsEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)


class TestComputeValue5(unittest.TestCase):
    """
    Star graph (1 SS, 3 MR)
    """

    @classmethod
    def setUpClass(cls):
        print 'setupClass'
        cls.v0 = gr.Vertex(0, 0, 0)
        cls.v1 = gr.Vertex(1, 0.5, 2)
        cls.v2 = gr.Vertex(1, 0.5, 2)
        cls.v3 = gr.Vertex(1, 0.5, 2)
        cls.v4 = gr.Vertex(1, 0.5, 2)
        cls.v5 = gr.Vertex(1, 0.5, 2)
        cls.v6 = gr.Vertex(1, 0.5, 2)

        cls.G = gr.Graph(np.array(
            [cls.v0, cls.v1, cls.v2, cls.v3, cls.v4, cls.v5, cls.v6]))
        cls.G.setAdjacents(cls.v0, np.array([0, 1, 1, 1, 1, 1, 1]))
        cls.G.setAdjacents(cls.v1, np.array([1, 0, 0, 0, 0, 0, 0]))
        cls.G.setAdjacents(cls.v2, np.array([1, 0, 0, 0, 0, 0, 0]))
        cls.G.setAdjacents(cls.v3, np.array([1, 0, 0, 0, 0, 0, 0]))
        cls.G.setAdjacents(cls.v4, np.array([1, 0, 0, 0, 0, 0, 0]))
        cls.G.setAdjacents(cls.v5, np.array([1, 0, 0, 0, 0, 0, 0]))
        cls.G.setAdjacents(cls.v6, np.array([1, 0, 0, 0, 0, 0, 0]))

    def test_compute_shortest_sets(self):
        f = cv.compute_shortest_sets
        result, _= f(self.G, self.G.getTargets())

        shortest_sets = np.array(
            [[0, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1],
             [0, 1, 1, 1, 1, 1, 1]])
        ok = (result == shortest_sets).all()
        ms = "Error computing the shortest sets\nResult:\n" \
            + str(result) + "\nShould be:\n" + str(shortest_sets)
        self.assertTrue(ok, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_covering_routes(self):
        f = cv.compute_covering_routes
        cov_routes = f(self.G, self.G.getTargets())

        result0 = cov_routes[self.v0.getVertexNumber()].toarray()
        cov_route_0 = np.array(
            [[1, 0, 0, 0, 0, 0, 0],
             [1, 1, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 0, 0, 0],
             [1, 0, 0, 1, 0, 0, 0],
             [1, 0, 0, 0, 1, 0, 0],
             [1, 0, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 0, 0, 1]])
        ok = tf.compare_row_mat(result0, cov_route_0)
        ms = "Error computing the covering routes v0\nResult:\n" \
            + str(result0) + "\nShould be:\n" + str(cov_route_0)
        self.assertTrue(ok, msg=ms)

        result4 = cov_routes[self.v4.getVertexNumber()].toarray()
        cov_route_4 = np.array(
            [[0, 0, 0, 0, 1, 0, 0],
             [0, 1, 0, 0, 1, 0, 0],
             [0, 0, 1, 0, 1, 0, 0],
             [0, 0, 0, 1, 1, 0, 0],
             [0, 0, 0, 0, 1, 1, 0],
             [0, 0, 0, 0, 1, 0, 1]])
        ok = tf.compare_row_mat(result4, cov_route_4)
        ms = "Error computing the covering routes v4\nResult:\n" \
            + str(result4) + "\nShould be:\n" + str(cov_route_4)
        self.assertTrue(ok, msg=ms)

        dom_cov_routes = f(self.G, self.G.getTargets(), True)
        dom_result0 = dom_cov_routes[self.v0.getVertexNumber()].toarray()
        dom_cov_route_0 = np.array(
            [[1, 1, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 0, 0, 0],
             [1, 0, 0, 1, 0, 0, 0],
             [1, 0, 0, 0, 1, 0, 0],
             [1, 0, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 0, 0, 1]])
        ok0_d = tf.compare_row_mat(dom_result0, dom_cov_route_0)
        ms = "Error computing the dominating covering routes v0\nResult:\n" \
            + str(dom_result0) + "\nShould be:\n" + str(dom_cov_route_0)
        self.assertTrue(ok0_d, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_values(self):
        compvalres = cv.compute_values(self.G, True, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][2])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.5, 2: 0.75, 3: 1}
        res_num_iter = 10
        res_plac = {1: [(1, 6)], 2: [(1, 1), (2, 2)],
                    3: [(1, 1), (2, 2), (3, 3)]}
        res_strat = {1: [([(1, 0)], 1.0)],
                     2: [([(1, 1), (2, 2)], 1.0)],
                     3: [([(1, 3), (2, 1), (3, 1)], 1.0)]}
        self.assertEqual(game_val[3], res_game_val[3], msg=ms)
        self.assertEqual(plac[1], res_plac[1], msg=ms)
        self.assertEqual(plac[3], res_plac[3], msg=ms)
        self.assertEqual(strat[3], res_strat[3], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_2(self):
        compvalres = cv.compute_values(self.G, True, enum=10, enumtype=2)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][2])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.5, 2: 0.75, 3: 1}
        res_plac = {1: [(1, 6)], 2: [(1, 1), (2, 2)],
                    3: [(1, 1), (2, 2), (3, 3)]}
        res_num_iter = 2
        res_strat = {1: [([(1, 0)], 1.0)],
                     2: [([(1, 1), (2, 2)], 1.0)],
                     3: [([(1, 3), (2, 1), (3, 1)], 1.0)]}
        self.assertEqual(game_val[3], res_game_val[3], msg=ms)
        self.assertEqual(plac[1], res_plac[1], msg=ms)
        self.assertEqual(plac[3], res_plac[3], msg=ms)
        self.assertEqual(strat[3], res_strat[3], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_3(self):
        compvalres = cv.compute_values(self.G, True, enum=10, enumtype=3)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.5, 2: 0.75, 3: 1}
        res_plac = {1: [(1, 6)], 2: [(1, 1), (2, 2)],
                    3: [(1, 1), (2, 2), (3, 3)]}
        res_num_iter = 2
        res_strat = {1: [([(1, 0)], 1.0)],
                     2: [([(1, 1), (2, 2)], 1.0)],
                     3: [([(1, 3), (2, 1), (3, 1)], 1.0)]}
        self.assertEqual(game_val[3], res_game_val[3], msg=ms)
        self.assertEqual(plac[1], res_plac[1], msg=ms)
        self.assertEqual(plac[3], res_plac[3], msg=ms)
        self.assertEqual(strat[3], res_strat[3], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_4(self):
        compvalres = cv.compute_values(self.G, True, enum=10, enumtype=4)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = (len(compvalres[5][1]), len(compvalres[5][2]))
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.5, 2: 0.75, 3: 1}
        res_plac = {1: [(1, 6)], 2: [(1, 1), (2, 2)],
                    3: [(1, 1), (2, 2), (3, 3)]}
        res_num_iter = (7, 10)
        res_strat = {1: [([(1, 0)], 1.0)],
                     2: [([(1, 1), (2, 2)], 1.0)],
                     3: [([(1, 3), (2, 1), (3, 1)], 1.0)]}
        self.assertEqual(game_val[3], res_game_val[3], msg=ms)
        self.assertEqual(plac[1], res_plac[1], msg=ms)
        self.assertEqual(plac[3], res_plac[3], msg=ms)
        self.assertEqual(strat[3], res_strat[3], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_6(self):
        compvalres = cv.compute_values(self.G, True, enum=10, enumtype=6)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = (len(compvalres[5][1]), len(compvalres[5][2]))
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.5, 2: 0.75, 3: 1}
        res_plac = {1: [(1, 6)], 2: [(1, 1), (2, 2)],
                    3: [(1, 1), (2, 2), (3, 3)]}
        res_num_iter = (7, 10)
        res_strat = {1: [([(1, 0)], 1.0)],
                     2: [([(1, 1), (2, 2)], 1.0)],
                     3: [([(1, 3), (2, 1), (3, 1)], 1.0)]}
        self.assertEqual(game_val[3], res_game_val[3], msg=ms)
        self.assertEqual(plac[1], res_plac[1], msg=ms)
        self.assertEqual(plac[3], res_plac[3], msg=ms)
        self.assertEqual(strat[3], res_strat[3], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)


class TestComputeValue6(unittest.TestCase):
    """
    Figure Triangle Graph  (1 SS, 2 MR)
    """

    @classmethod
    def setUpClass(cls):
        print 'setupClass'
        cls.v0 = gr.Vertex(1, 0.5, 1)
        cls.v1 = gr.Vertex(1, 0.5, 1)
        cls.v2 = gr.Vertex(1, 0.5, 1)

        cls.G = gr.Graph(np.array([cls.v0, cls.v1, cls.v2]))
        cls.G.setAdjacents(cls.v0, np.array([0, 1, 1]))
        cls.G.setAdjacents(cls.v1, np.array([1, 0, 1]))
        cls.G.setAdjacents(cls.v2, np.array([1, 1, 0]))

    def test_compute_shortest_sets(self):
        f = cv.compute_shortest_sets
        result, _ = f(self.G, self.G.getTargets())

        shortest_sets = np.array(
            [[1, 1, 1],
             [1, 1, 1],
             [1, 1, 1]])
        ok = (result == shortest_sets).all()
        ms = "Error computing the shortest sets\nResult:\n" \
            + str(result) + "\nShould be:\n" + str(shortest_sets)
        self.assertTrue(ok, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_covering_routes(self):
        f = cv.compute_covering_routes
        cov_routes = f(self.G, self.G.getTargets())

        result0 = cov_routes[self.v0.getVertexNumber()].toarray()
        cov_route_0 = np.array(
            [[1, 0, 0],
             [1, 1, 0],
             [1, 0, 1]])
        ok0 = tf.compare_row_mat(result0, cov_route_0)
        ms = "Error computing the covering routes v0\nResult:\n" \
            + str(result0) + "\nShould be:\n" + str(cov_route_0)
        self.assertTrue(ok0, msg=ms)

        result2 = cov_routes[self.v2.getVertexNumber()].toarray()
        cov_route_2 = np.array(
            [[0, 0, 1],
             [1, 0, 1],
             [0, 1, 1]])
        ok4 = tf.compare_row_mat(result2, cov_route_2)
        ms = "Error computing the covering routes v4\nResult:\n" \
            + str(result2) + "\nShould be:\n" + str(cov_route_2)
        self.assertTrue(ok4, msg=ms)

        dom_cov_routes = f(self.G, self.G.getTargets(), True)
        dom_result0 = dom_cov_routes[self.v0.getVertexNumber()].toarray()
        dom_cov_route_0 = np.array(
            [[1, 1, 0],
             [1, 0, 1]])
        ok0_d = tf.compare_row_mat(dom_result0, dom_cov_route_0)
        ms = "Error computing the dominating covering routes v0\nResult:\n" \
            + str(dom_result0) + "\nShould be:\n" + str(dom_cov_route_0)
        self.assertTrue(ok0_d, msg=ms)

        too_long = np.arange(len(self.G.getTargets()) + 1)
        self.assertRaises(ValueError, f, self.G, too_long)

    def test_compute_values(self):
        compvalres = cv.compute_values(self.G, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 3
        res_strat = {1: [([(1, 2)], 0.5), ([(1, 1)], 0.5)],
                     2: [([(1, 1), (2, 2)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_2(self):
        compvalres = cv.compute_values(self.G, enumtype=2, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 3
        res_strat = {1: [([(1, 2)], 0.5), ([(1, 1)], 0.5)],
                     2: [([(1, 1), (2, 2)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_3(self):
        compvalres = cv.compute_values(self.G, enumtype=3, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_strat = {1: [([(1, 2)], 0.5), ([(1, 1)], 0.5)],
                     2: [([(1, 1), (2, 2)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)

    def test_compute_values_4(self):
        compvalres = cv.compute_values(self.G, enumtype=4, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 3
        res_strat = {1: [([(1, 2)], 0.5), ([(1, 1)], 0.5)],
                     2: [([(1, 1), (2, 2)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_dom(self):
        compvalres = cv.compute_values(self.G, True, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 3
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 2)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 1)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(plac[2], res_plac[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_dom_2(self):
        compvalres = cv.compute_values(self.G, True, enumtype=2, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 3
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 2)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 1)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(plac[2], res_plac[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_dom_3(self):
        compvalres = cv.compute_values(self.G, True, enumtype=3, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 3
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 2)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 1)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(plac[2], res_plac[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)

    def test_compute_values_dom_4(self):
        compvalres = cv.compute_values(self.G, True, enumtype=4, enum=10)
        game_val = compvalres[0]
        plac = compvalres[1]
        strat = compvalres[2]
        num_iter = len(compvalres[5][1])
        ms = str(game_val) + '\n' + str(plac) + '\n'\
            + str(strat) + '\n' + str(num_iter)
        res_game_val = {1: 0.75, 2: 1}
        res_num_iter = 3
        res_plac = {1: [(1, 2)], 2: [(1, 2), (2, 2)]}
        res_strat = {1: [([(1, 1)], 0.5), ([(1, 0)], 0.5)],
                     2: [([(1, 0), (2, 1)], 1.0)]}
        self.assertEqual(game_val[2], res_game_val[2], msg=ms)
        self.assertEqual(plac[2], res_plac[2], msg=ms)
        self.assertEqual(strat[2], res_strat[2], msg=ms)
        self.assertEqual(num_iter, res_num_iter, msg=ms)
