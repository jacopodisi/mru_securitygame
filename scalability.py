import computevalue as cv
import time
from srg import graph as gr
import iomanager as io
import numpy as np
import tqdm


if __name__ == '__main__':
    nodes = [10, 12, 14, 16, 18, 20]
    densities = [0.25]
    tests = 3
    temp_times = np.empty(shape=(tests))
    stat = {}
    for dead in [4, 5, 6]:
        for n in nodes:
            for d in densities:
                t_range = tqdm.trange(tests)
                for t in t_range:
                    mat = gr.generateRandMatrix(
                        n, d, niter=1000000, density=True)
                    graph = gr.generateRandomGraph(
                        mat, mat.shape[0], 1, dead, dead)
                    st = time.time()
                    cv.compute_values(graph)
                    temp_times[t] = time.time() - st
                stat[(n, d)] = np.mean(temp_times)
                print "\nComputed val for "\
                      + str(n) + "\n" + str(temp_times)\
                      + '\n' + str(stat[(n, d)])
        fn = "statistics_n" + str(nodes[0]) + "_"\
             + str(nodes[-1]) + "_dead" + str(dead) + "_t" + str(tests)
        io.save_results(stat, filename=fn)
