#!/bin/bash
echo "-------------Values for when P(S) = 0.3-------------"
echo "
-----No evidence-----"
python Main.py -m "~p" -m "s" -m "c" -m "x" -m "d"
echo "
-----Diagnostic-----"
python Main.py -g "~p|d" -g "s|d" -g "c|d" -g "x|d" -g "d|d"
echo "
-----Predictive-----"
python Main.py -g "~p|s" -g "s|s" -g "c|s" -g "x|s" -g "d|s"
echo "
-----Intercausal-----"
python Main.py -g "~p|c" -g "s|c" -g "c|c" -g "x|c" -g "d|c"
python Main.py -g "~p|cs" -g "s|cs" -g "c|cs" -g "x|cs" -g "d|cs"
echo "
-----Combined-----"
python Main.py -g "~p|ds" -g "s|ds" -g "c|ds" -g "x|ds" -g "d|ds"

echo "
-------------Values for when P(S) = 0.5-------------"
echo "
-----No evidence-----"
python Main.py -p "S=0.5" -m "~p" -m "s" -m "c" -m "x" -m "d"
echo "
-----Diagnostic-----"
python Main.py -p "S=0.5" -g "~p|d" -g "s|d" -g "c|d" -g "x|d" -g "d|d"
echo "
-----Predictive-----"
python Main.py -p "S=0.5" -g "~p|s" -g "s|s" -g "c|s" -g "x|s" -g "d|s"
echo "
-----Intercausal-----"
python Main.py -p "S=0.5" -g "~p|c" -g "s|c" -g "c|c" -g "x|c" -g "d|c"
python Main.py -p "S=0.5" -g "~p|cs" -g "s|cs" -g "c|cs" -g "x|cs" -g "d|cs"
echo "
-----Combined-----"
python Main.py -p "S=0.5" -g "~p|ds" -g "s|ds" -g "c|ds" -g "x|ds" -g "d|ds"
