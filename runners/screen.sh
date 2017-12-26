#!/bin/sh
screen -dmS core1
screen -S core1 -p 0 -X stuff './runcore1.sh\n'
screen -dmS core2
screen -S core2 -p 0 -X stuff './runcore2.sh\n'
screen -dmS core3
screen -S core3 -p 0 -X stuff './runcore3.sh\n'
screen -dmS core4
screen -S core4 -p 0 -X stuff './runcore4.sh\n'
screen -dmS core5
screen -S core5 -p 0 -X stuff './runcore5.sh\n'
screen -dmS core6
screen -S core6 -p 0 -X stuff './runcore6.sh\n'
screen -dmS core7
screen -S core7 -p 0 -X stuff './runcore7.sh\n'
screen -dmS core8
screen -S core8 -p 0 -X stuff './runcore8.sh\n'
screen -dmS core9
screen -S core9 -p 0 -X stuff './runcore9.sh\n'
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
