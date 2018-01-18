import pickle


def get_times(den=None, dead=None, ntgts=None):
    timesfile = "aggregate_times_0.pickle"
    with open(timesfile, mode='r') as f:
        timesdict = pickle.load(f)

    result1 = []
    result2 = []
    if ntgts is None:
        result1 = sorted(timesdict[den][dead].keys())
        for tgt in result1:
            result2.append(timesdict[den][dead][tgt])
    elif dead is None:
        deadlines = sorted(timesdict[den].keys())
        for dead in deadlines:
            result2.append(timesdict[den][dead][ntgts])
    elif den is None:
        pass
