#!/bin/sh
screen -dmS core01scr
screen -S core01scr -p 0 -X stuff './runcore1.sh\n'
screen -dmS core02scr
screen -S core02scr -p 0 -X stuff './runcore2.sh\n'
screen -dmS core03scr
screen -S core03scr -p 0 -X stuff './runcore3.sh\n'
screen -dmS core04scr
screen -S core04scr -p 0 -X stuff './runcore4.sh\n'
screen -dmS core05scr
screen -S core05scr -p 0 -X stuff './runcore5.sh\n'
screen -dmS core06scr
screen -S core06scr -p 0 -X stuff './runcore6.sh\n'
screen -dmS core07scr
screen -S core07scr -p 0 -X stuff './runcore7.sh\n'
screen -dmS core08scr
screen -S core08scr -p 0 -X stuff './runcore8.sh\n'
screen -dmS core09scr
screen -S core09scr -p 0 -X stuff './runcore9.sh\n'
screen -dmS core10scr
screen -S core10scr -p 0 -X stuff './runcore10.sh\n'
screen -dmS core11scr
screen -S core11scr -p 0 -X stuff './runcore11.sh\n'
screen -dmS core12scr
screen -S core12scr -p 0 -X stuff './runcore12.sh\n'
screen -dmS core13scr
screen -S core13scr -p 0 -X stuff './runcore13.sh\n'
screen -dmS core14scr
screen -S core14scr -p 0 -X stuff './runcore14.sh\n'
screen -dmS core15scr
screen -S core15scr -p 0 -X stuff './runcore15.sh\n'
screen -dmS core16scr
screen -S core16scr -p 0 -X stuff './runcore16.sh\n'
