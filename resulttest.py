import computevalue as cv
from srg import graph as gr
import iomanager as io


if True:
    nodes = [30]
    densities = [0.15]
    dominance = False
    values = {}
    strategies = {}
    placements = {}
    for n in nodes:
        for d in densities:
            mat = gr.generateRandMatrix(n, d, 1000000)
            graph = gr.generateRandomGraph(mat, mat.shape[0], 1, 0, 3)
            values, placements, strategies = cv.compute_values(
                graph, dominance=dominance)
            print "\nComputed val for " + str(n)\
                  + "\n" + "values: " + str(values)\
                  + "\n" + "placements: " + str(placements)\
                  + "\n" + "strategies: " + str(strategies)\
                  + "\n" + "--------------------------------------------------"
            file_gr = "graph_n" + str(n) + "_d" + str(d)
            io.save_results(graph, filename=file_gr)
            res = (values, placements, strategies)
            file_res = ''
            if dominance:
                file_res = "results_" + file_gr + "vps_dom"
            else:
                file_res = "results_" + file_gr + "vps"
            io.save_results(res, filename=file_res)
else:
    n = 30
    ix = 0
    d = 0.15
    dominance = False
    file_gr = "graph_n" + str(n) + "_d" + str(d) + "_ix" + str(ix)
    graph = io.load_results(file_gr)
    values, placements, strategies = cv.compute_values(graph, dominance)
    print "\nComputed val for " + str(n)\
          + "\n" + "values: " + str(values)\
          + "\n" + "placements: " + str(placements)\
          + "\n" + "strategies: " + str(strategies)\
          + "\n" + "--------------------------------------------------"
    res = (values, placements, strategies)
    file_res = ''
    if dominance:
        file_res = "results_graph_n" + str(n) + "_d" + str(d) + "vps_dom"
    else:
        file_res = "results_graph_n" + str(n) + "_d" + str(d) + "vps"
    io.save_results(res, filename=file_res)
