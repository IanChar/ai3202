# Bayesian Network

## Overview
Using BayesNetworkCalculator.py, one can construct and run calculations on a
given Bayes Net.

## Cancer Bayes Net
For this assignment a sample Bayes Net was constructed in Main.py that includes
the causes of cancer (Polution, Smoking), cancer itself (Cancer), and the
effects of cancer (Xray is positive, Dyspnoea). In order to run a specific
command on the net type...

```
python Main.py <flag_option> "<command>"
```

The possible flags are -m for marginal, -j for joint, -c for conditional, and
-p to set a prior. The commands are composed of the lower case name of each node
and possibly "~" to negate the event. If a capital character is entered, each
possibility will be accounted for. Examples include...

```
python Main.py -p "S=0.5"
python Main.py -m "C"
python Main.py -j "x~d"
python Main.py -g "x|D~s"
```

## Results
In order to see all of the probabilities that we had to be able to emulate
you can either look below (looks better if viewed raw) or execute...

```
./RunTableCommands.sh
```

-------------Values for when P(S) = 0.3-------------

-----No evidence-----
P(~p) = 0.1
P(s) = 0.3
P(c) = 0.01163
P(x) = 0.208141
P(d) = 0.3040705

-----Diagnostic-----
P(~p|d) = 0.101999371856
P(s|d) = 0.307034059536
P(c|d) = 0.0248610108511
P(x|d) = 0.217402707596
P(d|d) = 1

-----Predictive-----
P(~p|s) = 0.1
P(s|s) = 1
P(c|s) = 0.032
P(x|s) = 0.2224
P(d|s) = 0.3112

-----Intercausal-----
P(~p|c) = 0.249355116079
P(s|c) = 0.825451418745
P(c|c) = 1
P(x|c) = 0.9
P(d|c) = 0.65
P(~p|cs) = 0.15625
P(s|cs) = 1
P(c|cs) = 1
P(x|cs) = 0.9
P(d|cs) = 0.65

-----Combined-----
P(~p|ds) = 0.102024421594
P(s|ds) = 1
P(c|ds) = 0.0668380462725
P(x|ds) = 0.246786632391
P(d|ds) = 1

-------------Values for when P(S) = 0.5-------------

-----No evidence-----
P(S) = 0.5
P(~p) = 0.1
P(s) = 0.5
P(c) = 0.01745
P(x) = 0.212215
P(d) = 0.3061075

-----Diagnostic-----
P(S) = 0.5
P(~p|d) = 0.102006647991
P(s|d) = 0.508318156203
P(c|d) = 0.0370539761358
P(x|d) = 0.225937783295
P(d|d) = 1

-----Predictive-----
P(S) = 0.5
P(~p|s) = 0.1
P(s|s) = 1
P(c|s) = 0.032
P(x|s) = 0.2224
P(d|s) = 0.3112

-----Intercausal-----
P(S) = 0.5
P(~p|c) = 0.200573065903
P(s|c) = 0.916905444126
P(c|c) = 1
P(x|c) = 0.9
P(d|c) = 0.65
P(S) = 0.5
P(~p|cs) = 0.15625
P(s|cs) = 1
P(c|cs) = 1
P(x|cs) = 0.9
P(d|cs) = 0.65

-----Combined-----
P(S) = 0.5
P(~p|ds) = 0.102024421594
P(s|ds) = 1
P(c|ds) = 0.0668380462725
P(x|ds) = 0.246786632391
P(d|ds) = 1
