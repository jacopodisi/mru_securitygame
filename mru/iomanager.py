# -*- coding: utf-8 -*-

import os
import pickle
import logging
import re
import numpy as np

from srg import graph as gr


FILEDIR = "file/"


def save(res, filename=""):
    """ save the results in a pickle file in FILEDIR folder
    Parameters
    ----------
    res: results to be saved
    filename: name of the file, if empty save results incrementally in file
          with incremental name
    """
    if not os.path.exists(FILEDIR):
        os.makedirs(FILEDIR)
    if filename == "":
        filename = "file"
    filename = FILEDIR + filename
    fileid = 0
    while True:
        if not os.path.isfile(filename + "_ix_" + str(fileid) + ".pickle"):
            break
        fileid += 1
    filename = filename + "_ix_" + str(fileid) + ".pickle"
    with open(filename, mode='wb') as f:
        pickle.dump(res, f, protocol=pickle.HIGHEST_PROTOCOL)
    return filename


def load(filename):
    """Read the result stored in a file.
    Parameters
    ----------
    filename: name of the file (full path)

    Result
    ------
    boolean: described the success of the operation
    dicitonary: actual results
    """
    if not os.path.isfile(filename):
        m = 'File {} do not exist'.format(filename)
        raise IOError(m)
    with open(filename, mode='r') as f:
        res = pickle.load(f)
    return res


def save_graph(graph):
    """save graph in file
    example -> ./file/
                  graphs/
                    graphs_20_ntgts/
                      instance_ntgts_20_den_25_dead_4_ix_0.pickle
    Parameter
    ---------
    graph: graph instance to be saved
    Return
    ------
    fn: complete file path ./file/....pickle
    """
    tgts = graph.getTargets()
    size = tgts.shape[0]

    adj = graph.getAdjacencyMatrix()
    adj[adj == gr.inf] = 0
    nedges = np.sum(adj) / 2
    den = round((2 * nedges) / ((size * (size - 1)) + 0.0), 2) * 100
    den = str(int(den))

    dead = graph.vertices[tgts[0]].deadline
    dirname = "graphs/graphs_" + str(size) + "_ntgts/"
    if not os.path.exists(FILEDIR + dirname):
        os.makedirs(FILEDIR + dirname)
    filename = "instance_ntgts_" + str(size) + "_den_" + den\
               + "_dead_" + str(dead)
    fn = save(graph, dirname + filename)
    logging.info('iomanager: saved graph in ' + fn)

    return fn


def save_results(graph_path, result):
    """save results in file
    example -> ./file/
                  results/
                    res_graphs_20_ntgts/
                      res_instance_ntgts_20_den_25_dead_4_graphix_0_ix_0.pickle
    Parameter
    ---------
    graph_path: path of the graph instance computed results
    results: results of the compute_value function
    Return
    ------
    fn: complete file path ./file/....pickle
    """
    ntgts = re.search('ntgts_([0-9]+?)_', graph_path).group(1)
    den = re.search('den_([0-9]+?)_', graph_path).group(1)
    dead = re.search('dead_([0-9]+?)_', graph_path).group(1)
    index = re.search('_ix_([0-9]+?)$', graph_path).group(1)
    dirname = "results/res_graphs_" + str(ntgts) + "_ntgts/"
    if not os.path.exists(FILEDIR + dirname):
        os.makedirs(FILEDIR + dirname)
    filename = "res_instance_ntgts_" + str(ntgts) + "_den_" + den + "_dead_"\
               + str(dead) + "_graphix_" + str(index)
    fn = save(result, dirname + filename)
    logging.info('iomanager: saved results in ' + fn)

    if not os.path.isfile(FILEDIR + "graphs/" + graph_path + ".pickle"):
        logging.warn('wrong graph path specified for saving the result')

    return fn
