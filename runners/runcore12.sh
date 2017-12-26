#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../script.py -d 10 -t 20 -D 4 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 4 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 5 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 5 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 10 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 10 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 15 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 15 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 19 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 20 -D 19 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 25 -D 5 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 25 -D 5 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 25 -D 10 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 25 -D 10 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 30 -D 5 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 30 -D 5 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 30 -D 10 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 30 -D 10 -i 6 -l logcore12.log
python $DIR/../script.py -d 10 -t 35 -D 5 -i 1 -l logcore12.log
python $DIR/../script.py -d 10 -t 40 -D 10 -i 0 -l logcore12.log
python $DIR/../script.py -d 10 -t 45 -D 10 -i 1 -l logcore12.log