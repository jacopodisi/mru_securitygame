#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../script.py -d 25 -t 20 -D 4 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 20 -D 5 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 20 -D 10 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 20 -D 15 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 20 -D 19 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 25 -D 5 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 25 -D 10 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 30 -D 5 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 30 -D 10 -i 7 -l logcore8.log
python $DIR/../script.py -d 25 -t 40 -D 10 -i 1 -l logcore8.log