import psutil
import sys

pid = int(sys.argv[1])

p = psutil.Process(pid)
p.suspend()
