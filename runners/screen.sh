#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
screen -dmS core1  bash -c 'source $HOME/.profile; $DIR/runcore1.sh: exec sh'
echo "$DIR"
screen -dmS core2  bash -c 'source $HOME/.profile; $DIR/runcore2.sh: exec sh'
echo "$DIR"
screen -dmS core3  bash -c 'source $HOME/.profile; $DIR/runcore3.sh: exec sh'
echo "$DIR"
screen -dmS core4  bash -c 'source $HOME/.profile; $DIR/runcore4.sh: exec sh'
echo "$DIR"
screen -dmS core5  bash -c 'source $HOME/.profile; $DIR/runcore5.sh: exec sh'
echo "$DIR"
screen -dmS core6  bash -c 'source $HOME/.profile; $DIR/runcore6.sh: exec sh'
echo "$DIR"
screen -dmS core7  bash -c 'source $HOME/.profile; $DIR/runcore7.sh: exec sh'
echo "$DIR"
screen -dmS core8  bash -c 'source $HOME/.profile; $DIR/runcore8.sh: exec sh'
echo "$DIR"
screen -dmS core9  bash -c 'source $HOME/.profile; $DIR/runcore9.sh: exec sh'
echo "$DIR"
screen -dmS core10 bash -c 'source $HOME/.profile; $DIR/runcore10.sh: exec sh'
echo "$DIR"
screen -dmS core11 bash -c 'source $HOME/.profile; $DIR/runcore11.sh: exec sh'
echo "$DIR"
screen -dmS core12 bash -c 'source $HOME/.profile; $DIR/runcore12.sh: exec sh'
echo "$DIR"
screen -dmS core13 bash -c 'source $HOME/.profile; $DIR/runcore13.sh: exec sh'
echo "$DIR"
screen -dmS core14 bash -c 'source $HOME/.profile; $DIR/runcore14.sh: exec sh'
echo "$DIR"
screen -dmS core15 bash -c 'source $HOME/.profile; $DIR/runcore15.sh: exec sh'
echo "$DIR"
screen -dmS core16 bash -c 'source $HOME/.profile; $DIR/runcore16.sh: exec sh'
echo "$DIR"

