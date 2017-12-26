#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
screen -dmS core1  bash -c 'source $HOME/.profile; $DIR/runcore1.sh'
screen -dmS core2  bash -c 'source $HOME/.profile; $DIR/runcore2.sh'
screen -dmS core3  bash -c 'source $HOME/.profile; $DIR/runcore3.sh'
screen -dmS core4  bash -c 'source $HOME/.profile; $DIR/runcore4.sh'
screen -dmS core5  bash -c 'source $HOME/.profile; $DIR/runcore5.sh'
screen -dmS core6  bash -c 'source $HOME/.profile; $DIR/runcore6.sh'
screen -dmS core7  bash -c 'source $HOME/.profile; $DIR/runcore7.sh'
screen -dmS core8  bash -c 'source $HOME/.profile; $DIR/runcore8.sh'
screen -dmS core9  bash -c 'source $HOME/.profile; $DIR/runcore9.sh'
screen -dmS core10 bash -c 'source $HOME/.profile; $DIR/runcore10.sh'
screen -dmS core11 bash -c 'source $HOME/.profile; $DIR/runcore11.sh'
screen -dmS core12 bash -c 'source $HOME/.profile; $DIR/runcore12.sh'
screen -dmS core13 bash -c 'source $HOME/.profile; $DIR/runcore13.sh'
screen -dmS core14 bash -c 'source $HOME/.profile; $DIR/runcore14.sh'
screen -dmS core15 bash -c 'source $HOME/.profile; $DIR/runcore15.sh'
screen -dmS core16 bash -c 'source $HOME/.profile; $DIR/runcore16.sh'

