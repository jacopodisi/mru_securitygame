import unittest
import ILP_solver as ilp
from scipy import sparse
import numpy as np
import gurobi as gb


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
        result = ilp.set_cover_solver(sets)
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
        f = ilp.set_cover_solver
        self.assertRaises(gb.GurobiError, f, sets)

    def test_set_cover_solver_k_succ(self):
        sets = np.array(self.ok_sets)
        result = ilp.set_cover_solver(sets, k=2)
        set_cover_k = np.array([3, 4])
        if set_cover_k.shape == result.shape:
            ok = (result == set_cover_k).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover K:\n" + str(result))

    def test_set_cover_solver_k_fail(self):
        sets = np.array(self.ok_sets)
        f = ilp.set_cover_solver
        self.assertRaises(gb.GurobiError, f, sets, 1)

    def test_maximum_resources_success(self):
        dict_sets = {
            6: sparse.csr_matrix(self.ok_sets[:3, :]),
            13: sparse.csr_matrix(self.ok_sets[3:, :])}
        result = ilp.maximum_resources(dict_sets, np.arange(14))
        max_res_solution = np.array([13, 13])
        if result.shape == max_res_solution.shape:
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
        f = ilp.maximum_resources
        self.assertRaises(gb.GurobiError, f, dict_sets, np.arange(14))

    def test_maximum_resources_fail2(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:3, :]),
            13: sparse.csr_matrix(self.wrong_sets[3:, :])}
        f = ilp.maximum_resources
        self.assertRaises(ValueError, f, dict_sets, np.arange(15))


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
        result = ilp.set_cover_solver(sets)
        set_cover_optimum = np.arange(9)
        if set_cover_optimum.shape == result.shape:
            ok = (result == set_cover_optimum).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover optimum:\n" + str(result))

    def test_set_cover_solver_fail(self):
        sets = self.wrong_sets
        f = ilp.set_cover_solver
        self.assertRaises(gb.GurobiError, f, sets)

    def test_set_cover_solver_k_succ(self):
        sets = np.array(self.ok_sets)
        result = ilp.set_cover_solver(sets, k=9)
        set_cover_k = np.arange(9)
        if set_cover_k.shape == result.shape:
            ok = (result == set_cover_k).all()
        else:
            ok = False
        self.assertTrue(
            ok,
            msg="Error computing the set cover K:\n" + str(result))

    def test_set_cover_solver_k_fail(self):
        sets = np.array(self.ok_sets)
        f = ilp.set_cover_solver
        self.assertRaises(gb.GurobiError, f, sets, 10)

    def test_maximum_resources_success(self):
        dict_sets = {
            6: sparse.csr_matrix(self.ok_sets[:5, :]),
            13: sparse.csr_matrix(self.ok_sets[5:, :])}
        result = ilp.maximum_resources(dict_sets, np.arange(9))
        max_res_solution = np.array([6, 6, 6, 6, 6, 13, 13, 13, 13])
        if result.shape == max_res_solution.shape:
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
        f = ilp.maximum_resources
        self.assertRaises(gb.GurobiError, f, dict_sets, np.arange(9))

    def test_maximum_resources_fail2(self):
        dict_sets = {
            6: sparse.csr_matrix(self.wrong_sets[:5, :]),
            13: sparse.csr_matrix(self.wrong_sets[5:, :])}
        f = ilp.maximum_resources
        self.assertRaises(ValueError, f, dict_sets, np.arange(10))
