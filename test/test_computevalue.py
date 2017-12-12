import unittest
import computevalue as cv
from srg import graph as gr
import numpy as np
import testfunctions as tf


class TestComputeValue1(unittest.TestCase):
    """
    Figure 1 Graph  (1 SS, 1 MR)
    """

    @classmethod
    def setUpClass(cls):
        print('setupClass')
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
        result = f(self.G, self.G.getTargets())

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

        dom_cov_routes = f(self.G, self.G.getTargets(), dominance=True)
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
        res, _, _ = cv.compute_values(self.G)
        ms = str(res)
        self.assertEqual(1, max(res.values()), msg=ms)


class TestComputeValue2(unittest.TestCase):
    """
    Figure 1 Graph  (4 SS, 4 MR)
    """

    @classmethod
    def setUpClass(cls):
        print('setupClass')
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
        result = f(self.G, self.G.getTargets())

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

        dom_cov_routes = f(self.G, self.G.getTargets(), dominance=True)
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
        res, _, _ = cv.compute_values(self.G)
        self.assertEqual(1, max(res.values()), msg=None)


class TestComputeValue3(unittest.TestCase):
    """
    Linear graph (1 SS, 1 MR)
    """

    @classmethod
    def setUpClass(cls):
        print('setupClass')
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
        result = f(self.G, self.G.getTargets())

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

        dom_cov_routes = f(self.G, self.G.getTargets(), dominance=True)
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
        res, _, _ = cv.compute_values(self.G)
        self.assertEqual(1, max(res.values()), msg=None)


class TestComputeValue4(unittest.TestCase):
    """
    Linear graph (1 SS, 2 MR)
    """

    @classmethod
    def setUpClass(cls):
        print('setupClass')
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
        result = f(self.G, self.G.getTargets())

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

        dom_cov_routes = f(self.G, self.G.getTargets(), dominance=True)
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
        res, _, _ = cv.compute_values(self.G)
        self.assertEqual(1, max(res.values()), msg=None)


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
        cls.v6 = gr.Vertex(1, 0.000001, 2)

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
        result = f(self.G, self.G.getTargets())

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

        dom_cov_routes = f(self.G, self.G.getTargets(), dominance=True)
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
        res, _, _ = cv.compute_values(self.G)
        self.assertEqual(1, max(res.values()), msg=None)


class TestComputeValue6(unittest.TestCase):
    """
    Figure Triangle Graph  (1 SS, 2 MR)
    """

    @classmethod
    def setUpClass(cls):
        print('setupClass')
        cls.v0 = gr.Vertex(1, 0.5, 1)
        cls.v1 = gr.Vertex(1, 0.5, 1)
        cls.v2 = gr.Vertex(1, 0.5, 1)

        cls.G = gr.Graph(np.array([cls.v0, cls.v1, cls.v2]))
        cls.G.setAdjacents(cls.v0, np.array([0, 1, 1]))
        cls.G.setAdjacents(cls.v1, np.array([1, 0, 1]))
        cls.G.setAdjacents(cls.v2, np.array([1, 1, 0]))

    def test_compute_shortest_sets(self):
        f = cv.compute_shortest_sets
        result = f(self.G, self.G.getTargets())

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

        dom_cov_routes = f(self.G, self.G.getTargets(), dominance=True)
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
        f = cv.compute_values
        result, _, _ = f(self.G)

        values = {1: 0.75, 2: 1}

        self.assertAlmostEqual(result[1], values[1], delta=0.25)

    def test_compute_values_dom(self):
        f = cv.compute_values
        result, _, _ = f(self.G, dominance=True)

        values = {1: 0.75, 2: 1}

        self.assertEqual(result[1], values[1])