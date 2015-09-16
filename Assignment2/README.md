# Assignment 2: A*Search
## Run instructions
In order to run execute the following...
```
python MazeSolver.py
```

## My heuristic
I chose my heuristic in such a way that the heuristic takes obstacles and
diagonals into account. I thought this would be a good heuristic because it takes
advantage of the fact that moving diagonal is cheaper per square moved.
In addition, my heuristic takes obstacles into account which the Manhattan
heuristic does not. In the end, my heuristic did worse on world one with a
total cost of 156 compared to 130 (although it only explored 59 squares instead
of 62). For the second world, my heuristic did better with a score of 142
compared with 144 (both explored 60 squares).

My heuristic did not outperform the Manhattan in world 1 because it tried to
find a diagonal path with a small amount of obstacles in the way. This turned
out to not always be the most efficient path. However, it was more efficient
for world 2.

### Heuristic function
My function will first try to make as many diagonal moves from a spot as possible.
If no more diagonal moves can be made it will go horizontally or vertically to the
goal. Each diagonal move adds 3 points, each horizontal or vertical move adds 2 points,
mountains add 2 points, and walls add 7 points.

### Results
Results of my heuristic are shown below. In order to view correctly view original
source of README. Otherwise, you can just run the program to get the same output.

World 1:
--------------------Log----------------------

(0, 0) with cost 0
(0, 1) with cost 44
(0, 2) with cost 76
(0, 3) with cost 102
(1, 4) with cost 129
(2, 5) with cost 153
(3, 5) with cost 169
(4, 6) with cost 186
(5, 7) with cost 200
(6, 7) with cost 220
(7, 7) with cost 240
(8, 7) with cost 250
(9, 7) with cost 260
Total cost without heuristic is: 156
-------------------Maze---------------------
0 0 0 0 1 x x x x x
2 2 1 1 x 0 2 0 2 0
0 0 x x 0 0 2 0 0 0
2 x 2 2 0 0 0 0 2 0
x 0 2 0 0 2 1 0 1 0
x 0 2 0 0 2 0 0 2 0
x 0 2 0 1 2 0 1 2 2
x 0 0 0 0 0 0 0 0 0
Squares explored (had distances calculated for them): 59

World 2:
--------------------Log----------------------
(0, 0) with cost 0
(0, 1) with cost 49
(0, 2) with cost 81
(1, 3) with cost 114
(2, 3) with cost 150
(3, 3) with cost 186
(4, 4) with cost 223
(4, 5) with cost 246
(4, 6) with cost 259
(5, 7) with cost 273
(6, 7) with cost 283
(7, 7) with cost 293
(8, 7) with cost 303
(9, 7) with cost 313
Total cost without heuristic is: 142
-------------------Maze---------------------
0 0 0 0 0 x x x x x
2 2 1 1 x 2 2 1 1 0
0 0 0 0 x 2 2 1 1 0
2 2 2 2 x 0 0 1 1 0
0 x x x 0 2 1 1 1 0
x 2 2 0 2 2 0 0 2 0
x 0 2 0 1 2 0 1 2 2
x 0 0 0 0 0 0 0 0 0
Squares explored (had distances calculated for them): 60
