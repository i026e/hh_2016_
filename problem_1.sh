#! /bin/sh

echo "3
3 3
4 5 4
3 1 5
5 4 1
4 4
5 3 4 5
6 2 1 4
3 1 1 4
8 5 4 3
4 3
2 2 2
2 1 2
2 1 2
2 1 2" | python3 ./problem_1.py

echo "Read from files"
python3 ./problem_1.py < pr1_ex1.txt
python3 ./problem_1.py < pr1_ex2.txt
