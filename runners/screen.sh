#!/bin/sh
screen -dmS core1
screen -S core01 -p 0 -X stuff './runcore1.sh\n'
screen -dmS core02
screen -S core02 -p 0 -X stuff './runcore2.sh\n'
screen -dmS core03
screen -S core03 -p 0 -X stuff './runcore3.sh\n'
screen -dmS core04
screen -S core04 -p 0 -X stuff './runcore4.sh\n'
screen -dmS core05
screen -S core05 -p 0 -X stuff './runcore5.sh\n'
screen -dmS core06
screen -S core06 -p 0 -X stuff './runcore6.sh\n'
screen -dmS core07
screen -S core07 -p 0 -X stuff './runcore7.sh\n'
screen -dmS core08
screen -S core08 -p 0 -X stuff './runcore8.sh\n'
screen -dmS core09
screen -S core09 -p 0 -X stuff './runcore9.sh\n'
screen -dmS core10
screen -S core10 -p 0 -X stuff './runcore10.sh\n'
screen -dmS core11
screen -S core11 -p 0 -X stuff './runcore11.sh\n'
screen -dmS core12
screen -S core12 -p 0 -X stuff './runcore12.sh\n'
screen -dmS core13
screen -S core13 -p 0 -X stuff './runcore13.sh\n'
screen -dmS core14
screen -S core14 -p 0 -X stuff './runcore14.sh\n'
screen -dmS core15
screen -S core15 -p 0 -X stuff './runcore15.sh\n'
screen -dmS core16
screen -S core16 -p 0 -X stuff './runcore16.sh\n'
