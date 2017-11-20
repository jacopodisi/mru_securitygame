import computevalue as cv
import time
from srg import graph as gr
import iomanager as io
import numpy as np


if __name__ == '__main__':
    nodes = [10, 12, 14, 16, 18, 20]
    densities = [0.25]
    tests = 5
    temp_times = np.empty(shape=(tests))
    stat = {}
    for n in nodes:
        for d in densities:
            for t in xrange(tests):
                mat = gr.generateRandMatrix(n, d, 1000000)
                graph = gr.generateRandomGraph(mat, mat.shape[0], 1, 0, 3)
                st = time.time()
                cv.compute_values(graph)
                temp_times[t] = time.time() - st
            stat[(n, d)] = np.mean(temp_times)
            print "\nComputed val for "\
                  + str(n) + "\n" + str(stat[(n, d)])
    fn = "statistics_n" + str(nodes[0]) + "_"\
         + str(nodes[-1]) + "_d" + str(densities[0]) + "_"\
         + str(densities[-1]) + "_t" + str(tests)
    io.save_results(stat, filename=fn)
