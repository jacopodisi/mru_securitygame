# -*- coding: utf-8 -*-

import os
import pickle
import logging


FILEDIR = os.path.join(os.path.dirname(__file__), '../file/')

log = logging.getLogger(__name__)


def save_file(res, filename=""):
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


def load_file(filename):
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


def save_graph(graph, den, dead):
    """save graph in file
    example -> ./file/
                  graphs/
                    graphs_20_ntgts/
                      instance_ntgts_20_den_25_dead_4_ix_0.pickle
    Parameter
    ---------
    graph: graph instance to be saved
    den: density of edges in the graph
    Return
    ------
    fn: complete file path ./file/....pickle
    """
    tgts = graph.getTargets()
    size = tgts.shape[0]
    den = str(int(den * 100))

    dirname = "graphs/graphs_" + str(size) + "_ntgts/"
    if not os.path.exists(FILEDIR + dirname):
        os.makedirs(FILEDIR + dirname)
    filename = "instance_ntgts_" + str(size) + "_den_" + den\
               + "_dead_" + str(dead)
    fn = save_file(graph, dirname + filename)
    log.debug('saved graph in ' + fn)

    return fn


def load_graph(ntgts, dead, den, gix):

    ntgts = str(ntgts)
    dead = str(dead)
    den = str(den)
    gix = str(gix)
    graph_path = "graphs/graphs_" + ntgts + "_ntgts/instance_ntgts_"\
                 + ntgts + "_den_" + den + "_dead_" + dead + "_ix_" + gix

    return load_file(FILEDIR + graph_path + ".pickle")


def save_results(ntgts, dead, den, gix, result):
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
    ntgts = str(ntgts)
    dead = str(dead)
    den = str(den)
    gix = str(gix)
    dirname = "results/res_graphs_" + str(ntgts) + "_ntgts/"
    if not os.path.exists(FILEDIR + dirname):
        os.makedirs(FILEDIR + dirname)
    filename = "res_instance_ntgts_" + str(ntgts) + "_den_" + den + "_dead_"\
               + str(dead) + "_graphix_" + str(gix)
    fn = save_file(result, dirname + filename)
    log.debug('saved results in ' + fn)

    graph_path = "graphs/graphs_" + ntgts + "_ntgts/instance_ntgts_"\
                 + ntgts + "_den_" + den + "_dead_" + dead + "_ix_" + gix

    if not os.path.isfile(FILEDIR + graph_path + ".pickle"):
        log.warn('wrong graph path specified for saving the result')

    return fn


def load_results(ntgts, dead, den, gix):

    ntgts = str(ntgts)
    dead = str(dead)
    den = str(den)
    gix = str(gix)
    res_path = "results/res_graphs_" + ntgts + "_ntgts/res_instance_ntgts_"\
               + ntgts + "_den_" + den + "_dead_" + dead + "_graphix_"\
               + gix + "_ix_0"

    return load_file(FILEDIR + res_path + ".pickle")
