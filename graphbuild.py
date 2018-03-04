# -*- coding: utf-8 -*-

from mru.srg import graph as gr
from mru import iomanager as io


def main():

    # den = [0.06, 0.10, 0.25]
    # ntgts = [35, 40, 45, 50]
    # dead = [0]  # , 5, 10, 15, 19]
    # ninsta = 2

    # for d in den:
    #     for t in ntgts:
    #         for dl in dead:
    #             for _ in range(ninsta):
    #                 try:
    #                     mat = gr.generateRandMatrix(t,
    #                                                 d,
    #                                                 density=True,
    #                                                 niter=100000)
    #                     gra = gr.generateRandomGraph(mat,
    #                                                  mat.shape[0],
    #                                                  1,
    #                                                  dl,
    #                                                  dl)
    #                     min_dead = gr.getDiameter(gra)

    #                     max_dead = int(min_dead * 1.5)
    #                     gra.setAllDeadlines(min_dead, max_dead)
    #                     print(io.save_graph(gra, d, min_dead, rel_dead=1.5))

    #                     max_dead = int(min_dead * 2)
    #                     gra.setAllDeadlines(min_dead, max_dead)
    #                     print(io.save_graph(gra, d, min_dead, rel_dead=2))

    #                 except ValueError:
    #                     print(ValueError)

    den = [0.08, 0.10, 0.25]
    ntgts = [25, 30]
    dead = [0]  # , 5, 10, 15, 19]
    ninsta = 10

    for d in den:
        for t in ntgts:
            for dl in dead:
                for _ in range(ninsta):
                    try:
                        mat = gr.generateRandMatrix(t,
                                                    d,
                                                    density=True,
                                                    niter=100000)
                        gra = gr.generateRandomGraph(mat,
                                                     mat.shape[0],
                                                     1,
                                                     dl,
                                                     dl)
                        min_dead = gr.getDiameter(gra)

                        max_dead = int(min_dead * 1.5)
                        gra.setAllDeadlines(min_dead, max_dead)
                        print(io.save_graph(gra, d, min_dead, rel_dead=1.5))

                        max_dead = int(min_dead * 2)
                        gra.setAllDeadlines(min_dead, max_dead)
                        print(io.save_graph(gra, d, min_dead, rel_dead=2))

                    except ValueError:
                        print(ValueError)

    den = [0.10, 0.25]
    ntgts = [20]
    dead = [0]  # , 5, 10, 15, 19]
    ninsta = 10

    for d in den:
        for t in ntgts:
            for dl in dead:
                for _ in range(ninsta):
                    try:
                        mat = gr.generateRandMatrix(t,
                                                    d,
                                                    density=True,
                                                    niter=100000)
                        gra = gr.generateRandomGraph(mat,
                                                     mat.shape[0],
                                                     1,
                                                     dl,
                                                     dl)
                        min_dead = gr.getDiameter(gra)

                        max_dead = int(min_dead * 1.5)
                        gra.setAllDeadlines(min_dead, max_dead)
                        print(io.save_graph(gra, d, min_dead, rel_dead=1.5))

                        max_dead = int(min_dead * 2)
                        gra.setAllDeadlines(min_dead, max_dead)
                        print(io.save_graph(gra, d, min_dead, rel_dead=2))

                    except ValueError:
                        print(ValueError)


if __name__ == '__main__':
    main()
