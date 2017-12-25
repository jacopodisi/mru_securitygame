# -*- coding: utf-8 -*-

from mru.srg import graph as gr
from mru import iomanager as io


def main():

    den = [0.06]
    ntgts = [35, 40, 45, 50]
    dead = [5, 10] # , 5, 10, 15, 19]
    ninsta = 2

    for d in den:
        for t in ntgts:
            for dl in dead:
                for _ in xrange(ninsta):
                    try:
                        mat = gr.generateRandMatrix(t, d, density=True, niter=100000)
                        gra = gr.generateRandomGraph(mat, mat.shape[0], 1, dl, dl)

                        print io.save_graph(gra, d, dl)
                    except ValueError:
                        print ValueError


if __name__ == '__main__':
    main()
