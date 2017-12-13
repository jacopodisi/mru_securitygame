# -*- coding: utf-8 -*-

from mru.srg import graph as gr
from mru import iomanager as io


def main():

    den = [0.25]
    ntgts = [35, 40, 45, 50]
    dead = [5, 10]
    ninsta = 2

    for d in den:
        for t in ntgts:
            for dl in dead:
                for _ in xrange(ninsta):
                    mat = gr.generateRandMatrix(t, d, density=True)
                    gra = gr.generateRandomGraph(mat, mat.shape[0], 1, dl, dl)

                    io.save_graph(gra)


if __name__ == '__main__':
    main()
