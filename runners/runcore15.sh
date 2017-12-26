#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../script.py -d 10 -t 20 -D 4 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 4 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 5 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 5 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 10 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 10 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 15 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 15 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 19 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 20 -D 19 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 25 -D 5 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 25 -D 5 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 25 -D 10 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 25 -D 10 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 30 -D 5 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 30 -D 5 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 30 -D 10 -i 4 -l logcore15.log
python $DIR/../script.py -d 10 -t 30 -D 10 -i 9 -l logcore15.log
python $DIR/../script.py -d 10 -t 40 -D 5 -i 0 -l logcore15.log
python $DIR/../script.py -d 10 -t 45 -D 5 -i 1 -l logcore15.log
python $DIR/../script.py -d 10 -t 50 -D 10 -i 0 -l logcore15.log