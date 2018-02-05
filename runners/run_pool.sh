#!/bin/sh
screen -dmS core01scr
screen -S core01scr -p 0 -X stuff 'python ../script.py -l logcorepool1.log\n'
screen -dmS core02scr
screen -S core02scr -p 0 -X stuff 'python ../script.py -l logcorepool2.log\n'
screen -dmS core03scr
screen -S core03scr -p 0 -X stuff 'python ../script.py -l logcorepool3.log\n'
screen -dmS core04scr
screen -S core04scr -p 0 -X stuff 'python ../script.py -l logcorepool4.log\n'
screen -dmS core05scr
screen -S core05scr -p 0 -X stuff 'python ../script.py -l logcorepool5.log\n'
# screen -dmS core06scr
# screen -S core06scr -p 0 -X stuff 'python ../script.py -l logcorepool6.log\n'
# screen -dmS core07scr
# screen -S core07scr -p 0 -X stuff 'python ../script.py -l logcorepool7.log\n'
# screen -dmS core08scr
# screen -S core08scr -p 0 -X stuff 'python ../script.py -l logcorepool8.log\n'
# screen -dmS core09scr
# screen -S core09scr -p 0 -X stuff 'python ../script.py -l logcorepool9.log\n'
# screen -dmS core10scr
# screen -S core10scr -p 0 -X stuff 'python ../script.py -l logcorepool10.log\n'
# screen -dmS core11scr
# screen -S core11scr -p 0 -X stuff 'python ../script.py -l logcorepool11.log\n'
# screen -dmS core12scr
# screen -S core12scr -p 0 -X stuff 'python ../script.py -l logcorepool12.log\n'
# screen -dmS core13scr
# screen -S core13scr -p 0 -X stuff 'python ../script.py -l logcorepool13.log\n'
# screen -dmS core14scr
# screen -S core14scr -p 0 -X stuff 'python ../script.py -l logcorepool14.log\n'
# screen -dmS core15scr
# screen -S core15scr -p 0 -X stuff 'python ../script.py -l logcorepool15.log\n'
# screen -dmS core16scr
# screen -S core16scr -p 0 -X stuff 'python ../script.py -l logcorepool16.log\n'
