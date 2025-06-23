# Bachelor Semester Project : The stabbing problem
This repository contains the code for my semester project at EPFL with the DISOPT chair under the supervision of Martina Gallato. 

##Introduction
The horizontal stabbing problem consists in finding a set of horizontal segments of minimal length that stabs a given set of n axis-aligned rectangles such that each segment starts and ends at the extremity of one or multiple rectangles. The algorithm implemented here give an 8-approximation algorithm for this problem in O(n^4). This algorithm was first described in Eisenbrand et al. (2021).

##Usage

###Librairies
The libraries math, copy, igraph, numpy, matplotlib, random, time and gurobipy are needed to run all the files.
A gurobi licence might be necessary to have the optimal solution for big instances. The files concerned are approx_particular.py example and test_approximation.py.

###Dependencies
DPfonction depends on ClassRectangle and all the main files depends on ClassRectangle and DPfonction.
Only limit_ratio.py and test_time.py in this folder depend on ClassRectangle and Dpfonction.

###Saving results
In test debug and presentation, the before.py and final average.py files need the text files that they read to be on the same folder as them (or to change the path name).

##References
Eisenbrand et al. (2021) : Eisenbrand, Gallato, Svensson and Venzin (2021) A qptas for stabbing rectangles.
