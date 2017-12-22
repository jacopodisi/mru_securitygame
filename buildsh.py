core = 1

# write #!/bin/bash in scripts
for c in range(1, 17):
    fn = "./runners/runcore" + str(c) + ".sh"
    with open(fn, mode='a') as f:
        f.write("#!/bin/bash")

# graph 20
for d in [4, 5, 10, 15, 19]:
    for i in range(10):
        fn = "./runners/runcore" + str(core) + ".sh"
        command = "python ../script.py -d 25 -t 20 -D "\
                  + str(d) + " -i " + str(i) + " -l logcore"\
                  + str(core) + ".log"
        with open(fn, mode='a') as f:
            f.write("\n" + command)
        core += 1
        if core == 17:
            core = 1

# graph 25, 30
for t in [25, 30]:
    for d in [5, 10]:
        for i in range(10):
            fn = "./runners/runcore" + str(core) + ".sh"
            command = "python ../script.py -d 25 -t " + str(t) + " -D "\
                      + str(d) + " -i " + str(i) + " -l logcore"\
                      + str(core) + ".log"
            with open(fn, mode='a') as f:
                f.write("\n" + command)
            core += 1
            if core == 17:
                core = 1

# graph 35, 40, 45, 50
for t in [35, 40, 45, 50]:
    for d in [5, 10]:
        for i in [0, 1]:
            fn = "./runners/runcore" + str(core) + ".sh"
            command = "python ../script.py -d 25 -t " + str(t) + " -D "\
                      + str(d) + " -i " + str(i) + " -l logcore"\
                      + str(core) + ".log"
            with open(fn, mode='a') as f:
                f.write("\n" + command)
            core += 1
            if core == 17:
                core = 1
