#!/bin/bash
var1='-dmS core'
var2='scr'
for i in {1..16}
do
    name=$var1$i$var2
    echo $name
    #screen -S core01scr -p 0 -X stuff './runcore1.sh\n'
done