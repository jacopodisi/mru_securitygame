import unittest
from .. import ILP_solver as ilp
from scipy import sparse
import numpy as np
import gurobipy as gb


class TestILPSolver1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ok_sets = np.array(
            [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]])
        cls.wrong_sets = np.array(
            [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
             [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]])

    def test_set_cover_solver_succ(self):
        sets = self.ok_sets
        result = ilp.set_cover_solver(sets)[0][0]
        set_cover_optimum = np.array([3, 4])
        if set_cover_optimum.shape == result.shape:
            ok = (result == set_cover_optimum).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover optimum:\n" + str(result))

    def test_set_cover_solver_fail(self):
        sets = self.wrong_sets
        with self.assertRaises(gb.GurobiError):
            ilp.set_cover_solver(sets)

    def test_set_cover_solver_k_succ(self):
        sets = np.array(self.ok_sets)
        result = ilp.set_cover_solver(sets, k=3, nsol=10)[0]
        set_cover_k = np.array([[2, 3, 4], [0, 3, 4],
                                [1, 3, 4], [1, 2, 3]])
        if set_cover_k.shape == result.shape:
            ok = (result == set_cover_k).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover K:\n" + str(result))

    def test_set_cover_solver_k_fail(self):
        sets = np.array(self.ok_sets)
        with self.assertRaises(gb.GurobiError):
            ilp.set_cover_solver(sets, k=10)

    def test_set_cover_solver_place_succ(self):
        sets = np.array(self.ok_sets)
        result, _ = ilp.set_cover_solver(sets, place=0, k=3)
        result = result[0]
        set_cover_k = np.array([0, 3, 4])
        if set_cover_k.shape == result.shape:
            ok = (result == set_cover_k).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover K:\n" + str(result))

    def test_set_cover_solver_place_fail(self):
        sets = np.array(self.ok_sets)
        _, isok = ilp.set_cover_solver(sets, place=0, k=2)
        self.assertFalse(isok)

    def test_set_cover_solver_hist_succ(self):
        sets = np.array(self.ok_sets)
        hist = np.array([[0, 3, 4]])
        result, _ = ilp.set_cover_solver(sets, place=4, k=3, sets_hist=hist)
        result = result[0]
        set_cover_k = np.array([2, 3, 4])
        if set_cover_k.shape == result.shape:
            ok = (result == set_cover_k).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover K:\n" + str(result))

    def test_set_cover_solver_hist_fail(self):
        sets = np.array(self.ok_sets)
        hist = np.array([[0, 3, 4]])
        _, isok = ilp.set_cover_solver(sets, place=0, k=3, sets_hist=hist)
        self.assertFalse(isok)

    def test_maximum_resources_success(self):
        dict_sets = {
            6: sparse.csr_matrix(self.ok_sets[:3, :]),
            13: sparse.csr_matrix(self.ok_sets[3:, :])}
        result = ilp.maximum_resources(dict_sets, np.arange(14))
        max_res_solution = np.array([(13, 0), (13, 1)])
        if len(result) == len(max_res_solution):
            ok = np.all(np.in1d(result, max_res_solution))
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the max resources 1:\n" + str(result))

    def test_maximum_resources_fail1(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:3, :]),
            13: sparse.csr_matrix(self.wrong_sets[3:, :])}
        with self.assertRaises(gb.GurobiError):
            ilp.maximum_resources(dict_sets, np.arange(14))

    def test_maximum_resources_fail2(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:3, :]),
            13: sparse.csr_matrix(self.wrong_sets[3:, :])}
        with self.assertRaises(ValueError):
            ilp.maximum_resources(dict_sets, np.arange(15))


class TestILPSolver2(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ok_sets = np.array(
            # 0  1  2  3  4  5  6  7  8
            [[1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 1]])
        cls.wrong_sets = np.array(
            [[1, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 0, 0, 1, 0]])

    def test_set_cover_solver_succ(self):
        sets = self.ok_sets
        result = ilp.set_cover_solver(sets)[0]
        set_cover_optimum = np.array([np.arange(9)])
        if set_cover_optimum.shape == result.shape:
            ok = (result == set_cover_optimum).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover optimum:\n" + str(result))

    def test_set_cover_solver_fail(self):
        sets = self.wrong_sets
        with self.assertRaises(gb.GurobiError):
            ilp.set_cover_solver(sets)

    def test_set_cover_solver_k_succ(self):
        sets = np.array(self.ok_sets)
        result = ilp.set_cover_solver(sets, k=9)[0]
        set_cover_k = np.array([np.arange(9)])
        if set_cover_k.shape == result.shape:
            ok = (result == set_cover_k).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover K:\n" + str(result))

    def test_set_cover_solver_k_fail(self):
        sets = np.array(self.ok_sets)
        with self.assertRaises(gb.GurobiError):
            ilp.set_cover_solver(sets, k=10)

    def test_maximum_resources_success(self):
        dict_sets = {
            6: sparse.csr_matrix(self.ok_sets[:5, :]),
            13: sparse.csr_matrix(self.ok_sets[5:, :])}
        result = ilp.maximum_resources(dict_sets, np.arange(9))
        max_res_solution = np.array([(6, 0),
                                     (6, 1),
                                     (6, 2),
                                     (6, 3),
                                     (6, 4),
                                     (13, 0),
                                     (13, 1),
                                     (13, 2),
                                     (13, 3)])
        if len(result) == len(max_res_solution):
            ok = np.all(np.in1d(result, max_res_solution))
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the max resources 1:\n" + str(result))

    def test_maximum_resources_fail1(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:5, :]),
            13: sparse.csr_matrix(self.wrong_sets[5:, :])}
        with self.assertRaises(gb.GurobiError):
            ilp.maximum_resources(dict_sets, np.arange(9))

    def test_maximum_resources_fail2(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:5, :]),
            13: sparse.csr_matrix(self.wrong_sets[5:, :])}
        with self.assertRaises(ValueError):
            ilp.maximum_resources(dict_sets, np.arange(14))


class TestILPSolver3(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ok_sets = np.array(
            # 0  1  2  3  4  5  6  7  8
            [[1, 1, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 1, 1, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1],
             [0, 1, 0, 1, 0, 1, 0, 1, 0]])
        cls.wrong_sets = np.array(
            [[1, 1, 1, 1, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 1, 1, 0],
             [1, 0, 1, 0, 1, 0, 1, 0, 0],
             [0, 1, 0, 1, 0, 1, 0, 1, 0]])

    def test_set_cover_solver_succ(self):
        sets = self.ok_sets
        result = ilp.set_cover_solver(sets)[0]
        set_cover_optimum = np.array([[2, 3]])
        if set_cover_optimum.shape == result.shape:
            ok = (result == set_cover_optimum).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover optimum:\n" + str(result))

    def test_set_cover_solver_fail(self):
        sets = self.wrong_sets
        with self.assertRaises(gb.GurobiError):
            ilp.set_cover_solver(sets)

    def test_set_cover_solver_k_succ(self):
        sets = np.array(self.ok_sets)
        result = ilp.set_cover_solver(sets, k=3, nsol=10)[0]
        set_cover_k = np.array([[0, 1, 2], [0, 1, 3],
                                [1, 2, 3], [0, 2, 3]])
        if set_cover_k.shape == result.shape:
            ok = (result == set_cover_k).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover K:\n" + str(result))

    def test_set_cover_solver_k_fail(self):
        sets = np.array(self.ok_sets)
        with self.assertRaises(gb.GurobiError):
            ilp.set_cover_solver(sets, k=10)

    def test_maximum_resources_success(self):
        dict_sets = {
            6: sparse.csr_matrix(self.ok_sets[:5, :]),
            13: sparse.csr_matrix(self.ok_sets[5:, :])}
        result = ilp.maximum_resources(dict_sets, np.arange(9))
        max_res_solution = np.array([[6, 2], [6, 3]])
        if len(result) == len(max_res_solution):
            ok = np.all(np.in1d(result, max_res_solution))
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the max resources 1:\n" + str(result))

    def test_maximum_resources_fail1(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:5, :]),
            13: sparse.csr_matrix(self.wrong_sets[5:, :])}
        with self.assertRaises(gb.GurobiError):
            ilp.maximum_resources(dict_sets, np.arange(9))

    def test_maximum_resources_fail2(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:5, :]),
            13: sparse.csr_matrix(self.wrong_sets[5:, :])}
        with self.assertRaises(ValueError):
            ilp.maximum_resources(dict_sets, np.arange(14))
