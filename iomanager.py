# -*- coding: utf-8 -*-

from srg import graph as gr
import numpy as np
import os
import pickle
import matplotlib.pylab as plt


def compute_graph(file_path):
    """ given the path of the file containing the description of the graph
        return a corresponding Graph object
    """
    vertices = np.array([])
    G = gr.Graph(vertices)
    return G


def save_results(res, filename=""):
    """ save the results in a pickle file in ./results folder
    Parameters
    ----------
    res: results to be saved
    filename: name of the file, if empty save results incrementally in file
          with incremental name
    """
    if not os.path.exists("./results/"):
        os.makedirs("./results/")
    if filename == "":
        file = 0
        while True:
            if not os.path.isfile("res" + str(file) + ".pickle"):
                break
            file += 1
        filename = "res" + str(file) + ".pickle"
    with open("./results/" + filename, mode='wb') as f:
        pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_results(filename, plot=False):
    """Read the result stored in a file. Can also display a plot of the results
    Parameters
    ----------
    filename: name of the file
    plot: boolean to enable the plotting

    Result
    ------
    boolean: described the success of the operation
    dicitonary: actual results
    """
    filename = "./results/" + filename
    if not os.path.isfile(filename):
        m = 'File {} do not exist'.format(filename)
        raise IOError(m)
    with open(filename, mode='r') as f:
        res = pickle.load(f)
    sort_res = sorted(res.items())
    if plot:
        x, y = zip(*sort_res)
        plt.plot(x, y)
        plt.show()
    return sort_res
