#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python $DIR/../script.py -d 25 -t 20 -D 4 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 20 -D 5 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 20 -D 10 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 20 -D 15 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 20 -D 19 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 25 -D 5 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 25 -D 10 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 30 -D 5 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 30 -D 10 -i 8 -l logcore9.log
python $DIR/../script.py -d 25 -t 45 -D 5 -i 0 -l logcore9.log