#!/bin/sh
python suspend_pid.py 14493
screen -S core01scr -p 0 -X quit
python suspend_pid.py 113252
screen -S core02scr -p 0 -X quit
python suspend_pid.py 10105
screen -S core03scr -p 0 -X quit
python suspend_pid.py 88768
screen -S core04scr -p 0 -X quit
python suspend_pid.py 7975
screen -S core05scr -p 0 -X quit
python suspend_pid.py 118925
screen -S core06scr -p 0 -X quit
python suspend_pid.py 111969
screen -S core07scr -p 0 -X quit
python suspend_pid.py 20912
screen -S core08scr -p 0 -X quit
python suspend_pid.py 102381
screen -S core09scr -p 0 -X quit
python suspend_pid.py 54634
screen -S core10scr -p 0 -X quit
