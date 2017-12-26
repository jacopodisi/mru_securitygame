import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('coredisp.xlsx')
worksheet = workbook.add_worksheet()

# Some data we want to write to the worksheet.
# de = "08"
# ncol = 1
corebutch = [(1, 10, 1, 1, 1, "25", True),
             (11, 15, 1, 1, 1, "10", True),
             (16, 16, 0, 1, 0, "08", True),
             (16, 16, 0, 0, 1, "06", False)]

# Start from the first cell. Rows and columns are zero indexed.
row = 0

for core in range(corebutch[0][0], corebutch[-1][1]):
    fn = "./runners/runcore" + str(core) + ".sh"
    with open(fn, mode='a') as f:
        f.write("#!/bin/bash\n")
        f.write("DIR=\"$( cd \"$( dirname \"${BASH_SOURCE[0]}\" )\" && pwd )\"")

for tp in corebutch:
    inicore = tp[0]
    endcore = tp[1]
    core = inicore
    if tp[-1]:
        row = 0
    if tp[2]:
        for t in [20]:
            for d in [4, 5, 10, 15, 19]:
                for i in range(10):
                    worksheet.write(row, core - 1, str(t) + "." + tp[-2] +
                                    "." + str(d) + "." + str(i))
                    fn = "./runners/runcore" + str(core) + ".sh"
                    command = "python $DIR/../script.py -d " + tp[-2] + " -t "\
                              + str(t) + " -D " + str(d) + " -i " + str(i)\
                              + " -l logcore" + str(core) + ".log"
                    with open(fn, mode='a') as f:
                        f.write("\n" + command)
                    core += 1
                    if core == endcore + 1:
                        core = inicore
                        row += 1

    # graph 25, 30
    if tp[3]:
        for t in [25, 30]:
            for d in [5, 10]:
                for i in range(10):
                    worksheet.write(row, core - 1, str(t) + "." + tp[-2] +
                                    "." + str(d) + "." + str(i))
                    fn = "./runners/runcore" + str(core) + ".sh"
                    command = "python $DIR/../script.py -d " + tp[-2] + " -t "\
                              + str(t) + " -D " + str(d) + " -i " + str(i)\
                              + " -l logcore" + str(core) + ".log"
                    with open(fn, mode='a') as f:
                        f.write("\n" + command)
                    core += 1
                    if core == endcore + 1:
                        core = inicore
                        row += 1

    # graph 35, 40, 45, 50
    if tp[4]:
        for t in [35, 40, 45, 50]:
            for d in [5, 10]:
                for i in range(2):
                    worksheet.write(row, core - 1, str(t) + "." + tp[-2] +
                                    "." + str(d) + "." + str(i))
                    fn = "./runners/runcore" + str(core) + ".sh"
                    command = "python $DIR/../script.py -d " + tp[-2] + " -t "\
                              + str(t) + " -D " + str(d) + " -i " + str(i)\
                              + " -l logcore" + str(core) + ".log"
                    with open(fn, mode='a') as f:
                        f.write("\n" + command)
                    core += 1
                    if core == endcore + 1:
                        core = inicore
                        row += 1

# Write a total using a formula.

workbook.close()
