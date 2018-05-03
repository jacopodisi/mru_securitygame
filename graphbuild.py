# -*- coding: utf-8 -*-

from mru.srg import graph as gr
from mru import iomanager as io


def main():

    den = [0.06]
    ntgts = [20, 25, 30, 35, 40, 45, 50]
    dead = [1.5, 2, 5, 10]
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

                        if dead > 3:
                            print(io.save_graph(gra, d, dl))
                        else:
                            min_dead = gr.getDiameter(gra)
                            max_dead = int(min_dead * dl)
                            gra.setAllDeadlines(min_dead, max_dead)
                            print(io.save_graph(gra, d, min_dead, rel_dead=dl))

                    except ValueError:
                        print(ValueError)


if __name__ == '__main__':
    main()
